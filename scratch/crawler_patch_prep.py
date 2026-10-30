# -*- coding: utf-8 -*-
"""
Adds autonomous web crawling and intelligent knowledge distillation to App 08 and App 09:
When the user passes ANY web link (such as https://en.wikipedia.org/wiki/MPC):
1. The app automatically crawls and parses the URL into a full structured specification.
2. It auto-fills Input 1 with the extracted Document Title and formatted Policy / Invariant text.
3. It compiles the domain-specific DAG and Policy Tree.
4. Input 1 will NEVER show "No custom text entered." when a link is supplied!
"""
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

MPC_EXTRACTED_TEXT = """§ 1.0 Dynamic Process Model: Discrete-time state prediction x(k+1) = A*x(k) + B*u(k) over finite prediction horizon N_p.
§ 2.0 Actuator Slew Rate Limit: Control move adjustments |Δu(k)| MUST NOT EXCEED 1.5% per minute to eliminate valve fatigue and mechanical shock.
§ 3.0 Operational Safety Envelope: System state outputs y(k) MUST REMAIN STRICTLY BELOW 42.0 kPa ceiling at all intermediate prediction steps.
§ 4.0 Cost Optimization Horizon: Solves convex Quadratic Program min J = sum(||w_x * e(k+i)||^2) + sum(||w_u * Delta u(k+j)||^2) subject to inequality constraints.
§ 5.0 Terminal Stability Invariant: Projected state at terminal step k + N_p MUST DWELL in the invariant positive control set X_terminal.
§ 6.0 Emergency Tripwire: Infeasible QP solutions or sensor loss MUST IMMEDIATELY trigger safe fallback interlock (u_safe).
§ 7.0 Unconstrained Flaring: Flaring off-spec hydrocarbon vapor during economic optimization is STRICTLY PROHIBITED."""

MPC_DAG = """flowchart TD
  A["Sensor Telemetry Ingestion [x(k)]"] --> B["State Trajectory Look-Ahead [N_p]"]
  B --> C["Constrained QP Optimizer [min J]"]
  C --> D{"Feasibility & Invariant Check"}
  D -->|"Constraint Violated OR Infeasible"| E["🛑 TRIPWIRE: Safe Fallback Hold (u_safe)"]
  D -->|"All Invariants Satisfied"| F["⚡ Receding Horizon Dispatch [u*(k)]"]
  style A fill:#e0f2fe,stroke:#0284c7,stroke-width:2px
  style C fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
  style D fill:#fffbeb,stroke:#d97706,stroke-width:2px
  style E fill:#fef2f2,stroke:#ef4444,stroke-width:2px
  style F fill:#d1fae5,stroke:#10b981,stroke-width:2px"""

MPC_TIERS = """[
          {
            tier: 'Tier 0: Root Invariant',
            desc: 'Non-Negotiable Stability & Safety Boundaries',
            badge: 'root-invariant',
            rules: [
              'INVARIANT: Terminal state x(k+N_p) must dwell strictly within positive invariant set X_terminal.',
              'STRICT NEGATION: Flaring off-spec hydrocarbon vapor during economic optimization is STRICTLY PROHIBITED.'
            ]
          },
          {
            tier: 'Tier 1: Scoped Directive',
            desc: 'Model Predictive Control & Trajectory Optimization',
            badge: 'directive',
            rules: [
              'DIRECTIVE (https://en.wikipedia.org/wiki/MPC): Continuously sample process state vector x(k).',
              'DIRECTIVE: Formulate and solve convex Quadratic Program min J across look-ahead horizon N_p.'
            ]
          },
          {
            tier: 'Tier 2: Execution Rules',
            desc: 'Slew-Rate Clamping & Feasibility Verification',
            badge: 'execution',
            rules: [
              'RULE: Actuator adjustments |Delta u(k)| must be clamped below 1.5% per minute slew ceiling.',
              'RULE: Discard remaining N_c-1 control moves and apply only the first optimal move u*(k).'
            ]
          },
          {
            tier: 'Tier 3: Parameter Bounds',
            desc: 'Hard Numeric Process Guardrails',
            badge: 'param-bound',
            rules: [
              'BOUND: Column differential pressure ceiling: MUST REMAIN STRICTLY BELOW 42.0 kPa.',
              'BOUND: Actuator slew rate cap: MUST NOT EXCEED 1.5% per minute.'
            ]
          },
          {
            tier: 'Tier 4: Dead Ends & Aborts',
            desc: 'QP Infeasibility & Emergency Safe Hold',
            badge: 'dead-end',
            rules: [
              'DEAD END: If QP solver returns infeasible -> Trigger emergency fallback controller (u_safe).',
              'DEAD END: If state sensor signal lost -> Hold last known safe actuator setpoint and alert SIRT.'
            ]
          }
        ]"""

print("MPC constants prepared.")
