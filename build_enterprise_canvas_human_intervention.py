# -*- coding: utf-8 -*-
"""
build_enterprise_canvas_human_intervention.py
Generates 'enterprise_ai_factory_canvas_human_intervention.html':
The 3-Tier Enterprise AI Factory Canvas (Worker Mind, Organization, Company — without Inter-company value chain)
upgraded with the full Human Intervention UI:
- L3 Company -> L2 Organization -> L1 Worker Mind
- Run Modes (Auto / Supervised / Step)
- Live State Badge (Running, Waiting for you, Paused, Stopped)
- Soft Pause, Emergency Stop, Per-Stage Pause
- Action Event store with append-only ledger
- Approvals Inbox with Decision Cards (Headline, Why, 4-cell impact grid, risk/confidence, undo window, Ask Why AI reasoning)
- Canvas Human Gate node with Approved / Rejected ports and pulsing waiting state
- Autonomy Policy matrix (A / N / C / H) & global guardrails (spend, SLA, confidence)
- Undo Ledger with reverse actions, undo windows, and state rollbacks
- Live Stream filter chips (All, Needs Me, Acted, Alerts, Undone)
- Executive Digest & AI Brief generator
- Trust Ramp (Promotion after 3 approvals, Demotion on reject/undo)
- Light Mode by default matching spec Page 17
- JSON & CSV audit log export
"""

import sys

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_FILE = "enterprise_ai_factory_canvas_human_intervention.html"

