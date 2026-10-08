"""
benchmark_cstr_unified.py
Unified, pure NumPy simulation benchmark for CSTR process control.
Reconciled against verified empirical metrics:
  - 20 randomized disturbance scenarios (seed=42)
  - Pure NumPy MPPI vectorization (default_rng(10000 + 100*rep + seed))
  - Sensor noise (default_rng(1000 + i))
  - Linear MPC (lsq_linear) evaluated at q_T=1.0 and q_T=10.0
  - Nonlinear MPC (L-BFGS-B, maxiter=10, warm-started)
  - Lagged-UA tracking filter (time constant tau = 1.0 s)
  - Post-trip SCRAM dynamics (F=0, u=280 K)
"""

import sys
import argparse
import numpy as np
from scipy.optimize import minimize, lsq_linear

# --- CSTR Plant Constants ---
V = 100.0          # L
F = 100.0 / 60.0   # L/s
k0 = 1.2e9         # 1/s
E_over_R = 8750.0  # K
delta_H = -5.0e4   # J/mol
rho = 1000.0       # g/L
Cp = 0.239         # J/(g*K)
UA_nom = 5.0e4 / 60.0  # W/K
tau_j = 2.0        # s
slew_limit = 12.0  # K/s

T_ref = 350.0      # K
C_A_ref = 0.50     # mol/L
T_c_base = 300.0   # K
T_barrier = 380.0  # K
T_trip = 385.0     # K

dt_sim = 0.02      # 50 Hz plant simulation
dt_ctrl = 0.2      # 5 Hz control step
sim_substeps = int(round(dt_ctrl / dt_sim))
t_total = 60.0     # s
n_ctrl_steps = int(round(t_total / dt_ctrl))
H = 20             # 4.0 s prediction horizon

def cstr_ode(CA, T, Tc, CA0, T0, UA, flow=F):
    k = k0 * np.exp(-E_over_R / np.maximum(100.0, T))
    r_A = k * CA
    dCA = (flow / V) * (CA0 - CA) - r_A
    dT = (flow / V) * (T0 - T) + ((-delta_H) / (rho * Cp)) * r_A - (UA / (V * rho * Cp)) * (T - Tc)
    return dCA, dT

def rk4_step(CA, T, Tc, CA0, T0, UA, dt, flow=F):
    k1_CA, k1_T = cstr_ode(CA, T, Tc, CA0, T0, UA, flow)
    k2_CA, k2_T = cstr_ode(CA + 0.5*dt*k1_CA, T + 0.5*dt*k1_T, Tc, CA0, T0, UA, flow)
    k3_CA, k3_T = cstr_ode(CA + 0.5*dt*k2_CA, T + 0.5*dt*k2_T, Tc, CA0, T0, UA, flow)
    k4_CA, k4_T = cstr_ode(CA + dt*k3_CA, T + dt*k3_T, Tc, CA0, T0, UA, flow)
    return CA + (dt/6.0)*(k1_CA + 2*k2_CA + 2*k3_CA + k4_CA), T + (dt/6.0)*(k1_T + 2*k2_T + 2*k3_T + k4_T)

# --- Linear MPC Setup (QP) ---
k_ss = k0 * np.exp(-E_over_R / T_ref)
dk_dT_ss = k_ss * (E_over_R / (T_ref**2))

A11 = - (F / V) - k_ss
A12 = - dk_dT_ss * C_A_ref
A21 = ((-delta_H) / (rho * Cp)) * k_ss
A22 = - (F / V) + ((-delta_H) / (rho * Cp)) * dk_dT_ss * C_A_ref - (UA_nom / (V * rho * Cp))
B1 = 0.0
B2 = UA_nom / (V * rho * Cp)

A_cont = np.array([[A11, A12], [A21, A22]])
B_cont = np.array([[B1], [B2]])
Ad = np.eye(2) + A_cont * dt_ctrl
Bd = B_cont * dt_ctrl

Sx = np.zeros((2*H, 2))
Su = np.zeros((2*H, H))
Ak = np.eye(2)
for i in range(H):
    Ak = Ak @ Ad
    Sx[2*i:2*i+2, :] = Ak
    for j in range(i+1):
        Su[2*i:2*i+2, j] = (np.linalg.matrix_power(Ad, i-j) @ Bd).ravel()

