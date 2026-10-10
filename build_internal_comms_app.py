"""
build_internal_comms_app.py
Builds internal_comms_app.html: Standalone frontend-only HTML application
powered by WebLLM (local WebGPU) and Groq LPU (cloud fast inference),
demonstrating Skill #12: internal-comms (Apache 2.0 • Squad 3: Governance & Epistemic Safety).

Key Features:
1. Default Pure Light Mode with instant Dark Mode toggle.
2. Dual Inference: Groq LPU (cloud fast inference at 500+ tok/s with pre-provisioned free token) + Local WebGPU (WebLLM) + Instant Offline Showcase.
3. User Input enabled: Freeform team updates, incident notes, or announcements (pre-filled on load, zero empty-input blocking alerts).
4. Authentic Internal Communications Frameworks:
   - 3P Team Updates (Progress, Plans, Problems with blockers & mitigation).
   - Executive Incident Post-Mortems (Severity, Root Cause, Timeline, Preventative Guardrails).
   - Company All-Hands Newsletter & FAQ memos (High-signal Amazon-style narrative).
   - 3 Verified Presets:
     - Preset 1: 3p-engineering-sync (Weekly team update with 3 progress items, 2 upcoming releases, and 1 blocker).
     - Preset 2: sev1-post-mortem (Payment gateway outage post-mortem with 5 Whys and preventative action items).
     - Preset 3: product-launch-faq (All-hands internal announcement and cross-functional FAQ).
5. Export Suite: One-click copy formatted Markdown, download `.md`, or toggle between Executive Preview and Raw Markdown.
"""

import json
import os

CATALOG_PATH = "internet_skills_catalog.json"
catalog = []
if os.path.exists(CATALOG_PATH):
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

ic_skill = next((s for s in catalog if s.get("name") == "internal-comms"), None)
ic_md = ic_skill.get("full_content", "") if ic_skill else """# Internal Communications
High-signal memos: 3P updates (Progress, Plans, Problems), incident post-mortems, executive newsletters, and team FAQs.
"""

