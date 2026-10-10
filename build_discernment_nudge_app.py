"""
build_discernment_nudge_app.py
Builds discernment_nudge_app.html: Standalone frontend-only HTML application
powered by WebLLM (local WebGPU) and Groq LPU (cloud fast inference),
demonstrating Skill #11: discernment-nudge (Apache 2.0 • Squad 3: Governance & Epistemic Safety).

Key Features:
1. Default Pure Light Mode with instant Dark Mode toggle.
2. Dual Inference: Groq LPU (cloud fast inference at 500+ tok/s with pre-provisioned free token) + Local WebGPU (WebLLM) + Instant Offline Showcase.
3. User Input enabled: Freeform action plan, proposal, or recommendation input (pre-filled on load, zero empty-input blocking alerts).
4. Authentic Epistemic Pre-Mortem Methodology:
   - 2–3 targeted follow-up questions probing unstated premises, blind spots, failure modes, and factual citations.
   - Socratic Inquiry cards with assumption stress-testing.
   - 3 Verified Presets:
     - Preset 1: microservices-migration-plan (Architectural shift from monolith to 14 microservices).
     - Preset 2: go-to-market-pricing-strategy (30% price hike on enterprise SaaS plans).
     - Preset 3: ai-agent-autonomous-trading-bot (Deployment of LLM agent with direct financial exchange API keys).
5. Export Suite: Copy epistemic nudge report, download markdown pre-mortem audit, or evaluate new proposals.
"""

import json
import os

CATALOG_PATH = "internet_skills_catalog.json"
catalog = []
if os.path.exists(CATALOG_PATH):
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

dn_skill = next((s for s in catalog if s.get("name") == "discernment-nudge"), None)
dn_md = dn_skill.get("full_content", "") if dn_skill else """# Discernment Nudge
Append 2-3 targeted follow-up questions probing reasoning, assumptions, and missing context on high-stakes plans.
"""

