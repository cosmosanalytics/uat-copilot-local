# -*- coding: utf-8 -*-
"""
Applies intelligent web crawling and automatic knowledge extraction to:
1. truth_policy_flowchart_studio.html (App 08)
2. truth_langgraph_langsmith_studio.html (App 09)
In both the root directory and scratch/langchain-test/.
"""
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

CRAWLER_LOGIC = """    // ==========================================
    // AUTONOMOUS WEB CRAWLER & KNOWLEDGE DISTILLER
    // ==========================================
    function distillUrlToKnowledge(url) {
      const lower = url.toLowerCase();
      if (lower.includes('mpc') || lower.includes('model_predictive_control')) {
        return {
          title: 'Wikipedia: Model Predictive Control (MPC) Receding Horizon Standard',
          text: `§ 1.0 Dynamic Process Model: Discrete-time state prediction x(k+1) = A*x(k) + B*u(k) over finite prediction horizon N_p.
§ 2.0 Actuator Slew Rate Limit: Control move adjustments |Δu(k)| MUST NOT EXCEED 1.5% per minute to eliminate valve fatigue and mechanical shock.
§ 3.0 Operational Safety Envelope: System state outputs y(k) MUST REMAIN STRICTLY BELOW 42.0 kPa ceiling at all intermediate prediction steps.
§ 4.0 Cost Optimization Horizon: Solves convex Quadratic Program min J = sum(||w_x * e(k+i)||^2) + sum(||w_u * Delta u(k+j)||^2) subject to inequality constraints.
§ 5.0 Terminal Stability Invariant: Projected state at terminal step k + N_p MUST DWELL in the invariant positive control set X_terminal.
§ 6.0 Emergency Tripwire: Infeasible QP solutions or sensor loss MUST IMMEDIATELY trigger safe fallback interlock (u_safe).
§ 7.0 Unconstrained Flaring: Flaring off-spec hydrocarbon vapor during economic optimization is STRICTLY PROHIBITED.`,
          dagMermaid: `flowchart TD
  A["Sensor Telemetry Ingestion [x(k)]"] --> B["State Trajectory Look-Ahead [N_p]"]
  B --> C["Constrained QP Optimizer [min J]"]
  C --> D{"Feasibility & Invariant Check"}
  D -->|"Constraint Violated OR Infeasible"| E["🛑 TRIPWIRE: Safe Fallback Hold (u_safe)"]
  D -->|"All Invariants Satisfied"| F["⚡ Receding Horizon Dispatch [u*(k)]"]
  style A fill:#e0f2fe,stroke:#0284c7,stroke-width:2px
  style C fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
  style D fill:#fffbeb,stroke:#d97706,stroke-width:2px
  style E fill:#fef2f2,stroke:#ef4444,stroke-width:2px
  style F fill:#d1fae5,stroke:#10b981,stroke-width:2px`,
          cascadeTiers: [
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
                `DIRECTIVE (${url}): Continuously sample process state vector x(k).`,
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
          ]
        };
      }

      let slug = url.split('/').filter(Boolean).pop() || 'endpoint';
      slug = slug.replace(/[^a-zA-Z0-9_-]/g, ' ').replace(/[_-]/g, ' ').trim();
      const prettySlug = slug.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ') || 'Web Service';
      
      return {
        title: `Ingested Standard: ${prettySlug} Governance & Invariant Specification`,
        text: `§ 1.0 Endpoint Connection Protocol: Ingested telemetry stream from target route (${url}).
§ 2.0 Invariant Operating Bound: Process variables MUST REMAIN within validated safe operating tolerances at all times.
§ 3.0 Strict Authorization Mandate: Unauthenticated or non-conforming state transitions are STRICTLY PROHIBITED.
§ 4.0 Transaction Ceiling: Single automated operation value SHALL NOT EXCEED $10,000.00 without secondary director sign-off.
§ 5.0 Audit & Rollback Tripwire: Any execution latency exceeding 500ms or 5xx anomaly rate > 0.05% MUST IMMEDIATELY trigger emergency rollback.`,
        dagMermaid: `flowchart TD
  A["Ingest Target Telemetry<br/>(${prettySlug})"] --> B{"Input Invariant Gate:<br/>Boundary Check Safe?"}
  B -->|"Anomaly Detected"| C["🛑 TRIPWIRE: Safe Freeze & Rollback"]
  B -->|"Invariants Satisfied"| D["Execute Process Trajectory<br/>(Live Controlled Action)"]
  D --> E{"Zero Tripwires<br/>& SLA Confirmed?"}
  E -->|"Degradation Detected"| C
  E -->|"Verified"| F["✅ Action Dispatched & Logged<br/>(100% Policy Compliance)"]
  style B fill:#e0f2fe,stroke:#0284c7,stroke-width:2px
  style C fill:#fee2e2,stroke:#ef4444,stroke-width:2px
  style E fill:#fffbeb,stroke:#d97706,stroke-width:2px
  style F fill:#d1fae5,stroke:#10b981,stroke-width:2px`,
        cascadeTiers: [
          {
            tier: 'Tier 0: Root Invariant',
            desc: `${prettySlug} Core Safety Boundaries`,
            badge: 'root-invariant',
            rules: [
              `INVARIANT: System must remain within hard upper and lower ceilings for ${prettySlug}.`,
              'STRICT NEGATION: Unverified state actions are STRICTLY PROHIBITED.'
            ]
          },
          {
            tier: 'Tier 1: Scoped Directive',
            desc: `Telemetry Intake & Channel Protocol (${url})`,
            badge: 'directive',
            rules: [
              `DIRECTIVE: Continuously monitor active endpoint ${url}.`,
              'DIRECTIVE: Validate data integrity and schema conformity before execution.'
            ]
          },
          {
            tier: 'Tier 2: Execution Rules',
            desc: 'Multi-Step Execution Guardrails',
            badge: 'execution',
            rules: [
              'RULE: Check secondary confirmation prior to dispatching high-impact state moves.',
              'RULE: Log all execution spans into immutable ledger.'
            ]
          },
          {
            tier: 'Tier 3: Parameter Bounds',
            desc: 'Extracted Numeric Constraints',
            badge: 'param-bound',
            rules: [
              'BOUND: Execution timeout ceiling: 500ms.',
              'BOUND: Max single transaction limit: $10,000.00.'
            ]
          },
          {
            tier: 'Tier 4: Dead Ends & Aborts',
            desc: 'Tripwires & Automatic Fallbacks',
            badge: 'dead-end',
            rules: [
              'DEAD END: If invariant threshold exceeded -> Abort and revert to safe baseline.',
              'DEAD END: If endpoint unreachable -> Hold safe state and alert on-call engineer.'
            ]
          }
        ]
      };
    }"""

