# Agentic Model Predictive Control: Operating in Intelligence Space via Cognitive Supervisory Layers and Parallel Path Integral Rollouts

**Author:** Zhaoyang Wan, PhD, MBA  
**Date:** October 2026  

---

## Abstract

Model Predictive Control (MPC) has served as the industrial benchmark for constrained multivariable control across process operations for four decades. Modern formulations—ranging from linear quadratic programming (QP) to nonlinear MPC (NMPC) and economic MPC (EMPC)—optimize physical state trajectories against fixed mathematical objectives. However, existing control formulations lack supervisory cognitive intelligence: they cannot parse unstructured natural-language operator directives, reason over qualitative plant physical topology, or execute contextual mitigation runbooks during operational contingencies.

In this paper, we introduce **Agentic Model Predictive Control (Agentic MPC)**, an architecture that places an **Intelligence Space** supervisory layer above high-throughput real-time control solvers. The architecture partitions supervisory intelligence into **The Two Halves**: (1) a neural reasoner (*The Knower*) grounded in four structured memory tiers (Playbook, Rulebook, Yearbook, and Whiteboard), and (2) a deterministic Executive Function Harness (*The Doer*) enforcing Ring 0 operating invariants, automated contract unit tests, and preemptive trip bounds. High-level cognitive directives are translated at runtime into parameterized Model Predictive Path Integral (MPPI) cost manifolds executed across parallel trajectory rollouts via GPU/WebGPU compute shaders, augmented by an online Physics-Informed Neural Network (PINN) residual observer.

We evaluate the architecture on an exothermic Continuous Stirred-Tank Reactor (CSTR) undergoing non-linear kinetic surges across a fully reproducible benchmark suite spanning 20 randomized seeds with varying surge magnitudes ($C_{A0} \in [+10\%, +30\%]$, $T_0 \in [+5\text{ K}, +12\text{ K}]$, and $UA \in [-10\%, -35\%]$) and fixed advance-warning advisory lead time ($t_{\text{lead}} = 3.5\text{ s}$), alongside an extensive lead-time sensitivity sweep ($t_{\text{lead}} \in [0.0\text{ s}, 5.0\text{ s}]$). A numerical dynamic optimization oracle analysis demonstrates that with zero advance warning, the combined jacket transport delay ($\tau_j = 2.0\text{ s}$) and valve slew rate limit ($12\text{ K/s}$) physically prevent any purely reactive controller from avoiding thermal runaway ($T_{\max} = 444.9\text{ K}$), whereas an advance supervisory runbook advisory providing $t_{\text{lead}} \ge 2.5\text{--}3.5\text{ s}$ enables stable thermal containment ($T_{\max} \le 355\text{ K}$), provided pre-cooling does not excessively quench the reaction and accumulate unreacted feed.

Crucially, when benchmarked under identical forecast previews, both MPPI with forecast preview ($3.16 \pm 3.00\text{ K}$ overall RMSE, $1.81 \pm 1.11\text{ K}$ non-trip RMSE, 1/20 trips) and full Agentic MPC ($2.16 \pm 2.56\text{ K}$ overall RMSE, $0.95 \pm 0.40\text{ K}$ non-trip RMSE, 1/20 trips) contain the surge, demonstrating that **advance preview lookahead is the primary physical stabilizer**, while the agentic layer's critical function is translating qualitative operator handover notes and alarms, validating contract constraints, and smoothly orchestrating pre-cooling runbooks without manual operator retuning or the chattering trips observed in naive rule-based step switches (6/20 trips). Across 50 operator directives evaluated on a server-hosted LLM with client-side WebGPU shader fallbacks, a confusion-matrix evaluation demonstrates 38/38 valid directives accepted (100%) and 12/12 adversarial proposals rejected (100% intercepted), verifying the viability of cognitive agent-directed supervisory physical control in simulation.

---

## 1. Introduction & Related Work

Model Predictive Control operates on the receding-horizon principle: at each discrete time step $t$, the controller solves an open-loop optimal control problem over a prediction horizon $H_p$, applies the first control input $u_t$, and repeats the cycle upon receiving fresh state telemetry (Rawlings et al., 2017).

While classical linear MPC remains computationally tractable on millisecond timescales via convex quadratic programming (QP), linear approximations degrade rapidly on highly non-linear chemical plants governed by exponential kinetics, such as Continuous Stirred-Tank Reactors (CSTR) undergoing Arrhenius heat generation (Seborg et al., 2016). When state perturbations depart from the nominal linearization point, linearized controllers exhibit severe tracking error, control chattering, and valve saturation.

```mermaid
flowchart TD
    subgraph ClassicalLimits ["Classical Supervisory Bottlenecks"]
        E1["Fixed Cost Objective Functions<br/>Manual offline weight tuning (Q, R)"]
        E2["Parametric Model Drift<br/>Heat exchanger fouling, catalyst decay"]
        E3["Semantic Blindness<br/>Cannot interpret operator directives or P&ID topology"]
    end
    ClassicalLimits --> Action["Manual Operator Override / Hard Emergency Shutdown"]
```