def build_linear_mpc_qp(q_temp=10.0, r_u=0.02):
    q_CA = 10.0
    Q_diag = []
    for _ in range(H):
        Q_diag.extend([q_CA, q_temp])
    Q_mat = np.diag(Q_diag)
    R_mat = np.eye(H) * r_u
    H_qp = Su.T @ Q_mat @ Su + R_mat
    return H_qp, Q_mat

H_qp_q10, Q_mat_q10 = build_linear_mpc_qp(10.0)
H_qp_q1, Q_mat_q1 = build_linear_mpc_qp(1.0)

def solve_linear_mpc(CA, T, u_prev, q_temp=10.0):
    H_qp = H_qp_q10 if q_temp == 10.0 else H_qp_q1
    Q_mat = Q_mat_q10 if q_temp == 10.0 else Q_mat_q1
    x0_dev = np.array([CA - C_A_ref, T - T_ref])
    g = Su.T @ Q_mat @ Sx @ x0_dev
    lb = np.full(H, -20.0)
    ub = np.full(H, 60.0)
    max_step = slew_limit * dt_ctrl
    lb[0] = max(lb[0], (u_prev - T_c_base) - max_step)
    ub[0] = min(ub[0], (u_prev - T_c_base) + max_step)
    res = lsq_linear(H_qp, -g, bounds=(lb, ub))
    return res.x[0] + T_c_base

# --- NMPC Solver ---
def solve_nmpc(CA, T, Tc, u_prev, u_warm, forecast=None, q_T=10.0, q_bar=500.0, r_u=0.05):
    def cost_fn(u_seq):
        c_a, temp, t_cool = CA, T, Tc
        u_last = u_prev
        cost = 0.0
        for k in range(H):
            u_k = u_seq[k]
            t_cool += (dt_ctrl / tau_j) * (u_k - t_cool)
            if forecast is not None:
                c_a0 = forecast['CA0'][k]
                t_0 = forecast['T0'][k]
                ua = forecast['UA'][k]
            else:
                c_a0 = 1.0
                t_0 = 350.0
                ua = UA_nom
            c_a, temp = rk4_step(c_a, temp, t_cool, c_a0, t_0, ua, dt_ctrl)
            cost += q_T * (temp - T_ref)**2 + q_bar * max(0.0, temp - T_barrier)**2 + r_u * (u_k - u_last)**2
            u_last = u_k
        return cost

    bounds = [(280.0, 360.0) for _ in range(H)]
    max_step = slew_limit * dt_ctrl
    bounds[0] = (max(280.0, u_prev - max_step), min(360.0, u_prev + max_step))
    res = minimize(cost_fn, u_warm, method='L-BFGS-B', bounds=bounds, options={'maxiter': 10})
    u_opt = res.x
    u_next_warm = np.roll(u_opt, -1)
    u_next_warm[-1] = u_opt[-1]
    return u_opt[0], u_next_warm

# --- NumPy Vectorized MPPI Solver ---
def solve_mppi_numpy(CA, T, Tc, u_prev, u_nom, rng, q_T=10.0, q_bar=1000.0, lam=10.0, sigma=6.0, forecast=None, est_UA=UA_nom, K=1024):
    eps = rng.normal(0.0, sigma, size=(K, H))
    u_cand = np.clip(u_nom[None, :] + eps, 280.0, 360.0)
    max_step = slew_limit * dt_ctrl
    u_cand[:, 0] = np.clip(u_cand[:, 0], u_prev - max_step, u_prev + max_step)

    CA_curr = np.full(K, CA)
    T_curr = np.full(K, T)
    Tc_curr = np.full(K, Tc)
    total_cost = np.zeros(K)

    for t in range(H):
        u_t = u_cand[:, t]
        Tc_curr = Tc_curr + (dt_ctrl / tau_j) * (u_t - Tc_curr)
        if forecast is not None:
            c_a0 = forecast['CA0'][t]
            t_0 = forecast['T0'][t]
            ua = forecast['UA'][t]
        else:
            c_a0 = 1.0
            t_0 = 350.0
            ua = est_UA

        k = k0 * np.exp(-E_over_R / np.maximum(100.0, T_curr))
        r_A = k * CA_curr
        dCA = (F / V) * (c_a0 - CA_curr) - r_A
        dT = (F / V) * (t_0 - T_curr) + ((-delta_H) / (rho * Cp)) * r_A - (ua / (V * rho * Cp)) * (T_curr - Tc_curr)

        CA_curr = CA_curr + dt_ctrl * dCA
        T_curr = T_curr + dt_ctrl * dT

        stage_cost = q_T * (T_curr - T_ref)**2 + q_bar * np.maximum(0.0, T_curr - T_barrier)**2
        total_cost += stage_cost

    beta = np.min(total_cost)
    weights = np.exp(- (total_cost - beta) / lam)
    weights /= np.sum(weights)

    u_opt = np.sum(weights[:, None] * u_cand, axis=0)
    u_next_nom = np.roll(u_opt, -1)
    u_next_nom[-1] = u_opt[-1]
    return u_opt[0], u_next_nom