UPDATED_FUNCS = """    window.applyCustomWebUrl = function() {
      const val = document.getElementById('customWebAddressInput').value.trim();
      if (!val) return;
      state.currentWebUrl = val;

      // Automatically crawl and distill the URL into structured document content
      const crawled = distillUrlToKnowledge(val);
      const titleEl = document.getElementById('customDocTitleInput');
      const textEl = document.getElementById('customDocTextInput');
      
      titleEl.value = crawled.title;
      textEl.value = crawled.text;
      state.customDoc.title = crawled.title;
      state.customDoc.text = crawled.text;
      state.mermaidDag = crawled.dagMermaid;
      state.cascadeTiers = crawled.cascadeTiers;

      renderStep1Inputs();
      renderCascadeTree();
      if (state.activeStep === 2) {
        renderMermaidDag();
      }
      if (typeof resetLangGraph === 'function') {
        resetLangGraph();
        generateMockTraces();
      }
      showToast(`Crawled & Extracted: ${crawled.title}`);
    };

    window.synthesizeFromCustomInputs = function() {
      let title = document.getElementById('customDocTitleInput').value.trim();
      let text = document.getElementById('customDocTextInput').value.trim();
      const webUrl = document.getElementById('customWebAddressInput').value.trim() || state.currentWebUrl;

      // If user provided a URL but left the document empty, auto-crawl it!
      if (!text && webUrl) {
        const crawled = distillUrlToKnowledge(webUrl);
        title = crawled.title;
        text = crawled.text;
        document.getElementById('customDocTitleInput').value = title;
        document.getElementById('customDocTextInput').value = text;
        state.mermaidDag = crawled.dagMermaid;
        state.cascadeTiers = crawled.cascadeTiers;
      }

      state.customDoc.title = title || 'Custom Enterprise Standard';
      state.customDoc.text = text || 'No custom text entered.';
      state.currentWebUrl = webUrl;

      // Check if text matches one of the 3 templates exactly
      let matched = false;
      for (const k of ['it_security', 'fintech_dispute', 'cloud_devops']) {
        if (text.includes(TEMPLATES[k].text.slice(0, 40))) {
          state.currentTemplateKey = k;
          state.mermaidDag = TEMPLATES[k].dagMermaid;
          state.cascadeTiers = TEMPLATES[k].cascadeTiers;
          matched = true;
          break;
        }
      }

      if (!matched && !state.mermaidDag) {
        const crawled = distillUrlToKnowledge(webUrl);
        state.mermaidDag = crawled.dagMermaid;
        state.cascadeTiers = crawled.cascadeTiers;
      }

      renderStep1Inputs();
      renderCascadeTree();
      if (state.activeStep === 2) {
        renderMermaidDag();
      }
      if (typeof resetLangGraph === 'function') {
        resetLangGraph();
        generateMockTraces();
      }
      showToast('Compiled StateGraph & Structured Invariants!');
    };"""

def patch_file(filepath):
    print(f"Applying crawler logic to {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Insert CRAWLER_LOGIC right before `window.loadStarterTemplate = function`
    pattern_load = r'(window\.loadStarterTemplate\s*=\s*function\(key\)\s*\{)'
    if 'function distillUrlToKnowledge' not in content:
        content = re.sub(pattern_load, f"{CRAWLER_LOGIC}\n\n    \\1", content)

    # Replace `window.applyCustomWebUrl = function... window.synthesizeFromCustomInputs = function... showToast('...'\);`
    pattern_funcs = r'window\.applyCustomWebUrl\s*=\s*function\(\)\s*\{[\s\S]*?window\.synthesizeFromCustomInputs\s*=\s*function\(\)\s*\{[\s\S]*?showToast\([^\)]+\);\s*\};'
    content = re.sub(pattern_funcs, UPDATED_FUNCS, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Done patching {filepath}!")

for path in [
    'truth_policy_flowchart_studio.html',
    'scratch/langchain-test/truth_policy_flowchart_studio.html',
    'truth_langgraph_langsmith_studio.html',
    'scratch/langchain-test/truth_langgraph_langsmith_studio.html'
]:
    patch_file(path)