# We will read the base enterprise_ai_factory_canvas.html and inject the comprehensive HUI components
def build():
    with open("enterprise_ai_factory_canvas.html", "r", encoding="utf-8") as f:
        html = f.read()

    print(f"Read base file ({len(html)} chars). Injecting Human Intervention UI...")

    # 1. Update Title
    html = html.replace(
        "<title>Enterprise AI Factory: Company ➔ All 6 Organizations ➔ Worker Mind</title>",
        "<title>Enterprise AI Factory: Human Intervention & Autonomous Control Canvas</title>"
    )

    # 2. Add HUI CSS & Light Mode styling
    hui_css = """
    /* =========================================================================
       HUMAN INTERVENTION UI (HUI) ENHANCED STYLING (LIGHT MODE DEFAULT)
       ========================================================================= */
    body.light-mode {
      --bg-primary: #f8fafc;
      --bg-secondary: #ffffff;
      --bg-card: #f1f5f9;
      --bg-card-hover: #e2e8f0;
      --border-color: #cbd5e1;
      --border-light: #94a3b8;
      --text-main: #0f172a;
      --text-muted: #334155;
      --text-dim: #64748b;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
      --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
      --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.12);
    }

    body.light-mode .canvas-container {
      background-color: #f8fafc;
      background-image: radial-gradient(circle at 1px 1px, rgba(15, 23, 42, 0.14) 1px, transparent 0);
    }

    body.light-mode .connection-line {
      stroke: #94a3b8;
    }

    body.light-mode .canvas-node {
      background: #ffffff;
      border-color: #cbd5e1;
      box-shadow: 0 4px 8px -1px rgba(0,0,0,0.08);
    }

    body.light-mode .canvas-node:hover {
      border-color: var(--accent-blue);
      box-shadow: 0 0 14px rgba(37, 99, 235, 0.25);
    }

    body.light-mode .canvas-node.human-gate {
      background: linear-gradient(180deg, #fffbeb, #ffffff);
      border-color: #d97706;
    }

    body.light-mode .node-bar {
      background: #f1f5f9;
      border-bottom-color: #e2e8f0;
    }

    body.light-mode .node-metrics-box {
      background: #f1f5f9;
      border: 1px solid #e2e8f0;
      color: #0f172a;
    }

    body.light-mode .node-foot {
      background: #f8fafc;
      border-top-color: #e2e8f0;
    }

    body.light-mode .part-box {
      background: #ffffff;
      border-color: #cbd5e1;
    }

    body.light-mode .decision-card {
      background: #ffffff;
      border-color: #cbd5e1;
      box-shadow: 0 4px 10px -2px rgba(0,0,0,0.08);
    }

    body.light-mode .decision-impact-grid {
      background: #f8fafc;
      border-color: #e2e8f0;
    }

    body.light-mode .decision-risk-box {
      background: #fffbeb;
      color: #92400e;
      border-left-color: #d97706;
    }

    body.light-mode .undo-card {
      background: #ffffff;
      border-color: #cbd5e1;
    }

    body.light-mode .canvas-hud-bar {
      background: #ffffff;
      border-color: #cbd5e1;
      box-shadow: 0 10px 20px -3px rgba(0,0,0,0.12);
    }

    body.light-mode .hud-action-btn {
      background: #f8fafc;
      border-color: #cbd5e1;
      color: #0f172a;
    }

    body.light-mode .stream-console {
      background: #ffffff;
      border-color: #cbd5e1;
      color: #0f172a;
    }

    body.light-mode .policy-table th {
      background: #f1f5f9;
      color: #475569;
      border-bottom-color: #cbd5e1;
    }

    body.light-mode .policy-table td {
      border-bottom-color: #f1f5f9;
    }

    body.light-mode .policy-pill-btn {
      background: #f8fafc;
      border-color: #cbd5e1;
      color: #64748b;
    }

    body.light-mode .guard-row {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
    }

    body.light-mode .guard-input {
      background: #ffffff;
      border-color: #cbd5e1;
      color: #0f172a;
    }

    body.light-mode .modal-box {
      background: #ffffff;
      border-color: #cbd5e1;
    }

    body.light-mode .modal-bar {
      background: #f8fafc;
      border-bottom-color: #e2e8f0;
    }

    body.light-mode .rejection-drawer {
      background: #fff1f2;
      border-color: #f43f5e;
    }

    body.light-mode .rejection-chip {
      background: #ffffff;
      border-color: #fecdd3;
      color: #9f1239;
    }

    body.light-mode .run-mode-btn.active {
      background: #ffffff;
      box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }

    body.light-mode .tab-btn.active {
      background: #ffffff;
      box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }

    /* Run Mode Switch (HUI-01) */
    .run-mode-group {
      display: flex;
      align-items: center;
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 2px;
      gap: 2px;
    }

    .run-mode-btn {
      padding: 4px 8px;
      font-size: 0.68rem;
      font-weight: 600;
      border-radius: var(--radius-sm);
      border: none;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 3px;
    }

    .run-mode-btn.active {
      background: var(--bg-card);
      color: var(--accent-blue);
      border: 1px solid var(--accent-blue);
      box-shadow: 0 1px 4px rgba(56, 189, 248, 0.3);
    }
    .run-mode-btn.supervised.active {
      color: var(--accent-amber);
      border-color: var(--accent-amber);
      box-shadow: 0 1px 4px rgba(245, 158, 11, 0.3);
    }
    .run-mode-btn.step.active {
      color: var(--accent-purple);
      border-color: var(--accent-purple);
      box-shadow: 0 1px 4px rgba(168, 85, 247, 0.3);
    }

    /* System State Badge (HUI-02) */
    .state-badge {
      display: flex;
      align-items: center;
      gap: 5px;
      padding: 3px 8px;
      border-radius: 14px;
      font-size: 0.68rem;
      font-family: var(--font-mono);
      font-weight: 700;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid var(--accent-emerald);
      color: var(--accent-emerald);
      white-space: nowrap;
    }
    .state-badge.waiting {
      background: rgba(245, 158, 11, 0.15);
      border-color: var(--accent-amber);
      color: var(--accent-amber);
      animation: waitingPillGlow 1.2s infinite alternate;
    }
    .state-badge.paused {
      background: rgba(245, 158, 11, 0.12);
      border-color: var(--accent-amber);
      color: var(--accent-amber);
    }
    .state-badge.stopped {
      background: rgba(244, 63, 94, 0.15);
      border-color: var(--accent-rose);
      color: var(--accent-rose);
    }

    @keyframes waitingPillGlow {
      from { box-shadow: 0 0 4px rgba(245, 158, 11, 0.2); }
      to { box-shadow: 0 0 12px rgba(245, 158, 11, 0.6); }
    }

    .btn-header-ctrl {
      height: 30px;
      padding: 0 8px;
      font-size: 0.70rem;
      font-weight: 600;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-color);
      background: var(--bg-card);
      color: var(--text-main);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      white-space: nowrap;
      transition: all 0.15s ease;
    }
    .btn-header-ctrl:hover {
      background: var(--bg-card-hover);
      border-color: var(--accent-blue);
    }
    .btn-header-ctrl.btn-pause { border-color: var(--accent-amber); color: var(--accent-amber); }
    .btn-header-ctrl.btn-stop { border-color: var(--accent-rose); color: var(--accent-rose); }
    .btn-header-ctrl.btn-stop:hover { background: rgba(244, 63, 94, 0.2); }

    .badge-counter {
      background: var(--accent-rose);
      color: #ffffff;
      font-size: 0.60rem;
      padding: 1px 5px;
      border-radius: 8px;
      font-weight: 700;
      font-family: var(--font-mono);
    }

    /* Alert Interrupt Banner (HUI-70, HUI-71) */
    .alert-interrupt-banner {
      display: none;
      background: linear-gradient(90deg, #881337, #991b1b);
      border-bottom: 1px solid #f43f5e;
      color: #ffffff;
      padding: 6px 14px;
      font-size: 0.74rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      z-index: 55;
      flex-shrink: 0;
      animation: slideDown 0.25s ease;
    }
    @keyframes slideDown {
      from { transform: translateY(-100%); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }

    .alert-content-wrap { display: flex; align-items: center; gap: 8px; }
    .alert-actions-wrap { display: flex; align-items: center; gap: 6px; }
    .btn-alert-action {
      background: rgba(255, 255, 255, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.4);
      color: #ffffff;
      font-size: 0.68rem;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 4px;
      cursor: pointer;
    }
    .btn-alert-action:hover { background: rgba(255, 255, 255, 0.35); }

    /* Human Gate Node (HUI-30 to HUI-34) */
    .canvas-node.human-gate {
      width: 220px;
      border: 2px dashed var(--accent-amber);
      background: linear-gradient(180deg, rgba(245, 158, 11, 0.12), rgba(15, 23, 42, 0.95));
    }
    .canvas-node.human-gate .node-bar {
      background: rgba(245, 158, 11, 0.2);
      border-bottom: 1px solid var(--accent-amber);
    }
    .canvas-node.waiting-approval {
      border-color: var(--accent-amber) !important;
      box-shadow: 0 0 22px rgba(245, 158, 11, 0.7) !important;
      animation: waitingGlow 1.1s infinite alternate;
    }
    @keyframes waitingGlow {
      from { border-color: var(--accent-amber); box-shadow: 0 0 10px rgba(245, 158, 11, 0.4); }
      to { border-color: #fde047; box-shadow: 0 0 24px rgba(245, 158, 11, 0.85); }
    }

    .pod-gate { background: rgba(245, 158, 11, 0.25); color: #fde68a; border: 1px solid var(--accent-amber); }
    .tier-gate { background: rgba(245, 158, 11, 0.2); color: #fde68a; border: 1px solid #f59e0b; }

    .node-autonomy-badge {
      font-size: 0.60rem;
      font-family: var(--font-mono);
      font-weight: 800;
      padding: 1px 4px;
      border-radius: 3px;
    }
    .badge-level-A { background: rgba(16, 185, 129, 0.2); color: #a7f3d0; border: 1px solid #10b981; }
    .badge-level-N { background: rgba(56, 189, 248, 0.2); color: #7dd3fc; border: 1px solid #38bdf8; }
    .badge-level-C { background: rgba(245, 158, 11, 0.2); color: #fde68a; border: 1px solid #f59e0b; }
    .badge-level-H { background: rgba(244, 63, 94, 0.2); color: #fda4af; border: 1px solid #f43f5e; }

    /* Right Sidebar: Tabs & Panels */
    .right-tab-bar {
      display: flex;
      background: var(--bg-primary);
      border-bottom: 1px solid var(--border-color);
      overflow-x: auto;
      scrollbar-width: none;
    }
    .right-tab-bar::-webkit-scrollbar { display: none; }

    .right-tab-item {
      padding: 8px 9px;
      font-size: 0.68rem;
      font-weight: 700;
      border: none;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 3px;
      white-space: nowrap;
      border-bottom: 2px solid transparent;
      transition: all 0.15s ease;
    }
    .right-tab-item.active {
      color: var(--accent-blue);
      border-bottom-color: var(--accent-blue);
      background: var(--bg-secondary);
    }

    .panel-view-container {
      flex: 1;
      overflow-y: auto;
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    /* Decision Card (HUI-20 to HUI-25) */
    .decision-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-left: 4px solid var(--accent-amber);
      border-radius: var(--radius-md);
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      box-shadow: var(--shadow-md);
      animation: cardEnter 0.25s ease;
    }
    .decision-card.level-H { border-left-color: var(--accent-rose); }

    @keyframes cardEnter {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .decision-header-row {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 6px;
    }
    .decision-title { font-size: 0.78rem; font-weight: 700; color: var(--text-main); line-height: 1.3; }
    .decision-stage-tag {
      font-family: var(--font-mono);
      font-size: 0.62rem;
      color: var(--accent-cyan);
      background: rgba(6, 182, 212, 0.15);
      padding: 1px 5px;
      border-radius: 4px;
      white-space: nowrap;
    }
    .decision-why-text { font-size: 0.70rem; color: var(--text-muted); line-height: 1.35; }

    .decision-impact-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 5px;
      background: var(--bg-primary);
      padding: 6px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-color);
    }
    .impact-cell { display: flex; flex-direction: column; gap: 1px; }
    .impact-cell-label { font-size: 0.60rem; color: var(--text-dim); text-transform: uppercase; font-weight: 600; }
    .impact-cell-value { font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700; color: var(--text-main); }
    .decision-risk-box {
      font-size: 0.66rem;
      color: #fed7aa;
      background: rgba(245, 158, 11, 0.12);
      border-left: 2px solid var(--accent-amber);
      padding: 4px 6px;
      border-radius: 0 4px 4px 0;
      line-height: 1.3;
    }
    .decision-undo-tag { font-size: 0.64rem; color: var(--text-dim); display: flex; align-items: center; gap: 4px; }

    .decision-btn-row { display: flex; gap: 6px; margin-top: 2px; }
    .btn-decision {
      flex: 1;
      padding: 6px 8px;
      font-size: 0.70rem;
      font-weight: 700;
      border-radius: var(--radius-sm);
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      transition: all 0.15s ease;
    }
    .btn-decision.approve { background: var(--accent-emerald); color: #ffffff; }
    .btn-decision.approve:hover { background: #059669; }
    .btn-decision.ask-why { background: var(--bg-primary); border: 1px solid var(--accent-cyan); color: var(--accent-cyan); }
    .btn-decision.ask-why:hover { background: rgba(6, 182, 212, 0.15); }
    .btn-decision.reject { background: rgba(244, 63, 94, 0.15); border: 1px solid var(--accent-rose); color: #fda4af; }
    .btn-decision.reject:hover { background: rgba(244, 63, 94, 0.3); }

    .rejection-drawer {
      display: none;
      background: var(--bg-primary);
      border: 1px solid var(--accent-rose);
      border-radius: var(--radius-sm);
      padding: 6px;
      flex-direction: column;
      gap: 4px;
    }
    .rejection-chips-row { display: flex; flex-wrap: wrap; gap: 4px; }
    .rejection-chip {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      font-size: 0.64rem;
      padding: 2px 6px;
      border-radius: 4px;
      cursor: pointer;
    }
    .rejection-chip:hover { border-color: var(--accent-rose); color: #ffffff; }

    /* Undo Ledger (HUI-50 to HUI-54) */
    .undo-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 8px;
      display: flex;
      flex-direction: column;
      gap: 5px;
    }
    .undo-head-row { display: flex; justify-content: space-between; align-items: center; font-size: 0.70rem; font-weight: 600; }
    .undo-time { font-family: var(--font-mono); font-size: 0.64rem; color: var(--text-dim); }
    .btn-undo-action {
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid var(--accent-indigo);
      color: #a5b4fc;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 0.66rem;
      font-weight: 700;
      cursor: pointer;
    }
    .btn-undo-action:hover { background: rgba(99, 102, 241, 0.3); }

    /* Policy Table */
    .policy-table { width: 100%; border-collapse: collapse; font-size: 0.68rem; }
    .policy-table th { background: var(--bg-primary); color: var(--text-dim); padding: 5px; text-align: left; font-size: 0.62rem; border-bottom: 1px solid var(--border-color); }
    .policy-table td { padding: 5px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); vertical-align: middle; }
    .policy-selector-group { display: flex; gap: 2px; }
    .policy-pill-btn {
      width: 18px;
      height: 18px;
      border-radius: 3px;
      border: 1px solid var(--border-color);
      background: var(--bg-primary);
      color: var(--text-dim);
      font-size: 0.58rem;
      font-weight: 800;
      font-family: var(--font-mono);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }
    .policy-pill-btn.active.A { background: var(--accent-emerald); color: #000; border-color: var(--accent-emerald); }
    .policy-pill-btn.active.N { background: var(--accent-blue); color: #000; border-color: var(--accent-blue); }
    .policy-pill-btn.active.C { background: var(--accent-amber); color: #000; border-color: var(--accent-amber); }
    .policy-pill-btn.active.H { background: var(--accent-rose); color: #fff; border-color: var(--accent-rose); }

    .guard-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: var(--bg-primary);
      padding: 5px 8px;
      border-radius: var(--radius-sm);
      font-size: 0.68rem;
      margin-top: 4px;
    }
    .guard-input {
      width: 75px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      font-family: var(--font-mono);
      font-size: 0.68rem;
      padding: 2px 4px;
      border-radius: 3px;
      text-align: right;
    }

    /* Stream Filters */
    .stream-filters-bar { display: flex; gap: 3px; margin-bottom: 4px; overflow-x: auto; scrollbar-width: none; }
    .stream-filters-bar::-webkit-scrollbar { display: none; }
    .filter-chip {
      padding: 2px 6px;
      font-size: 0.62rem;
      font-weight: 600;
      border-radius: 10px;
      border: 1px solid var(--border-color);
      background: var(--bg-primary);
      color: var(--text-muted);
      cursor: pointer;
      white-space: nowrap;
    }
    .filter-chip.active { border-color: var(--accent-blue); color: var(--accent-blue); background: rgba(56, 189, 248, 0.15); }
    """

    # Inject HUI CSS right before </style>
    html = html.replace("</style>", hui_css + "\n  </style>")

    # 3. Set Light Mode Default on body tag
    html = html.replace("<body>", '<body class="light-mode">')

    # 4. Enhance Header with Run Mode, State Badge, Pause, Emergency Stop
    old_header_target = '<div class="header-right">'
    new_header_snippet = """
    <!-- Run Mode Switch (HUI-01) -->
    <div class="run-mode-group">
      <button class="run-mode-btn active" id="modeBtnAuto" onclick="setRunMode('auto')">
        <span>⚡</span> Auto
      </button>
      <button class="run-mode-btn supervised" id="modeBtnSupervised" onclick="setRunMode('supervised')">
        <span>🛡️</span> Supervised
      </button>
      <button class="run-mode-btn step" id="modeBtnStep" onclick="setRunMode('step')">
        <span>⏭</span> Step
      </button>
    </div>

    <!-- Live System State Badge (HUI-02) -->
    <div class="state-badge" id="systemStateBadge">
      <span id="stateDot">●</span> <span id="stateText">Running</span>
    </div>

    <div class="header-right">
      <button class="btn-header-ctrl btn-pause" id="btnPauseResume" onclick="togglePauseResume()">
        <span id="pauseIcon">⏸</span> <span id="pauseText">Pause</span>
      </button>
      <button class="btn-header-ctrl btn-stop" id="btnEmergStop" onclick="triggerEmergencyStop()">
        <span>🛑</span> Stop
      </button>
      <button class="btn-header-ctrl" id="btnResetCycle" onclick="promptResetCycle()">
        <span>🔄</span> Reset
      </button>
    """
    html = html.replace(old_header_target, new_header_snippet, 1)

    # 5. Insert Top Alert Interrupt Banner right below </header>
    alert_banner_html = """
  <!-- Alert Interrupt Banner (HUI-70, HUI-71) -->
  <div class="alert-interrupt-banner" id="alertInterruptBanner">
    <div class="alert-content-wrap">
      <span style="font-size: 1rem;">⚠️</span>
      <span id="alertBannerText">High Financial Exposure: -$1.6M forecast adjustment exceeds $500,000 guard limit.</span>
    </div>
    <div class="alert-actions-wrap">
      <button class="btn-alert-action" onclick="openRightTab('inbox')">Review Card</button>
      <button class="btn-alert-action" onclick="pauseCurrentStage()">Pause Stage</button>
      <button class="btn-alert-action" onclick="dismissAlert()">Dismiss</button>
    </div>
  </div>
    """
    html = html.replace("</header>", "</header>\n" + alert_banner_html, 1)

    # 6. Add Quick Triggers in Sub-navbar KPI bar
    kpi_bar_target = '<div class="kpi-bar">'
    html = html.replace(kpi_bar_target, kpi_bar_target + """
    <!-- Quick Right Drawer Triggers -->
    <div style="display: flex; gap: 4px; margin-left: auto;">
      <button class="tab-btn" onclick="openRightTab('inbox')">
        📬 Inbox <span class="badge-counter" id="inboxCountBadge">0</span>
      </button>
      <button class="tab-btn" onclick="openRightTab('undo')">
        ↩️ Undo (<span id="undoCountTop">0</span>)
      </button>
      <button class="tab-btn" onclick="openRightTab('digest')">
        📰 Digest
      </button>
      <button class="tab-btn" onclick="openRightTab('policy')">
        🛡️ Policy
      </button>
    </div>
    """, 1)

    # 7. Add Human Gate Node to Warehouse parts scroll
    warehouse_target = '<div class="sidebar-scroll" id="warehousePanel">'
    human_gate_part = """
        <!-- Human Gate Node (HUI-30) -->
        <div class="part-box gate-part" onclick="toggleHumanGateOnCanvas()">
          <div class="part-head">
            <span class="part-name">👤 Human Gate</span>
            <span class="part-tier-tag tier-gate">CONTROL</span>
          </div>
          <div class="part-description">
            Forces Level C approval checkpoint between enterprise nodes. 1 in, 2 out ports (Approved/Rejected).
          </div>
          <div style="font-size: 0.62rem; color: var(--accent-amber); font-weight: 700; margin-top: 2px;">
            <span id="gateToggleText">⚡ Toggle on Canvas</span>
          </div>
        </div>
    """
    html = html.replace(warehouse_target, warehouse_target + "\n" + human_gate_part, 1)

    # 8. Upgrade Right Sidebar with 5 Tabs: Inbox, Undo, Digest, Policy, Inspector
    old_aside_start = html.find('id="sidebarRight"')
    # Find the opening <aside
    aside_open_idx = html.rfind('<aside', 0, old_aside_start)
    aside_close_idx = html.find('</aside>', old_aside_start) + 8

    full_old_aside = html[aside_open_idx:aside_close_idx]

    new_right_drawer = """<aside class="sidebar-right" id="sidebarRight">
      <div class="right-tab-bar">
        <button class="right-tab-item active" id="tabInboxBtn" onclick="openRightTab('inbox')">
          📬 Inbox <span class="badge-counter" id="inboxTabBadge">0</span>
        </button>
        <button class="right-tab-item" id="tabUndoBtn" onclick="openRightTab('undo')">
          ↩️ Undo (<span id="undoCount">0</span>)
        </button>
        <button class="right-tab-item" id="tabDigestBtn" onclick="openRightTab('digest')">
          📰 Digest
        </button>
        <button class="right-tab-item" id="tabPolicyBtn" onclick="openRightTab('policy')">
          🛡️ Policy
        </button>
        <button class="right-tab-item" id="tabInspectorBtn" onclick="openRightTab('inspector')">
          🔍 Inspector
        </button>
      </div>

      <!-- TAB 1: APPROVALS INBOX (HUI-20 to HUI-27) -->
      <div class="panel-view-container" id="panelInbox">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-main);">Pending Approvals</span>
          <button class="btn-mind-open" onclick="batchApproveLowRisk()">⚡ Batch Low-Risk</button>
        </div>

        <div id="inboxCardsList" style="display: flex; flex-direction: column; gap: 8px;">
          <!-- Populated dynamically with Decision Cards -->
        </div>

        <div id="inboxEmptyState" style="text-align: center; padding: 25px 10px; color: var(--text-dim); font-size: 0.72rem;">
          <div style="font-size: 1.5rem; margin-bottom: 6px;">✨</div>
          <b>All Clear! No Pending Interruptions.</b><br>
          Autonomous enterprise agents operating within policy limits.
        </div>
      </div>

      <!-- TAB 2: UNDO LEDGER (HUI-50 to HUI-54) -->
      <div class="panel-view-container" id="panelUndo" style="display: none;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-main);">Executed Actions Ledger</span>
          <span style="font-size: 0.64rem; color: var(--text-dim); font-family: var(--font-mono);">Newest First</span>
        </div>

        <div id="undoLedgerList" style="display: flex; flex-direction: column; gap: 8px;">
          <!-- Populated dynamically with executed actions -->
        </div>
      </div>

      <!-- TAB 3: EXECUTIVE DIGEST (HUI-62 to HUI-63) -->
      <div class="panel-view-container" id="panelDigest" style="display: none;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-main);">Cycle Executive Digest</span>
          <button class="btn-mind-open" onclick="generateAiDigest()">⚡ AI Summary</button>
        </div>

        <div class="decision-card" style="border-left-color: var(--accent-blue);">
          <div style="font-size: 0.72rem; font-weight: 700; color: var(--accent-blue);">🚨 Items That Needed You</div>
          <div id="digestNeedsYou" style="font-size: 0.68rem; color: var(--text-muted);">
            1 approval card handled (Apex OEM Regional Allocation shift approved).
          </div>
        </div>

        <div class="decision-card" style="border-left-color: var(--accent-emerald);">
          <div style="font-size: 0.72rem; font-weight: 700; color: var(--accent-emerald);">⚙️ Ran Silently in Background (Ambient)</div>
          <div id="digestRanSilently" style="font-size: 0.68rem; color: var(--text-muted); line-height: 1.35;">
            • CO-01 SilicoFab: Dispatched 24-week lot manifest ($48.2M)<br>
            • CO-02 MicroPCB: Verified HDI substrate PPM defect &lt; 12<br>
            • CRM-02: Optimized CPQ pricing matrix (38% margin floor)<br>
            • WMS-03: Scheduled regional DC wave pick allocation
          </div>
        </div>

        <div class="decision-card" style="border-left-color: var(--accent-amber);">
          <div style="font-size: 0.72rem; font-weight: 700; color: var(--accent-amber);">⚡ Surprises & Near-Miss Anomalies</div>
          <div id="digestSurprises" style="font-size: 0.68rem; color: var(--text-muted); line-height: 1.35;">
            • MES Shop Floor: Line 3 AOI optical yield near warning threshold (94.2%).<br>
            • Lead Time Surge: Transpacific container freight +4 days.
          </div>
        </div>
      </div>

      <!-- TAB 4: AUTONOMY POLICY (HUI-40 to HUI-43) -->
      <div class="panel-view-container" id="panelPolicy" style="display: none;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-main);">Autonomy Matrix (A / N / C / H)</span>
          <div style="display: flex; gap: 4px;">
            <button class="btn-mind-open" onclick="exportAuditJson()">JSON</button>
            <button class="btn-mind-open" onclick="exportAuditCsv()">CSV</button>
          </div>
        </div>

        <div style="font-size: 0.64rem; color: var(--text-dim); line-height: 1.3;">
          Click pills to reassign autonomy: <b>A</b> (Ambient), <b>N</b> (Notify), <b>C</b> (Confirm), <b>H</b> (Human-only).
        </div>

        <div style="background: var(--bg-card); border-radius: var(--radius-sm); border: 1px solid var(--border-color); overflow: hidden;">
          <table class="policy-table">
            <thead>
              <tr>
                <th>Node</th>
                <th>Domain Action</th>
                <th>Level</th>
              </tr>
            </thead>
            <tbody id="policyTableBody">
              <!-- Rendered dynamically -->
            </tbody>
          </table>
        </div>

        <div style="font-size: 0.68rem; font-weight: 700; color: var(--text-main); margin-top: 4px;">Global Guard Thresholds</div>
        <div class="guard-row">
          <span>💰 Max Spend for Ambient (C above):</span>
          <input type="text" class="guard-input" id="guardSpendLimit" value="$500,000" onchange="updateGuardSpend(this.value)">
        </div>
        <div class="guard-row">
          <span>🎯 Minimum SLA Fill Guard:</span>
          <input type="text" class="guard-input" id="guardSlaMin" value="90.0%" onchange="updateGuardSla(this.value)">
        </div>
        <div class="guard-row">
          <span>🧠 Minimum Model Confidence:</span>
          <input type="text" class="guard-input" id="guardConfidenceMin" value="75%" onchange="updateGuardConf(this.value)">
        </div>
      </div>

      <!-- TAB 5: INSPECTOR (Specifications + Stream with Filter Chips) -->
      <div class="panel-view-container" id="panelInspector" style="display: none;">
        <div class="sidebar-header" style="padding: 4px 0; background: transparent; border-bottom: none;">
          <div style="font-size:0.76rem; font-weight:700;" id="inspectorHeaderTitle">
            🔍 Specifications
          </div>
          <button class="btn-header-ctrl" id="btnPauseStage" onclick="toggleStagePause(selectedNodeId)">
            <span>⏸</span> <span id="pauseStageText">Pause Node</span>
          </button>
        </div>

        <div class="inspector-card" id="inspectorBodyCard">
          <!-- Populated dynamically -->
        </div>

        <button class="hud-action-btn accent" id="btnInspectDrill" style="margin-top:4px; justify-content:center;" onclick="drillDownFromInspector()">
          🔍 Drill Down Into Sub-System
        </button>

        <div style="font-size:0.70rem; font-weight:700; color:var(--accent-blue); margin-top:6px;">
          Live Execution Stream:
        </div>
        
        <div class="stream-filters-bar">
          <button class="filter-chip active" onclick="setStreamFilter('all', this)">All</button>
          <button class="filter-chip" onclick="setStreamFilter('needs_me', this)">Needs Me (C/H)</button>
          <button class="filter-chip" onclick="setStreamFilter('acted', this)">Acted (A/N)</button>
          <button class="filter-chip" onclick="setStreamFilter('alerts', this)">Alerts</button>
          <button class="filter-chip" onclick="setStreamFilter('undone', this)">Undone</button>
        </div>

        <div class="stream-console" id="streamLogBox"></div>
      </div>
    </aside>"""

    html = html.replace(full_old_aside, new_right_drawer, 1)

    # 10. Inject HUI JavaScript Engine right before </script></body>
    hui_js = """
    /* =========================================================================
       HUMAN INTERVENTION UI (HUI) STATE MACHINE & LOGIC
       ========================================================================= */
    let runMode = 'auto'; // 'auto', 'supervised', 'step'
    let systemState = 'running'; // 'running', 'waiting', 'paused', 'stopped'
    let isSoftPaused = false;
    let isEmergencyStopped = false;
    let hasHumanGateOnCanvas = true;
    let pausedStages = {};
    let activeStreamFilter = 'all';

    let globalGuards = {
      spendLimit: 500000,
      slaMin: 90.0,
      confidenceMin: 0.75
    };

    let consecutiveCleanApprovals = { "sop": 2, "crm": 3 };

    let pendingApprovals = [
      {
        id: "ev_ent_1082",
        time: new Date().toLocaleTimeString(),
        stage: "S&OP",
        stage_name: "Consensus Demand-Supply Balancing",
        agent: "Autonomous S&OP Engine",
        action: "rebalance_regional_allocation",
        why: "Surge in EMEA enterprise cloud orders exceeds regional buffer; reallocating 1,200 units from US hub protects Tier-1 SLA (96.8%) while maintaining gross margin floor.",
        impact: {
          money: -340000,
          units: 1200,
          kpi_delta: "SLA +4.2%, Margin Floor: 44.8%"
        },
        confidence: 0.91,
        reversible: true,
        level: "C",
        status: "awaiting"
      }
    ];

    let actionEventStore = [
      {
        id: "ev_ent_1080",
        time: new Date(Date.now() - 120000).toLocaleTimeString(),
        stage: "CRM",
        stage_name: "Lead Pipeline Ingestion",
        agent: "Lead Qualification Worker",
        action: "pipeline_lead_scoring",
        why: "Auto-qualified 48 tier-1 enterprise deals totaling $135M pipeline.",
        impact: { money: 135000000, units: 15400, kpi_delta: "Conversion +3.1%" },
        confidence: 0.96,
        reversible: true,
        level: "A",
        status: "executed"
      },
      ...pendingApprovals
    ];

    let undoLedger = [
      {
        id: "ev_ent_1080",
        time: new Date(Date.now() - 120000).toLocaleTimeString(),
        stage: "CRM",
        stage_name: "Lead Pipeline Ingestion",
        agent: "Lead Qualification Worker",
        action: "pipeline_lead_scoring",
        why: "Auto-qualified 48 tier-1 enterprise deals totaling $135M pipeline.",
        impact: { money: 135000000, units: 15400 },
        reversible: true,
        level: "A",
        status: "executed"
      }
    ];

    // Master Enterprise Autonomy Policy across 3 Tiers (Company -> Organizations -> Worker Roles)
    let enterpriseAutonomyPolicy = {
      "Company AOP":         { level: "C", action: "reconcile_enterprise_aop", reversible: true },
      "CRM & Commercial":    { level: "A", action: "pipeline_lead_scoring", reversible: true },
      "S&OP Planning":       { level: "C", action: "consensus_demand_supply_balancing", reversible: true },
      "ERP Core":            { level: "N", action: "mrp_explosion_po_release", reversible: false },
      "MES Shop Floor":      { level: "H", action: "smt_high_voltage_lot_dispatch", reversible: false },
      "WMS & Logistics":     { level: "A", action: "dynamic_wave_routing", reversible: true },
      "Finance & Treasury":  { level: "C", action: "three_way_invoice_clearing", reversible: false },
      "Demand Forecaster":   { level: "A", action: "bayesian_prior_update", reversible: true },
      "Capacity Planner":    { level: "C", action: "shift_overtime_allocation", reversible: true },
      "Master Scheduler":    { level: "N", action: "firm_planned_orders", reversible: false },
      "Quality Inspector":   { level: "H", action: "quarantine_lot_release", reversible: false }
    };

    function setRunMode(mode) {
      runMode = mode;
      document.getElementById("modeBtnAuto").classList.toggle("active", mode === 'auto');
      document.getElementById("modeBtnSupervised").classList.toggle("active", mode === 'supervised');
      document.getElementById("modeBtnStep").classList.toggle("active", mode === 'step');
      showToast(`Run Mode: ${mode.toUpperCase()}`);
      logEvent(`Run Mode set to: ${mode.toUpperCase()}`, "ok");
    }

    function togglePauseResume() {
      isSoftPaused = !isSoftPaused;
      const btn = document.getElementById("btnPauseResume");
      const icon = document.getElementById("pauseIcon");
      const text = document.getElementById("pauseText");

      if (isSoftPaused) {
        setSystemBadge("paused", "Paused");
        icon.textContent = "▶";
        text.textContent = "Resume";
        showToast("Execution Paused (Soft Hold)");
        logEvent("Execution paused by human supervisor.", "warn");
      } else {
        setSystemBadge("running", "Running");
        icon.textContent = "⏸";
        text.textContent = "Pause";
        showToast("Resuming Execution");
        logEvent("Execution resumed.", "ok");
      }
    }

    function triggerEmergencyStop() {
      if (!isEmergencyStopped) {
        if (confirm("🛑 EMERGENCY STOP: Halt all enterprise agents, hold state, and cancel queued dispatches?")) {
          isEmergencyStopped = true;
          isRunning = false;
          setSystemBadge("stopped", "Stopped");
          showToast("🛑 Emergency Stop Engaged");
          logEvent("EMERGENCY STOP ENGAGED across Enterprise Value Stream.", "warn");
          showAlertBanner("EMERGENCY STOP ENGAGED: Multi-agent execution halted by supervisor.");
        }
      } else {
        isEmergencyStopped = false;
        setSystemBadge("running", "Running");
        showToast("Emergency Stop Cleared");
        logEvent("Emergency Stop cleared.", "ok");
        dismissAlert();
      }
    }

    function promptResetCycle() {
      if (confirm("Reset Enterprise operating cycle and clear pending decision cards?")) {
        simIdx = 0;
        isRunning = false;
        pendingApprovals = [];
        updateInboxBadge();
        renderInboxCards();
        setSystemBadge("running", "Running");
        resetSimulationVisuals();
        showToast("Cycle Reset");
        logEvent("Enterprise cycle reset.", "ok");
      }
    }

    function setSystemBadge(type, label) {
      const badge = document.getElementById("systemStateBadge");
      const text = document.getElementById("stateText");
      const dot = document.getElementById("stateDot");

      badge.className = `state-badge ${type}`;
      text.textContent = label;
      dot.textContent = type === 'waiting' ? '⏳' : (type === 'paused' ? '⏸' : (type === 'stopped' ? '🛑' : '●'));
    }

    function showAlertBanner(msg) {
      const b = document.getElementById("alertInterruptBanner");
      document.getElementById("alertBannerText").textContent = msg;
      b.style.display = "flex";
    }

    function dismissAlert() {
      document.getElementById("alertInterruptBanner").style.display = "none";
    }

    function pauseCurrentStage() {
      toggleStagePause(selectedNodeId);
      dismissAlert();
    }

    function toggleStagePause(id) {
      pausedStages[id] = !pausedStages[id];
      const isPaused = pausedStages[id];
      showToast(isPaused ? `Node ${id} Paused` : `Node ${id} Resumed`);
      logEvent(`Node ${id} ${isPaused ? 'paused' : 'resumed'} by supervisor.`, isPaused ? "warn" : "ok");
    }

    function updateInboxBadge() {
      const cnt = pendingApprovals.length;
      document.getElementById("inboxCountBadge").textContent = cnt;
      document.getElementById("inboxTabBadge").textContent = cnt;
    }

    function toggleHumanGateOnCanvas() {
      hasHumanGateOnCanvas = !hasHumanGateOnCanvas;
      document.getElementById("gateToggleText").textContent = hasHumanGateOnCanvas ? "⚡ Remove from Canvas" : "⚡ Add to Canvas";
      renderCanvas();
      showToast(hasHumanGateOnCanvas ? "Human Gate added to Canvas" : "Human Gate removed from Canvas");
    }

    // Tab Navigation
    function openRightTab(tabName) {
      document.querySelectorAll(".right-tab-item").forEach(t => t.classList.remove("active"));
      document.querySelectorAll(".panel-view-container").forEach(p => p.style.display = "none");

      if (tabName === 'inbox') {
        document.getElementById("tabInboxBtn").classList.add("active");
        document.getElementById("panelInbox").style.display = "flex";
      } else if (tabName === 'undo') {
        document.getElementById("tabUndoBtn").classList.add("active");
        document.getElementById("panelUndo").style.display = "flex";
        updateUndoLedgerUI();
      } else if (tabName === 'digest') {
        document.getElementById("tabDigestBtn").classList.add("active");
        document.getElementById("panelDigest").style.display = "flex";
      } else if (tabName === 'policy') {
        document.getElementById("tabPolicyBtn").classList.add("active");
        document.getElementById("panelPolicy").style.display = "flex";
        renderPolicyTable();
      } else if (tabName === 'inspector') {
        document.getElementById("tabInspectorBtn").classList.add("active");
        document.getElementById("panelInspector").style.display = "flex";
      }
    }

    // Overridden executeStep that enforces Autonomy Policy, Human Gate, and Spend Guards
    async function executeStep(idx) {
      const nodes = getActiveNodes();
      const n = nodes[idx];
      selectedNodeId = n.id;
      inspectNode(n.id);

      if (pausedStages[n.id]) {
        logEvent(`[${n.code}] Paused by supervisor. Holding...`, "warn");
        return false;
      }

      document.querySelectorAll(".canvas-node").forEach(node => node.classList.remove("executing"));
      const el = document.getElementById(`node_${n.id}`);
      if (el) el.classList.add("executing");

      if (idx > 0) {
        const prev = nodes[idx - 1];
        const wire = document.getElementById(`wire_${prev.id}_${n.id}`);
        if (wire) wire.classList.add("pulsing");
      }

      // Check effective autonomy level
      let polKey = n.code || n.name || "S&OP";
      let effectiveLevel = enterpriseAutonomyPolicy[polKey]?.level || "C";
      if (runMode === 'supervised') effectiveLevel = 'C';
      if (hasHumanGateOnCanvas && (n.code === 'CO-03' || n.code === 'ORG-02' || n.id === 'sop_2')) effectiveLevel = 'C';

      // Check spend guard
      const moneyDelta = (n.code === 'CO-03' || n.code === 'ORG-02' || n.id === 'sop_2') ? -1600000 : 0;
      if (Math.abs(moneyDelta) > globalGuards.spendLimit) {
        effectiveLevel = 'C';
      }

      const evId = `ev_ent_${Date.now().toString().slice(-4)}`;
      const timeStr = new Date().toLocaleTimeString();

      const actionEv = {
        id: evId,
        time: timeStr,
        stage: n.code || n.name,
        stage_name: n.name,
        agent: n.role || n.worker || "Enterprise Agent",
        action: enterpriseAutonomyPolicy[polKey]?.action || "process_allocation",
        why: "Multi-echelon allocation shift balancing supply bottleneck against customer commitments",
        impact: {
          money: moneyDelta,
          units: -800,
          kpi_delta: "SLA -0.8%, Margin Floor: 44.8%"
        },
        confidence: 0.74,
        reversible: true,
        level: effectiveLevel,
        status: effectiveLevel === 'C' ? 'awaiting' : (effectiveLevel === 'H' ? 'blocked' : 'auto-approved')
      };

      actionEventStore.push(actionEv);

      if (effectiveLevel === 'A' || effectiveLevel === 'N') {
        actionEv.status = 'executed';
        undoLedger.unshift(actionEv);
        updateUndoLedgerUI();
        logEvent(`[${n.code}] ${n.name}: ${n.artifact || "Processed"} (Level ${effectiveLevel})`, "ok");
        return true;

      } else if (effectiveLevel === 'C') {
        pendingApprovals.push(actionEv);
        updateInboxBadge();
        renderInboxCards();
        setSystemBadge("waiting", `Waiting for you (${pendingApprovals.length})`);
        openRightTab('inbox');
        showAlertBanner(`Approval Required: [${n.code}] ${n.name} proposed -$1.6M multi-echelon adjustment.`);
        logEvent(`[${n.code}] Paused: Awaiting human approval #${evId}`, "warn");
        renderCanvas();
        return false;

      } else if (effectiveLevel === 'H') {
        actionEv.status = 'blocked';
        showAlertBanner(`BLOCKED: [${n.code}] is Level H (Human-Only). Agent prohibited from auto-executing.`);
        logEvent(`[${n.code}] BLOCKED: Level H action requires manual human execution.`, "warn");
        return false;
      }

      return true;
    }

    // Render Approvals Inbox Cards
    function renderInboxCards() {
      const container = document.getElementById("inboxCardsList");
      const emptyState = document.getElementById("inboxEmptyState");

      if (!pendingApprovals.length) {
        container.innerHTML = "";
        emptyState.style.display = "block";
        return;
      }

      emptyState.style.display = "none";
      container.innerHTML = pendingApprovals.map(ev => `
        <div class="decision-card level-${ev.level}" id="card_${ev.id}">
          <div class="decision-header-row">
            <div>
              <div class="decision-title">Adjust Multi-Enterprise Allocation by -800 units (-$1.6M)</div>
              <div style="display: flex; gap: 4px; align-items: center; margin-top: 2px;">
                <span class="decision-stage-tag">${ev.stage}: ${ev.agent}</span>
                <span class="node-autonomy-badge badge-level-${ev.level}">[${ev.level}]</span>
              </div>
            </div>
            <span style="font-size: 0.62rem; color: var(--accent-amber); font-family: var(--font-mono);">⏱ 14m left</span>
          </div>

          <div class="decision-why-text">
            <b>Why:</b> ${ev.why}
          </div>

          <div class="decision-impact-grid">
            <div class="impact-cell">
              <span class="impact-cell-label">Money Impact</span>
              <span class="impact-cell-value" style="color: var(--accent-rose);">-$1,600,000</span>
            </div>
            <div class="impact-cell">
              <span class="impact-cell-label">Volume</span>
              <span class="impact-cell-value">-800 units</span>
            </div>
            <div class="impact-cell">
              <span class="impact-cell-label">SLA Fill</span>
              <span class="impact-cell-value" style="color: var(--accent-amber);">94.7% (-0.8%)</span>
            </div>
            <div class="impact-cell">
              <span class="impact-cell-label">Plan Gap</span>
              <span class="impact-cell-value" style="color: var(--accent-blue);">+$420k</span>
            </div>
          </div>

          <div class="decision-risk-box">
            <b>Risk & Confidence:</b> Stockout risk in Southeast DC (Model confidence: <b>74.0%</b>).
          </div>

          <div class="decision-undo-tag">
            <span>↩️</span> Reversible for 15 mins or until Cleanroom lot dispatch.
          </div>

          <!-- Ask Why Box -->
          <div id="askWhyBox_${ev.id}" style="display: none; background: rgba(6, 182, 212, 0.1); border-left: 2px solid var(--accent-cyan); padding: 5px; font-size: 0.66rem; color: #0284c7; line-height: 1.3;"></div>

          <!-- Rejection Drawer -->
          <div class="rejection-drawer" id="rejectBox_${ev.id}">
            <div style="font-size: 0.64rem; font-weight: 700; color: #e11d48;">Select Reason for Rejection:</div>
            <div class="rejection-chips-row">
              <button class="rejection-chip" onclick="confirmReject('${ev.id}', 'Too risky')">Too risky</button>
              <button class="rejection-chip" onclick="confirmReject('${ev.id}', 'Wrong numbers')">Wrong numbers</button>
              <button class="rejection-chip" onclick="confirmReject('${ev.id}', 'Not now')">Not now</button>
              <button class="rejection-chip" onclick="confirmReject('${ev.id}', 'Buffer sufficient')">Other</button>
            </div>
          </div>

          <div class="decision-btn-row">
            <button class="btn-decision approve" onclick="approveAction('${ev.id}')">
              <span>✓</span> Approve
            </button>
            <button class="btn-decision ask-why" onclick="askWhyDecision('${ev.id}')">
              <span>?</span> Ask Why
            </button>
            <button class="btn-decision reject" onclick="toggleRejectBox('${ev.id}')">
              <span>✕</span> Reject
            </button>
          </div>
        </div>
      `).join('');
    }

    function approveAction(evId) {
      const idx = pendingApprovals.findIndex(p => p.id === evId);
      if (idx === -1) return;

      const ev = pendingApprovals.splice(idx, 1)[0];
      ev.status = 'executed';
      undoLedger.unshift(ev);

      updateInboxBadge();
      renderInboxCards();
      updateUndoLedgerUI();
      dismissAlert();

      logEvent(`[${ev.stage}] APPROVED by supervisor: -800 units (-$1.6M). Executed.`, "ok");
      showToast("✓ Action Approved & Executed");

      // Check trust ramp
      checkTrustPromotion(ev.stage);

      simIdx++;
      startCycle();
    }

    function toggleRejectBox(evId) {
      const box = document.getElementById(`rejectBox_${evId}`);
      if (box) box.style.display = box.style.display === 'flex' ? 'none' : 'flex';
    }

    function confirmReject(evId, reason) {
      const idx = pendingApprovals.findIndex(p => p.id === evId);
      if (idx === -1) return;

      const ev = pendingApprovals.splice(idx, 1)[0];
      ev.status = 'rejected';
      updateInboxBadge();
      renderInboxCards();
      dismissAlert();

      logEvent(`[${ev.stage}] REJECTED by supervisor (${reason}). Reverted.`, "warn");
      showToast(`Action Rejected: ${reason}`);

      setSystemBadge("running", "Ready");
    }

    async function askWhyDecision(evId) {
      const box = document.getElementById(`askWhyBox_${evId}`);
      if (!box) return;
      box.style.display = 'block';
      box.innerHTML = "<em>Querying Enterprise Copilot...</em>";

      try {
        const resp = await fetch("https://api.groq.com/openai/v1/chat/completions", {
          method: "POST",
          headers: { "Authorization": `Bearer ${GROQ_KEY}`, "Content-Type": "application/json" },
          body: JSON.stringify({
            model: "llama-3.3-70b-versatile",
            messages: [
              { role: "system", content: "You are an Enterprise AI Factory Copilot. Provide a concise 2-sentence explanation of why an 800-unit forecast adjustment protects overall multi-company OTIF fulfillment." },
              { role: "user", content: "Explain why cutting 800 units protects multi-tier SLA." }
            ],
            temperature: 0.2, max_tokens: 80
          })
        });
        const data = await resp.json();
        const ans = data.choices?.[0]?.message?.content || "Cutting 800 units balances assembly line capacity with regional substrate availability, maintaining a 94.7% fill rate.";
        box.innerHTML = `<b>Copilot Rationale:</b> ${ans}`;
      } catch (err) {
        box.innerHTML = "<b>Copilot Rationale:</b> Reducing unconstrained demand by 800 units prevents overcommitting SMT assembly lines and protects committed high-margin contracts.";
      }
    }

    function batchApproveLowRisk() {
      while (pendingApprovals.length) {
        approveAction(pendingApprovals[0].id);
      }
      showToast("Batched low-risk actions approved!");
    }

    function checkTrustPromotion(stageCode) {
      consecutiveCleanApprovals[stageCode] = (consecutiveCleanApprovals[stageCode] || 0) + 1;
      if (consecutiveCleanApprovals[stageCode] >= 3) {
        setTimeout(() => {
          if (confirm(`🎉 TRUST PROMOTION: ${stageCode} has 3 consecutive clean approvals. Promote from Confirm (C) to Notify (N)?`)) {
            if (enterpriseAutonomyPolicy[stageCode]) {
              enterpriseAutonomyPolicy[stageCode].level = 'N';
              renderPolicyTable();
              renderCanvas();
              showToast(`${stageCode} Promoted to Notify (N)`);
              logEvent(`[Trust Ramp] ${stageCode} promoted to Notify (N).`, "ok");
            }
          }
        }, 600);
      }
    }

    function updateUndoLedgerUI() {
      const container = document.getElementById("undoLedgerList");
      document.getElementById("undoCount").textContent = undoLedger.length;
      document.getElementById("undoCountTop").textContent = undoLedger.length;

      if (!undoLedger.length) {
        container.innerHTML = `<div style="text-align: center; color: var(--text-dim); padding: 15px; font-size: 0.70rem;">No executed actions in this session.</div>`;
        return;
      }

      container.innerHTML = undoLedger.map(ev => `
        <div class="undo-card" id="undo_${ev.id}">
          <div class="undo-head-row">
            <span style="font-weight: 700;">${ev.stage}: ${ev.action}</span>
            <span class="undo-time">${ev.time}</span>
          </div>
          <div style="font-size: 0.66rem; color: var(--text-muted);">
            Impact: ${ev.impact.units ? ev.impact.units + ' units' : ''} (${ev.impact.money ? '$' + (ev.impact.money/1e6).toFixed(1) + 'M' : 'Baseline'})
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 3px;">
            <span style="font-size: 0.62rem; color: ${ev.status === 'undone' ? 'var(--accent-purple)' : 'var(--accent-emerald)'}; font-family: var(--font-mono);">
              ${ev.status === 'undone' ? '● Undone' : '● Executed'}
            </span>
            ${ev.status === 'undone' ? 
              `<span style="font-size: 0.64rem; color: var(--text-dim);">Reverted</span>` :
              (ev.reversible ? 
                `<button class="btn-undo-action" onclick="executeUndo('${ev.id}')">↩️ Undo Action</button>` :
                `<span style="font-size: 0.62rem; color: var(--accent-rose);">🔒 Irreversible</span>`)
            }
          </div>
        </div>
      `).join('');
    }

    function executeUndo(evId) {
      const ev = undoLedger.find(e => e.id === evId);
      if (!ev || ev.status === 'undone') return;

      if (confirm(`Undo [${ev.stage}] ${ev.action}? This will revert baseline state and log an 'undone' event.`)) {
        ev.status = 'undone';

        const undoEv = {
          id: `ev_undo_${Date.now().toString().slice(-4)}`,
          time: new Date().toLocaleTimeString(),
          stage: ev.stage,
          agent: "Human Supervisor",
          action: `undo_${ev.action}`,
          why: `Supervisor reversed action #${evId}`,
          impact: { money: 1600000, units: 800 },
          reversible: false,
          level: "H",
          status: "executed"
        };
        actionEventStore.push(undoEv);
        updateUndoLedgerUI();
        logEvent(`[UNDO] Reverted ${ev.stage}: ${ev.action}. Baseline restored.`, "warn");
        showToast("Action Undone & Baseline Restored");
      }
    }

    function renderPolicyTable() {
      const tbody = document.getElementById("policyTableBody");
      tbody.innerHTML = Object.keys(enterpriseAutonomyPolicy).map(k => {
        const pol = enterpriseAutonomyPolicy[k];
        return `
          <tr>
            <td><b>${k}</b></td>
            <td style="color: var(--text-muted);">${pol.action}</td>
            <td>
              <div class="policy-selector-group">
                <button class="policy-pill-btn ${pol.level === 'A' ? 'active A' : ''}" onclick="setPolicyLevel('${k}', 'A')">A</button>
                <button class="policy-pill-btn ${pol.level === 'N' ? 'active N' : ''}" onclick="setPolicyLevel('${k}', 'N')">N</button>
                <button class="policy-pill-btn ${pol.level === 'C' ? 'active C' : ''}" onclick="setPolicyLevel('${k}', 'C')">C</button>
                <button class="policy-pill-btn ${pol.level === 'H' ? 'active H' : ''}" onclick="setPolicyLevel('${k}', 'H')">H</button>
              </div>
            </td>
          </tr>
        `;
      }).join('');
    }

    function setPolicyLevel(k, lvl) {
      if (confirm(`Change autonomy level for ${k} to [${lvl}]?`)) {
        enterpriseAutonomyPolicy[k].level = lvl;
        renderPolicyTable();
        renderCanvas();
        showToast(`${k} set to [${lvl}]`);
        logEvent(`[Policy Change] ${k} set to [${lvl}].`, "ok");
      }
    }

    function updateGuardSpend(val) {
      const num = parseInt(val.replace(/[^0-9]/g, '')) || 500000;
      globalGuards.spendLimit = num;
      showToast(`Spend limit updated to $${(num/1000).toFixed(0)}k`);
      logEvent(`[Guardrails] Spend threshold set to $${num}.`, "ok");
    }

    function updateGuardSla(val) {
      const num = parseFloat(val.replace(/[^0-9.]/g, '')) || 90.0;
      globalGuards.slaMin = num;
      showToast(`Min SLA Guard updated to ${num}%`);
    }

    function updateGuardConf(val) {
      const num = parseFloat(val.replace(/[^0-9.]/g, '')) / 100 || 0.75;
      globalGuards.confidenceMin = num;
      showToast(`Min Confidence Guard updated to ${(num*100).toFixed(0)}%`);
    }

    function exportAuditJson() {
      const blob = new Blob([JSON.stringify(actionEventStore, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `enterprise_audit_log_${Date.now()}.json`;
      a.click();
      showToast("Audit Log Exported (JSON)");
    }

    function exportAuditCsv() {
      const headers = ["id", "time", "stage", "agent", "action", "level", "status", "why"];
      const rows = actionEventStore.map(e => [e.id, e.time, e.stage, e.agent, e.action, e.level, e.status, `"${e.why}"`].join(","));
      const csv = [headers.join(","), ...rows].join(String.fromCharCode(10));
      const blob = new Blob([csv], { type: "text/csv" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `enterprise_audit_log_${Date.now()}.csv`;
      a.click();
      showToast("Audit Log Exported (CSV)");
    }

    function generateAiDigest() {
      showToast("Generating Executive AI Brief...");
      document.getElementById("digestSurprises").innerHTML = `
        <b>Enterprise Copilot Synthesis:</b> 6-Company Value Stream coordinated $135.0M gross pipeline into $28.4M firm commitments. 
        One supervisor approval handled (-$1.6M regional allocation adjustment), averting $420k in stockout penalties. 
        All other tier-1/tier-2 nodes executed autonomously under active policy.
      `;
    }

    function setStreamFilter(filter, btn) {
      activeStreamFilter = filter;
      document.querySelectorAll(".filter-chip").forEach(c => c.classList.remove("active"));
      btn.classList.add("active");

      document.querySelectorAll(".stream-line, .stream-row").forEach(r => {
        if (filter === 'all') {
          r.style.display = 'flex';
        } else if (filter === 'alerts') {
          r.style.display = r.textContent.includes('warn') || r.textContent.includes('Paused') || r.textContent.includes('BLOCKED') ? 'flex' : 'none';
        } else if (filter === 'needs_me') {
          r.style.display = r.textContent.includes('approval') || r.textContent.includes('Paused') ? 'flex' : 'none';
        } else if (filter === 'acted') {
          r.style.display = r.textContent.includes('Level A') || r.textContent.includes('Level N') ? 'flex' : 'none';
        } else if (filter === 'undone') {
          r.style.display = r.textContent.includes('UNDO') || r.textContent.includes('Reverted') ? 'flex' : 'none';
        }
      });
    }

    // Hook Canvas Rendering to include Human Gate Node
    const origRenderCurrentCanvas = window.renderCurrentCanvas || renderCurrentCanvas;
    renderCurrentCanvas = function() {
      if (typeof origRenderCurrentCanvas === 'function') origRenderCurrentCanvas();
      if (hasHumanGateOnCanvas && currentLevel === 3) {
        const isWaiting = pendingApprovals.length > 0;
        const gateNode = document.createElement("div");
        gateNode.id = "node_gate_human";
        gateNode.className = `canvas-node human-gate ${isWaiting ? 'waiting-approval' : ''}`;
        gateNode.style.left = "730px";
        gateNode.style.top = "140px";
        gateNode.innerHTML = `
          <div class="node-bar">
            <div class="node-title-wrap">
              <span class="node-badge-pill badge-level-C">GATE</span>
              <span style="color: var(--accent-amber); font-weight: 700;">👤 Human Gate</span>
            </div>
            <span class="node-autonomy-badge badge-level-C">${isWaiting ? 'HOLD' : 'ARMED'}</span>
          </div>
          <div class="node-content">
            <div class="node-role-label">Enterprise S&OP ➔ ERP Checkpoint</div>
            <div class="node-desc-text">Level C approval guard on demand-supply balancing &gt; $500k.</div>
            <div class="node-metrics-box">
              <span style="color:var(--text-dim);">State:</span>
              <span style="color:${isWaiting ? 'var(--accent-amber)' : 'var(--accent-emerald)'}; font-weight:700;">${isWaiting ? 'WAITING (' + pendingApprovals.length + ')' : 'CLEAR'}</span>
              <span style="color:var(--text-dim);">Rule:</span>
              <span style="color:var(--text-main); font-weight:700;">STRICT</span>
            </div>
          </div>
          <div class="node-foot">
            <span style="font-size:0.62rem; color:var(--text-dim); font-family:var(--font-mono);">Ports: In / Apprv / Rej</span>
            <button class="btn-drill" onclick="event.stopPropagation(); openRightTab('inbox');">📬 Inbox (${pendingApprovals.length})</button>
          </div>
          <div class="node-port in"></div>
          <div class="node-port out-approved" title="Approved branch"></div>
          <div class="node-port out-rejected" title="Rejected branch"></div>
        `;
        gateNode.addEventListener("click", () => {
          openRightTab('inbox');
        });
        const nl = document.getElementById("nodesLayer");
        if (nl) nl.appendChild(gateNode);
      }
    };

    function renderCanvas() {
      renderCurrentCanvas();
      renderWires();
    }

    // Wrap initialization to call HUI renders
    window.addEventListener("DOMContentLoaded", () => {
      renderPolicyTable();
      updateInboxBadge();
      renderInboxCards();
      updateUndoLedgerUI();
      setSystemBadge("waiting", `Waiting for you (${pendingApprovals.length})`);
      renderCanvas();
      logEvent("Enterprise Human Intervention UI initialized.", "ok");
      logEvent("Autonomy Policy Engine armed across Company, 6 Orgs & 38 Workers.", "ok");
      logEvent("Active Guardrails: Spend Limit $500,000 | Min SLA 90.0% | Min Confidence 75%.", "ok");
    });
    """

    # Inject HUI JS right before </script>
    html = html.replace("</script>\n</body>", hui_js + "\n  </script>\n</body>")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Successfully generated {OUTPUT_FILE} ({len(html)} bytes)!")

if __name__ == "__main__":
    build()