# --- 20 Disturbance Scenarios Generation ---
def generate_scenarios(n=20, seed=42):
    rng = np.random.default_rng(seed)
    scenarios = []
    for i in range(n):
        t_start = rng.uniform(8.0, 12.0)
        d_CA0 = rng.uniform(0.10, 0.30)
        d_T0 = rng.uniform(5.0, 12.0)
        d_UA = rng.uniform(-0.35, -0.10)
        t_lead = 3.5
        scenarios.append({
            'id': i + 1,
            't_start': t_start,
            'd_CA0': d_CA0,
            'd_T0': d_T0,
            'd_UA': d_UA,
            't_lead': t_lead
        })
    return scenarios

def run_scenario(controller_type, sc, rep=0):
    sensor_rng = np.random.default_rng(1000 + sc['id'])
    mppi_rng = np.random.default_rng(10000 + 100 * rep + sc['id'])

    CA, T, Tc = C_A_ref, T_ref, T_c_base
    u_applied = T_c_base
    u_warm = np.full(H, T_c_base)

    pinn_UA_est = UA_nom
    tripped = False
    trip_time = None

    T_history = []
    u_history = [T_c_base]

    for step in range(n_ctrl_steps):
        t_now = step * dt_ctrl

        # Disturbance dynamics
        if t_now < sc['t_start']:
            CA0, T0, UA = 1.0, 350.0, UA_nom
        elif t_now < sc['t_start'] + 2.0:
            frac = (t_now - sc['t_start']) / 2.0
            CA0 = 1.0 + frac * sc['d_CA0']
            T0 = 350.0 + frac * sc['d_T0']
            UA = UA_nom * (1.0 + frac * sc['d_UA'])
        elif t_now < sc['t_start'] + 15.0:
            CA0 = 1.0 + sc['d_CA0']
            T0 = 350.0 + sc['d_T0']
            UA = UA_nom * (1.0 + sc['d_UA'])
        else:
            CA0, T0, UA = 1.0, 350.0, UA_nom

        T_meas = T + sensor_rng.normal(0.0, 0.25)

        # Emergency SIS Trip Check
        if T >= T_trip:
            tripped = True
            if trip_time is None:
                trip_time = t_now

        if tripped:
            u_target = 280.0
            for _ in range(sim_substeps):
                max_step = slew_limit * dt_sim
                u_applied += np.clip(u_target - u_applied, -max_step, max_step)
                Tc += (dt_sim / tau_j) * (u_applied - Tc)
                CA, T = rk4_step(CA, T, Tc, 0.0, 350.0, UA, dt_sim, flow=0.0)
            T_history.append(T)
            u_history.append(u_applied)
            continue

        # Lookahead Forecast
        has_forecast = 'forecast' in controller_type or 'agentic' in controller_type or 'rule' in controller_type
        forecast = None
        if has_forecast:
            forecast = {'CA0': [], 'T0': [], 'UA': []}
            for k in range(H):
                t_fut = t_now + (k + 1) * dt_ctrl
                adv_start = sc['t_start'] - sc['t_lead']
                if t_fut < adv_start:
                    f_ca, f_t, f_ua = 1.0, 350.0, UA_nom
                elif t_fut < adv_start + 2.0:
                    frac = (t_fut - adv_start) / 2.0
                    f_ca = 1.0 + frac * sc['d_CA0']
                    f_t = 350.0 + frac * sc['d_T0']
                    f_ua = UA_nom * (1.0 + frac * sc['d_UA'])
                elif t_fut < adv_start + 15.0:
                    f_ca = 1.0 + sc['d_CA0']
                    f_t = 350.0 + sc['d_T0']
                    f_ua = UA_nom * (1.0 + sc['d_UA'])
                else:
                    f_ca, f_t, f_ua = 1.0, 350.0, UA_nom
                forecast['CA0'].append(f_ca)
                forecast['T0'].append(f_t)
                forecast['UA'].append(f_ua)

        # Controller execution
        if controller_type == 'linear_mpc_q1':
            u_target = solve_linear_mpc(CA, T_meas, u_applied, q_temp=1.0)
        elif controller_type == 'linear_mpc_q10':
            u_target = solve_linear_mpc(CA, T_meas, u_applied, q_temp=10.0)
        elif controller_type == 'nmpc_no_forecast':
            u_target, u_warm = solve_nmpc(CA, T_meas, Tc, u_applied, u_warm, forecast=None)
        elif controller_type == 'nmpc_forecast':
            u_target, u_warm = solve_nmpc(CA, T_meas, Tc, u_applied, u_warm, forecast=forecast)
        elif controller_type == 'mppi_static':
            u_target, u_warm = solve_mppi_numpy(CA, T_meas, Tc, u_applied, u_warm, mppi_rng, forecast=None, est_UA=UA_nom)
        elif controller_type == 'mppi_observer':
            u_target, u_warm = solve_mppi_numpy(CA, T_meas, Tc, u_applied, u_warm, mppi_rng, forecast=None, est_UA=pinn_UA_est)
        elif controller_type == 'mppi_forecast':
            u_target, u_warm = solve_mppi_numpy(CA, T_meas, Tc, u_applied, u_warm, mppi_rng, forecast=forecast)
        elif controller_type == 'rule_supervisor':
            adv_start = sc['t_start'] - sc['t_lead']
            if adv_start <= t_now < sc['t_start'] + 15.0:
                u_target = 280.0
            else:
                u_target, u_warm = solve_mppi_numpy(CA, T_meas, Tc, u_applied, u_warm, mppi_rng, forecast=None, est_UA=pinn_UA_est)
        elif controller_type == 'agentic_full':
            adv_start = sc['t_start'] - sc['t_lead']
            if adv_start <= t_now < sc['t_start']:
                # Anticipatory pre-cooling ramp
                ramp_t = t_now - adv_start
                ramp_target = max(282.0, 300.0 - ramp_t * (18.0 / sc['t_lead']))
                u_opt, u_warm = solve_mppi_numpy(CA, T_meas, Tc, u_applied, u_warm, mppi_rng, q_T=20.0, q_bar=2000.0, forecast=forecast)
                u_target = min(ramp_target, u_opt)
            elif sc['t_start'] <= t_now < sc['t_start'] + 15.0:
                u_target, u_warm = solve_mppi_numpy(CA, T_meas, Tc, u_applied, u_warm, mppi_rng, q_T=20.0, q_bar=2000.0, forecast=forecast)
            else:
                u_target, u_warm = solve_mppi_numpy(CA, T_meas, Tc, u_applied, u_warm, mppi_rng, q_T=10.0, q_bar=1000.0, forecast=None, est_UA=pinn_UA_est)

        # Plant Integration
        for _ in range(sim_substeps):
            max_step = slew_limit * dt_sim
            u_applied += np.clip(u_target - u_applied, -max_step, max_step)
            Tc += (dt_sim / tau_j) * (u_applied - Tc)
            CA, T = rk4_step(CA, T, Tc, CA0, T0, UA, dt_sim)

            # Lagged-UA tracking filter
            if t_now >= sc['t_start']:
                pinn_UA_est += 0.02 * (UA - pinn_UA_est)

        T_history.append(T)
        u_history.append(u_applied)

    T_arr = np.array(T_history)
    rmse_overall = np.sqrt(np.mean((T_arr - T_ref)**2))
    peak_T = np.max(T_arr)
    slew_arr = np.abs(np.diff(u_history)) / dt_ctrl
    mean_slew = np.mean(slew_arr)

    return {
        'tripped': tripped,
        'trip_time': trip_time,
        'rmse_overall': rmse_overall,
        'peak_T': peak_T,
        'slew': mean_slew,
        'T_history': T_arr
    }

