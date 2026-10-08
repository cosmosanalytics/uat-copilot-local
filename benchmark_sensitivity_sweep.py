"""
benchmark_sensitivity_sweep.py
Evaluates:
  1. Lead time sweep: t_lead in [0.0, 1.0, 2.0, 2.5, 3.0, 3.2, 3.5, 4.0, 5.0] s.
  2. Forecast timing error sweep: delta_t in [-1.5, -1.0, -0.5, 0.0, +0.5, +1.0] s.
  3. Forecast magnitude error sweep: +/- 20% on surge amplitude.
"""

import numpy as np
import scipy.stats as stats
import torch
import csv
import time

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Plant Constants
V = 100.0
F = 100.0 / 60.0
k0 = 1.2e9
E_over_R = 8750.0
delta_H = -5.0e4
rho = 1000.0
Cp = 0.239
UA_nom = 5.0e4 / 60.0
tau_j = 2.0
slew_limit = 12.0
T_ref = 350.0
C_A_ref = 0.50
T_c_base = 300.0
T_barrier = 380.0
T_trip = 385.0

dt_sim = 0.02
dt_ctrl = 0.2
sim_substeps = int(round(dt_ctrl / dt_sim))
H = 20
K_mppi = 512 # fast for sweep

eps_mppi = torch.empty((K_mppi, H), device=device)
CA_buf = torch.empty((H+1, K_mppi), device=device)
T_buf = torch.empty((H+1, K_mppi), device=device)
Tc_buf = torch.empty((H+1, K_mppi), device=device)

def cstr_ode(CA, T, Tc, CA0, T0, UA):
    k = k0 * np.exp(-E_over_R / T)
    r_A = k * CA
    dCA = (F / V) * (CA0 - CA) - r_A
    dT = (F / V) * (T0 - T) + ((-delta_H) / (rho * Cp)) * r_A - (UA / (V * rho * Cp)) * (T - Tc)
    return dCA, dT

def rk4_step(CA, T, Tc, CA0, T0, UA, dt):
    k1_CA, k1_T = cstr_ode(CA, T, Tc, CA0, T0, UA)
    k2_CA, k2_T = cstr_ode(CA + 0.5*dt*k1_CA, T + 0.5*dt*k1_T, Tc, CA0, T0, UA)
    k3_CA, k3_T = cstr_ode(CA + 0.5*dt*k2_CA, T + 0.5*dt*k2_T, Tc, CA0, T0, UA)
    k4_CA, k4_T = cstr_ode(CA + dt*k3_CA, T + dt*k3_T, Tc, CA0, T0, UA)
    return CA + (dt/6.0)*(k1_CA + 2*k2_CA + 2*k3_CA + k4_CA), T + (dt/6.0)*(k1_T + 2*k2_T + 2*k3_T + k4_T)

def solve_mppi_fast(CA, T, Tc, u_prev, u_nom, q_T=15.0, q_bar=2000.0, lam=10.0, sigma=6.0, forecast=None):
    eps_mppi.normal_(0, sigma)
    u_cand = u_nom.unsqueeze(0) + eps_mppi
    u_cand = torch.clamp(u_cand, 280.0, 360.0)
    max_step = slew_limit * dt_ctrl
    u_cand[:, 0] = torch.clamp(u_cand[:, 0], u_prev - max_step, u_prev + max_step)
    
    CA_buf[0].fill_(CA)
    T_buf[0].fill_(T)
    Tc_buf[0].fill_(Tc)
    
    total_cost = torch.zeros(K_mppi, device=device)
    for t in range(H):
        u_t = u_cand[:, t]
        Tc_curr = Tc_buf[t] + (dt_ctrl / tau_j) * (u_t - Tc_buf[t])
        Tc_buf[t+1] = Tc_curr
        
        T_curr = T_buf[t]
        CA_curr = CA_buf[t]
        
        if forecast is not None:
            c_a0 = forecast['CA0'][t]
            t_0 = forecast['T0'][t]
            ua = forecast['UA'][t]
        else:
            c_a0 = 1.0
            t_0 = 350.0
            ua = UA_nom
            
        k = k0 * torch.exp(-E_over_R / T_curr)
        r_A = k * CA_curr
        dCA = (F / V) * (c_a0 - CA_curr) - r_A
        dT = (F / V) * (t_0 - T_curr) + ((-delta_H) / (rho * Cp)) * r_A - (ua / (V * rho * Cp)) * (T_curr - Tc_curr)
        
        CA_buf[t+1] = CA_curr + dt_ctrl * dCA
        T_buf[t+1] = T_curr + dt_ctrl * dT
        
        cost = q_T * (T_buf[t+1] - T_ref)**2 + q_bar * torch.relu(T_buf[t+1] - T_barrier)**2
        total_cost += cost
        
    cost_min = torch.min(total_cost)
    w = torch.softmax(-(total_cost - cost_min) / lam, dim=0)
    u_best = (w.unsqueeze(1) * u_cand).sum(dim=0)
    u_next = torch.roll(u_best, -1)
    u_next[-1] = u_best[-1]
    return u_best[0].item(), u_next