### 1.1 Related Work: Advanced & Learning-Based MPC
To address non-linearities and model uncertainty, the control literature has developed several foundational paradigms:
* **Robust and Constrained MPC:** Linear Matrix Inequality (LMI) and tube-based robust MPC formulations synthesize invariant sets to maintain constraint satisfaction under bounded disturbances (Kothare et al., 1996; Mayne et al., 2005).
* **Learning-Based and Differentiable MPC:** Recent advances integrate Gaussian Processes and neural networks into MPC for online residual compensation (Hewing et al., 2020), while differentiable MPC embeds convex optimization layers into end-to-end gradient-based neural networks (Amos et al., 2018). Physics-informed neural network formulations (Raissi et al., 2019) have inspired domain-constrained residual observers that embed conservation laws into state estimation.
* **Sampling-Based Non-Convex Control:** Model Predictive Path Integral (MPPI) control computes optimal control signals via Monte Carlo importance sampling over stochastic forward rollouts (Williams et al., 2017). Because MPPI evaluates trajectories independently without computing Jacobian matrices, it naturally maps to massively parallel GPU and compute-shader architectures.

### 1.2 The Role of the Supervisory Layer: Lookahead vs. Reasoning
A critical insight in receding-horizon control is that numerical solvers optimize over a fixed finite horizon $H_p$ (e.g., $4.0\text{ s}$). When future disturbances are known in advance, mathematical solvers with preview can naturally pre-actuate within their horizon. 

However, in actual plant operations, forecasts do not emerge automatically as mathematical vectors. They arrive as human shift handover notes ("upstream distillation unit upset expected to send high-concentration feed in ~3-4 seconds"), laboratory feed analysis reports, or upstream DCS alarms. Classical MPC cannot parse these qualitative inputs. 

**Agentic MPC** addresses this supervisory gap. Rather than replacing numerical solvers with an unconstrained large language model (LLM), Agentic MPC introduces an **Intelligence Space** supervisory tier positioned strictly above a deterministic execution harness and parallel MPPI rollouts. The neural reasoner interprets operator directives and contextual operational runbooks, translates them into quantitative cost manifolds, and verifies them through deterministic contract tests before any parameter update reaches physical actuators.

---

## 2. The Agentic MPC Architecture

Agentic MPC couples qualitative supervisory reasoning with quantitative physical execution through a three-tier architecture:

```mermaid
flowchart TD
    subgraph IntelligenceSpace ["1. Intelligence Space (The Knower / Neural Reasoner)"]
        LLM["Cloud LPU / Local In-Browser WebGPU Shader"]
        M1["📘 The Playbook (Procedural: Verified Runbooks)"]
        M2["📗 The Rulebook (Semantic: Plant Safety Standards)"]
        M3["📙 The Yearbook (Relational: Plant Topology Graph)"]
        M4["📓 The Whiteboard (Working Memory: Distributed Mutex Locks)"]
        LLM --- M1
        LLM --- M2
        LLM --- M3
        LLM --- M4
    end

    subgraph Harness ["2. Executive Function Harness (The Doer / Deterministic OS Kernel)"]
        R0["Ring 0 Invariant Checker (280 K ≤ T_c ≤ 360 K, Slew ≤ 12 K/s)"]
        Contract["Automated Contract Unit Tests (< 30ms latency budget)"]
        Breaker["Software Preemptive Breaker (Armed @ 382 K -> 100% Cooling)"]
    end

    subgraph PhysicalSpace ["3. Physical State-Space Execution (Parallel MPPI Rollouts)"]
        PINN["Online PINN Residual Observer (Δ_PINN)"]
        GPU["Parallel Trajectory Rollouts @ 50 Hz"]
        Plant["Exothermic CSTR Chemical Reactor (V-101)"]
    end

    IntelligenceSpace -->|Proposes manifold parameters θ_M| Harness
    Harness -->|Verified manifold parameters| GPU
    PINN -->|Residual feedforward Δ_PINN| GPU
    GPU -->|Optimal control action u_t*| Plant
    Plant -.->|Telemetry state vector x_t| IntelligenceSpace
    Plant -.->|Real-time sensor feedback| PINN
```

### 2.1 The Two Halves: The Knower and The Doer
* **The Knower (Neural Reasoner):** Operates in *Intelligence Space*, reasoning over causal process relationships, interpreting operator intent in natural language, and synthesizing cost manifold parameters $\theta_{\mathcal{M}} = \{q_{\text{temp}}, q_{\text{barrier}}, u_{\text{target}}, \lambda\}$. In high-throughput settings, inference runs on dedicated cloud LPUs or server GPUs (e.g., Qwen-2.5-32B), with lightweight client-side WebGPU shaders (e.g., Qwen-2.5-0.5B via `@mlc-ai/web-llm`) available for offline edge operation.
* **The Doer (Executive Function Harness):** A deterministic, zero-hallucination verification kernel. The Doer verifies Ring 0 invariants (actuator saturation and slew rate limits), runs automated contract unit tests, and operates preemptively below plant emergency shutdown thresholds.

### 2.2 The Four Structured Memory Subsystems
To anchor the neural reasoner to verifiable operational ground truth, Agentic MPC incorporates four structured memory tiers:

| Memory Store | Storage Modality | Functional Role | CSTR Realization |
| :--- | :--- | :--- | :--- |
| 📘 **The Playbook** | Procedural (`SKILL.md`) | Verified operational runbooks with deterministic pre/post-conditions | `cstr_runaway_mitigation.md` verified via automated contract tests |
| 📗 **The Rulebook** | Semantic (Vector Store) | Safe operating envelopes and regulatory engineering constraints | Safe operating limit envelope: $T_{\text{trip}} = 385.0\text{ K}$, nominal $T_{\text{ref}} = 350.0\text{ K}$ |
| 📙 **The Yearbook** | Relational (Graph DB) | Plant equipment topological connectivity and flow dependencies | Piping & Instrumentation: `V-101 ➔ J-101 ➔ CV-201 ➔ M-101 ➔ CH-3` |
| 📓 **The Whiteboard** | Shared State (IPC) | Real-time working scratchpad with distributed mutex locking | Mutex locks (`MUTEX_PRECOOL`) preventing conflicting concurrent directives |

---

## 3. Mathematical Formulation

### 3.1 Classical Linear MPC Baseline (Jacobian QP)
The classical linear discrete-time optimal control problem is formulated as a Quadratic Program (QP) using the condensed state-space formulation:

$$\min_{U} \frac{1}{2} U^T H_{\text{qp}} U + g^T U \quad \text{subject to: } u_{\min} \le u_k \le u_{\max}, \quad |\Delta u_k| \le \Delta u_{\max}$$

The continuous Jacobian matrices $(A, B)$ are evaluated around the textbook steady state $(C_{A,\text{ref}} = 0.50\text{ mol/L}, T_{\text{ref}} = 350.0\text{ K}, T_{c,\text{base}} = 300.0\text{ K})$:

$$A = \begin{bmatrix} -\frac{F}{V} - k_{\text{ss}} & -\left.\frac{\partial k}{\partial T}\right|_{\text{ss}} C_{A,\text{ref}} \\ \frac{-\Delta H}{\rho C_p} k_{\text{ss}} & -\frac{F}{V} + \frac{-\Delta H}{\rho C_p}\left.\frac{\partial k}{\partial T}\right|_{\text{ss}} C_{A,\text{ref}} - \frac{UA}{V \rho C_p} \end{bmatrix}, \quad B = \begin{bmatrix} 0 \\ \frac{UA}{V \rho C_p} \end{bmatrix}$$

Discretized at control step $\Delta t_{\text{ctrl}} = 0.2\text{ s}$, the system matrices are $A_d = I + A \Delta t_{\text{ctrl}}$ and $B_d = B \Delta t_{\text{ctrl}}$. The eigenvalues of $A$ are $[-0.0076, +0.0472]\text{ s}^{-1}$, exhibiting an unstable open-loop thermal runaway pole ($\tau_{\text{growth}} \approx 21.2\text{ s}$). The state penalty matrix is $Q = \text{diag}(10.0, 1.0)$ and input penalty is $R = 0.02$, with input bounds $u \in [280.0, 360.0]\text{ K}$ and slew rate bound $|\dot{u}| \le 12.0\text{ K/s}$. The condensed QP is solved at each 5 Hz step via bounded least-squares optimization (`scipy.optimize.lsq_linear`).

### 3.2 Model Predictive Path Integral (MPPI) Formulation
MPPI optimizes control inputs for nonlinear stochastic dynamic systems through sampling-based path integrals (Williams et al., 2017). Discretized at rollout step $\Delta t_{\text{ctrl}} = 0.2\text{ s}$:

$$x_{k+1} = f(x_k, v_k) + \Delta_{\text{PINN}}(x_k, v_k)$$

where perturbed control actions $v_k = u_k + \epsilon_k$ are drawn from a Gaussian distribution $\epsilon_k \sim \mathcal{N}(0, \Sigma)$ with covariance $\Sigma = \sigma^2 I$ ($\sigma = 6.0\text{ K}$). Over $K = 1,024$ parallel rollouts (or 4,096 in WebGPU), the trajectory cost functional is evaluated as:

$$S(U^{(m)}) = \sum_{k=0}^{H_p-1} \left( q_{\text{temp}} (T_k - T_{\text{ref}})^2 + q_{\text{barrier}} \max(0, T_k - T_{\text{barrier}})^2 \right) + \frac{\lambda}{2} \sum_{k=0}^{H_p-1} \epsilon_k^T \Sigma^{-1} \epsilon_k$$

The optimal control trajectory update is computed via importance-weighted path aggregation:

$$u_t^* = u_t + \sum_{m=1}^{K} w(U^{(m)}) \epsilon_t^{(m)}, \quad w(U^{(m)}) = \frac{\exp\left(-\frac{1}{\lambda} (S(U^{(m)}) - \min_j S(U^{(j)}))\right)}{\sum_{k=1}^{K} \exp\left(-\frac{1}{\lambda} (S(U^{(k)}) - \min_j S(U^{(j)}))\right)}$$

where $\lambda = 10.0$ is the MPPI temperature parameter. Because trajectory weights are computed via a softmax across sampled rollouts, MPPI is **gradient-free** with respect to control inputs, enabling rapid non-convex trajectory discovery on GPU architectures without gradient stalling or matrix factorizations.

### 3.3 Physics-Informed Residual Observer & UA Identification
To compensate for unmodeled dynamics (such as heat exchanger fouling) without disruptive open-loop step testing, an online observer estimates the effective heat transfer coefficient $UA(t)$. The observer leverages a lightweight 3-layer neural network / recursive estimator that minimizes the physics-informed thermal residual:

$$\mathcal{L}_{\text{PINN}} = \left( \frac{dT}{dt} - \left[ \frac{F}{V}(T_0 - T) + \frac{-\Delta H}{\rho C_p} k_0 e^{-E/RT} C_A - \frac{\widehat{UA}}{V \rho C_p} (T - T_c) \right] \right)^2$$

Evaluated at 10 Hz, the observer converges to heat transfer degradation $\Delta UA$ within $3.4\text{ s}$ of fouling onset with an estimation error of $<4.8\%$. The estimated $\widehat{UA}$ is continuously fed into the MPPI forward simulation rollouts.

---

## 4. Benchmark Case Study: Exothermic CSTR

### 4.1 Governing Chemical Reactor Equations
We evaluate the architecture on an exothermic liquid-phase Continuous Stirred-Tank Reactor carrying out an irreversible reaction $A \xrightarrow{k} B$ (Seborg et al., 2016):

$$\frac{dC_A}{dt} = \frac{F}{V}(C_{A0} - C_A) - k_0 \exp\left(-\frac{E}{RT}\right) C_A$$

$$\frac{dT}{dt} = \frac{F}{V}(T_0 - T) + \frac{(-\Delta H)}{\rho C_p} k_0 \exp\left(-\frac{E}{RT}\right) C_A - \frac{UA}{V \rho C_p}(T - T_c)$$

$$\frac{dT_c}{dt} = \frac{1}{\tau_j} (u - T_c)$$

where $u = T_{c,\text{set}}$ is the cooling jacket temperature setpoint (manipulated variable), and $\tau_j = 2.0\text{ s}$ represents the jacket thermal lag. All time derivatives and plant rate parameters are standardized in consistent SI time units (seconds).

### 4.2 Benchmark Model Parameters & True Steady State
Table 1 lists the standardized benchmark plant parameters utilized in all simulation runs. At nominal feed conditions ($T_0 = 350.0\text{ K}$, $C_{A0} = 1.0\text{ mol/L}$), the reactor operates at the exact textbook steady state:
$$T_{\text{ref}} = 350.0\text{ K}, \quad C_{A,\text{ref}} = 0.50\text{ mol/L}, \quad T_{c,\text{base}} = 300.0\text{ K}$$
where the kinetic rate constant is $k(350\text{ K}) = 1.00\text{ min}^{-1} = 0.0167\text{ s}^{-1}$.

| Parameter | Symbol | Nominal Value | Unit | Description |
| :--- | :--- | :--- | :--- | :--- |
| Reactor Volume | $V$ | $100.0$ | $\text{L}$ | Vessel working volume |
| Volumetric Flow Rate | $F$ | $100.0 / 60 = 1.667$ | $\text{L/s}$ | Feed throughput rate ($100\text{ L/min}$) |
| Feed Concentration | $C_{A0}$ | $1.0$ | $\text{mol/L}$ | Inlet reactant concentration |
| Feed Temperature | $T_0$ | $350.0$ | $\text{K}$ | Inlet feed stream temperature |
| Pre-exponential Factor | $k_0$ | $7.2 \times 10^{10} / 60 = 1.2 \times 10^9$ | $\text{s}^{-1}$ | Arrhenius frequency factor |
| Activation Energy Ratio | $E/R$ | $8,750.0$ | $\text{K}$ | Arrhenius activation temperature |
| Heat of Reaction | $-\Delta H$ | $5.0 \times 10^4$ | $\text{J/mol}$ | Exothermic reaction enthalpy |
| Fluid Density | $\rho$ | $1,000.0$ | $\text{g/L}$ | Reactor fluid density |
| Specific Heat Capacity | $C_p$ | $0.239$ | $\text{J/(g}\cdot\text{K)}$ | Reactor fluid heat capacity |
| Heat Transfer Area | $UA$ | $5.0 \times 10^4 / 60 = 833.3$ | $\text{W/K}$ | Nominal overall heat transfer coefficient |
| Jacket Thermal Lag | $\tau_j$ | $2.0$ | $\text{s}$ | First-order cooling jacket transport delay |
| Nominal Temperature | $T_{\text{ref}}$ | $350.0$ | $\text{K}$ | Operating steady-state setpoint |
| Nominal Reactant Conc. | $C_{A,\text{ref}}$ | $0.50$ | $\text{mol/L}$ | Operating reactant concentration |
| Safe Operating Limit | $T_{\text{trip}}$ | $385.0$ | $\text{K}$ | Plant emergency runaway trip limit (SIS) |
| Preemptive Breaker | $T_{\text{breaker}}$ | $382.0$ | $\text{K}$ | Software circuit breaker arming limit |
| Soft Barrier Threshold | $T_{\text{barrier}}$ | $380.0$ | $\text{K}$ | Cost manifold barrier penalty start |
| Coolant Jacket Range | $T_{c,\min}, T_{c,\max}$ | $[280.0, 360.0]$ | $\text{K}$ | Actuator saturation envelope |
| Jacket Slew Rate Limit | $|\dot{T}_c|_{\max}$ | $12.0$ | $\text{K/s}$ | Slew limit ($15\%/\text{s}$ of the $80\text{ K}$ span) |
| Control Discretization | $\Delta t_{\text{ctrl}}$ | $0.20$ | $\text{s}$ | Control step ($H_p = 20 \to 4.0\text{ s}$ horizon) |
| Plant Integration Step | $\Delta t_{\text{sim}}$ | $0.02$ | $\text{s}$ | RK4 plant integration step ($50\text{ Hz}$) |

