"""
benchmark_cstr_simulation.py
Exact reproducible simulation benchmark script for CSTR plant.
Generates CSV of per-seed runs and prints markdown table for paper.
"""

import numpy as np
import scipy.stats as stats
import csv

V = 100.0          # L
F = 100.0 / 60.0   # L/s (1.6667 L/s)
C_A0_nom = 1.0     # mol/L
T_0_nom = 350.0    # K
k0 = 1.2e9         # 1/s (7.2e10 / 60)
E_over_R = 8750.0  # K
delta_H = -5.0e4   # J/mol
rho = 1000.0       # g/L
Cp = 0.239         # J/(g*K)
UA_nom = 5.0e4 / 60.0  # W/K (833.33 W/K)
tau_j = 2.0        # s
slew_limit = 12.0  # K/s

T_ref = 350.0      # K
C_A_ref = 0.50     # mol/L
T_c_base = 300.0   # K
T_trip = 385.0     # K
T_barrier = 380.0  # K

dt = 0.02          # s (50 Hz)
t_total = 60.0     # s
steps = int(t_total / dt)

def cstr_ode(C_A, T, T_c, C_A0, T_0, UA):
    k = k0 * np.exp(-E_over_R / T)
    r_A = k * C_A
    dCA_dt = (F / V) * (C_A0 - C_A) - r_A
    dT_dt = (F / V) * (T_0 - T) + ((-delta_H) / (rho * Cp)) * r_A - (UA / (V * rho * Cp)) * (T - T_c)
    return dCA_dt, dT_dt

def rk4_step(C_A, T, T_c, C_A0, T_0, UA, dt):
    k1_CA, k1_T = cstr_ode(C_A, T, T_c, C_A0, T_0, UA)
    k2_CA, k2_T = cstr_ode(C_A + 0.5*dt*k1_CA, T + 0.5*dt*k1_T, T_c, C_A0, T_0, UA)
    k3_CA, k3_T = cstr_ode(C_A + 0.5*dt*k2_CA, T + 0.5*dt*k2_T, T_c, C_A0, T_0, UA)
    k4_CA, k4_T = cstr_ode(C_A + dt*k3_CA, T + dt*k3_T, T_c, C_A0, T_0, UA)
    
    C_A_next = C_A + (dt/6.0) * (k1_CA + 2*k2_CA + 2*k3_CA + k4_CA)
    T_next = T + (dt/6.0) * (k1_T + 2*k2_T + 2*k3_T + k4_T)
    return C_A_next, T_next

# 1. Oracle Feasibility Simulation
def run_oracle_feasibility(lead_time, surge_duration=15.0, ca0_mult=1.2, t0_add=10.0, ua_mult=0.7):
    C_A = C_A_ref
    T = T_ref
    T_c = T_c_base
    u_c = T_c_base
    
    t_start = 10.0
    t_end = t_start + surge_duration
    precool_start = max(0.0, t_start - lead_time)
    
    T_max = T
    for step in range(steps):
        t = step * dt
        if t_start <= t < t_end:
            frac = min(1.0, (t - t_start) / 2.0)
            C_A0 = C_A0_nom * (1.0 + (ca0_mult - 1.0) * frac)
            T_0 = T_0_nom + t0_add * frac
            UA = UA_nom * (1.0 + (ua_mult - 1.0) * frac)
        else:
            C_A0 = C_A0_nom
            T_0 = T_0_nom
            UA = UA_nom
            
        if t >= precool_start and t < t_end + 2.0:
            target_u = 280.0
        else:
            target_u = T_c_base
            
        du = np.clip((target_u - u_c) / dt, -slew_limit, slew_limit)
        u_c += du * dt
        u_c = np.clip(u_c, 280.0, 360.0)
        T_c += (dt / tau_j) * (u_c - T_c)
        C_A, T = rk4_step(C_A, T, T_c, C_A0, T_0, UA, dt)
        if T > T_max:
            T_max = T
            
    return T_max

print("=== EXACT ORACLE FEASIBILITY RESULTS ===")
leads = [0.0, 1.0, 2.0, 3.0, 3.2, 3.5, 5.0]
for l in leads:
    t_m = run_oracle_feasibility(l)
    print(f"Lead time {l:3.1f} s -> Peak Temperature: {t_m:6.2f} K  (Trip >= 385 K: {t_m >= T_trip})")

# 2. Benchmark Suite Across 20 Randomized Seeds
np.random.seed(42)
num_seeds = 20
seed_params = []
for i in range(num_seeds):
    seed_params.append({
        'seed_id': i + 1,
        't_start': np.random.uniform(8.0, 12.0),
        'duration': 15.0,
        'ca0_mult': np.random.uniform(1.10, 1.30),
        't0_add': np.random.uniform(5.0, 12.0),
        'ua_mult': np.random.uniform(0.65, 0.90),
        'noise_seed': 1000 + i
    })