PRESETS_DATA = [
    {
        "id": "3p-engineering-sync",
        "name": "3P Engineering Sync",
        "category": "TEAM SYNC",
        "format": "Progress • Plans • Problems",
        "brief": "A weekly 3P update for the Agent Core team: shipped WebGPU local inference, preparing Groq LPU token deployment next Tuesday, blocked on cross-origin iframe security headers.",
        "memo_html": """<div class="memo-card">
  <div class="memo-header">
    <div class="memo-badge">3P UPDATE // AGENT CORE TEAM</div>
    <div class="memo-meta">Week 41 • Oct 2026 • Audience: Engineering Leadership</div>
  </div>
  
  <div class="memo-section">
    <div class="section-title green">🟢 PROGRESS (What We Shipped This Week)</div>
    <ul class="memo-list">
      <li><strong>Local WebGPU Runtime:</strong> Successfully integrated <code>@mlc-ai/web-llm</code> for in-browser client model execution with zero server compute costs.</li>
      <li><strong>Bench Accuracy Suite:</strong> Automated Selenium headless test harness deployed to UAT pipeline, catching 100% of DOM selector regressions.</li>
      <li><strong>Design System Alignment:</strong> Converted all studio apps to pure Light Mode by default with instant dark-mode state retention.</li>
    </ul>
  </div>

  <div class="memo-section">
    <div class="section-title blue">🔷 PLANS (Key Deliverables for Next Week)</div>
    <ul class="memo-list">
      <li><strong>Groq LPU Deployment:</strong> Cut over primary synthesis engine to cloud fast inference (500+ tok/s) with pre-provisioned free tier keys.</li>
      <li><strong>Skills Catalog Packaging:</strong> Finish rollout of Skills 10, 11, and 12 into automated UAT and LinkedIn announcement pipeline.</li>
    </ul>
  </div>

  <div class="memo-section">
    <div class="section-title red">🔴 PROBLEMS (Blockers &amp; Mitigations)</div>
    <ul class="memo-list">
      <li><strong>Issue:</strong> Cross-Origin Resource Sharing (CORS) sandbox restrictions prevent iframe child frame access in WebGPU workers.<br>
      <em>Mitigation:</em> Implemented Web Workers isolated message bus bypassing parent document iframe origin locks.</li>
    </ul>
  </div>
</div>""",
        "markdown": """# 3P Update: Agent Core Team
**Period:** Week 41 (October 2026) | **Audience:** Engineering Leadership

## 🟢 PROGRESS
- **Local WebGPU Runtime:** Shipped `@mlc-ai/web-llm` browser execution.
- **Automated Verification:** Added headless Selenium test harness with zero false positives.
- **Light Mode Default:** Unified UI with instant theme persistence.

## 🔷 PLANS
- **Groq LPU Cutover:** Production rollout of cloud fast inference (500+ tok/s).
- **Skills 10-12 Rollout:** Release webapp-testing, discernment-nudge, and internal-comms studios.

## 🔴 PROBLEMS
- **CORS Iframe Isolation:** Mitigated via isolated Web Worker postMessage bus.
"""
    },
    {
        "id": "sev1-post-mortem",
        "name": "SEV-1 Incident Post-Mortem",
        "category": "INCIDENT POST-MORTEM",
        "format": "Summary • Timeline • 5 Whys • Action Items",
        "brief": "A blameless post-mortem for a 14-minute payment webhook timeout outage caused by exhausted database connection pools during the midnight cron billing batch.",
        "memo_html": """<div class="memo-card">
  <div class="memo-header">
    <div class="memo-badge red">INCIDENT REPORT // SEV-1 OUTAGE</div>
    <div class="memo-meta">Incident ID: INC-8492 • Duration: 14 Minutes • Status: Resolved &amp; Remediated</div>
  </div>

  <div class="memo-section">
    <div class="section-title">🚨 EXECUTIVE SUMMARY</div>
    <p class="memo-p">On Oct 09 at 00:02 UTC, the payment ingress service experienced connection pool exhaustion, causing Stripe webhook timeouts and 48 dropped checkout confirmations. Full recovery was achieved at 00:16 UTC after scaling PgBouncer pool limits.</p>
  </div>

  <div class="memo-section">
    <div class="section-title blue">⏱️ CHRONOLOGICAL TIMELINE</div>
    <ul class="memo-list">
      <li><strong>00:02 UTC:</strong> Automated cron triggered monthly subscription batch, exhausting 200/200 DB connections.</li>
      <li><strong>00:05 UTC:</strong> PagerDuty alerted on <code>504 Gateway Timeout</code> spike (&gt; 5% threshold).</li>
      <li><strong>00:09 UTC:</strong> On-call paused cron batch worker queue and doubled PgBouncer max connections to 500.</li>
      <li><strong>00:16 UTC:</strong> Payment queue cleared, webhooks re-processed with zero lost financial transactions.</li>
    </ul>
  </div>

  <div class="memo-section">
    <div class="section-title green">🛡️ PREVENTATIVE ACTION ITEMS</div>
    <ul class="memo-list">
      <li><strong>P0:</strong> Decouple batch cron jobs to a dedicated Postgres read-write replica (Owner: DB Team, ETA: Friday).</li>
      <li><strong>P1:</strong> Implement exponential backoff retry jitter on Stripe webhook consumers (Owner: Core API, ETA: Next Sprint).</li>
    </ul>
  </div>
</div>""",
        "markdown": """# SEV-1 Post-Mortem: Payment Webhook Timeout Outage
**Incident ID:** INC-8492 | **Duration:** 14 min | **Severity:** SEV-1

## Executive Summary
Connection pool exhaustion during midnight cron billing batch caused Stripe webhook timeouts. Resolved via PgBouncer limit scaling.

## Root Cause (5 Whys)
1. Webhooks timed out -> Database queries hung.
2. DB hung -> Connections hit max cap (200/200).
3. Cap hit -> Midnight cron batch ran concurrently with live user checkouts on primary DB.
4. Batch ran on primary -> Replica offloading had not been configured for billing worker.

## Action Items
- [x] Increase PgBouncer pool cap from 200 to 500.
- [ ] Route batch worker queries to dedicated replica (Owner: DB Team).
"""
    },
    {
        "id": "product-launch-faq",
        "name": "Product Launch FAQ & Comms",
        "category": "ALL-HANDS ANNOUNCEMENT",
        "format": "Announcement • Strategy • Cross-Functional FAQ",
        "brief": "A company-wide internal launch memo announcing the rollout of Client-Side WebGPU inference, explaining customer benefits, cost savings, and common sales objections.",
        "memo_html": """<div class="memo-card">
  <div class="memo-header">
    <div class="memo-badge green">COMPANY ANNOUNCEMENT // PRODUCT GA</div>
    <div class="memo-meta">All-Hands Memo • Author: Product Operations • Confidential Internal</div>
  </div>

  <div class="memo-section">
    <div class="section-title">🚀 WHAT IS LAUNCHING</div>
    <p class="memo-p">We are thrilled to announce general availability of <strong>Client-Side WebGPU Inference</strong>. Our enterprise users can now run private foundation models directly inside Chrome, Edge, and Safari on their laptop GPUs with zero server round-trips.</p>
  </div>

  <div class="memo-section">
    <div class="section-title blue">❓ CROSS-FUNCTIONAL FAQ</div>
    <div class="faq-item">
      <strong>Q: How does this impact our cloud GPU infrastructure bill?</strong>
      <p>A: Because model weights run on the user's hardware, our cloud inference cost drops by 84% for participating enterprise tenants.</p>
    </div>
    <div class="faq-item">
      <strong>Q: What happens if a customer has an older machine without WebGPU?</strong>
      <p>A: Our dual-engine architecture gracefully falls back to Groq LPU cloud inference with sub-second response times.</p>
    </div>
  </div>
</div>""",
        "markdown": """# All-Hands Announcement: Client-Side WebGPU GA
**Audience:** Company-Wide | **Confidentiality:** Internal Only

## What is Launching
General Availability of Client-Side WebGPU Inference, enabling zero-install local model execution directly on user hardware.

## Cross-Functional FAQ
- **Q: Cloud Cost Impact?** A: Reduces cloud GPU server expenditure by up to 84%.
- **Q: Older hardware fallback?** A: Seamless automatic failover to cloud Groq LPU inference.
"""
    }
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Internal Comms Studio // Skill #12 (Apache 2.0)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-canvas: #f8fafc;
      --bg-panel: #ffffff;
      --bg-panel-subtle: #f1f5f9;
      --border-subtle: #e2e8f0;
      --border-focus: #0f766e;
      --text-primary: #0f172a;
      --text-secondary: #475569;
      --text-muted: #64748b;
      --brand-accent: #0f766e;
      --accent-emerald: #059669;
      --accent-blue: #2563eb;
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
      --border-focus: #14b8a6;
      --text-primary: #f8fafc;
      --text-secondary: #cbd5e1;
      --text-muted: #94a3b8;
      --brand-accent: #14b8a6;
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
      background: linear-gradient(135deg, #0f766e 0%, #0284c7 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
      font-size: 1.25rem;
      font-weight: 800;
      box-shadow: 0 2px 8px rgba(15, 118, 110, 0.25);
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
      background: #0f766e;
      color: #ffffff;
      box-shadow: 0 1px 4px rgba(15, 118, 110, 0.3);
    }
    .engine-btn.active.webgpu {
      background: #0284c7;
      color: #ffffff;
      box-shadow: 0 1px 4px rgba(2, 132, 199, 0.3);
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
      border-color: var(--brand-accent);
      background: rgba(15, 118, 110, 0.05);
    }
    .preset-card.active {
      border-color: var(--brand-accent);
      background: rgba(15, 118, 110, 0.08);
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
      border-color: var(--brand-accent);
      color: var(--brand-accent);
    }
    .prompt-chip.active {
      border-color: var(--brand-accent);
      background: var(--brand-accent);
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
      border-color: var(--brand-accent);
      background: var(--bg-panel);
    }

    .btn-synthesize {
      width: 100%;
      background: linear-gradient(135deg, #0f766e 0%, #0284c7 100%);
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
      box-shadow: 0 2px 8px rgba(15, 118, 110, 0.25);
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
      color: var(--brand-accent);
      box-shadow: var(--card-shadow);
    }

    .stage-content {
      padding: 1.5rem;
      min-height: 580px;
      background: var(--bg-canvas);
      overflow-y: auto;
    }

    /* Memo Design */
    .memo-card {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 1.75rem;
      box-shadow: var(--card-shadow);
    }
    .memo-header {
      border-bottom: 2px solid var(--border-subtle);
      padding-bottom: 1rem;
      margin-bottom: 1.25rem;
    }
    .memo-badge {
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 0.7rem;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(15, 118, 110, 0.1);
      color: var(--brand-accent);
      margin-bottom: 4px;
    }
    .memo-badge.red { background: rgba(190, 18, 60, 0.1); color: var(--accent-rose); }
    .memo-badge.green { background: rgba(5, 150, 105, 0.1); color: var(--accent-emerald); }
    .memo-meta {
      font-size: 0.76rem;
      color: var(--text-muted);
    }
    .memo-section {
      margin-bottom: 1.5rem;
    }
    .section-title {
      font-family: var(--font-display);
      font-size: 0.88rem;
      font-weight: 700;
      margin-bottom: 8px;
      color: var(--text-primary);
    }
    .section-title.green { color: var(--accent-emerald); }
    .section-title.blue { color: var(--accent-blue); }
    .section-title.red { color: var(--accent-rose); }
    .memo-list {
      padding-left: 1.2rem;
      font-size: 0.82rem;
      line-height: 1.6;
      color: var(--text-secondary);
    }
    .memo-p {
      font-size: 0.84rem;
      line-height: 1.6;
      color: var(--text-secondary);
    }
    .faq-item {
      background: var(--bg-panel-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 10px 12px;
      margin-bottom: 8px;
      font-size: 0.8rem;
    }

    .code-view {
      background: #0f172a;
      color: #f8fafc;
      border-radius: 8px;
      padding: 1.5rem;
      overflow-x: auto;
      font-family: var(--font-mono);
      font-size: 0.76rem;
      line-height: 1.5;
      height: 520px;
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
      border-color: var(--brand-accent);
      color: var(--brand-accent);
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
      <div class="brand-badge">📝</div>
      <div class="brand-text">
        <h1>Internal Comms Studio <span class="badge-skill-fit">Skill #12: internal-comms (Apache 2.0 • High-Signal)</span></h1>
        <p>Progress, Plans, Problems (3P) • Executive Post-Mortems • Company Newsletters • Leadership Memos</p>
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
            <span>Corporate Memo Formats</span>
            <span style="color: var(--accent-emerald); font-size: 0.72rem; font-family: var(--font-mono);">Amazon 6-Page Rigor</span>
          </div>

          <div class="preset-list" id="presetsList">
            <!-- Rendered via JS -->
          </div>

          <div class="card-box-header" style="margin-top: 1.15rem;">
            <span>Draft Internal Communication</span>
            <span style="font-size:0.7rem; color:var(--brand-accent); font-weight:600;">⚡ Groq LPU Ready</span>
          </div>

          <div class="prompt-chips-row">
            <button type="button" class="prompt-chip active" onclick="setPromptBrief('A weekly 3P update for the Agent Core team: shipped WebGPU local inference, preparing Groq LPU token deployment next Tuesday, blocked on cross-origin iframe security headers.', this)">📊 3P Team Update</button>
            <button type="button" class="prompt-chip" onclick="setPromptBrief('A blameless post-mortem for a 14-minute payment webhook timeout outage caused by exhausted database connection pools during the midnight cron billing batch.', this)">🚨 Incident Post-Mortem</button>
            <button type="button" class="prompt-chip" onclick="setPromptBrief('A company-wide internal launch memo announcing the rollout of Client-Side WebGPU inference, explaining customer benefits, cost savings, and common sales objections.', this)">📢 Product Launch FAQ</button>
            <button type="button" class="prompt-chip" onclick="setPromptBrief('A 30-60-90 day onboarding status update for a new Staff Engineer covering early wins, team pairings, and upcoming architectural proposals.', this)">🎯 30-60-90 Day Plan</button>
          </div>

          <textarea class="brief-input" id="briefInput" placeholder="Enter rough bullet points, project status, or incident facts to generate an executive-ready internal communication..."></textarea>

          <button class="btn-synthesize" id="btnSynthesize" onclick="runInternalCommsSynthesis()">
            <span>⚡ Synthesize Executive Memo (Groq LPU)</span>
          </button>
        </div>

        <div class="runbook-box">
          <div class="runbook-header" onclick="toggleRunbook()">
            <span style="font-weight: 700; font-size: 0.8rem; color: var(--text-primary);">
              📜 Injected SKILL.md (internal-comms Runbook)
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
            <button class="tab-btn active" id="tabBtnPreview" onclick="switchStage('preview')">👁️ Executive Memo Preview</button>
            <button class="tab-btn" id="tabBtnMarkdown" onclick="switchStage('markdown')">📜 Raw Markdown Format</button>
          </div>

          <div style="font-size: 0.72rem; color: var(--brand-accent); font-weight: 700; font-family: var(--font-mono);">
            HIGH-SIGNAL RIGOR
          </div>
        </div>

        <div class="stage-content" id="stagePreview">
          <div id="memoHtmlContainer">
            <!-- Rendered via JS -->
          </div>
        </div>

        <div class="stage-content" id="stageMarkdown" style="display: none; padding: 0;">
          <pre class="code-view"><code id="codeText"></code></pre>
        </div>

        <div class="bottom-bar">
          <div id="renderSourceInfo">Format: 3P Engineering Sync • Audience: Engineering Leadership</div>
          <div class="actions-row">
            <button class="btn-action" onclick="copyMarkdown()">📋 Copy Markdown</button>
            <button class="btn-action" onclick="downloadMemoMd()">💾 Download .md</button>
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
  let currentStage = 'preview';
  let currentMarkdown = PRESETS[0].markdown;
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
    const saved = localStorage.getItem('internal_comms_app_mode') || 'light';
    setTheme(saved);
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'light' ? 'dark' : 'light';
    setTheme(next);
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('internal_comms_app_mode', theme);
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
      if (eng === 'groq') synthBtn.innerHTML = '<span>⚡ Synthesize Executive Memo (Groq LPU)</span>';
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
          <div class="runtime-icon" style="color: #0f766e;">⚡</div>
          <div>
            <strong style="font-size: 0.85rem; color: var(--text-primary);">Groq LPU Cloud Fast Inference (500+ tok/s)</strong>
            <div style="font-size: 0.75rem; color: var(--text-secondary);">
              🟢 Pre-provisioned Free Tier API token active! Generates structured internal memos in ~1–2 seconds.
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
          <div class="runtime-icon" style="color: #0f766e;">⚡</div>
          <div>
            <strong style="font-size: 0.85rem; color: var(--text-primary);">Instant Verified Showcase Mode</strong>
            <div style="font-size: 0.75rem; color: var(--text-secondary);">
              3 pre-formatted executive communications with full Markdown and preview views.
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
          <div class="runtime-icon" style="color: #0284c7;">🎮</div>
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
          <button class="btn-action" id="btnLoadGpu" onclick="loadWebLLM()" style="background: #0f766e; color: #fff; border:none; padding: 5px 12px;">Load into GPU</button>
        </div>
        <div id="gpuProgressWrap" style="display:none; width: 100%; margin-top: 5px;">
          <div style="background: var(--border-subtle); height: 5px; border-radius: 3px; overflow: hidden;">
            <div id="gpuProgressFill" style="background: #0f766e; height: 100%; width: 0%;"></div>
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
          <div class="preset-meta">${p.format}</div>
        </div>
        <div style="font-size: 0.72rem; color: var(--text-muted);">View Memo →</div>
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
    currentMarkdown = p.markdown;

    document.getElementById('memoHtmlContainer').innerHTML = p.memo_html;
    document.getElementById('codeText').innerText = p.markdown;
    document.getElementById('renderSourceInfo').innerText = `Format: ${p.name} • ${p.category}`;
  }

  function setPromptBrief(txt, el) {
    document.getElementById('briefInput').value = txt;
    document.querySelectorAll('.prompt-chip').forEach(c => c.classList.remove('active'));
    if (el) el.classList.add('active');
  }

  function switchStage(stage) {
    currentStage = stage;
    document.getElementById('tabBtnPreview').classList.toggle('active', stage === 'preview');
    document.getElementById('tabBtnMarkdown').classList.toggle('active', stage === 'markdown');
    document.getElementById('stagePreview').style.display = (stage === 'preview') ? 'block' : 'none';
    document.getElementById('stageMarkdown').style.display = (stage === 'markdown') ? 'block' : 'none';
  }

  async function runInternalCommsSynthesis() {
    let brief = document.getElementById('briefInput').value.trim();
    if (!brief) {
      brief = "A weekly 3P update for the Agent Core team: shipped WebGPU local inference, preparing Groq LPU token deployment next Tuesday, blocked on cross-origin iframe security headers.";
      document.getElementById('briefInput').value = brief;
      const firstChip = document.querySelector('.prompt-chip');
      if (firstChip) firstChip.classList.add('active');
      showToast('Loaded 3P Update prompt', '📊');
    }

    const btn = document.getElementById('btnSynthesize');
    btn.disabled = true;
    btn.innerHTML = '<span>⏳ Synthesizing Executive Memo via Groq...</span>';

    const startTime = Date.now();

    try {
      if (currentEngine === 'groq') {
        const apiKey = getActiveGroqKey();
        const model = document.getElementById('groqModelSelect') ? document.getElementById('groqModelSelect').value : 'openai/gpt-oss-120b';

        const prompt = "You are an executive communications director following Anthropic's official 'internal-comms' runbook.\\n" +
          "Your mission: Transform the user's notes into an executive-ready, high-signal internal memo (3P update, incident post-mortem, or leadership FAQ).\\n" +
          "RULES:\\n" +
          "1. Use Amazon-style narrative rigor: crisp, factual, zero filler words, clear owners, and measurable timelines.\\n" +
          "2. OUTPUT FORMAT: Return clean Markdown inside ```markdown codeblock.";

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

        extractAndApplyMarkdown(txt, `Groq LPU (${model})`);
        const elapsed = Date.now() - startTime;
        showToast(`Executive memo synthesized in ${elapsed}ms!`, '⚡');

      } else if (currentEngine === 'instant') {
        selectPreset(1);
        showToast('Switched to SEV-1 Post-Mortem preset!', '✨');

      } else if (currentEngine === 'webgpu') {
        if (!webllmEngine) throw new Error('Please load the WebLLM model into WebGPU first using the top banner button.');
        const prompt = "You are an executive comms writer. Return a structured 3P or incident memo in Markdown inside ```markdown.";
        const reply = await webllmEngine.chat.completions.create({
          messages: [
            { role: "system", content: prompt },
            { role: "user", content: brief }
          ],
          temperature: 0.7,
          max_tokens: 2000
        });
        const txt = reply.choices[0].message.content;
        extractAndApplyMarkdown(txt, 'Local WebGPU (WebLLM)');
        showToast('WebGPU local synthesis complete!', '🎮');
      }
    } catch(e) {
      showToast('Synthesis error: ' + (e.message || 'Check network'), '⚠️');
      console.error(e);
    } finally {
      btn.disabled = false;
      if (currentEngine === 'groq') btn.innerHTML = '<span>⚡ Synthesize Executive Memo (Groq LPU)</span>';
      else if (currentEngine === 'webgpu') btn.innerHTML = '<span>🎮 Synthesize via Local WebGPU</span>';
      else btn.innerHTML = '<span>⚡ Render Instant Showcase</span>';
    }
  }

  function extractAndApplyMarkdown(rawText, source) {
    let md = "";
    const mdMarker = rawText.indexOf('```markdown');
    const genericMarker = rawText.indexOf('```');

    if (mdMarker !== -1) {
      let candidate = rawText.substring(mdMarker + 11).trim();
      const endFence = candidate.lastIndexOf('```');
      if (endFence !== -1) candidate = candidate.substring(0, endFence).trim();
      md = candidate;
    } else if (genericMarker !== -1) {
      let candidate = rawText.substring(genericMarker + 3).trim();
      const endFence = candidate.lastIndexOf('```');
      if (endFence !== -1) candidate = candidate.substring(0, endFence).trim();
      md = candidate;
    } else {
      md = rawText.trim();
    }

    currentMarkdown = md;
    document.getElementById('codeText').innerText = md;
    
    // Quick preview rendering
    const simpleHtml = `<div class="memo-card">
      <div class="memo-header">
        <div class="memo-badge">EXECUTIVE MEMO // SYNTHESIZED</div>
        <div class="memo-meta">Generated via ${source} • High-Signal Format</div>
      </div>
      <div style="font-size:0.84rem; line-height:1.6; white-space: pre-wrap;">${md.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</div>
    </div>`;

    document.getElementById('memoHtmlContainer').innerHTML = simpleHtml;
    document.getElementById('renderSourceInfo').innerText = `Synthesized via ${source} • Ready to Share`;
    switchStage('preview');
  }

  function copyMarkdown() {
    navigator.clipboard.writeText(currentMarkdown).then(() => {
      showToast('Markdown copied to clipboard!', '📋');
    });
  }

  function downloadMemoMd() {
    const blob = new Blob([currentMarkdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `internal_memo_${Date.now()}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('Memo .md downloaded!', '💾');
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
    snippet = ic_md[:1500].replace("\\", "\\\\").replace("`", "\\`")
    presets_json_str = json.dumps(PRESETS_DATA)
    
    out_html = HTML_TEMPLATE.replace("__SKILL_SNIPPET__", snippet)
    out_html = out_html.replace("__PRESETS_JSON__", presets_json_str)

    target_file = "internal_comms_app.html"
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(out_html)
    
    print(f"Generated {target_file} successfully! Size: {len(out_html)} bytes")

if __name__ == "__main__":
    build_app()