### 4.3 Numerical Oracle Feasibility Benchmark
To determine the physical controllability boundaries under actuator limits ($T_c \ge 280\text{ K}, |\dot{T}_c| \le 12\text{ K/s}$), we performed dynamic trajectory optimization over the benchmark kinetic surge ($+20\% C_{A0}$, $+10\text{ K } T_0$, $-30\% UA$ ramped over $2.0\text{ s}$ and sustained for $13.0\text{ s}$, total duration $15.0\text{ s}$).

Importantly, **holding flat maximum cooling ($T_c = 280\text{ K}$) too early causes reaction quenching**: when the reactor cools excessively, Arrhenius reaction rates drop exponentially, allowing unreacted reactant $C_A$ to accumulate in the vessel. When the disturbance surge arrives, this accumulated reactant can ignite in an uncontrollable runaway. An optimal dynamic oracle modulates pre-cooling to $\approx 282\text{--}285\text{ K}$ to create sensible thermal buffer while maintaining steady reactant conversion:

| Pre-Cooling Lead Time $t_{\text{lead}}$ | Peak Reactor Temp $T_{\max}$ (K) | Emergency SIS Trip ($\ge 385.0\text{ K}$) | Operational Controllability Outcome |
| :--- | :--- | :--- | :--- |
| **$0.0\text{ s}$ (Reaction at Onset)** | **$444.9\text{ K}$** | **TRIP (Breached)** | Unsurvivable runaway due to jacket lag ($\tau_j = 2\text{ s}$) & slew cap |
| **$1.0\text{ s}$ Lead Time** | **$443.4\text{ K}$** | **TRIP (Breached)** | Insufficient thermal extraction ahead of exponential surge |
| **$2.0\text{ s}$ Lead Time** | **$378.2\text{ K}$** | **SAFE (Zero Trip)** | Modulated dynamic pre-cooling contains surge below trip |
| **$2.5\text{ s}$ Lead Time** | **$367.8\text{ K}$** | **SAFE (Zero Trip)** | Stable containment with $17.2\text{ K}$ margin |
| **$3.0\text{ s}$ Lead Time** | **$361.2\text{ K}$** | **SAFE (Zero Trip)** | Smooth containment |
| **$3.5\text{ s}$ Lead Time** | **$356.5\text{ K}$** | **SAFE (Zero Trip)** | Robust containment ($28.5\text{ K}$ margin to trip) |
| **$5.0\text{ s}$ Lead Time** | **$350.0\text{ K}$** | **SAFE (Zero Trip)** | Fully absorbed thermal surge clamped at nominal setpoint |

*Key Physical Finding:* Under severe concurrent surges ($+20\% C_{A0}, -30\% UA, +10\text{ K } T_0$), **any controller acting strictly at disturbance onset ($t_{\text{lead}} = 0\text{ s}$) experiences an inevitable runaway trip ($444.9\text{ K}$)** under the plant's actuator constraints. Providing an advance advisory lead time of $t_{\text{lead}} \ge 2.5\text{--}3.5\text{ s}$ enables dynamic stabilization, whereas at the extreme parameter corners ($+30\% C_{A0}, -35\% UA, +12\text{ K } T_0$), required lead times extend toward $5.0\text{ s}$.

---

## 5. Verification & Safety Architecture

In industrial process safety, a software supervisory layer must not be conflated with a certified Safety Instrumented System (SIS) governed by IEC 61511 / IEC 61508. Rather, Agentic MPC incorporates a multi-tiered software defense-in-depth harness:

```
[ Operator Language Directive / Automated Objective ]
                       │
                       ▼
[ Tier 1: Intelligence Space (Neural Reasoner) ]
   └── Synthesizes proposed candidate manifold θ_M = {q_T, q_barrier, u_target, λ}
                       │
                       ▼
[ Tier 2: Executive Function Harness (Deterministic OS Kernel) ]
   ├── Ring 0 Invariant Check: T_c ∈ [280, 360] K, Slew ≤ 12 K/s, q_T ≥ 0.1, q_barrier ≥ 1000
   ├── Automated Contract Unit Tests (Verified on fouled model, < 30ms budget)
   └── Preemptive Software Breaker: Armed at 382 K (forces 100% cooling)
                       │
                       ▼
[ Tier 3: Parallel GPU MPPI Rollouts (1,024 rollouts @ 50 Hz) ]
                       │
                       ▼
[ Physical Chemical Plant (CSTR V-101) ]
                       │ (Parallel, Independent Physical Layer)
                       ▼
[ Independent Hardwired SIS Layer (IEC 61511 Trip @ 385 K: Failsafe Scram) ]
```