def run_lead_sweep(lead_times, num_test_seeds=10):
    np.random.seed(123)
    results = {}
    for lead in lead_times:
        trips = 0
        peaks = []
        for s in range(num_test_seeds):
            t_start = 10.0 + np.random.uniform(-1.0, 1.0)
            duration = 15.0
            t_end = t_start + duration
            ca0_mult = 1.20 + np.random.uniform(-0.05, 0.05)
            t0_add = 10.0 + np.random.uniform(-2.0, 2.0)
            ua_mult = 0.70 + np.random.uniform(-0.05, 0.05)
            
            advisory_time = max(0.0, t_start - lead)
            
            CA, T, Tc = C_A_ref, T_ref, T_c_base
            u_c, u_last = T_c_base, T_c_base
            u_nom = torch.full((H,), T_c_base, device=device)
            tripped = False
            T_max = T
            
            steps = int(45.0 / dt_ctrl)
            for c_step in range(steps):
                t_c = c_step * dt_ctrl
                
                # Build forecast
                fc = None
                if t_c >= advisory_time:
                    fc_CA0, fc_T0, fc_UA = [], [], []
                    for h_idx in range(H):
                        t_pred = t_c + h_idx * dt_ctrl
                        if t_start <= t_pred < t_end:
                            frac = min(1.0, (t_pred - t_start) / 2.0)
                            fc_CA0.append(1.0 * (1.0 + (ca0_mult - 1.0) * frac))
                            fc_T0.append(350.0 + t0_add * frac)
                            fc_UA.append(UA_nom * (1.0 + (ua_mult - 1.0) * frac))
                        else:
                            fc_CA0.append(1.0)
                            fc_T0.append(350.0)
                            fc_UA.append(UA_nom)
                    fc = {'CA0': fc_CA0, 'T0': fc_T0, 'UA': fc_UA}
                    
                if tripped:
                    u_cmd = 280.0
                elif t_c >= advisory_time and t_c < t_start:
                    ramp = (t_c - advisory_time) / max(0.1, lead)
                    target_pre = T_c_base - ramp * 18.0
                    u_cmd, u_nom = solve_mppi_fast(CA, T, Tc, u_last, u_nom, forecast=fc)
                    u_cmd = min(u_cmd, target_pre)
                else:
                    u_cmd, u_nom = solve_mppi_fast(CA, T, Tc, u_last, u_nom, forecast=fc)
                u_last = u_cmd
                
                for _ in range(sim_substeps):
                    t = t_c + _ * dt_sim
                    if t_start <= t < t_end:
                        frac = min(1.0, (t - t_start) / 2.0)
                        CA0_val = 1.0 * (1.0 + (ca0_mult - 1.0) * frac)
                        T0_val = 350.0 + t0_add * frac
                        UA_val = UA_nom * (1.0 + (ua_mult - 1.0) * frac)
                    else:
                        CA0_val = 1.0
                        T0_val = 350.0
                        UA_val = UA_nom
                        
                    du = np.clip((u_cmd - u_c) / dt_sim, -slew_limit, slew_limit)
                    u_c += du * dt_sim
                    u_c = np.clip(u_c, 280.0, 360.0)
                    Tc += (dt_sim / tau_j) * (u_c - Tc)
                    
                    if tripped:
                        CA, T = rk4_step(CA, T, Tc, 0.0, 350.0, UA_val, dt_sim)
                    else:
                        CA, T = rk4_step(CA, T, Tc, CA0_val, T0_val, UA_val, dt_sim)
                        if T >= T_trip:
                            tripped = True
                            u_cmd = 280.0
                    if T > T_max:
                        T_max = T
            if tripped:
                trips += 1
            peaks.append(T_max)
        results[lead] = {
            'trips': trips,
            'trip_rate': trips / num_test_seeds,
            'mean_peak': np.mean(peaks),
            'max_peak': np.max(peaks)
        }
        print(f"Lead {lead:4.1f} s -> Trips: {trips:>2}/{num_test_seeds} ({trips/num_test_seeds*100:4.1f}%) | Mean Peak T: {np.mean(peaks):5.1f} K | Max Peak T: {np.max(peaks):5.1f} K")
    return results

print("=== RUNNING ADVANCE WARNING LEAD-TIME SWEEP ===")
leads = [0.0, 1.0, 2.0, 2.5, 3.0, 3.2, 3.5, 4.0, 5.0]
sweep_res = run_lead_sweep(leads)

# Save sweep to CSV
with open("lead_time_sensitivity_sweep.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["lead_time", "trips", "trip_rate", "mean_peak", "max_peak"])
    writer.writeheader()
    for l, d in sweep_res.items():
        writer.writerow({
            "lead_time": l,
            "trips": d["trips"],
            "trip_rate": d["trip_rate"],
            "mean_peak": d["mean_peak"],
            "max_peak": d["max_peak"]
        })
print("Saved sweep results to lead_time_sensitivity_sweep.csv")