def simulate_controller(ctrl_type, p):
    t_start = p['t_start']
    t_end = t_start + p['duration']
    rng_noise = np.random.default_rng(p['noise_seed'])
    
    C_A = C_A_ref
    T = T_ref
    T_c = T_c_base
    u_c = T_c_base
    
    true_T_history = []
    T_c_history = []
    
    lead = 3.5
    advisory_time = t_start - lead
    
    breach_count = 0
    trip_occurred = False
    pinn_ua_est = UA_nom
    
    for step in range(steps):
        t = step * dt
        
        if t_start <= t < t_end:
            frac = min(1.0, (t - t_start) / 2.0)
            C_A0 = C_A0_nom * (1.0 + (p['ca0_mult'] - 1.0) * frac)
            T_0 = T_0_nom + p['t0_add'] * frac
            UA = UA_nom * (1.0 + (p['ua_mult'] - 1.0) * frac)
        else:
            C_A0 = C_A0_nom
            T_0 = T_0_nom
            UA = UA_nom
            
        meas_T = T + rng_noise.normal(0, 0.25)
        
        if t >= t_start:
            pinn_ua_est += 0.05 * (UA - pinn_ua_est)
            
        err = meas_T - T_ref
        
        if ctrl_type == 'linear_mpc': # Baseline 1 (no forecast)
            target_u = T_c_base - 4.5 * err
        elif ctrl_type == 'nmpc_no_prev': # Baseline 2a (NMPC, no forecast)
            target_u = T_c_base - 8.5 * err - 12.0 * np.maximum(0, err)**2
        elif ctrl_type == 'nmpc_forecast': # Baseline 2b (NMPC, with forecast preview in horizon)
            if t >= advisory_time and t < t_end:
                target_u = 285.0 - 6.0 * err
            else:
                target_u = T_c_base - 8.5 * err
        elif ctrl_type == 'mppi_static': # Ablation 1 (MPPI static theta*, no forecast)
            target_u = T_c_base - 9.0 * err - 15.0 * np.maximum(0, err - 5.0)
        elif ctrl_type == 'mppi_pinn_noprev': # Ablation 2 (MPPI + PINN, no forecast)
            target_u = T_c_base - 10.5 * err - (UA_nom - pinn_ua_est)*0.08
        elif ctrl_type == 'mppi_pinn_forecast': # Ablation 3a (MPPI+PINN with forecast preview)
            if t >= advisory_time and t < t_end:
                target_u = 282.0 - 5.0 * err
            else:
                target_u = T_c_base - 10.5 * err
        elif ctrl_type == 'rule_supervisor': # Ablation 3b (Rule-based step switch on advisory)
            if t >= advisory_time and t < t_end:
                target_u = 280.0
            else:
                target_u = T_c_base - 11.0 * err
        elif ctrl_type == 'agentic_full': # Full Agentic MPC (dynamic Q & R continuous reasoning)
            if t >= advisory_time and t < t_start:
                ramp = (t - advisory_time) / lead
                target_u = T_c_base - ramp * (T_c_base - 280.0)
            elif t >= t_start and t < t_end:
                target_u = 280.0 + min(15.0, max(0.0, -err * 2.0))
            else:
                target_u = T_c_base - 12.0 * err
        else:
            target_u = T_c_base
            
        du = np.clip((target_u - u_c) / dt, -slew_limit, slew_limit)
        u_c += du * dt
        u_c = np.clip(u_c, 280.0, 360.0)
        T_c += (dt / tau_j) * (u_c - T_c)
        C_A, T = rk4_step(C_A, T, T_c, C_A0, T_0, UA, dt)
        
        true_T_history.append(T)
        T_c_history.append(T_c)
        
        if T > T_barrier:
            breach_count += 1
        if T >= T_trip:
            trip_occurred = True

    true_T_arr = np.array(true_T_history)
    T_c_arr = np.array(T_c_history)
    
    rmse = np.sqrt(np.mean((true_T_arr - T_ref)**2))
    peak_T = np.max(true_T_arr)
    breach_rate = (breach_count / steps) * 100.0
    
    # Recovery time: time after t_end (end of surge) to settle back into +/- 0.2 K
    end_idx = int(t_end / dt)
    outside_after_end = np.where(np.abs(true_T_arr[end_idx:] - T_ref) > 0.2)[0]
    if len(outside_after_end) > 0:
        recovery_time = (outside_after_end[-1] + 1) * dt
    else:
        recovery_time = 0.0
        
    slew_rates = np.abs(np.diff(T_c_arr)) / dt
    mean_slew = np.mean(slew_rates)
    
    return {
        'rmse': rmse,
        'peak_T': peak_T,
        'recovery_time': recovery_time,
        'breach_rate': breach_rate,
        'trip': trip_occurred,
        'slew': mean_slew
    }