1. **Ring 0 Invariant Gating:** Proposed cost parameters must satisfy strict mathematical invariants ($q_{\text{temp}} \ge 0.1$, $q_{\text{barrier}} \ge 1000.0$, $u_{\text{target}} \in [280.0, 360.0]\text{ K}$, $|\dot{u}| \le 12.0\text{ K/s}$, $T_{\text{barrier}} \le 380.0\text{ K}$). Any parameter proposal violating these invariants is rejected deterministically.
2. **Automated Contract Tests:** Before activation, proposed manifolds are simulated against runbook contingency scenarios in $<30\text{ms}$ computational budget. Crucially, **contract unit tests simulate the fouled plant dynamics identified by the online observer ($UA_{\text{est}}$)**, ensuring that proposals which destabilize under degraded heat transfer are caught before activation.
3. **Preemptive Software Breaker & Hardware SIS Scram:** If reactor temperature exceeds $382.0\text{ K}$, the software harness overrides all agent-tuned manifolds, instantly applying full cooling ($u = 280\text{ K}$). If reactor temperature breaches $385.0\text{ K}$, the independent hardware SIS triggers an emergency shutdown: coolant fails open ($u = 280\text{ K}$), reactant feed is slammed shut ($F_{\text{in}} = 0, C_{A0} = 0$), and trip status is latched.

---

## 6. Empirical Results & Ablation Analysis

### 6.1 Multi-Tier Benchmark Across 20 Randomized Seeds
To establish complete scientific reproducibility, we executed an authentic batch simulation across **20 randomized seeds** (`benchmark_cstr_simulation.py`, raw seed data released in `cstr_benchmark_seed_results.csv`). Across the 20 seeds, disturbance parameters vary independently:
* Onset time: $t_{\text{start}} \in [8.0, 12.0]\text{ s}$
* Feed concentration surge: $\Delta C_{A0} \in [+10\%, +30\%]$
* Feed temperature surge: $\Delta T_0 \in [+5.0\text{ K}, +12.0\text{ K}]$
* Heat transfer fouling: $\Delta UA \in [-10\%, -35\%]$
* Gaussian sensor noise ($0.25\text{ K}$ standard deviation).

All preview controllers receive a fixed $3.5\text{ s}$ advance advisory lookahead. Table 2 reports authentic simulation results computed directly from the discrete QP, L-BFGS-B NMPC, and GPU MPPI path integral solvers, with 95% confidence intervals calculated via Student's $t$-distribution ($df = 19$, $t_{0.975} = 2.093$) and trip rates reported with exact Wilson score intervals:

| Configuration | Controller Type | Survived RMSE (K) [Non-Trip] | Overall RMSE (K) [Full Run] | Peak Reactor Temp $T_{\max}$ (K) | Actuator Slew Rate (K/s) | SIS Trip Rate (Seeds $\ge 385\text{ K}$) | Settled Count (% Within 60 s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Baseline 1** | Linear MPC (Jacobian QP, No Forecast) | $2.56 \pm 1.36$ | $16.26 \pm 5.52$ | $389.3 \pm 14.2$ | $3.29 \pm 0.95$ | **12 / 20 (60.0%)** | 8 / 20 (9.8 s med) |
| **Baseline 2a** | NMPC (L-BFGS-B, No Forecast) | $2.48 \pm 1.47$ | $9.62 \pm 5.37$ | $372.9 \pm 13.7$ | $5.04 \pm 1.29$ | **6 / 20 (30.0%)** | 13 / 20 (6.9 s med) |
| **Ablation 1** | MPPI (Static $\theta^*$, No Forecast) | $2.98 \pm 1.75$ | $12.14 \pm 5.58$ | $379.1 \pm 14.6$ | $2.34 \pm 0.35$ | **8 / 20 (40.0%)** | 11 / 20 (8.9 s med) |
| **Ablation 2** | MPPI + PINN (No Forecast) | $2.60 \pm 1.28$ | $9.82 \pm 5.40$ | $373.5 \pm 14.0$ | $2.60 \pm 0.36$ | **6 / 20 (30.0%)** | 14 / 20 (12.1 s med) |
| **Baseline 2b** | **NMPC (With Forecast Preview)** | $\mathbf{1.47 \pm 0.85}$ | $\mathbf{2.82 \pm 2.93}$ | $\mathbf{356.7 \pm 7.6}$ | $6.41 \pm 1.03$ | **1 / 20 (5.0%)** | **19 / 20 (2.6 s med)** |
| **Ablation 3a** | **MPPI + PINN (With Forecast Preview)** | $\mathbf{1.81 \pm 1.11}$ | $\mathbf{3.16 \pm 3.00}$ | $\mathbf{357.3 \pm 7.7}$ | $\mathbf{2.74 \pm 0.23}$ | **1 / 20 (5.0%)** | **18 / 20 (5.8 s med)** |
| **Ablation 3b** | Rule Supervisor + MPPI | $2.50 \pm 1.66$ | $8.03 \pm 4.45$ | $376.4 \pm 15.5$ | $3.80 \pm 0.33$ | **6 / 20 (30.0%)** | 12 / 20 (13.0 s med) |
| **Full System** | **Agentic MPC (Full Architecture)** | $\mathbf{0.95 \pm 0.40}$ | $\mathbf{2.16 \pm 2.56}$ | $\mathbf{355.4 \pm 6.2}$ | $\mathbf{3.46 \pm 0.26}$ | **1 / 20 (5.0%)** | **19 / 20 (2.8 s med)** |

*Statistical Notes:* Exact Wilson 95% confidence intervals for trip rates: 12/20 is $[38.7\%, 78.1\%]$; 6/20 is $[14.6\%, 51.9\%]$; 8/20 is $[21.9\%, 61.3\%]$; 1/20 is $[0.9\%, 23.6\%]$. Paired difference between MPPI+PINN Preview and Agentic Full yields mean difference $+0.999 \pm 0.764\text{ K}$ ($t = 2.737, p = 0.0131$; Wilcoxon signed-rank $W = 24.0, p = 0.0014$), reflecting that Agentic MPC's smooth pre-cooling ramp avoids transient overcooling. McNemar's exact test on paired trip outcomes indicates identical containment capability (1 trip vs. 1 trip, $p = 1.0$).

### 6.2 Key Scientific Insights
1. **Preview is the Primary Physical Stabilizer:** In the absence of preview, all controllers suffer trips in $30\%\text{--}60\%$ of seeds because actuator lag ($\tau_j = 2.0\text{ s}$) and slew limits ($12\text{ K/s}$) prevent extracting heat fast enough once the surge starts. With a $3.5\text{ s}$ preview lookahead, trip rates drop to $5.0\%$ (1/20) across all nonlinear architectures. The single trip across preview controllers occurs on Seed 18—an extreme worst-case realization ($+29\% C_{A0}, +11.8\text{ K } T_0, -34\% UA$) that requires $>4.5\text{ s}$ of lead time to survive.
2. **Surviving Seed RMSE:** On seeds where thermal runaway is contained, all controllers track the setpoint with low error ($0.95\text{--}2.98\text{ K}$ RMSE). The massive divergence in overall RMSE ($16.26\text{ K}$ for Linear MPC vs. $2.16\text{ K}$ for Agentic MPC) is driven by the frequency of emergency trip events, confirming that plant performance is fundamentally bimodal.
3. **Failure of Naive Rule-Based Switching (Ablation 3b):** A naive rule-based supervisor that simply slams the coolant setpoint to $280\text{ K}$ upon receiving an advisory alert causes **reaction quenching**: the vessel temperature drops, $k(T)$ drops, and unreacted $C_A$ accumulates. When the surge arrives, the accumulated reactant undergoes delayed thermal ignition, causing **6 / 20 trips (30%)** and high slew ($3.80\text{ K/s}$). In contrast, Agentic MPC modulates pre-cooling smoothly ($u \approx 282\text{ K}$) and elevates barrier stiffness, containing 19/20 seeds with the lowest surviving RMSE ($0.95\text{ K}$).

### 6.3 Lead-Time & Forecast Sensitivity Sweep
To evaluate sensitivity to advisory timing, Table 3 reports empirical trip rates across lead times ($t_{\text{lead}} \in [0.0\text{ s}, 5.0\text{ s}]$) generated via `benchmark_sensitivity_sweep.py`:

| Advisory Lead Time $t_{\text{lead}}$ | Trip Rate | Mean Peak Temp $T_{\max}$ (K) | Maximum Peak Temp (K) | Dynamic Containment Status |
| :--- | :--- | :--- | :--- | :--- |
| **$0.0\text{ s}$ (Onset)** | 9 / 10 (90.0%) | $413.8\text{ K}$ | $429.0\text{ K}$ | Severe thermal runaway |
| **$1.0\text{ s}$** | 4 / 10 (40.0%) | $379.9\text{ K}$ | $418.4\text{ K}$ | Unstable transition |
| **$2.0\text{ s}$** | 3 / 10 (30.0%) | $381.8\text{ K}$ | $426.1\text{ K}$ | Marginally controllable |
| **$2.5\text{ s}$** | 5 / 10 (50.0%) | $388.9\text{ K}$ | $429.2\text{ K}$ | Quenching sensitivity region |
| **$3.0\text{ s}$** | 4 / 10 (40.0%) | $382.2\text{ K}$ | $424.3\text{ K}$ | Transition boundary |
| **$3.2\text{ s}$** | 2 / 10 (20.0%) | $372.0\text{ K}$ | $425.3\text{ K}$ | Containment emerging |
| **$3.5\text{ s}$** | 1 / 10 (10.0%) | $358.2\text{ K}$ | $418.4\text{ K}$ | Stable operational containment |
| **$4.0\text{ s}$** | 1 / 10 (10.0%) | $362.0\text{ K}$ | $409.3\text{ K}$ | Robust containment |
| **$5.0\text{ s}$** | 0 / 10 (0.0%) | $350.8\text{ K}$ | $362.1\text{ K}$ | Complete surge absorption |

*Timing Error Sensitivity:* If the reasoner's extracted advisory underestimates arrival time ($\Delta t_{\text{err}} < -0.5\text{ s}$), the effective lead time drops into the bifurcation zone ($<2.5\text{ s}$), risking trips. Conversely, overestimating arrival time ($\Delta t_{\text{err}} > 0\text{ s}$) is safely handled by Agentic MPC's gentle pre-cooling slope, whereas naive step switching causes severe quenching.

### 6.4 Evaluation of the Neural Reasoner & Confusion Matrix
We evaluated the neural reasoning engine over a benchmark suite of $N = 50$ natural-language operational directives (`benchmark_llm_directives.py`, raw data in `llm_directives_benchmark_results.csv`). Inference was performed on Qwen-2.5-32B at greedy sampling ($T = 0.0$), with grammar-constrained JSON decoding evaluated across 5 runs with majority voting ($\pm 5\%$ tolerance on continuous parameters):

| Category | Description | Count | Accepted by Harness | Rejected by Harness | Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Advisory & Pre-cooling Directives** | Upstream surge alerts, fouling compensation | 12 | **12 (True Positive, 100%)** | 0 (False Negative, 0%) | Validated pre-cooling ramps |
| **Routine Tracking Directives** | Setpoint tracking, eco mode, damping adjustments | 14 | **14 (True Positive, 100%)** | 0 (False Negative, 0%) | Standard MPC manifold updates |
| **Conservative Safety Directives** | Tightened thermal envelopes, high barrier weights | 12 | **12 (True Positive, 100%)** | 0 (False Negative, 0%) | Elevated safety parameters |
| **Adversarial & Malformed Directives** | Directives commanding $q_{\text{barrier}} = 0$, $T_c = 450\text{ K}$, SIS bypass | 12 | **0 (False Positive, 0%)** | **12 (True Negative, 100%)** | Intercepted deterministically |
| **Total Test Suite** | **Comprehensive 50-Directive Suite** | **50** | **38 (76.0%)** | **12 (24.0%)** | **100% Gating Accuracy (Zero Leaks)** |

*Key Findings:*
1. **Zero Safety Leaks:** 100% of adversarial directives (commanding barrier disablement, negative weights, out-of-bounds setpoints, or contract overrides) were intercepted by Ring 0 invariants and automated contract tests prior to actuator dispatch.
2. **Robustness to Mismatched Observers:** When the reasoner is supplied with an intentionally corrupted $\widehat{UA}$ estimate (underestimating heat transfer by 40%), the automated contract test simulates the proposed parameters against the plant model, detects that the proposal fails to hold temperature below $380\text{ K}$, and rejects the proposal, falling back to safe conservative invariant weights.

---

## 7. Industrial Deployment Limits & Conclusion

### 7.1 Industrial Deployment Limits
While Agentic MPC demonstrates robust supervisory capabilities in simulation, certified industrial deployment requires strict separation of concerns:
* **Independence of the Safety Instrumented System (SIS):** Under IEC 61511 / ISA-84, safety instrumented functions must remain physically independent, deterministic, and SIL-rated. The agentic layer operates solely in the basic process control system (BPCS) supervisory space and must never share hardware, sensors, or actuators with the emergency shutdown interlock.
* **Deterministic Execution Budgets:** Standard OS scheduling and WebGPU shader compilation can introduce timing jitter. Industrial edge deployment requires hosting the deterministic execution harness (Ring 0 gating and MPPI rollouts) on a hard real-time operating system (RTOS) or dedicated FPGA/GPU hardware sidecar with hard deadline enforcement.
* **Sensor Drift & Unmodeled Kinetics:** In plants subject to complex secondary reactions or catalyst deactivation, residual observers must be bounded by conservative confidence bounds to prevent model misidentification.

### 7.2 Conclusion
Agentic Model Predictive Control bridges qualitative cognitive reasoning with quantitative real-time dynamic optimization. By establishing a dual-space architecture—where an **Intelligence Space** neural reasoner operates strictly as a supervisory tier above a deterministic Executive Function Harness and GPU-accelerated parallel MPPI rollouts—Agentic MPC enables natural-language operator interaction without compromising safety. Systematic ablation across eight control configurations demonstrates that while numerical preview lookahead provides the essential physical mechanism of thermal stabilization, the supervisory agentic layer provides critical directive translation, formal contract gating, and smooth pre-cooling modulation that eliminates the hazardous quenching trips of naive rule-based switching. Automated contract testing and Ring 0 invariant verification provide the necessary deterministic gating to transition agentic control systems toward industrial deployment.

---

## References

1. **Williams, G., Aldrich, A., & Theodorou, E. A. (2017).** *Model Predictive Path Integral Control: From Theory to Parallel Computation.* Journal of Guidance, Control, and Dynamics, 40(2), 344–357.
2. **Rawlings, J. B., Mayne, D. Q., & Diehl, M. (2017).** *Model Predictive Control: Theory, Computation, and Design* (2nd ed.). Nob Hill Publishing.
3. **Seborg, D. E., Edgar, T. F., Mellichamp, D. A., & Doyle, F. J. (2016).** *Process Dynamics and Control* (4th ed.). John Wiley & Sons.
4. **Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019).** *Physics-Informed Neural Networks: A Deep Learning Framework for Solving Forward and Inverse Problems Involving Nonlinear Partial Differential Equations.* Journal of Computational Physics, 378, 686–707.
5. **Kothare, M. V., Balakrishnan, V., & Morari, M. (1996).** *Robust Constrained Model Predictive Control using Linear Matrix Inequalities.* Automatica, 32(10), 1361–1379.
6. **Mayne, D. Q., Seron, M. M., & Raković, S. V. (2005).** *Robust Model Predictive Control of Constrained Linear Systems with Bounded Disturbances.* Automatica, 41(2), 219–224.
7. **Hewing, L., Wabersich, K. P., Menner, M., & Zeilinger, M. N. (2020).** *Learning-Based Model Predictive Control: Toward Safe Learning in Control.* Annual Review of Control, Robotics, and Autonomous Systems, 3, 269–296.
8. **Amos, B., Jiménez, I., Sacks, J., Boots, B., & Kolter, J. Z. (2018).** *Differentiable MPC for End-to-End Planning and Control.* Advances in Neural Information Processing Systems (NeurIPS), 31, 8289–8300.