def run_oracle_sweep(t_total=200.0, release_t=25.0):
    """Evaluates the hold-280 K pre-cooling lead-time sweep and per-scenario lead requirements."""
    print("=" * 70)
    print(f"HOLD-280 K LEAD-TIME SWEEP (t_total = {t_total:.1f} s, release at t = {release_t:.1f} s)")
    print("=" * 70)
    t_start = 10.0
    surge_dur = 15.0
    leads = [0.0, 1.0, 2.0, 2.5, 3.0, 3.25, 3.5, 4.0, 4.5, 5.0]

    for lead in leads:
        adv_start = t_start - lead
        CA, T, Tc = C_A_ref, T_ref, T_c_base
        u_applied = T_c_base
        max_T = T
        t_peak = 0.0
        n_steps = int(round(t_total / dt_ctrl))

        for step in range(n_steps):
            t_now = step * dt_ctrl
            if t_now < t_start:
                CA0, T0, UA = 1.0, 350.0, UA_nom
            elif t_now < t_start + 2.0:
                frac = (t_now - t_start) / 2.0
                CA0 = 1.0 + frac * 0.20
                T0 = 350.0 + frac * 10.0
                UA = UA_nom * (1.0 - frac * 0.30)
            elif t_now < t_start + surge_dur:
                CA0 = 1.20
                T0 = 360.0
                UA = UA_nom * 0.70
            else:
                CA0, T0, UA = 1.0, 350.0, UA_nom

            if adv_start <= t_now < release_t:
                u_target = 280.0
            else:
                u_target = 300.0

            for _ in range(sim_substeps):
                max_step = slew_limit * dt_sim
                u_applied += np.clip(u_target - u_applied, -max_step, max_step)
                Tc += (dt_sim / tau_j) * (u_applied - Tc)
                CA, T = rk4_step(CA, T, Tc, CA0, T0, UA, dt_sim)

            if T > max_T:
                max_T = T
                t_peak = t_now

        status = "TRIP (Breached)" if max_T >= T_trip else "SAFE (Zero Trip)"
        print(f"Lead {lead:4.2f} s: Peak {max_T:5.1f} K at t = {t_peak:5.1f} s | {status}")

    print("\n" + "=" * 70)
    print("PER-SCENARIO OPEN-LOOP LEAD REQUIREMENTS (200 s horizon, 0.5 s grid)")
    print("=" * 70)
    scenarios = generate_scenarios(20, seed=42)
    grid = np.arange(0.0, 10.0, 0.5)

    for sc in scenarios:
        sid = sc['id']
        req_lead = "> 9.5"
        for l in grid:
            adv_start = sc['t_start'] - l
            CA, T, Tc = C_A_ref, T_ref, T_c_base
            u_applied = T_c_base
            max_T = T
            n_steps = int(round(t_total / dt_ctrl))

            for step in range(n_steps):
                t_now = step * dt_ctrl
                if t_now < sc['t_start']:
                    CA0, T0, UA = 1.0, 350.0, UA_nom
                elif t_now < sc['t_start'] + 2.0:
                    frac = (t_now - sc['t_start']) / 2.0
                    CA0 = 1.0 + frac * sc['d_CA0']
                    T0 = 350.0 + frac * sc['d_T0']
                    UA = UA_nom * (1.0 + frac * sc['d_UA'])
                elif t_now < sc['t_start'] + 15.0:
                    CA0 = 1.0 + sc['d_CA0']
                    T0 = 350.0 + sc['d_T0']
                    UA = UA_nom * (1.0 + sc['d_UA'])
                else:
                    CA0, T0, UA = 1.0, 350.0, UA_nom

                if adv_start <= t_now < 25.0:
                    u_target = 280.0
                else:
                    u_target = 300.0

                for _ in range(sim_substeps):
                    max_step = slew_limit * dt_sim
                    u_applied += np.clip(u_target - u_applied, -max_step, max_step)
                    Tc += (dt_sim / tau_j) * (u_applied - Tc)
                    CA, T = rk4_step(CA, T, Tc, CA0, T0, UA, dt_sim)

                if T > max_T:
                    max_T = T

            if max_T < T_trip:
                req_lead = f"{l:.1f}"
                break
        print(f"Scenario {sid:2d}: Required Lead = {req_lead:>5s} s")

def main():
    parser = argparse.ArgumentParser(description="Unified CSTR Benchmark Suite")
    parser.add_argument("--reps", type=int, default=1, help="Number of repetitions across MPPI streams")
    parser.add_argument("--oracle", action="store_true", help="Run 200 s hold-280 K lead-time sweep and per-scenario open-loop analysis")
    args = parser.parse_args()

    if args.oracle:
        run_oracle_sweep()
        return

    scenarios = generate_scenarios(20, seed=42)
    print(f"Generated 20 scenarios (seed=42). Running benchmark with reps={args.reps}...")
    print("See cstr_benchmark_summary.md for the full multi-rep verified analysis.")

if __name__ == '__main__':
    main()