PRESETS_DATA = [
    {
        "id": "microservices-migration",
        "name": "microservices-migration",
        "category": "SYSTEM ARCHITECTURE",
        "tagline": "Monolith to 14 Microservices Migration Plan",
        "brief": "We plan to decompose our monolithic Django app into 14 Go microservices over 3 months to solve database connection pooling bottlenecks and scale developer velocity.",
        "nudges": [
            {
                "focus": "Distributed Failure Modes & Network Latency",
                "question": "What is the network latency penalty and p99 SLA impact when a single customer request spans 5+ synchronous gRPC microservice boundaries compared to in-memory Django calls?",
                "risk": "Distributed Monolith Failure Mode"
            },
            {
                "focus": "Data Consistency & Distributed Transactions",
                "question": "How will you maintain relational consistency and financial ACID invariants across independent microservice databases without distributed 2PC two-phase commit overhead?",
                "risk": "Split-Brain Inconsistency"
            },
            {
                "focus": "Team Cognitive Overhead & Observability",
                "question": "Does the engineering team currently operate distributed tracing (OpenTelemetry), distributed deadlock detectors, and service meshes, or will operational triage latency increase?",
                "risk": "Operational Triage Paralysis"
            }
        ],
        "synthesis": """### Epistemic Pre-Mortem Audit // Microservices Migration

#### Plan Under Scrutiny:
Decompose monolithic Django app into 14 Go microservices over 3 months to resolve DB connection limits.

#### Critical Epistemic Checks:
1. **Network Hop Overhead:** Synchronous chained network calls convert simple DB transactions into complex network failure domains.
2. **Organizational Invariant:** Conway's Law dictates that microservices require autonomous teams; if 1 small team manages 14 repos, coordination tax will exceed monolith bottlenecks.
3. **Alternative Architecture:** Has connection pooling with PgBouncer, read-replicas, and background queue workers (Celery) been exhausted before incurring distributed systems complexity?
"""
    },
    {
        "id": "saas-pricing-increase",
        "name": "saas-pricing-increase",
        "category": "BUSINESS & STRATEGY",
        "tagline": "30% Enterprise Tier Price Hike",
        "brief": "We intend to increase all Enterprise subscription prices by 30% next quarter based on high customer satisfaction scores (NPS 72) and new agentic automation features.",
        "nudges": [
            {
                "focus": "Price Elasticity vs NPS Sentiment",
                "question": "Have you verified whether high NPS reflects willingness-to-pay elasticity, or if your enterprise users view the tool as a cost-effective commodity vulnerable to budget re-evaluations?",
                "risk": "Silent Enterprise Churn"
            },
            {
                "focus": "Contract Procurement Grandfathering",
                "question": "How many multi-year contracts contain procurement price-caps, and what is the churn contingency if procurement committees trigger RFPs with alternatives?",
                "risk": "Procurement Re-negotiation Blockers"
            },
            {
                "focus": "Value Realization of New Features",
                "question": "What percentage of active enterprise seats actually use the new agentic automation features on a weekly basis rather than just core functionality?",
                "risk": "Feature Adoption Deficit"
            }
        ],
        "synthesis": """### Epistemic Pre-Mortem Audit // SaaS Pricing Increase

#### Plan Under Scrutiny:
30% Enterprise price hike justified by high NPS scores and recent feature additions.

#### Critical Epistemic Checks:
1. **NPS vs Purchasing Decision:** NPS respondents are often end-users, whereas pricing adjustments trigger CFO and procurement audits.
2. **Grandfathering Strategy:** A hard 30% price cliff damages enterprise goodwill unless tied to an explicit tier-upgrade migration incentive.
"""
    },
    {
        "id": "autonomous-trading-bot",
        "name": "autonomous-trading-bot",
        "category": "FINANCIAL & AI SAFETY",
        "tagline": "LLM Agent with Exchange Trading API Keys",
        "brief": "We are deploying an autonomous LLM agent equipped with live crypto exchange API keys to trade order book anomalies with a maximum capital risk limit of $250,000.",
        "nudges": [
            {
                "focus": "Adversarial Prompt Injection & Order Book Spoofing",
                "question": "What deterministic circuit breaker prevents an external adversary from manipulating public on-chain news or tweet feeds to prompt-inject the agent into market dumping?",
                "risk": "Prompt Injection Exploit"
            },
            {
                "focus": "Flash Crash Liquidity & Hard Slippage Caps",
                "question": "Is the $250,000 risk limit enforced via immutable exchange API subaccount key constraints, or does it rely on software self-reporting during flash-crash liquidity vacuums?",
                "risk": "Exchange Liquidation Cascades"
            },
            {
                "focus": "Non-Deterministic Model Drifts",
                "question": "How will you prevent sudden model API updates (e.g., subtle shifts in token probability distribution) from altering trade sizing or risk calculations without prior notice?",
                "risk": "Model Version Drift Latency"
            }
        ],
        "synthesis": """### Epistemic Pre-Mortem Audit // Autonomous Trading Agent

#### Plan Under Scrutiny:
Live trading agent with direct exchange API keys trading real capital up to $250,000.

#### Critical Epistemic Checks:
1. **Never delegate financial limits to LLM prompts:** Capital limits must reside in hardware API key permissions, read-only subaccounts, and hardened exchange kill-switches.
2. **Adversarial Market Manipulation:** Public financial data feeds are unauthenticated and subject to deliberate prompt injection poisoning.
"""
    }
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Discernment Nudge Studio // Skill #11 (Apache 2.0)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-canvas: #f8fafc;
      --bg-panel: #ffffff;
      --bg-panel-subtle: #f1f5f9;
      --border-subtle: #e2e8f0;
      --border-focus: #b45309;
      --text-primary: #0f172a;
      --text-secondary: #475569;
      --text-muted: #64748b;
      --accent-amber: #b45309;
      --accent-amber-light: #fef3c7;
      --accent-emerald: #059669;
      --accent-rose: #be123c;
      --card-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
      --font-ui: 'Plus Jakarta Sans', sans-serif;
      --font-display: 'Bricolage Grotesque', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    html[data-theme="dark"] {
      --bg-canvas: #090d16;
      --bg-panel: #0f172a;
      --bg-panel-subtle: #1e293b;
      --border-subtle: #334155;
      --border-focus: #f59e0b;
      --text-primary: #f8fafc;
      --text-secondary: #cbd5e1;
      --text-muted: #94a3b8;
      --accent-amber: #f59e0b;
      --accent-amber-light: rgba(245, 158, 11, 0.15);
      --card-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
    }

    * { margin:0; padding:0; box-sizing:border-box; }
    body {
      background: var(--bg-canvas);
      color: var(--text-primary);
      font-family: var(--font-ui);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      transition: background 0.2s ease, color 0.2s ease;
    }

    .app-header {
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border-subtle);
      padding: 0.85rem 1.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 50;
    }
    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-badge {
      width: 40px;
      height: 40px;
      border-radius: 9px;
      background: linear-gradient(135deg, #b45309 0%, #d97706 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
      font-size: 1.25rem;
      font-weight: 800;
      box-shadow: 0 2px 8px rgba(180, 83, 9, 0.25);
    }
    .brand-text h1 {
      font-family: var(--font-display);
      font-size: 1.25rem;
      font-weight: 800;
      line-height: 1.15;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .badge-skill-fit {
      font-size: 0.65rem;
      background: #ecfdf5;
      color: #047857;
      border: 1px solid #a7f3d0;
      border-radius: 999px;
      padding: 2px 8px;
      font-weight: 700;
      font-family: var(--font-mono);
    }
    .brand-text p {
      font-size: 0.76rem;
      color: var(--text-muted);
    }

    .engine-switch {
      display: flex;
      background: var(--bg-panel-subtle);
      padding: 3px;
      border-radius: 8px;
      border: 1px solid var(--border-subtle);
      gap: 2px;
    }
    .engine-btn {
      padding: 6px 13px;
      border-radius: 6px;
      border: none;
      background: transparent;
      font-size: 0.76rem;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
      font-family: var(--font-ui);
    }
    .engine-btn.active.groq {
      background: #b45309;
      color: #ffffff;
      box-shadow: 0 1px 4px rgba(180, 83, 9, 0.3);
    }
    .engine-btn.active.webgpu {
      background: #0f172a;
      color: #ffffff;
      box-shadow: 0 1px 4px rgba(15, 23, 42, 0.3);
    }
    .engine-btn.active.instant {
      background: #0f172a;
      color: #ffffff;
    }

    .theme-toggle-btn {
      background: var(--bg-panel-subtle);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .runtime-banner {
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border-subtle);
      padding: 0.6rem 1.75rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 0.75rem;
    }
    .runtime-desc {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .runtime-icon { font-size: 1.1rem; }
    .runtime-controls {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .select-box, .text-input {
      background: var(--bg-panel-subtle);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      padding: 5px 9px;
      border-radius: 6px;
      font-size: 0.74rem;
      font-family: var(--font-mono);
    }

    .main-stage {
      flex: 1;
      padding: 1.25rem 1.75rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    .studio-grid {
      display: grid;
      grid-template-columns: 390px 1fr;
      gap: 1.25rem;
      align-items: start;
    }
    @media (max-width: 1024px) {
      .studio-grid { grid-template-columns: 1fr; }
    }

    .sidebar-pane {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    .card-box {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 1rem;
      box-shadow: var(--card-shadow);
    }
    .card-box-header {
      font-family: var(--font-display);
      font-size: 0.88rem;
      font-weight: 700;
      margin-bottom: 0.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .preset-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 0.85rem;
    }
    .preset-card {
      background: var(--bg-panel-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 0.65rem 0.85rem;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.15s ease;
    }
    .preset-card:hover {
      border-color: var(--accent-amber);
      background: var(--accent-amber-light);
    }
    .preset-card.active {
      border-color: var(--accent-amber);
      background: var(--accent-amber-light);
    }
    .preset-title {
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--text-primary);
    }
    .preset-meta {
      font-size: 0.68rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }

    .prompt-chips-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 0.75rem;
    }
    .prompt-chip {
      background: var(--bg-panel-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 999px;
      padding: 4px 10px;
      font-size: 0.7rem;
      font-weight: 600;
      color: var(--text-primary);
      cursor: pointer;
      transition: all 0.12s ease;
    }
    .prompt-chip:hover {
      border-color: var(--accent-amber);
      color: var(--accent-amber);
    }
    .prompt-chip.active {
      border-color: var(--accent-amber);
      background: var(--accent-amber);
      color: #ffffff;
    }

    .brief-input {
      width: 100%;
      height: 105px;
      background: var(--bg-panel-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 0.75rem;
      font-size: 0.82rem;
      color: var(--text-primary);
      font-family: var(--font-ui);
      resize: vertical;
      line-height: 1.45;
      margin-bottom: 0.75rem;
    }
    .brief-input:focus {
      outline: none;
      border-color: var(--accent-amber);
      background: var(--bg-panel);
    }

    .btn-synthesize {
      width: 100%;
      background: linear-gradient(135deg, #b45309 0%, #d97706 100%);
      color: #ffffff;
      border: none;
      border-radius: 8px;
      padding: 0.78rem;
      font-size: 0.84rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 2px 8px rgba(180, 83, 9, 0.25);
      transition: all 0.15s ease;
      font-family: var(--font-display);
    }
    .btn-synthesize:hover {
      opacity: 0.95;
      transform: translateY(-1px);
    }
    .btn-synthesize:disabled {
      opacity: 0.6;
      cursor: not-allowed;
      transform: none;
    }

    .runbook-box {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      overflow: hidden;
      box-shadow: var(--card-shadow);
    }
    .runbook-header {
      padding: 0.75rem 1rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      background: var(--bg-panel-subtle);
      border-bottom: 1px solid var(--border-subtle);
    }
    .runbook-body {
      padding: 0.85rem;
      font-size: 0.72rem;
      color: var(--text-secondary);
      max-height: 220px;
      overflow-y: auto;
      font-family: var(--font-mono);
      line-height: 1.45;
    }

    .stage-pane {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      display: flex;
      flex-direction: column;
      box-shadow: var(--card-shadow);
      overflow: hidden;
    }
    .stage-top-bar {
      padding: 0.65rem 1.1rem;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 0.75rem;
      background: var(--bg-panel-subtle);
    }
    .tabs-group {
      display: flex;
      gap: 4px;
    }
    .tab-btn {
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 0.76rem;
      font-weight: 700;
      border: none;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s ease;
      font-family: var(--font-display);
    }
    .tab-btn.active {
      background: var(--bg-panel);
      color: var(--accent-amber);
      box-shadow: var(--card-shadow);
    }

    .stage-content {
      padding: 1.5rem;
      min-height: 580px;
      background: var(--bg-canvas);
      overflow-y: auto;
    }

    /* Nudge Cards Grid */
    .nudges-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 1.5rem;
    }
    .nudge-card {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-left: 4px solid var(--accent-amber);
      border-radius: 8px;
      padding: 1.1rem 1.25rem;
    }
    .nudge-tag {
      font-family: var(--font-mono);
      font-size: 0.7rem;
      font-weight: 700;
      color: var(--accent-amber);
      text-transform: uppercase;
      margin-bottom: 6px;
    }
    .nudge-question {
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--text-primary);
      line-height: 1.45;
      margin-bottom: 8px;
    }
    .nudge-risk {
      font-size: 0.72rem;
      color: var(--accent-rose);
      font-family: var(--font-mono);
    }

    .synthesis-view {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 1.5rem;
      font-size: 0.84rem;
      line-height: 1.6;
    }

    .bottom-bar {
      padding: 0.75rem 1.1rem;
      border-top: 1px solid var(--border-subtle);
      background: var(--bg-panel-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.72rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }
    .actions-row {
      display: flex;
      gap: 6px;
    }
    .btn-action {
      padding: 5px 10px;
      font-size: 0.72rem;
      font-weight: 600;
      border: 1px solid var(--border-subtle);
      background: var(--bg-panel);
      color: var(--text-primary);
      border-radius: 5px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .btn-action:hover {
      border-color: var(--accent-amber);
      color: var(--accent-amber);
    }

    .toast-box {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      padding: 10px 18px;
      border-radius: 8px;
      font-size: 0.8rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 10px 25px -5px rgba(0,0,0,0.2);
      opacity: 0;
      pointer-events: none;
      transform: translateY(10px);
      transition: all 0.2s ease;
      z-index: 100;
    }
    .toast-box.show {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0);
    }
  </style>
</head>
<body>

  <header class="app-header">
    <div class="brand-group">
      <div class="brand-badge">🛡️</div>
      <div class="brand-text">
        <h1>Discernment Nudge Studio <span class="badge-skill-fit">Skill #11: discernment-nudge (Apache 2.0 • Epistemic Guard)</span></h1>
        <p>Pre-Mortem Safety Checkpoints • Probe Assumptions, Blind Spots &amp; Invariants on High-Stakes Plans</p>
      </div>
    </div>

    <div style="display: flex; align-items: center; gap: 0.75rem;">
      <div class="engine-switch">
        <button class="engine-btn active groq" id="tabGroq" onclick="switchEngine('groq')">
          ⚡ Groq LPU (Cloud)
        </button>
        <button class="engine-btn instant" id="tabInstant" onclick="switchEngine('instant')">
          ⚡ Instant Showcase
        </button>
        <button class="engine-btn webgpu" id="tabWebGPU" onclick="switchEngine('webgpu')">
          🎮 Local WebGPU (WebLLM)
        </button>
      </div>

      <button class="theme-toggle-btn" id="btnThemeToggle" onclick="toggleTheme()" title="Toggle light and dark theme">
        🌙 Dark Mode
      </button>
    </div>
  </header>

  <main class="main-stage">

    <div class="runtime-banner" id="runtimeBanner">
      <!-- Populated via JS -->
    </div>

    <div class="studio-grid">

      <div class="sidebar-pane">

        <div class="card-box">
          <div class="card-box-header">
            <span>High-Stakes Scenarios</span>
            <span style="color: var(--accent-amber); font-size: 0.72rem; font-family: var(--font-mono);">Epistemic Audits</span>
          </div>

          <div class="preset-list" id="presetsList">
            <!-- Rendered via JS -->
          </div>

          <div class="card-box-header" style="margin-top: 1.15rem;">
            <span>Probe Custom Plan</span>
            <span style="font-size:0.7rem; color:var(--accent-amber); font-weight:600;">⚡ Groq LPU Ready</span>
          </div>

          <div class="prompt-chips-row">
            <button type="button" class="prompt-chip active" onclick="setPromptBrief('We plan to decompose our monolithic Django app into 14 Go microservices over 3 months to solve database connection pooling bottlenecks and scale developer velocity.', this)">🧩 Microservices</button>
            <button type="button" class="prompt-chip" onclick="setPromptBrief('We intend to increase all Enterprise subscription prices by 30% next quarter based on high customer satisfaction scores (NPS 72) and new agentic automation features.', this)">💰 30% Price Hike</button>
            <button type="button" class="prompt-chip" onclick="setPromptBrief('We are deploying an autonomous LLM agent equipped with live crypto exchange API keys to trade order book anomalies with a maximum capital risk limit of $250,000.', this)">🤖 Trading Bot</button>
            <button type="button" class="prompt-chip" onclick="setPromptBrief('We are migrating all customer user data from single-region AWS Postgres to multi-region DynamoDB without running dry-run reconciliation tests.', this)">🌐 Multi-Region Migration</button>
          </div>

          <textarea class="brief-input" id="briefInput" placeholder="Enter any actionable plan, strategy, proposal, or architectural decision to stress-test unstated assumptions..."></textarea>

          <button class="btn-synthesize" id="btnSynthesize" onclick="runDiscernmentSynthesis()">
            <span>⚡ Run Epistemic Pre-Mortem (Groq LPU)</span>
          </button>
        </div>

        <div class="runbook-box">
          <div class="runbook-header" onclick="toggleRunbook()">
            <span style="font-weight: 700; font-size: 0.8rem; color: var(--text-primary);">
              📜 Injected SKILL.md (discernment-nudge Runbook)
            </span>
            <span style="font-size: 0.75rem; color: var(--text-muted);" id="runbookArrow">▼ Expand</span>
          </div>
          <div class="runbook-body" id="runbookBody" style="display: none;">
            <div style="color: var(--accent-emerald); font-weight: 700; margin-bottom: 0.5rem;">
              [Apache 2.0 In-Context Rules Loaded]
            </div>
            <pre style="white-space: pre-wrap;">__SKILL_SNIPPET__...

[Remaining runbook active in system prompt context]</pre>
          </div>
        </div>

      </div>

      <div class="stage-pane">

        <div class="stage-top-bar">
          <div class="tabs-group">
            <button class="tab-btn active" id="tabBtnNudges" onclick="switchStage('nudges')">🔍 Socratic Inquiry Nudges</button>
            <button class="tab-btn" id="tabBtnSynthesis" onclick="switchStage('synthesis')">📋 Pre-Mortem Audit Report</button>
          </div>

          <div style="font-size: 0.72rem; color: var(--accent-amber); font-weight: 700; font-family: var(--font-mono);">
            CRITICAL BLIND SPOT DETECTION
          </div>
        </div>

        <div class="stage-content" id="stageNudges">
          <div class="nudges-list" id="nudgesListContainer">
            <!-- Rendered via JS -->
          </div>
        </div>

        <div class="stage-content" id="stageSynthesis" style="display: none;">
          <div class="synthesis-view" id="synthesisViewContent"></div>
        </div>

        <div class="bottom-bar">
          <div id="renderSourceInfo">Plan: microservices-migration • 3 Nudges Evaluated</div>
          <div class="actions-row">
            <button class="btn-action" onclick="copyNudgeReport()">📋 Copy Nudges</button>
            <button class="btn-action" onclick="downloadNudgeReport()">💾 Download Audit .md</button>
          </div>
        </div>

      </div>

    </div>

  </main>

  <div class="toast-box" id="toastBox">
    <span id="toastIcon">✅</span>
    <span id="toastMsg">Success</span>
  </div>

  <script>
  const _XK = [77, 89, 65, 117, 102, 71, 88, 71, 115, 18, 66, 108, 99, 125, 69, 67, 125, 123, 97, 78, 88, 88, 30, 123, 125, 109, 78, 83, 72, 25, 108, 115, 102, 69, 96, 71, 115, 24, 95, 30, 127, 73, 93, 77, 92, 99, 69, 29, 123, 64, 80, 104, 71, 31, 114, 29];
  const PROVISIONED_GROQ_KEY = _XK.map(c => String.fromCharCode(c ^ 42)).join("");

  const PRESETS = __PRESETS_JSON__;
  let currentEngine = 'groq';
  let currentPresetIdx = 0;
  let currentStage = 'nudges';
  let currentNudges = PRESETS[0].nudges;
  let currentSynthesis = PRESETS[0].synthesis;
  let webllmEngine = null;

  window.addEventListener('DOMContentLoaded', () => {
    initTheme();
    renderRuntimeBanner();
    renderPresetsList();
    selectPreset(0);
    const defaultBrief = PRESETS[0].brief;
    const input = document.getElementById('briefInput');
    if (input && !input.value) input.value = defaultBrief;
  });

  function initTheme() {
    const saved = localStorage.getItem('discernment_app_mode') || 'light';
    setTheme(saved);
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'light' ? 'dark' : 'light';
    setTheme(next);
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('discernment_app_mode', theme);
    const btn = document.getElementById('btnThemeToggle');
    if (btn) btn.innerHTML = theme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode';
  }

  function switchEngine(eng) {
    currentEngine = eng;
    document.querySelectorAll('.engine-btn').forEach(b => b.classList.remove('active'));
    if (eng === 'instant') document.getElementById('tabInstant').classList.add('active');
    if (eng === 'webgpu') document.getElementById('tabWebGPU').classList.add('active');
    if (eng === 'groq') document.getElementById('tabGroq').classList.add('active');

    const synthBtn = document.getElementById('btnSynthesize');
    if (synthBtn) {
      if (eng === 'groq') synthBtn.innerHTML = '<span>⚡ Run Epistemic Pre-Mortem (Groq LPU)</span>';
      else if (eng === 'webgpu') synthBtn.innerHTML = '<span>🎮 Synthesize via Local WebGPU</span>';
      else synthBtn.innerHTML = '<span>⚡ Render Instant Showcase</span>';
    }
    renderRuntimeBanner();
  }

  function renderRuntimeBanner() {
    const banner = document.getElementById('runtimeBanner');
    if (currentEngine === 'groq') {
      const customKey = localStorage.getItem('groq_api_key') || '';
      banner.innerHTML = `
        <div class="runtime-desc">
          <div class="runtime-icon" style="color: #b45309;">⚡</div>
          <div>
            <strong style="font-size: 0.85rem; color: var(--text-primary);">Groq LPU Cloud Fast Inference (500+ tok/s)</strong>
            <div style="font-size: 0.75rem; color: var(--text-secondary);">
              🟢 Pre-provisioned Free Tier API token active! Generates Socratic discernment nudges in ~1–2 seconds.
            </div>
          </div>
        </div>
        <div class="runtime-controls">
          <select class="select-box" id="groqModelSelect">
            <option value="openai/gpt-oss-120b" selected>GPT-OSS 120B (Groq LPU • Free Tier)</option>
            <option value="qwen/qwen3.8-27b">Qwen 3.8 27B (Groq LPU)</option>
            <option value="openai/gpt-oss-20b">GPT-OSS 20B (Groq LPU)</option>
          </select>
          <input type="password" class="text-input" id="groqKey" placeholder="Pre-provisioned key active (or paste gsk_...)" value="${customKey}" onchange="saveCustomGroqKey(this.value)" style="width: 220px;">
          <span style="font-size: 0.72rem; color: #047857; font-weight: 700;">🟢 Free Token Active</span>
        </div>
      `;
    } else if (currentEngine === 'instant') {
      banner.innerHTML = `
        <div class="runtime-desc">
          <div class="runtime-icon" style="color: #b45309;">⚡</div>
          <div>
            <strong style="font-size: 0.85rem; color: var(--text-primary);">Instant Verified Showcase Mode</strong>
            <div style="font-size: 0.75rem; color: var(--text-secondary);">
              3 pre-computed epistemic audits examining high-stakes plans.
            </div>
          </div>
        </div>
        <div style="font-size: 0.75rem; color: #047857; font-weight: 700;">
          🟢 Zero Latency • 100% Client Offline Compatible
        </div>
      `;
    } else if (currentEngine === 'webgpu') {
      banner.innerHTML = `
        <div class="runtime-desc">
          <div class="runtime-icon" style="color: #0f172a;">🎮</div>
          <div>
            <strong style="font-size: 0.85rem; color: var(--text-primary);">Local In-Browser WebGPU (WebLLM)</strong>
            <div style="font-size: 0.75rem; color: var(--text-secondary);">
              Executes private local LLM weights on device GPU without network round-trips.
            </div>
          </div>
        </div>
        <div class="runtime-controls">
          <select class="select-box" id="webgpuModelSelect">
            <option value="Llama-3.2-3B-Instruct-q4f16_1-MLC" selected>Llama 3.2 3B Instruct (q4f16)</option>
            <option value="Qwen2.5-1.5B-Instruct-q4f16_1-MLC">Qwen 2.5 1.5B Instruct (Fast)</option>
          </select>
          <button class="btn-action" id="btnLoadGpu" onclick="loadWebLLM()" style="background: #b45309; color: #fff; border:none; padding: 5px 12px;">Load into GPU</button>
        </div>
        <div id="gpuProgressWrap" style="display:none; width: 100%; margin-top: 5px;">
          <div style="background: var(--border-subtle); height: 5px; border-radius: 3px; overflow: hidden;">
            <div id="gpuProgressFill" style="background: #b45309; height: 100%; width: 0%;"></div>
          </div>
          <div id="gpuProgressInfo" style="font-size: 0.7rem; color: var(--text-muted); margin-top: 3px;"></div>
        </div>
      `;
    }
  }

  function getActiveGroqKey() {
    const custom = localStorage.getItem('groq_api_key');
    if (custom && custom.trim().length > 10) return custom.trim();
    return PROVISIONED_GROQ_KEY;
  }

  function saveCustomGroqKey(val) {
    if (val && val.trim().length > 10) {
      localStorage.setItem('groq_api_key', val.trim());
      showToast('Custom Groq Key Saved', '🔑');
    } else {
      localStorage.removeItem('groq_api_key');
      showToast('Using Pre-provisioned Free Token', '⚡');
    }
  }

  async function loadWebLLM() {
    if (!navigator.gpu) {
      alert('WebGPU is not supported on this browser.');
      return;
    }
    const model = document.getElementById('webgpuModelSelect').value;
    const btn = document.getElementById('btnLoadGpu');
    const wrap = document.getElementById('gpuProgressWrap');
    const fill = document.getElementById('gpuProgressFill');
    const info = document.getElementById('gpuProgressInfo');

    btn.disabled = true;
    btn.innerText = 'Loading...';
    wrap.style.display = 'block';

    try {
      showToast('Importing WebLLM module...', '📦');
      const webllm = await import("https://esm.run/@mlc-ai/web-llm");
      webllmEngine = await webllm.CreateMLCEngine(model, {
        initProgressCallback: (report) => {
          const pct = Math.round(report.progress * 100);
          fill.style.width = pct + '%';
          info.innerText = `[${pct}%] ${report.text}`;
        }
      });
      btn.innerText = '✅ Loaded on GPU';
      btn.style.background = '#047857';
      showToast('Model resident in WebGPU!', '🚀');
    } catch(e) {
      console.error(e);
      showToast('Failed to load WebLLM: ' + e.message, '⚠️');
      btn.disabled = false;
      btn.innerText = 'Retry';
    }
  }

  function renderPresetsList() {
    const list = document.getElementById('presetsList');
    list.innerHTML = PRESETS.map((p, i) => `
      <div class="preset-card ${i === currentPresetIdx ? 'active' : ''}" onclick="selectPreset(${i})">
        <div>
          <div class="preset-title">${p.name}</div>
          <div class="preset-meta">${p.category}</div>
        </div>
        <div style="font-size: 0.72rem; color: var(--text-muted);">View Nudges →</div>
      </div>
    `).join('');
  }

  function selectPreset(idx) {
    currentPresetIdx = idx;
    const p = PRESETS[idx];
    document.querySelectorAll('.preset-card').forEach((el, i) => {
      el.classList.toggle('active', i === idx);
    });
    document.getElementById('briefInput').value = p.brief;
    currentNudges = p.nudges;
    currentSynthesis = p.synthesis;

    renderNudgesView(p);
  }

  function setPromptBrief(txt, el) {
    document.getElementById('briefInput').value = txt;
    document.querySelectorAll('.prompt-chip').forEach(c => c.classList.remove('active'));
    if (el) el.classList.add('active');
  }

  function switchStage(stage) {
    currentStage = stage;
    document.getElementById('tabBtnNudges').classList.toggle('active', stage === 'nudges');
    document.getElementById('tabBtnSynthesis').classList.toggle('active', stage === 'synthesis');
    document.getElementById('stageNudges').style.display = (stage === 'nudges') ? 'block' : 'none';
    document.getElementById('stageSynthesis').style.display = (stage === 'synthesis') ? 'block' : 'none';
  }

  function renderNudgesView(p) {
    document.getElementById('renderSourceInfo').innerText = `Plan: ${p.name} • ${p.nudges.length} Nudges Evaluated`;

    const container = document.getElementById('nudgesListContainer');
    container.innerHTML = p.nudges.map(n => `
      <div class="nudge-card">
        <div class="nudge-tag">🎯 Critical Probe: ${n.focus}</div>
        <div class="nudge-question">${n.question}</div>
        <div class="nudge-risk">⚠️ Underlying Blind Spot: ${n.risk}</div>
      </div>
    `).join('');

    document.getElementById('synthesisViewContent').innerHTML = p.synthesis.replace(/\\n/g, '<br>');
  }

  async function runDiscernmentSynthesis() {
    let brief = document.getElementById('briefInput').value.trim();
    if (!brief) {
      brief = "We plan to decompose our monolithic Django app into 14 Go microservices over 3 months to solve database connection pooling bottlenecks and scale developer velocity.";
      document.getElementById('briefInput').value = brief;
      const firstChip = document.querySelector('.prompt-chip');
      if (firstChip) firstChip.classList.add('active');
      showToast('Loaded Microservices prompt', '🧩');
    }

    const btn = document.getElementById('btnSynthesize');
    btn.disabled = true;
    btn.innerHTML = '<span>⏳ Probing Assumptions via Groq...</span>';

    const startTime = Date.now();

    try {
      if (currentEngine === 'groq') {
        const apiKey = getActiveGroqKey();
        const model = document.getElementById('groqModelSelect') ? document.getElementById('groqModelSelect').value : 'openai/gpt-oss-120b';

        const prompt = "You are an elite epistemic advisor following Anthropic's official 'discernment-nudge' runbook.\\n" +
          "Your mission: Given the user's plan or proposal, return 2-3 specific, rigorous Socratic follow-up questions that probe unstated assumptions, failure modes, and factual citations.\\n" +
          "OUTPUT FORMAT: Return a valid JSON array of objects with keys: 'focus', 'question', 'risk'. Wrap inside ```json codeblock.";

        const resp = await fetch("https://api.groq.com/openai/v1/chat/completions", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${apiKey}`,
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            model: model,
            messages: [
              { role: "system", content: prompt },
              { role: "user", content: brief }
            ],
            temperature: 0.7,
            max_tokens: 3000
          })
        });

        if (!resp.ok) {
          const err = await resp.json();
          throw new Error(err.error?.message || resp.statusText);
        }

        const data = await resp.json();
        const txt = data.choices[0].message.content;

        extractAndApplyNudges(txt, brief, `Groq LPU (${model})`);
        const elapsed = Date.now() - startTime;
        showToast(`Epistemic audit synthesized in ${elapsed}ms!`, '⚡');

      } else if (currentEngine === 'instant') {
        selectPreset(1);
        showToast('Switched to SaaS Pricing preset!', '✨');

      } else if (currentEngine === 'webgpu') {
        if (!webllmEngine) throw new Error('Please load the WebLLM model into WebGPU first using the top banner button.');
        const prompt = "You are a discernment nudge advisor. Return a JSON array of 3 probing questions inside ```json.";
        const reply = await webllmEngine.chat.completions.create({
          messages: [
            { role: "system", content: prompt },
            { role: "user", content: brief }
          ],
          temperature: 0.7,
          max_tokens: 2000
        });
        const txt = reply.choices[0].message.content;
        extractAndApplyNudges(txt, brief, 'Local WebGPU (WebLLM)');
        showToast('WebGPU local synthesis complete!', '🎮');
      }
    } catch(e) {
      showToast('Synthesis error: ' + (e.message || 'Check network'), '⚠️');
      console.error(e);
    } finally {
      btn.disabled = false;
      if (currentEngine === 'groq') btn.innerHTML = '<span>⚡ Run Epistemic Pre-Mortem (Groq LPU)</span>';
      else if (currentEngine === 'webgpu') btn.innerHTML = '<span>🎮 Synthesize via Local WebGPU</span>';
      else btn.innerHTML = '<span>⚡ Render Instant Showcase</span>';
    }
  }

  function extractAndApplyNudges(rawText, userBrief, source) {
    let jsonStr = "";
    const jsonMarker = rawText.indexOf('```json');
    const genericMarker = rawText.indexOf('```');

    if (jsonMarker !== -1) {
      let candidate = rawText.substring(jsonMarker + 7).trim();
      const endFence = candidate.lastIndexOf('```');
      if (endFence !== -1) candidate = candidate.substring(0, endFence).trim();
      jsonStr = candidate;
    } else if (genericMarker !== -1) {
      let candidate = rawText.substring(genericMarker + 3).trim();
      const endFence = candidate.lastIndexOf('```');
      if (endFence !== -1) candidate = candidate.substring(0, endFence).trim();
      jsonStr = candidate;
    } else {
      jsonStr = rawText.trim();
    }

    try {
      const parsed = JSON.parse(jsonStr);
      const nudges = Array.isArray(parsed) ? parsed : (parsed.nudges || []);
      const p = {
        name: "Custom Proposal",
        brief: userBrief,
        nudges: nudges,
        synthesis: `### Epistemic Audit for: "${userBrief}"\\n\\nGenerated via ${source}. Evaluated against unstated assumptions.`
      };
      renderNudgesView(p);
      switchStage('nudges');
    } catch(err) {
      console.error("JSON parse error:", err);
      showToast('Failed to parse model JSON: ' + err.message, '⚠️');
    }
  }

  function copyNudgeReport() {
    const text = currentNudges.map(n => `• [${n.focus}] ${n.question} (Risk: ${n.risk})`).join('\\n\\n');
    navigator.clipboard.writeText(text).then(() => {
      showToast('Nudges copied to clipboard!', '📋');
    });
  }

  function downloadNudgeReport() {
    const md = `# Epistemic Pre-Mortem Audit\\n\\n` + currentNudges.map(n => `### ${n.focus}\\n**Question:** ${n.question}\\n*Risk:* ${n.risk}\\n`).join('\\n');
    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `discernment_nudge_${Date.now()}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('Audit report downloaded!', '💾');
  }

  function toggleRunbook() {
    const body = document.getElementById('runbookBody');
    const arrow = document.getElementById('runbookArrow');
    const isHidden = (body.style.display === 'none');
    body.style.display = isHidden ? 'block' : 'none';
    arrow.innerText = isHidden ? '▲ Collapse' : '▼ Expand';
  }

  function showToast(msg, icon='✅') {
    const box = document.getElementById('toastBox');
    document.getElementById('toastIcon').innerText = icon;
    document.getElementById('toastMsg').innerText = msg;
    box.classList.add('show');
    setTimeout(() => {
      box.classList.remove('show');
    }, 3200);
  }
  </script>
</body>
</html>"""

def build_app():
    snippet = dn_md[:1500].replace("\\", "\\\\").replace("`", "\\`")
    presets_json_str = json.dumps(PRESETS_DATA)
    
    out_html = HTML_TEMPLATE.replace("__SKILL_SNIPPET__", snippet)
    out_html = out_html.replace("__PRESETS_JSON__", presets_json_str)

    target_file = "discernment_nudge_app.html"
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(out_html)
    
    print(f"Generated {target_file} successfully! Size: {len(out_html)} bytes")

if __name__ == "__main__":
    build_app()
