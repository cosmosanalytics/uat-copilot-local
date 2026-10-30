# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/patch_templates_source.py', 'r', encoding='utf-8') as f:
    patch_code = f.read()

exec(patch_code)

def patch_app9(filepath):
    print(f"Patching {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace starter buttons
    old_buttons_pattern = r'<button[^>]*loadStarterTemplate\([\'"]mpc[\'"]\)[\s\S]*?<button[^>]*loadStarterTemplate\([\'"]water[\'"]\)[^<]*</button>'
    new_buttons = """<button class="btn btn-secondary btn-sm" onclick="loadStarterTemplate('it_security')">🛡️ Enterprise IT SSO</button>
              <button class="btn btn-secondary btn-sm" onclick="loadStarterTemplate('fintech_dispute')">💳 FinTech Dispute Intake</button>
              <button class="btn btn-secondary btn-sm" onclick="loadStarterTemplate('cloud_devops')">☁️ Cloud Canary Release</button>"""
    
    content = re.sub(old_buttons_pattern, new_buttons, content)

    # 2. Replace input fields values in HTML
    content = re.sub(r'value="https://vault\.custody\.finance\.local/transfer-gateway"', 'value="https://internal.corp.local/overview"', content)
    content = re.sub(r'>§ 1\.0 Autonomous Vault Transfer:[\s\S]*?</textarea>', r'>§ 1.0 Multi-Factor Authentication (MFA) Mandate: All engineers, contractor personnel, and automated system accounts accessing production VPCs, Kubernetes clusters, and database enclaves must authenticate using physical, hardware-backed FIDO2 WebAuthn cryptographic keys (e.g. YubiKey 5 Series). Legacy SMS OTP and voice-call telephone verifications are STRICTLY PROHIBITED.\n§ 2.0 Elevated Database Write Leases & Authorization Ceilings: Direct write access to customer relational databases (PostgreSQL/Aurora) requires an active JIRA Change Reference ticket and mandatory sign-off from an L2 Engineering Director or VP. Elevated access leases are strictly ephemeral: TTL SHALL NOT EXCEED 4 HOURS (240 minutes).\n§ 3.0 Emergency Break-Glass Exception Protocol: In the extraordinary circumstance of an active Sev-1 / P0 outage where designated approvers are unreachable, an on-call SRE may trigger the automated Emergency Break-Glass procedure. Break-Glass tokens are hard-capped at 2 HOURS (7,200 SECONDS). A non-dismissible audit event is dispatched instantly to SIRT.</textarea>', content)

    # 3. Replace state initialization
    old_state_pattern = r'let state = \{[\s\S]*?activeStep:\s*1,[\s\S]*?customDoc:\s*\{[\s\S]*?\},[\s\S]*?cascadeTiers:\s*\[\],[\s\S]*?mermaidDag:\s*\'\'[\s\S]*?\};'
    
    new_state = f"""let state = {{
      activeStep: 1,
      inputViewMode: 'side_by_side',
      highlightDocInvariants: true,
      currentWebUrl: 'https://internal.corp.local/overview',
      currentTemplateKey: 'it_security',
      customDoc: {{
        title: 'SEC-POL-402_Rev4: Enterprise IT SSO & Privilege Escalation Policy',
        text: `§ 1.0 Multi-Factor Authentication (MFA) Mandate: All engineers, contractor personnel, and automated system accounts accessing production VPCs, Kubernetes clusters, and database enclaves must authenticate using physical, hardware-backed FIDO2 WebAuthn cryptographic keys (e.g. YubiKey 5 Series). Legacy SMS OTP and voice-call telephone verifications are STRICTLY PROHIBITED.
§ 2.0 Elevated Database Write Leases & Authorization Ceilings: Direct write access to customer relational databases (PostgreSQL/Aurora) requires an active JIRA Change Reference ticket and mandatory sign-off from an L2 Engineering Director or VP. Elevated access leases are strictly ephemeral: TTL SHALL NOT EXCEED 4 HOURS (240 minutes).
§ 3.0 Emergency Break-Glass Exception Protocol: In the extraordinary circumstance of an active Sev-1 / P0 outage where designated approvers are unreachable, an on-call SRE may trigger the automated Emergency Break-Glass procedure. Break-Glass tokens are hard-capped at 2 HOURS (7,200 SECONDS). A non-dismissible audit event is dispatched instantly to SIRT.`
      }},
      cascadeTiers: [],
      mermaidDag: `{DAG_IT_SECURITY}`,
      lgCurrentNodeIndex: 0,
      lgState: {{}},
      traces: [],
      selectedTraceId: null,
      radarChart: null,
      comparativeChart: null
    }};"""
    
    content = re.sub(old_state_pattern, new_state, content)

    # 4. Replace TEMPLATES object and loadStarterTemplate and synthesizeFromCustomInputs
    old_templates_pattern = r'const TEMPLATES = \{[\s\S]*?\};\s*// ==========================================\s*// INITIALIZATION & DYNAMIC COMPILATION\s*// ==========================================\s*window\.loadStarterTemplate = function\(key\) \{[\s\S]*?window\.synthesizeFromCustomInputs = function\(\) \{[\s\S]*?showToast\([^\)]+\);\s*\};'

    new_templates_and_funcs = f"""{TEMPLATES_JS}

    // ==========================================
    // INITIALIZATION & DYNAMIC COMPILATION
    // ==========================================
    window.loadStarterTemplate = function(key) {{
      const t = TEMPLATES[key];
      if (!t) return;
      state.currentTemplateKey = key;
      document.getElementById('customDocTitleInput').value = t.title;
      document.getElementById('customDocTextInput').value = t.text;
      document.getElementById('customWebAddressInput').value = t.url;
      state.currentWebUrl = t.url;
      state.customDoc.title = t.title;
      state.customDoc.text = t.text;
      state.mermaidDag = t.dagMermaid;
      state.cascadeTiers = t.cascadeTiers;
      renderStep1Inputs();
      renderCascadeTree();
      if (state.activeStep === 2) {{
        renderMermaidDag();
      }}
      resetLangGraph();
      generateMockTraces();
      showToast(`Loaded ${{t.title}}`);
    }};

    window.applyCustomWebUrl = function() {{
      const val = document.getElementById('customWebAddressInput').value.trim();
      if (!val) return;
      state.currentWebUrl = val;
      renderStep1Inputs();
      showToast(`Connected web address: ${{val}}`);
    }};

    window.synthesizeFromCustomInputs = function() {{
      const title = document.getElementById('customDocTitleInput').value.trim() || 'Custom Enterprise Standard';
      const text = document.getElementById('customDocTextInput').value.trim();
      const webUrl = document.getElementById('customWebAddressInput').value.trim() || state.currentWebUrl;

      state.customDoc.title = title;
      state.customDoc.text = text || 'No custom text entered.';
      state.currentWebUrl = webUrl;

      // Check if text matches one of the 3 templates exactly
      let matched = false;
      for (const k of ['it_security', 'fintech_dispute', 'cloud_devops']) {{
        if (text.includes(TEMPLATES[k].text.slice(0, 40))) {{
          state.currentTemplateKey = k;
          state.mermaidDag = TEMPLATES[k].dagMermaid;
          state.cascadeTiers = TEMPLATES[k].cascadeTiers;
          matched = true;
          break;
        }}
      }}

      if (!matched) {{
        // Dynamic custom synthesis for user-provided text
        const extractedBounds = extractRulesFromText(text);
        state.cascadeTiers = [
          {{
            tier: 'Tier 0: Root Invariants',
            desc: 'Non-Negotiable System & Safety Bounds',
            badge: 'root-invariant',
            rules: extractedBounds.invariants.length > 0 ? extractedBounds.invariants : [
              'INVARIANT: Critical system constraints must remain within hard upper and lower ceilings.',
              'STRICT NEGATION: Actions causing unrecoverable tripwires are STRICTLY PROHIBITED.'
            ]
          }},
          {{
            tier: 'Tier 1: Scoped Directives',
            desc: 'Target Web Routes & Intake Protocols',
            badge: 'directive',
            rules: [
              `DIRECTIVE (${{webUrl}}): Continuously monitor active telemetry and incoming requests.`,
              'DIRECTIVE (State Intake): Validate sensor freshness and input integrity before execution.',
              'DIRECTIVE (Optimizer): Formulate execution trajectory adhering strictly to constraints.'
            ]
          }},
          {{
            tier: 'Tier 2: Execution Rules',
            desc: 'Step-by-Step Gate Prerequisites',
            badge: 'execution',
            rules: extractedBounds.rules.length > 0 ? extractedBounds.rules : [
              'RULE: Actuator and configuration move adjustments must respect slew-rate limits.',
              'RULE: Secondary confirmation required prior to dispatching high-impact commands.',
              'RULE: Log all state transitions to immutable audit ledger.'
            ]
          }},
          {{
            tier: 'Tier 3: Parameter Bounds',
            desc: 'Extracted Numeric Guardrails',
            badge: 'param-bound',
            rules: extractedBounds.bounds.length > 0 ? extractedBounds.bounds : [
              'BOUND: Operational safety margin: Strictly within specified tolerances.',
              'BOUND: Timeout ceiling: Control loop deadline enforced.'
            ]
          }},
          {{
            tier: 'Tier 4: Dead Ends & Aborts',
            desc: 'Automatic Circuit Breakers',
            badge: 'dead-end',
            rules: [
              'DEAD END: If invariant threshold exceeded -> Abort automated execution and trigger emergency safety interlock.',
              'DEAD END: If state sensor or web portal communication lost -> Hold safe state and alert supervisor.'
            ]
          }}
        ];

        state.mermaidDag = `flowchart TD
  A["Ingest User Inputs<br/>(Document + Web Portal)"] --> B{{"Pre-flight Validation:<br/>Inputs Grounded & Clean?"}}
  B -- "Stale or Invalid" --> C["DEAD END: Freeze Execution<br/>(Hold Safe Baseline)"]
  B -- "Valid Inputs" --> D["Evaluate Invariant Bounds<br/>(Target Endpoint)"]
  D --> E{{"Operating Ceiling<br/>Within Safety Bound?"}}
  E -- "Violates Invariant" --> F["EMERGENCY TRIP: Circuit Breaker<br/>(Revert to Safe State)"]
  E -- "Within Safe Bound" --> G["Dispatch Action Trajectory<br/>(Controlled Execution)"]
  G --> H{{"Telemetry Verified &<br/>Zero Invariant Breaches?"}}
  H -- "Anomalies Detected" --> F
  H -- "Verified" --> I["Execution Successful<br/>(100% Policy Compliance)"]
  style B fill:#e0f2fe,stroke:#0284c7,stroke-width:2px
  style E fill:#fffbeb,stroke:#d97706,stroke-width:2px
  style F fill:#fee2e2,stroke:#dc2626,stroke-width:2px
  style I fill:#f0fdf4,stroke:#16a34a,stroke-width:2px`;
      }}

      renderStep1Inputs();
      renderCascadeTree();
      if (state.activeStep === 2) {{
        renderMermaidDag();
      }}
      resetLangGraph();
      generateMockTraces();
      showToast('Compiled LangGraph StateGraph & Dual Governance Tree!');
    }};"""

    content = re.sub(old_templates_pattern, new_templates_and_funcs, content)

    # 5. Initialization on window load
    content = content.replace("loadStarterTemplate('mpc');", "loadStarterTemplate('it_security');")
    content = content.replace("synthesizeFromCustomInputs();\n  </script>", "loadStarterTemplate('it_security');\n  </script>")
    content = content.replace("synthesizeFromCustomInputs();\r\n  </script>", "loadStarterTemplate('it_security');\r\n  </script>")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully patched {filepath}!")

patch_app9('truth_langgraph_langsmith_studio.html')
patch_app9('scratch/langchain-test/truth_langgraph_langsmith_studio.html')
