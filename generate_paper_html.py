"""
generate_paper_html.py
Generates the publication-grade HTML version of agentic_mpc_paper.html with:
  1. Equal tuning across baselines (Linear MPC q_T=10 vs q_T=1).
  2. Deconstruction of the supervisory anticipatory pre-cooling schedule.
  3. Grounded architectural specification of the Agentic LLM layer.
"""

html_content = r"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Agentic Model Predictive Control — Technical Paper</title>

  <!-- Google Fonts: Inter, JetBrains Mono, & Newsreader for academic serif text -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;0,6..72,700;1,6..72,400&display=swap" rel="stylesheet">

  <!-- KaTeX for crisp mathematical typography -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="renderMath()"></script>

  <!-- Mermaid for clean architecture diagrams -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>

  <style>
    :root[data-theme="light"] {
      --bg-base: #f8fafc;
      --bg-surface: #ffffff;
      --bg-panel: #f1f5f9;
      --border: #e2e8f0;
      --text-main: #0f172a;
      --text-muted: #475569;
      --text-dim: #64748b;
      --accent: #059669;
      --accent-blue: #0284c7;
      --code-bg: #f8fafc;
    }

    :root[data-theme="dark"] {
      --bg-base: #090d16;
      --bg-surface: #111827;
      --bg-panel: #1e293b;
      --border: #1e293b;
      --text-main: #f8fafc;
      --text-muted: #cbd5e1;
      --text-dim: #94a3b8;
      --accent: #10b981;
      --accent-blue: #38bdf8;
      --code-bg: #0f172a;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Newsreader', Georgia, serif;
      background-color: var(--bg-base);
      color: var(--text-main);
      line-height: 1.75;
      font-size: 17.5px;
      padding: 0 16px 80px 16px;
    }

    header#top-nav {
      position: sticky;
      top: 0;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border);
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 100;
      font-family: 'Inter', sans-serif;
      font-size: 14px;
    }

    article#paper-container {
      max-width: 860px;
      margin: 40px auto;
      background: var(--bg-surface);
      padding: 56px 64px;
      border-radius: 12px;
      border: 1px solid var(--border);
      box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
    }

    h1.title {
      font-family: 'Inter', sans-serif;
      font-size: 2.1rem;
      font-weight: 800;
      line-height: 1.25;
      letter-spacing: -0.02em;
      color: var(--text-main);
      margin-bottom: 16px;
    }

    .meta-byline {
      font-family: 'Inter', sans-serif;
      font-size: 0.95rem;
      color: var(--text-muted);
      margin-bottom: 32px;
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
    }
    .meta-byline span strong { color: var(--text-main); }

    .abstract-box {
      background: var(--bg-panel);
      border-left: 4px solid var(--accent);
      padding: 24px 28px;
      border-radius: 6px;
      margin-bottom: 40px;
    }
    .abstract-box h3 {
      font-family: 'Inter', sans-serif;
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--accent);
      margin-bottom: 10px;
    }
    .abstract-box p {
      font-size: 0.96rem;
      line-height: 1.65;
      color: var(--text-main);
    }

    h2 {
      font-family: 'Inter', sans-serif;
      font-size: 1.45rem;
      font-weight: 700;
      letter-spacing: -0.01em;
      margin: 40px 0 16px 0;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--border);
      color: var(--text-main);
    }

    h3 {
      font-family: 'Inter', sans-serif;
      font-size: 1.15rem;
      font-weight: 600;
      margin: 24px 0 12px 0;
      color: var(--text-main);
    }

    p { margin-bottom: 18px; }

    table {
      width: 100%;
      border-collapse: collapse;
      margin: 24px 0;
      font-family: 'Inter', sans-serif;
      font-size: 0.88rem;
    }
    th, td {
      padding: 10px 14px;
      text-align: left;
      border-bottom: 1px solid var(--border);
    }
    th {
      background: var(--bg-panel);
      font-weight: 600;
      color: var(--text-main);
    }
    tr:hover { background: rgba(0,0,0,0.02); }

    pre, code {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.86rem;
    }
    pre {
      background: var(--code-bg);
      border: 1px solid var(--border);
      padding: 16px;
      border-radius: 8px;
      overflow-x: auto;
      margin: 20px 0;
    }

    .badge-safe { color: var(--accent); font-weight: 700; }
    .badge-trip { color: #dc2626; font-weight: 700; }

    ol, ul { margin: 0 0 20px 24px; }
    li { margin-bottom: 8px; }
  </style>
</head>
<body>

  <header id="top-nav">
    <div><strong>Agentic MPC</strong> — Technical Paper</div>
    <button id="btn-theme" onclick="toggleTheme()" style="background:none; border:1px solid var(--border); padding:6px 14px; border-radius:6px; cursor:pointer; color:var(--text-main); font-family:'Inter', sans-serif;">🌙 Dark Mode</button>
  </header>

  <article id="paper-container">
    <h1 class="title">Agentic Model Predictive Control: Operating in Intelligence Space via Cognitive Supervisory Layers and Parallel Path Integral Rollouts</h1>

    <div class="meta-byline">
      <span><strong>Author:</strong> Zhaoyang Wan, PhD, MBA</span>
      <span><strong>Date:</strong> October 2026</span>
      <span><strong>Repository:</strong> cosmosanalytics/uat-copilot-local</span>
    </div>

    <div class="abstract-box">
      <h3>Abstract</h3>
      <p>
        Model Predictive Control (MPC) has served as the industrial benchmark for constrained multivariable control across process operations for four decades. Modern formulations—ranging from linear quadratic programming (QP) to nonlinear MPC (NMPC) and economic MPC (EMPC)—optimize physical state trajectories against fixed mathematical objectives. However, existing control formulations lack supervisory cognitive intelligence: they cannot parse unstructured natural-language operator directives, reason over qualitative plant physical topology, or execute contextual mitigation runbooks during operational contingencies.
      </p>
      <p style="margin-top:12px;">
        In this paper, we propose <strong>Agentic Model Predictive Control (Agentic MPC)</strong>, an architecture that places an <strong>Intelligence Space</strong> supervisory layer above high-throughput real-time control solvers. The proposed architecture partitions supervisory intelligence into <strong>The Two Halves</strong>: (1) a neural reasoner (<em>The Knower</em>) grounded in four structured memory tiers (Playbook, Rulebook, Yearbook, and Whiteboard), and (2) a deterministic Executive Function Harness (<em>The Doer</em>) enforcing Ring 0 operating invariants, automated contract unit tests, and preemptive trip bounds. In our architecture, high-level cognitive directives are mapped into parameterized Model Predictive Path Integral (MPPI) cost manifolds executed across parallel trajectory rollouts via GPU/WebGPU compute shaders, supported by an online lagged parameter filter.
      </p>
      <p style="margin-top:12px;">
        We evaluate the physical dynamics on an exothermic Continuous Stirred-Tank Reactor (CSTR) undergoing non-linear kinetic surges across a fully reproducible simulation case study spanning 20 randomized scenarios (\(C_{A0} \in [+10\%, +30\%]\), \(T_0 \in [+5\text{ K}, +12\text{ K}]\), and \(UA \in [-10\%, -35\%]\)) with advance-warning advisory lead time (\(t_{\text{lead}} = 3.5\text{ s}\)). Numerical simulation establishes an <strong>empirical feedback floor of 6/20 trips across feedback controllers on this scenario set</strong>: when tuned equally (\(q_T = 10.0\)), Linear MPC trips in 6/20 scenarios (\(2.26 \pm 1.14\text{ K}\) non-trip RMSE, \(9.49 \pm 5.39\text{ K}\) overall RMSE), matching NMPC (6/20 trips, \(2.48 \pm 1.47\text{ K}\) non-trip, \(9.62 \pm 5.37\text{ K}\) overall) and MPPI with a lagged-UA filter (6/20 trips, \(2.61 \pm 1.34\text{ K}\) non-trip, \(9.82 \pm 5.39\text{ K}\) overall), all tripping on the identical six scenarios (Seeds 4, 5, 8, 16, 18, 20). When weakly penalized (\(q_T = 1.0\)), Linear MPC trips in 12/20 scenarios (\(16.26 \pm 5.52\text{ K}\) overall RMSE). Notably, all reactive trips and the single preview trip occur 4–31 s after the surge ends during post-surge recovery, rather than during surge onset.
      </p>
      <p style="margin-top:12px;">
        When advance preview lookahead (\(t_{\text{lead}} = 3.5\text{ s}\)) is supplied, trips drop to 1/20 across all preview controllers, with failure occurring exclusively on Seed 18 (an extreme realization requiring \(\approx 4.5\text{ s}\) of lead time). Crucially, our ablation isolates that the supervisory schedule's quantitative advantage (\(0.94 \pm 0.41\text{ K}\) non-trip RMSE vs. \(1.75 \pm 1.00\text{ K}\) for standard preview MPPI, representing a \(0.81\text{ K}\) gain across 19 shared survivors, paired \(t\)-test \(p = 0.013\)) stems from coordinating an anticipatory pre-cooling ramp that avoids <strong>reaction quenching</strong>: naive rule-based step switching quenches the reactor, accumulates unreacted feed, and triggers delayed thermal blowout (8/20 trips, \(1.45 \pm 0.68\text{ K}\) non-trip RMSE). We present the LLM supervisory layer as the proposed architecture for qualitative interaction and formulate the physical control and safety contract harness, establishing a simulation case study for anticipatory process control.
      </p>
    </div>

    <h2>1. Introduction & Related Work</h2>
    <p>Model Predictive Control operates on the receding-horizon principle: at each discrete time step \(t\), the controller solves an open-loop optimal control problem over a prediction horizon \(H_p\), applies the first control input \(u_t\), and repeats the cycle upon receiving fresh state telemetry (Rawlings et al., 2017).</p>
    <p>While classical linear MPC remains computationally tractable on millisecond timescales via convex quadratic programming (QP), linear approximations degrade on highly non-linear chemical plants governed by exponential kinetics, such as Continuous Stirred-Tank Reactors (CSTR) undergoing Arrhenius heat generation (Seborg et al., 2016). When state perturbations depart from the nominal linearization point, purely reactive controllers exhibit severe tracking error, control chattering, and valve saturation.</p>

    <h3>1.1 Related Work: Advanced & Learning-Based MPC</h3>
    <ul>
      <li><strong>Robust and Constrained MPC:</strong> Linear Matrix Inequality (LMI) and tube-based robust MPC formulations synthesize invariant sets to maintain constraint satisfaction under bounded disturbances (Kothare et al., 1996; Mayne et al., 2005).</li>
      <li><strong>Learning-Based and Differentiable MPC:</strong> Recent advances integrate Gaussian Processes and neural networks into MPC for online residual compensation (Hewing et al., 2020), while differentiable MPC embeds convex optimization layers into end-to-end gradient-based neural networks (Amos et al., 2018). Physics-informed parameter tracking formulations have motivated domain-constrained residual filters that track conservation laws during online estimation; in this study, parameter compensation is evaluated via a direct lagged parameter tracking filter.</li>
      <li><strong>Sampling-Based Non-Convex Control:</strong> Model Predictive Path Integral (MPPI) control computes optimal control signals via Monte Carlo importance sampling over stochastic forward rollouts (Williams et al., 2017). Because MPPI evaluates trajectories independently without computing Jacobian matrices, it naturally maps to massively parallel GPU compute shaders.</li>
    </ul>

    <h3>1.2 The Role of the Supervisory Layer: Lookahead vs. Reasoning</h3>
    <p>A critical insight in receding-horizon control is that numerical solvers optimize over a fixed finite horizon \(H_p\) (e.g., \(4.0\text{ s}\)). When future disturbances are known in advance, mathematical solvers with preview can naturally pre-actuate within their horizon. However, in actual plant operations, forecasts arrive as human shift handover notes, laboratory feed analysis reports, or upstream DCS alarms. Classical MPC cannot parse these qualitative inputs.</p>
    <p><strong>Agentic MPC</strong> addresses this supervisory gap. Rather than replacing numerical solvers with an unconstrained large language model (LLM), Agentic MPC introduces an <strong>Intelligence Space</strong> supervisory tier positioned strictly above a deterministic execution harness and parallel MPPI rollouts. The neural reasoner is designed to interpret operator directives and contextual operational runbooks, propose quantitative cost manifolds, and verify them through deterministic contract tests before any parameter update reaches physical actuators.</p>

    <h2>2. The Agentic MPC Architecture</h2>
    <h3>2.1 The Two Halves: The Knower and The Doer</h3>
    <ul>
      <li><strong>The Knower (Neural Reasoner):</strong> Operates in <em>Intelligence Space</em>, translating operator directives into candidate cost manifold parameters \(\theta_{\mathcal{M}} = \{q_{\text{temp}}, q_{\text{barrier}}, u_{\text{target}}, \lambda\}\). Inference runs on dedicated cloud LPUs or server GPUs (e.g., Qwen-2.5-32B), with lightweight client-side WebGPU shaders (e.g., Qwen-2.5-0.5B via <code>@mlc-ai/web-llm</code>) available for offline edge operation.</li>
      <li><strong>The Doer (Executive Function Harness):</strong> A deterministic verification kernel enforcing Ring 0 invariants (actuator saturation and slew rate limits), running automated contract unit tests, and operating preemptively below plant emergency shutdown thresholds.</li>
    </ul>

    <h3>2.2 The Four Structured Memory Subsystems</h3>
    <table>
      <thead>
        <tr>
          <th>Memory Store</th>
          <th>Storage Modality</th>
          <th>Functional Role</th>
          <th>CSTR Realization</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>📘 <strong>The Playbook</strong></td>
          <td>Procedural (<code>SKILL.md</code>)</td>
          <td>Verified operational runbooks with deterministic pre/post-conditions</td>
          <td><code>cstr_runaway_mitigation.md</code> verified via automated contract tests</td>
        </tr>
        <tr>
          <td>📗 <strong>The Rulebook</strong></td>
          <td>Semantic (Vector Store)</td>
          <td>Safe operating envelopes and regulatory engineering constraints</td>
          <td>Safe operating limit envelope: \(T_{\text{trip}} = 385.0\text{ K}\), nominal \(T_{\text{ref}} = 350.0\text{ K}\)</td>
        </tr>
        <tr>
          <td>📙 <strong>The Yearbook</strong></td>
          <td>Relational (Graph DB)</td>
          <td>Plant equipment topological connectivity and flow dependencies</td>
          <td>Piping & Instrumentation: <code>V-101 ➔ J-101 ➔ CV-201 ➔ M-101 ➔ CH-3</code></td>
        </tr>
        <tr>
          <td>📓 <strong>The Whiteboard</strong></td>
          <td>Shared State (IPC)</td>
          <td>Real-time working scratchpad with distributed mutex locking</td>
          <td>Mutex locks (<code>MUTEX_PRECOOL</code>) preventing conflicting concurrent directives</td>
        </tr>
      </tbody>
    </table>

    <h2>3. Mathematical Formulation</h2>

    <h3>3.1 Classical Linear MPC Baseline (Jacobian QP)</h3>
    <p>The linear discrete-time optimal control problem is solved as a condensed Quadratic Program (QP) around the textbook steady state (\(C_{A,\text{ref}} = 0.50\text{ mol/L}, T_{\text{ref}} = 350.0\text{ K}, T_{c,\text{base}} = 300.0\text{ K}\)):</p>
    \[\min_{U} \frac{1}{2} U^T H_{\text{qp}} U + g^T U \quad \text{subject to: } u_{\min} \le u_k \le u_{\max}, \quad |\Delta u_k| \le \Delta u_{\max}\]
    <p>The continuous Jacobian matrix \(A\) has eigenvalues \([-0.0076, +0.0472]\text{ s}^{-1}\), exhibiting an open-loop thermal runaway pole (\(\tau_{\text{growth}} \approx 21.2\text{ s}\)). State penalty is \(Q = \text{diag}(10.0, q_T)\), \(R = 0.02\), input bounds \([280, 360]\text{ K}\), and slew limit \(12\text{ K/s}\). We evaluate Linear MPC at both \(q_T = 1.0\) and \(q_T = 10.0\).</p>

    <h3>3.2 Model Predictive Path Integral (MPPI) Formulation</h3>
    <p>MPPI evaluates \(K = 1,024\) stochastic control rollouts sampled from \(\mathcal{N}(0, \Sigma)\) with covariance \(\Sigma = 6.0^2 I\) and temperature \(\lambda = 10.0\). Discretized at rollout step \(\Delta t_{\text{ctrl}} = 0.2\text{ s}\):</p>
    \[x_{k+1} = f(x_k, v_k)\]
    \[S(U^{(m)}) = \sum_{k=0}^{H_p-1} \left( q_{\text{temp}} (T_k - T_{\text{ref}})^2 + q_{\text{barrier}} \max(0, T_k - T_{\text{barrier}})^2 \right) + \frac{\lambda}{2} \sum_{k=0}^{H_p-1} \epsilon_k^T \Sigma^{-1} \epsilon_k\]
    <p>The optimal control update is computed via softmax importance weighting:</p>
    \[u_t^* = u_t + \sum_{m=1}^{K} w(U^{(m)}) \epsilon_t^{(m)}, \quad w(U^{(m)}) = \frac{\exp\left(-\frac{1}{\lambda} (S(U^{(m)}) - \min_j S(U^{(j)}))\right)}{\sum_{k=1}^{K} \exp\left(-\frac{1}{\lambda} (S(U^{(k)}) - \min_j S(U^{(j)}))\right)}\]

    <h3>3.3 Lagged-UA Tracking Filter</h3>
    <p>To evaluate parameter identification during fouling, a first-order lagged filter tracks the true parameter \(UA(t)\) after surge onset:</p>
    \[UA_{\text{est}} \leftarrow UA_{\text{est}} + 0.02 (UA_{\text{true}} - UA_{\text{est}})\]
    <p>evaluated at each integration step \(\Delta t_{\text{sim}} = 0.02\text{ s}\) (\(\tau = 1.0\text{ s}\)). Uses the true parameter directly. With forecast lookahead, the forecast vector supplies \(UA\) directly, so the filter primarily impacts the no-forecast baseline (\(12.03\text{ K} \to 9.82\text{ K}\) overall RMSE).</p>

    <h2>4. Benchmark Case Study: Exothermic CSTR</h2>

    <h3>4.1 Hold-280 K Lead-Time Sweep & Controllability Limits</h3>
    <p>An empirical <strong>hold-280 K lead-time sweep</strong> over the benchmark kinetic surge evaluates required early advisory warning when stepping jacket coolant flatly to \(u = 280\text{ K}\):</p>

    <table>
      <thead>
        <tr>
          <th>Pre-Cooling Lead Time \(t_{\text{lead}}\)</th>
          <th>Peak Reactor Temp \(T_{\max}\) (K)</th>
          <th>Emergency SIS Trip (\(\ge 385.0\text{ K}\))</th>
          <th>Operational Controllability Outcome</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><strong>0.0 s (Reaction at Onset)</strong></td><td><strong>444.9 K</strong></td><td><span class="badge-trip">TRIP (Breached)</span></td><td>Unsurvivable runaway due to jacket lag (\(\tau_j = 2\text{ s}\)) & slew cap</td></tr>
        <tr><td><strong>1.0 s Lead Time</strong></td><td><strong>443.3 K</strong></td><td><span class="badge-trip">TRIP (Breached)</span></td><td>Insufficient thermal extraction ahead of surge</td></tr>
        <tr><td><strong>2.0 s Lead Time</strong></td><td><strong>441.6 K</strong></td><td><span class="badge-trip">TRIP (Breached)</span></td><td>Thermal runaway breaches limit</td></tr>
        <tr><td><strong>2.5 s Lead Time</strong></td><td><strong>440.6 K</strong></td><td><span class="badge-trip">TRIP (Breached)</span></td><td>Slew rate cap delays thermal extraction</td></tr>
        <tr><td><strong>3.0 s Lead Time</strong></td><td><strong>439.6 K</strong></td><td><span class="badge-trip">TRIP (Breached)</span></td><td>Delayed post-surge blowout</td></tr>
        <tr><td><strong>3.25 s Lead Time</strong></td><td><strong>404.9 K</strong></td><td><span class="badge-trip">TRIP (Breached)</span></td><td>Marginal thermal breach</td></tr>
        <tr><td><strong>3.5 s Lead Time</strong></td><td><strong>369.3 K</strong></td><td><span class="badge-safe">SAFE (Zero Trip)</span></td><td>Thermal buffer prevents runaway (15.7 K margin)</td></tr>
        <tr><td><strong>4.0 s Lead Time</strong></td><td><strong>352.7 K</strong></td><td><span class="badge-safe">SAFE (Zero Trip)</span></td><td>Robust containment</td></tr>
        <tr><td><strong>5.0 s Lead Time</strong></td><td><strong>350.0 K</strong></td><td><span class="badge-safe">SAFE (Zero Trip)</span></td><td>Fully absorbed thermal surge clamped at nominal setpoint</td></tr>
      </tbody>
    </table>
    <p><em>Caveat:</em> Hold-280 K is an elementary heuristic policy tripping 12/20 seeds at zero lead (higher than feedback controllers at 6/20). It is an empirical sweep, not an optimal-control bound.</p>
    <p><em>Per-Scenario Lead Needs:</em> The six reactive trip scenarios require: Seeds 4, 5, 8, 16, 18, 20 need 3.0 s, 3.0 s, 3.0 s, 2.0 s, 4.5 s, and 3.0 s respectively; all other 14 scenarios need \(\le 1.0\text{ s}\).</p>

    <h2>5. Verification & Safety Architecture</h2>
    <p>Agentic MPC enforces defense-in-depth: Ring 0 invariant checking (\(q_T \ge 0.1\), \(q_{\text{barrier}} \ge 1000\), \(u \in [280, 360]\text{ K}\), slew \(\le 12\text{ K/s}\)), automated contract unit tests on the active fouled plant model (&lt;30 ms), a software preemptive breaker at 382 K, and an independent hardware SIS scram at 385 K (failsafe cooling valve full open, feed shut off).</p>
    <p><em>Metric Definition:</em> Overall RMSE includes the post-trip SCRAM transient and depends heavily on the emergency shutdown model. Non-trip RMSE and trip counts serve as the primary metrics.</p>

    <h2>6. Empirical Results & Ablation Analysis</h2>

    <h3>6.1 Multi-Tier Benchmark Across 20 Randomized Scenarios</h3>
    <p>Table 2 presents authentic simulation results across 20 randomized scenarios computed directly from discrete QP, L-BFGS-B NMPC, and NumPy MPPI path integral solvers:</p>

    <table>
      <thead>
        <tr>
          <th>Configuration</th>
          <th>Controller Type</th>
          <th>Non-Trip RMSE (K)</th>
          <th>Overall RMSE (K)</th>
          <th>Peak T (K)</th>
          <th>Slew (K/s)</th>
          <th>SIS Trips</th>
          <th>Settled</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Baseline 1a</strong></td>
          <td>Linear MPC (\(q_T = 1.0\), No Forecast)</td>
          <td>\(2.56 \pm 1.36\)</td>
          <td>\(16.26 \pm 5.52\)</td>
          <td>\(389.3 \pm 14.2\)</td>
          <td>\(3.29 \pm 0.95\)</td>
          <td><span class="badge-trip">12 / 20 (60%)</span></td>
          <td>8 / 20 (9.8 s)</td>
        </tr>
        <tr>
          <td><strong>Baseline 1b</strong></td>
          <td>Linear MPC (\(q_T = 10.0\), No Forecast)</td>
          <td>\(2.26 \pm 1.14\)</td>
          <td>\(9.49 \pm 5.39\)</td>
          <td>\(372.1 \pm 13.5\)</td>
          <td>\(4.85 \pm 1.12\)</td>
          <td><span class="badge-trip">6 / 20 (30%)</span></td>
          <td>13 / 20 (7.1 s)</td>
        </tr>
        <tr>
          <td><strong>Baseline 2a</strong></td>
          <td>NMPC (L-BFGS-B, No Forecast)</td>
          <td>\(2.48 \pm 1.47\)</td>
          <td>\(9.62 \pm 5.37\)</td>
          <td>\(372.9 \pm 13.7\)</td>
          <td>\(5.04 \pm 1.29\)</td>
          <td><span class="badge-trip">6 / 20 (30%)</span></td>
          <td>13 / 20 (6.9 s)</td>
        </tr>
        <tr>
          <td><strong>Ablation 1</strong></td>
          <td>MPPI (Static \(\theta^*\), No Forecast)</td>
          <td>\(3.00 \pm 1.80\)</td>
          <td>\(12.03 \pm 5.57\)</td>
          <td>\(378.9 \pm 14.6\)</td>
          <td>\(2.44 \pm 0.38\)</td>
          <td><span class="badge-trip">8 / 20 (40%)</span></td>
          <td>11 / 20 (8.6 s)</td>
        </tr>
        <tr>
          <td><strong>Ablation 2</strong></td>
          <td>MPPI + Lagged-UA Filter (No Forecast)</td>
          <td>\(2.61 \pm 1.34\)</td>
          <td>\(9.82 \pm 5.39\)</td>
          <td>\(373.4 \pm 13.9\)</td>
          <td>\(2.42 \pm 0.38\)</td>
          <td><span class="badge-trip">6 / 20 (30%)</span></td>
          <td>14 / 20 (11.6 s)</td>
        </tr>
        <tr>
          <td><strong>Baseline 2b</strong></td>
          <td>NMPC (With Forecast Preview)</td>
          <td>\(\mathbf{1.47 \pm 0.85}\)</td>
          <td>\(\mathbf{2.82 \pm 2.93}\)</td>
          <td>\(\mathbf{356.7 \pm 7.6}\)</td>
          <td>\(6.41 \pm 1.03\)</td>
          <td><span class="badge-safe">1 / 20 (5%)</span></td>
          <td><strong>19 / 20 (2.6 s)</strong></td>
        </tr>
        <tr>
          <td><strong>Ablation 3a</strong></td>
          <td>MPPI + Filter (With Forecast Preview)</td>
          <td>\(\mathbf{1.75 \pm 1.00}\)</td>
          <td>\(\mathbf{3.11 \pm 2.99}\)</td>
          <td>\(\mathbf{357.3 \pm 7.7}\)</td>
          <td>\(\mathbf{2.72 \pm 0.19}\)</td>
          <td><span class="badge-safe">1 / 20 (5%)</span></td>
          <td><strong>18 / 20 (5.7 s)</strong></td>
        </tr>
        <tr>
          <td><strong>Ablation 3b</strong></td>
          <td>Rule Supervisor + MPPI</td>
          <td>\(1.45 \pm 0.68\)</td>
          <td>\(9.44 \pm 4.92\)</td>
          <td>\(381.1 \pm 17.1\)</td>
          <td>\(3.77 \pm 0.37\)</td>
          <td><span class="badge-trip">8 / 20 (40%)</span></td>
          <td>12 / 20 (13.1 s)</td>
        </tr>
        <tr>
          <td><strong>Full System</strong></td>
          <td><strong>Anticipatory Schedule (Full Architecture)</strong></td>
          <td>\(\mathbf{0.94 \pm 0.41}\)</td>
          <td>\(\mathbf{2.17 \pm 2.57}\)</td>
          <td>\(\mathbf{355.5 \pm 6.2}\)</td>
          <td>\(\mathbf{3.36 \pm 0.19}\)</td>
          <td><span class="badge-safe">1 / 20 (5%)</span></td>
          <td><strong>19 / 20 (2.9 s)</strong></td>
        </tr>
      </tbody>
    </table>

    <p><em>Key Findings:</em> Linear MPC (\(q_T=10\)), NMPC, and MPPI+filter establish an empirical feedback floor of 6/20 trips, failing on the identical scenarios (Seeds 4, 5, 8, 16, 18, 20). All baseline trips and Seed 18 occur 4–31 s post-surge during recovery. The rule supervisor ties the full supervisor on surviving seeds (\(0.00\text{ K}\) difference) but trips on 7–8/20 seeds depending on MPPI stream (\(1.45\text{--}2.47\text{ K}\) non-trip RMSE across 5 streams), whereas preview controllers trip on only 1/20.</p>

    <h3>6.2 Deconstructing the Supervisory Advantage</h3>
    <p>Ablation across the 19 common surviving scenarios isolates the quantitative mechanism behind the supervisory schedule:</p>
    <table>
      <thead>
        <tr><th>Configuration</th><th>Non-Trip RMSE (K)</th><th>Physical Mechanism</th></tr>
      </thead>
      <tbody>
        <tr><td><strong>MPPI + Forecast Preview</strong></td><td>\(1.76 \pm 1.00\)</td><td>Unconstrained optimal preview tracking</td></tr>
        <tr><td><strong>+ Ramp Cap Only</strong></td><td>\(1.12 \pm 0.48\)</td><td>Modulates pre-cooling to 282 K, preventing reaction quenching</td></tr>
        <tr><td><strong>+ Elevated Barrier Weights Only</strong></td><td>\(1.33 \pm 0.72\)</td><td>Stiff penalty keeps state strictly within safe envelope</td></tr>
        <tr><td><strong>Both (Anticipatory Supervisory Schedule)</strong></td><td><strong>\(0.94 \pm 0.41\)</strong></td><td>Coordinated pre-cooling containment (gain: 0.81 K, p = 0.013)</td></tr>
      </tbody>
    </table>
    <p>Across the 19 shared survivors, the gain is 0.81 K (paired \(t\) \(p = 0.013\), Wilcoxon \(p = 0.0017\), Holm-adjusted \(p = 0.063\)). Overall difference across 20 scenarios is +0.95 K (\(p = 0.0069\)). Only the ramp-only comparison survives Holm (\(p = 0.0009\)). Results are stable across 5 MPPI sampling streams.</p>

    <h3>6.3 Reproducibility & Computational Budget</h3>
    <p>All tables were generated using a pure NumPy implementation (<code>benchmark_cstr_unified.py</code>):</p>
    <ul>
      <li>Scenario generation with <code>np.random.seed(42)</code>.</li>
      <li>Sensor noise: <code>default_rng(1000 + i)</code>; MPPI sampling: <code>default_rng(10000 + 100*rep + seed)</code>.</li>
      <li>NMPC: L-BFGS-B, <code>maxiter = 10</code>, warm-started (not converged at each step).</li>
      <li>Runtime: approximately 12 minutes on 2 CPU cores.</li>
    </ul>

    <h2>7. Industrial Deployment Limits & Conclusion</h2>
    <h3>7.1 Industrial Deployment Limits</h3>
    <p>While Agentic MPC demonstrates robust supervisory capabilities in simulation, certified industrial deployment requires strict separation of concerns. Under IEC 61511 / ISA-84, safety instrumented functions must remain physically independent, deterministic, and SIL-rated. The agentic layer operates solely in the basic process control system (BPCS) supervisory space and must never share hardware, sensors, or actuators with the emergency shutdown interlock.</p>
    
    <h3>7.2 Conclusion</h3>
    <p>This simulation case study demonstrates that preview lookahead and an anticipatory pre-cooling ramp stabilize an exothermic CSTR under severe kinetic surges. A naive rule-based supervisor that commands flat maximum cooling frequently quenches the reactor, accumulates reactant, and triggers delayed blowout. Modulating a pre-cooling ramp to 282 K avoids quenching while maintaining thermal absorption margin.</p>
    <p>We present the Agentic MPC framework as a proposed supervisory architecture for qualitative plant operations. Rather than acting as an evaluated numerical optimizer in these experiments, the LLM layer provides the architectural design pattern for interpreting unstructured operator directives and enforcing formal safety contracts in future human-in-the-loop autonomous plant workflows.</p>

    <h2>References</h2>
    <ol>
      <li><strong>Williams, G., Aldrich, A., & Theodorou, E. A. (2017).</strong> <em>Model Predictive Path Integral Control: From Theory to Parallel Computation.</em> Journal of Guidance, Control, and Dynamics, 40(2), 344–357.</li>
      <li><strong>Rawlings, J. B., Mayne, D. Q., & Diehl, M. (2017).</strong> <em>Model Predictive Control: Theory, Computation, and Design</em> (2nd ed.). Nob Hill Publishing.</li>
      <li><strong>Seborg, D. E., Edgar, T. F., Mellichamp, D. A., & Doyle, F. J. (2016).</strong> <em>Process Dynamics and Control</em> (4th ed.). John Wiley & Sons.</li>
      <li><strong>Kothare, M. V., Balakrishnan, V., & Morari, M. (1996).</strong> <em>Robust Constrained Model Predictive Control using Linear Matrix Inequalities.</em> Automatica, 32(10), 1361–1379.</li>
      <li><strong>Mayne, D. Q., Seron, M. M., & Raković, S. V. (2005).</strong> <em>Robust Model Predictive Control of Constrained Linear Systems with Bounded Disturbances.</em> Automatica, 41(2), 219–224.</li>
      <li><strong>Hewing, L., Wabersich, K. P., Menner, M., & Zeilinger, M. N. (2020).</strong> <em>Learning-Based Model Predictive Control: Toward Safe Learning in Control.</em> Annual Review of Control, Robotics, and Autonomous Systems, 3, 269–296.</li>
      <li><strong>Amos, B., Jiménez, I., Sacks, J., Boots, B., & Kolter, J. Z. (2018).</strong> <em>Differentiable MPC for End-to-End Planning and Control.</em> Advances in Neural Information Processing Systems (NeurIPS), 31, 8289–8300.</li>
    </ol>
  </article>

  <script>
    function renderMath() {
      if (window.renderMathInElement) {
        renderMathInElement(document.body, {
          delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '\\[', right: '\\]', display: true},
            {left: '$', right: '$', display: false},
            {left: '\\(', right: '\\)', display: false}
          ],
          throwOnError: false
        });
      }
      mermaid.initialize({ startOnLoad: true, theme: document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'default' });
    }

    function toggleTheme() {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      const target = current === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', target);
      document.getElementById('btn-theme').textContent = target === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode';
      localStorage.setItem('paper_theme', target);
    }

    window.addEventListener('DOMContentLoaded', () => {
      const saved = localStorage.getItem('paper_theme') || 'light';
      document.documentElement.setAttribute('data-theme', saved);
      document.getElementById('btn-theme').textContent = saved === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode';
    });
  </script>
</body>
</html>
"""

with open(r"C:\Users\richa\ai-engineering\agentic_mpc_paper.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Successfully generated agentic_mpc_paper.html")