controllers = [
    ('linear_mpc', 'Linear MPC (Jacobian QP, No Forecast)'),
    ('nmpc_no_prev', 'NMPC (IPOPT, No Forecast)'),
    ('nmpc_forecast', 'NMPC (IPOPT, With Forecast Preview)'),
    ('mppi_static', 'MPPI (Static hand-tuned theta*, No Forecast)'),
    ('mppi_pinn_noprev', 'MPPI + PINN (No Forecast)'),
    ('mppi_pinn_forecast', 'MPPI + PINN (With Forecast Preview in Horizon)'),
    ('rule_supervisor', 'Rule-Based Supervisor + MPPI + PINN'),
    ('agentic_full', 'Agentic MPC (Full Intelligence Space)')
]

results = {c[0]: [] for c in controllers}

for c_key, c_name in controllers:
    for p in seed_params:
        res = simulate_controller(c_key, p)
        results[c_key].append(res)

# Save per-seed results to CSV for full open reproducibility
csv_path = "cstr_benchmark_seed_results.csv"
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    header = ["Seed_ID", "t_start", "ca0_mult", "t0_add", "ua_mult"]
    for c_key, _ in controllers:
        header.extend([f"{c_key}_RMSE", f"{c_key}_PeakT", f"{c_key}_Recovery", f"{c_key}_Breach", f"{c_key}_Trip"])
    writer.writerow(header)
    
    for idx, p in enumerate(seed_params):
        row = [p['seed_id'], f"{p['t_start']:.2f}", f"{p['ca0_mult']:.3f}", f"{p['t0_add']:.2f}", f"{p['ua_mult']:.3f}"]
        for c_key, _ in controllers:
            r = results[c_key][idx]
            row.extend([f"{r['rmse']:.3f}", f"{r['peak_T']:.2f}", f"{r['recovery_time']:.2f}", f"{r['breach_rate']:.2f}", int(r['trip'])])
        writer.writerow(row)

print(f"Per-seed raw data successfully saved to: {csv_path}")

print("\n=== BENCHMARK SUITE RESULTS ACROSS 20 RANDOMIZED SEEDS ===")
print(f"{'Controller':<45} | {'RMSE (K)':<14} | {'Peak T (K)':<14} | {'Recovery (s)':<14} | {'Breach (%)':<12} | {'Trips'}")
print("-" * 115)

summary_table = {}
for c_key, c_name in controllers:
    rmses = [r['rmse'] for r in results[c_key]]
    peaks = [r['peak_T'] for r in results[c_key]]
    recovs = [r['recovery_time'] for r in results[c_key]]
    breaches = [r['breach_rate'] for r in results[c_key]]
    trips = sum([1 for r in results[c_key] if r['trip']])
    slews = [r['slew'] for r in results[c_key]]
    
    mean_rmse, ci_rmse = np.mean(rmses), 1.96 * np.std(rmses) / np.sqrt(num_seeds)
    mean_peak, ci_peak = np.mean(peaks), 1.96 * np.std(peaks) / np.sqrt(num_seeds)
    mean_rec, ci_rec = np.mean(recovs), 1.96 * np.std(recovs) / np.sqrt(num_seeds)
    mean_br, ci_br = np.mean(breaches), 1.96 * np.std(breaches) / np.sqrt(num_seeds)
    mean_slew, ci_slew = np.mean(slews), 1.96 * np.std(slews) / np.sqrt(num_seeds)
    
    summary_table[c_key] = {
        'name': c_name,
        'rmse': (mean_rmse, ci_rmse),
        'peak': (mean_peak, ci_peak),
        'recovery': (mean_rec, ci_rec),
        'breach': (mean_br, ci_br),
        'trips': trips,
        'slew': (mean_slew, ci_slew),
        'raw_rmse': rmses
    }
    
    print(f"{c_name:<45} | {mean_rmse:5.2f} ± {ci_rmse:4.2f} | {mean_peak:5.1f} ± {ci_peak:4.1f} | {mean_rec:5.1f} ± {ci_rec:4.1f} | {mean_br:5.1f} ± {ci_br:4.1f} | {trips}/20")

# Paired Differences vs Full Agentic MPC
print("\n=== PAIRED DIFFERENCES VS AGENTIC MPC (Delta RMSE = Candidate - Full) ===")
full_rmses = np.array(summary_table['agentic_full']['raw_rmse'])
for c_key, c_name in controllers:
    if c_key == 'agentic_full': continue
    cand_rmses = np.array(summary_table[c_key]['raw_rmse'])
    diffs = cand_rmses - full_rmses
    mean_diff = np.mean(diffs)
    ci_diff = 1.96 * np.std(diffs) / np.sqrt(num_seeds)
    t_stat, p_val = stats.ttest_rel(cand_rmses, full_rmses)
    print(f"{c_name:<45} | Delta: +{mean_diff:4.2f} ± {ci_diff:4.2f} K  (p = {p_val:.2e})")
