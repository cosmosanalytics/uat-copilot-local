# -*- coding: utf-8 -*-
"""
build_inter_company_canvas_human_intervention.py
Generates 'inter_company_ai_factory_canvas_human_intervention.html':
The 4-Tier Inter-Company AI Factory Canvas (Value Chain -> Company -> Organization -> Worker Mind)
upgraded with the full Human Intervention UI (HUI):
- L4 Value Chain -> L3 Company -> L2 Organization -> L1 Worker Mind
- Run Modes (Auto / Supervised / Step)
- Live State Badge (Running, Waiting for you, Paused, Stopped)
- Soft Pause, Emergency Stop, Per-Stage/Node Pause
- Action Event store with append-only ledger
- Approvals Inbox with Multi-Enterprise Decision Cards (Headline, Why, 4-cell impact grid, risk/confidence, undo window, Ask Why AI reasoning)
- Canvas Human Gate node positioned on Level 4 between Apex OEM and Pegasus EMS with Approved / Rejected ports and pulsing waiting state
- Autonomy Policy matrix (A / N / C / H) across all 6 commercial enterprises & organizations + global guardrails (spend, SLA, confidence)
- Undo Ledger with reverse actions, undo windows, and state rollbacks
- Live Stream filter chips (All, Needs Me, Acted, Alerts, Undone)
- Executive Digest & AI Brief generator
- Trust Ramp (Promotion after 3 approvals, Demotion on reject/undo)
- Light Mode by default matching spec Page 17
- JSON & CSV audit log export
"""

import sys

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_FILE = "inter_company_ai_factory_canvas_human_intervention.html"
ALT_OUTPUT_FILE = "enterprise_ai_factory_canvas_human_intervention.html"

def build():
    with open("inter_company_ai_factory_canvas.html", "r", encoding="utf-8") as f:
        html = f.read()

    print(f"Read base inter-company file ({len(html)} chars). Injecting Human Intervention UI...")

    # 1. Update Title
    html = html.replace(
        "<title>Enterprise AI Factory: Company ➔ All 6 Organizations ➔ Worker Mind</title>",
        "<title>Inter-Company AI Factory: Human Intervention & Autonomous Value Chain Canvas</title>"
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

    body.light-mode .app-header {
      background: #ffffff;
      border-bottom-color: #cbd5e1;
    }

    body.light-mode .canvas-container {
      background-color: #f8fafc;
      background-image: radial-gradient(circle at 1px 1px, rgba(15, 23, 42, 0.08) 1px, transparent 0);
    }

    body.light-mode .canvas-node {
      background: #ffffff;
      border-color: #cbd5e1;
      box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
      color: #0f172a;
    }

    body.light-mode .canvas-node:hover {
      border-color: #0284c7;
      box-shadow: 0 8px 20px rgba(14, 165, 233, 0.18);
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

    /* Run Mode Group (HUI-01) */
    .run-mode-group {
      display: flex;
      align-items: center;
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 2px;
      gap: 2px;
    }

    .run-mode-btn {
      padding: 4px 9px;
      font-size: 0.72rem;
      font-weight: 600;
      border-radius: 4px;
      border: none;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: all 0.15s ease;
    }

    .run-mode-btn.active {
      background: linear-gradient(135deg, #0284c7, #2563eb);
      color: #ffffff;
      box-shadow: 0 1px 3px rgba(2, 132, 199, 0.3);
    }

    .run-mode-btn.supervised.active {
      background: linear-gradient(135deg, #d97706, #b45309);
      color: #ffffff;
      box-shadow: 0 1px 3px rgba(217, 119, 6, 0.3);
    }

    .run-mode-btn.step.active {
      background: linear-gradient(135deg, #7c3aed, #6d28d9);
      color: #ffffff;
      box-shadow: 0 1px 3px rgba(124, 58, 237, 0.3);
    }

    /* Live System State Badge (HUI-02) */
    .state-badge {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.72rem;
      font-weight: 700;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid #10b981;
      color: #059669;
    }

    .state-badge.waiting {
      background: rgba(245, 158, 11, 0.18);
      border-color: #f59e0b;
      color: #d97706;
      animation: pulseBadge 1.2s infinite ease-in-out;
    }

    .state-badge.paused {
      background: rgba(100, 116, 139, 0.18);
      border-color: #64748b;
      color: #475569;
    }

    .state-badge.stopped {
      background: rgba(244, 63, 94, 0.18);
      border-color: #f43f5e;
      color: #e11d48;
    }

    @keyframes pulseBadge {
      0% { transform: scale(1); box-shadow: 0 0 0 rgba(245, 158, 11, 0); }
      50% { transform: scale(1.03); box-shadow: 0 0 12px rgba(245, 158, 11, 0.4); }
      100% { transform: scale(1); box-shadow: 0 0 0 rgba(245, 158, 11, 0); }
    }

    /* Control Actions in Header (HUI-03, HUI-04) */
    .btn-header-ctrl {
      height: 30px;
      padding: 0 9px;
      font-size: 0.72rem;
      font-weight: 600;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-color);
      background: var(--bg-card);
      color: var(--text-main);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: all 0.15s ease;
    }

    .btn-header-ctrl:hover {
      background: var(--bg-card-hover);
      border-color: var(--border-light);
    }

    .btn-header-ctrl.btn-pause {
      border-color: #f59e0b;
      color: #d97706;
    }

    .btn-header-ctrl.btn-stop {
      border-color: #f43f5e;
      color: #e11d48;
    }

    /* Top Alert Interrupt Banner (HUI-70) */
    .alert-interrupt-banner {
      background: linear-gradient(90deg, #fff1f2, #ffe4e6);
      border-bottom: 2px solid #f43f5e;
      padding: 8px 16px;
      display: none;
      align-items: center;
      justify-content: space-between;
      z-index: 55;
      color: #9f1239;
      font-size: 0.76rem;
      font-weight: 600;
      box-shadow: 0 2px 8px rgba(244, 63, 94, 0.15);
      animation: slideDownBanner 0.25s ease-out;
    }

    @keyframes slideDownBanner {
      from { transform: translateY(-100%); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }

    .alert-content-wrap {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .alert-actions-wrap {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .btn-alert-action {
      padding: 3px 10px;
      border-radius: 4px;
      font-size: 0.70rem;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid #e11d48;
      background: #ffffff;
      color: #e11d48;
    }
    .btn-alert-action:hover {
      background: #e11d48;
      color: #ffffff;
    }

    /* 5-Tab Right Sidebar (HUI-20, HUI-40, HUI-50, HUI-60, HUI-80) */
    .right-tab-bar {
      display: flex;
      border-bottom: 1px solid var(--border-color);
      background: var(--bg-card);
      flex-shrink: 0;
    }

    .right-tab-item {
      flex: 1;
      padding: 8px 4px;
      font-size: 0.68rem;
      font-weight: 600;
      text-align: center;
      background: transparent;
      border: none;
      border-bottom: 2px solid transparent;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 3px;
      transition: all 0.15s ease;
    }

    .right-tab-item:hover {
      color: var(--text-main);
    }

    .right-tab-item.active {
      color: #0284c7;
      border-bottom-color: #0284c7;
      background: var(--bg-secondary);
      font-weight: 700;
    }

    .badge-counter {
      padding: 1px 5px;
      border-radius: 10px;
      font-size: 0.58rem;
      font-weight: 800;
      background: #f43f5e;
      color: #ffffff;
    }

    .panel-view-container {
      flex: 1;
      overflow-y: auto;
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    /* Decision Card (HUI-20 to HUI-26) */
    .decision-card {
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-left: 4px solid var(--accent-amber);
      border-radius: var(--radius-sm);
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 7px;
      box-shadow: var(--shadow-sm);
      transition: all 0.15s ease;
    }

    .decision-card:hover {
      border-color: var(--border-light);
      box-shadow: var(--shadow-md);
    }

    .decision-headline {
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 6px;
    }

    .decision-why {
      font-size: 0.70rem;
      color: var(--text-muted);
      line-height: 1.35;
    }

    /* 4-Cell Impact Grid (HUI-21) */
    .impact-grid-4cell {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 4px;
      padding: 5px;
    }

    .impact-cell {
      display: flex;
      flex-direction: column;
      padding: 2px 4px;
    }

    .impact-label {
      font-size: 0.58rem;
      color: var(--text-dim);
      text-transform: uppercase;
      font-weight: 600;
    }

    .impact-value {
      font-size: 0.72rem;
      font-weight: 700;
      font-family: var(--font-mono);
      color: var(--text-main);
    }

    .impact-value.pos { color: #059669; }
    .impact-value.neg { color: #e11d48; }

    /* Confidence & Risk Gauge (HUI-22) */
    .confidence-risk-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.65rem;
      color: var(--text-muted);
      padding: 2px 0;
    }

    .decision-actions-row {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-top: 4px;
    }

    .btn-decision {
      flex: 1;
      padding: 5px 8px;
      border-radius: 4px;
      font-size: 0.70rem;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid transparent;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      transition: all 0.15s ease;
    }

    .btn-decision.approve {
      background: linear-gradient(135deg, #059669, #10b981);
      color: #ffffff;
    }
    .btn-decision.approve:hover {
      box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4);
    }

    .btn-decision.reject {
      background: var(--bg-card);
      border-color: #cbd5e1;
      color: #e11d48;
    }
    .btn-decision.reject:hover {
      background: #ffe4e6;
      border-color: #f43f5e;
    }

    .btn-decision.why {
      background: var(--bg-card);
      border-color: #cbd5e1;
      color: #0284c7;
    }
    .btn-decision.why:hover {
      background: #e0f2fe;
      border-color: #38bdf8;
    }

    /* Reject Chips Tray */
    .reject-chips-tray {
      display: none;
      flex-direction: column;
      gap: 4px;
      background: var(--bg-card);
      padding: 6px;
      border-radius: 4px;
      border: 1px dashed #f43f5e;
    }

    .chip-btn {
      padding: 3px 6px;
      font-size: 0.64rem;
      border-radius: 3px;
      border: 1px solid var(--border-color);
      background: var(--bg-secondary);
      color: var(--text-muted);
      cursor: pointer;
      text-align: left;
    }
    .chip-btn:hover {
      border-color: #f43f5e;
      color: #e11d48;
      background: #fff1f2;
    }

    /* Human Gate Node (HUI-30) */
    .canvas-node.human-gate {
      width: 220px;
      border: 2px dashed #d97706;
      background: linear-gradient(180deg, rgba(245, 158, 11, 0.12), rgba(15, 23, 42, 0.95));
    }
    .canvas-node.human-gate .node-bar {
      background: rgba(245, 158, 11, 0.2);
      border-bottom: 1px solid #d97706;
    }
    .canvas-node.waiting-approval {
      border-color: #d97706 !important;
      box-shadow: 0 0 22px rgba(245, 158, 11, 0.7) !important;
      animation: waitingGlow 1.1s infinite alternate;
    }
    @keyframes waitingGlow {
      from { border-color: #d97706; box-shadow: 0 0 10px rgba(245, 158, 11, 0.4); }
      to { border-color: #fde047; box-shadow: 0 0 24px rgba(245, 158, 11, 0.85); }
    }

    .pod-gate { background: rgba(245, 158, 11, 0.25); color: #fde68a; border: 1px solid #d97706; }
    .tier-gate { background: rgba(245, 158, 11, 0.2); color: #fde68a; border: 1px solid #f59e0b; }

    /* Autonomy Policy Table (HUI-40) */
    .policy-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.68rem;
    }
    .policy-table th, .policy-table td {
      padding: 6px 6px;
      border-bottom: 1px solid var(--border-color);
      text-align: left;
    }
    .policy-table th {
      font-size: 0.60rem;
      color: var(--text-dim);
      text-transform: uppercase;
      background: var(--bg-primary);
    }

    .policy-selector-group {
      display: flex;
      border: 1px solid var(--border-color);
      border-radius: 4px;
      overflow: hidden;
    }

    .policy-pill-btn {
      padding: 2px 6px;
      font-size: 0.62rem;
      font-weight: 700;
      border: none;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
    }

    .policy-pill-btn.active.A { background: #059669; color: #fff; }
    .policy-pill-btn.active.N { background: #0284c7; color: #fff; }
    .policy-pill-btn.active.C { background: #d97706; color: #fff; }
    .policy-pill-btn.active.H { background: #e11d48; color: #fff; }

    /* Undo Ledger Card (HUI-50) */
    .undo-card {
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 8px;
      display: flex;
      flex-direction: column;
      gap: 5px;
      font-size: 0.68rem;
    }

    .btn-undo-action {
      align-self: flex-end;
      padding: 3px 8px;
      font-size: 0.65rem;
      font-weight: 700;
      border-radius: 4px;
      border: 1px solid #cbd5e1;
      background: var(--bg-card);
      color: #0284c7;
      cursor: pointer;
    }
    .btn-undo-action:hover {
      background: #e0f2fe;
      border-color: #38bdf8;
    }

    /* Live Stream Filter Chips (HUI-80) */
    .stream-filters-bar {
      display: flex;
      gap: 4px;
      padding: 2px 0;
      overflow-x: auto;
    }

    .filter-chip {
      padding: 2px 8px;
      border-radius: 12px;
      font-size: 0.62rem;
      font-weight: 600;
      border: 1px solid var(--border-color);
      background: var(--bg-card);
      color: var(--text-muted);
      cursor: pointer;
      white-space: nowrap;
    }
    .filter-chip.active {
      background: #0284c7;
      color: #ffffff;
      border-color: #0284c7;
    }

    .guard-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 4px 0;
      font-size: 0.68rem;
    }

    .guard-input {
      width: 80px;
      padding: 2px 5px;
      font-size: 0.68rem;
      border-radius: 3px;
      border: 1px solid var(--border-color);
      background: var(--bg-card);
      color: var(--text-main);
      font-family: var(--font-mono);
      text-align: right;
    }
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
    <div class="state-badge waiting" id="systemStateBadge">
      <span id="stateDot">⏳</span> <span id="stateText">Waiting for you (1)</span>
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
  <div class="alert-interrupt-banner" id="alertInterruptBanner" style="display: flex;">
    <div class="alert-content-wrap">
      <span style="font-size: 1rem;">⚠️</span>
      <span id="alertBannerText">High Financial Exposure: -$480,000 wafer reallocation (Apex OEM ➔ Pegasus EMS) exceeds $500,000 spend guard.</span>
    </div>
    <div class="alert-actions-wrap">
      <button class="btn-alert-action" onclick="openRightTab('inbox')">Review Card</button>
      <button class="btn-alert-action" onclick="pauseCurrentStage()">Pause Node</button>
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
        📬 Inbox <span class="badge-counter" id="inboxCountBadge">1</span>
      </button>
      <button class="tab-btn" onclick="openRightTab('undo')">
        ↩️ Undo (<span id="undoCountTop">1</span>)
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
    warehouse_target = '<div class="sidebar-scroll" id="contentWarehouse">'
    human_gate_part = """
        <!-- Human Gate Node (HUI-30) -->
        <div class="part-box gate-part" onclick="toggleHumanGateOnCanvas()">
          <div class="part-head">
            <span class="part-name">👤 Human Gate</span>
            <span class="part-tier-tag tier-gate">CONTROL</span>
          </div>
          <div class="part-description">
            Forces Level C approval checkpoint on multi-enterprise handoffs &gt; $500k. 1 in, 2 out ports (Approved/Rejected).
          </div>
          <div style="font-size: 0.62rem; color: var(--accent-amber); font-weight: 700; margin-top: 2px;">
            <span id="gateToggleText">⚡ Toggle on Canvas</span>
          </div>
        </div>
    """
    html = html.replace(warehouse_target, warehouse_target + "\n" + human_gate_part, 1)

    # 8. Upgrade Right Sidebar with 5 Tabs: Inbox, Undo, Digest, Policy, Inspector
    old_aside_start = html.find('id="sidebarRight"')
    aside_open_idx = html.rfind('<aside', 0, old_aside_start)
    aside_close_idx = html.find('</aside>', old_aside_start) + 8

    full_old_aside = html[aside_open_idx:aside_close_idx]

    new_right_drawer = """<aside class="sidebar-right" id="sidebarRight">
      <div class="right-tab-bar">
        <button class="right-tab-item active" id="tabInboxBtn" onclick="openRightTab('inbox')">
          📬 Inbox <span class="badge-counter" id="inboxTabBadge">1</span>
        </button>
        <button class="right-tab-item" id="tabUndoBtn" onclick="openRightTab('undo')">
          ↩️ Undo (<span id="undoCount">1</span>)
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
          <!-- Rendered dynamically -->
        </div>

        <div id="inboxEmptyState" style="display: none; text-align: center; padding: 24px 10px; color: var(--text-dim); font-size: 0.74rem;">
          🎉 All inter-company approvals cleared!<br>Value Chain running autonomously under active policy.
        </div>
      </div>

      <!-- TAB 2: UNDO LEDGER (HUI-50 to HUI-53) -->
      <div class="panel-view-container" id="panelUndo" style="display: none;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-main);">Executed Action Ledger</span>
          <span style="font-size: 0.64rem; color: var(--text-dim);">Reverse &amp; Rollback</span>
        </div>
        <div id="undoLedgerList" style="display: flex; flex-direction: column; gap: 6px;">
          <!-- Rendered dynamically -->
        </div>
      </div>

      <!-- TAB 3: EXECUTIVE DIGEST & AI BRIEF (HUI-60) -->
      <div class="panel-view-container" id="panelDigest" style="display: none;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-main);">Value Chain Executive Digest</span>
          <button class="btn-mind-open" onclick="generateAiDigest()">✨ AI Synthesis</button>
        </div>

        <div style="background: var(--bg-card); border-radius: var(--radius-sm); border: 1px solid var(--border-color); padding: 8px; font-size: 0.70rem; display: flex; flex-direction: column; gap: 6px;">
          <div style="font-weight: 700; color: var(--accent-blue);">24h Value Chain Summary</div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4px;">
            <div>• Actions: <b id="digestTotalActions">14</b></div>
            <div>• Auto-Approved: <b style="color:var(--accent-emerald);">12 (85.7%)</b></div>
            <div>• Human Confirmed: <b style="color:var(--accent-amber);">2</b></div>
            <div>• Undone / Reverted: <b style="color:var(--text-dim);">0</b></div>
          </div>
          <div style="margin-top: 4px; font-size: 0.66rem; color: var(--text-muted); line-height: 1.35;" id="digestSurprises">
            <b>Value Chain Highlights:</b> SilicoFab ➔ Apex OEM wafer supply synchronized; Pegasus EMS line balance maintained. TransGlobal 3PL air freight cleared bonded customs without expedites.
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
                <th>Entity / Node</th>
                <th>Cross-Company Action</th>
                <th>Level</th>
              </tr>
            </thead>
            <tbody id="policyTableBody">
              <!-- Rendered dynamically -->
            </tbody>
          </table>
        </div>

        <div style="font-size: 0.68rem; font-weight: 700; color: var(--text-main); margin-top: 4px;">Global Value Chain Guards</div>
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

    # 9. Inject HUI JavaScript Engine right before </script></body>
    hui_js = """
    /* =========================================================================
       INTER-COMPANY HUMAN INTERVENTION UI (HUI) STATE MACHINE & LOGIC
       ========================================================================= */
    let runMode = 'auto'; // 'auto', 'supervised', 'step'
    let systemState = 'waiting'; // 'running', 'waiting', 'paused', 'stopped'
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

    let consecutiveCleanApprovals = { "comp_3": 2, "sop": 3 };

    let pendingApprovals = [
      {
        id: "ev_ic_401",
        time: new Date().toLocaleTimeString(),
        stage: "Apex OEM ➔ Pegasus EMS",
        stage_name: "Multi-Enterprise Wafer Reallocation",
        agent: "Apex S&OP Cross-Company Coordinator",
        action: "rebalance_intercompany_wafers",
        why: "SilicoFab 3nm fab delta (-12%) caused a component bottleneck. Reallocating 2,400 ASIC units from domestic buffer to Pegasus EMS Shenzhen protects OmniCloud Tier-1 Cloud SLA (99.4%) with zero contract penalty.",
        impact: {
          money: -480000,
          units: 2400,
          kpi_delta: "SLA 99.4% (+1.2%), Margin Floor: 44.8%"
        },
        confidence: 0.92,
        reversible: true,
        level: "C",
        status: "awaiting"
      }
    ];

    let actionEventStore = [
      {
        id: "ev_ic_399",
        time: new Date(Date.now() - 180000).toLocaleTimeString(),
        stage: "TransGlobal 3PL",
        stage_name: "Bonded Air Freight Slot Booking",
        agent: "Global Logistics Coordinator",
        action: "route_intermodal_freight",
        why: "Auto-reserved 4 Boeing 777F cargo pallets Shanghai ➔ Frankfurt under Level A policy.",
        impact: { money: -72000, units: 800, kpi_delta: "Transit: 36h vs 48h SLA" },
        confidence: 0.95,
        reversible: true,
        level: "A",
        status: "executed"
      },
      ...pendingApprovals
    ];

    let undoLedger = [
      {
        id: "ev_ic_399",
        time: new Date(Date.now() - 180000).toLocaleTimeString(),
        stage: "TransGlobal 3PL",
        stage_name: "Bonded Air Freight Slot Booking",
        agent: "Global Logistics Coordinator",
        action: "route_intermodal_freight",
        why: "Auto-reserved 4 Boeing 777F cargo pallets Shanghai ➔ Frankfurt under Level A policy.",
        impact: { money: -72000, units: 800 },
        reversible: true,
        level: "A",
        status: "executed"
      }
    ];

    // Master Autonomy Policy across 6 Enterprises & 6 Organizations
    let enterpriseAutonomyPolicy = {
      "SilicoFab Fab":        { level: "A", action: "dispatch_wafers", reversible: false },
      "MicroPCB Substrates":  { level: "A", action: "reserve_substrates", reversible: true },
      "Apex OEM S&OP":         { level: "C", action: "consensus_operating_plan", reversible: true },
      "Pegasus EMS Assembly": { level: "N", action: "firm_smt_schedule", reversible: false },
      "TransGlobal 3PL":      { level: "A", action: "route_intermodal_freight", reversible: true },
      "OmniCloud Acceptance": { level: "C", action: "signoff_cluster_racks", reversible: false },
      "CRM & Commercial":     { level: "A", action: "pipeline_lead_scoring", reversible: true },
      "S&OP Planning":        { level: "C", action: "consensus_demand_supply_balancing", reversible: true },
      "ERP Core":             { level: "N", action: "mrp_explosion_po_release", reversible: false },
      "MES Shop Floor":       { level: "H", action: "smt_high_voltage_lot_dispatch", reversible: false },
      "WMS & Logistics":      { level: "A", action: "dynamic_wave_routing", reversible: true },
      "Finance & Treasury":   { level: "C", action: "three_way_invoice_clearing", reversible: false }
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
        showToast("Value Chain Paused (Soft Hold)");
        logEvent("Value Chain paused by supervisor.", "warn");
      } else {
        const waitingCount = pendingApprovals.length;
        if (waitingCount > 0) {
          setSystemBadge("waiting", `Waiting for you (${waitingCount})`);
        } else {
          setSystemBadge("running", "Running");
        }
        icon.textContent = "⏸";
        text.textContent = "Pause";
        showToast("Resuming Value Chain Execution");
        logEvent("Value Chain execution resumed.", "ok");
      }
    }

    function triggerEmergencyStop() {
      if (!isEmergencyStopped) {
        if (confirm("🛑 EMERGENCY STOP: Halt all multi-enterprise agent handoffs, hold state, and cancel queued shipments?")) {
          isEmergencyStopped = true;
          isRunning = false;
          setSystemBadge("stopped", "Stopped");
          showToast("🛑 Emergency Stop Engaged");
          logEvent("EMERGENCY STOP ENGAGED across 6-Enterprise Value Chain.", "warn");
          showAlertBanner("EMERGENCY STOP ENGAGED: Multi-enterprise execution halted by supervisor.");
        }
      } else {
        isEmergencyStopped = false;
        const waitingCount = pendingApprovals.length;
        if (waitingCount > 0) {
          setSystemBadge("waiting", `Waiting for you (${waitingCount})`);
        } else {
          setSystemBadge("running", "Running");
        }
        showToast("Emergency Stop Cleared");
        logEvent("Emergency Stop cleared.", "ok");
        dismissAlert();
      }
    }

    function promptResetCycle() {
      if (confirm("Reset Value Chain operating cycle and clear pending decision cards?")) {
        simIdx = 0;
        isRunning = false;
        pendingApprovals = [];
        updateInboxBadge();
        renderInboxCards();
        setSystemBadge("running", "Running");
        showToast("Value Chain Cycle Reset");
        logEvent("Value Chain cycle reset.", "ok");
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

      container.innerHTML = pendingApprovals.map(p => `
        <div class="decision-card" id="card_${p.id}">
          <div class="decision-headline">
            <span>[${p.stage}] ${p.action}</span>
            <span style="font-size:0.62rem; color:var(--accent-amber); font-family:var(--font-mono);">⏳ 60s</span>
          </div>
          <div class="decision-why">${p.why}</div>

          <!-- 4-Cell Impact Grid (HUI-21) -->
          <div class="impact-grid-4cell">
            <div class="impact-cell">
              <span class="impact-label">Financial Delta</span>
              <span class="impact-value ${p.impact.money >= 0 ? 'pos' : 'neg'}">
                ${p.impact.money >= 0 ? '+' : ''}$${(Math.abs(p.impact.money) / 1000).toFixed(0)}k
              </span>
            </div>
            <div class="impact-cell">
              <span class="impact-label">Volume Units</span>
              <span class="impact-value">${p.impact.units ? p.impact.units + ' units' : 'N/A'}</span>
            </div>
            <div class="impact-cell">
              <span class="impact-label">SLA Impact</span>
              <span class="impact-value pos">${p.impact.kpi_delta || "Protected"}</span>
            </div>
            <div class="impact-cell">
              <span class="impact-label">Capacity Gap</span>
              <span class="impact-value pos">Balanced</span>
            </div>
          </div>

          <!-- Confidence & Risk (HUI-22) -->
          <div class="confidence-risk-bar">
            <span>Model Confidence: <b style="color:var(--accent-emerald);">${(p.confidence * 100).toFixed(0)}%</b></span>
            <span>Risk Score: <b style="color:var(--accent-cyan);">0.14 (Low)</b></span>
          </div>

          <!-- Actions Row (HUI-23, HUI-24, HUI-25) -->
          <div class="decision-actions-row">
            <button class="btn-decision approve" onclick="approveDecision('${p.id}')">
              ✓ Approve
            </button>
            <button class="btn-decision why" onclick="askWhyDecision('${p.id}')">
              ? Ask Why
            </button>
            <button class="btn-decision reject" onclick="toggleRejectChips('${p.id}')">
              ✕ Reject ▾
            </button>
          </div>

          <!-- Reject Chips Tray (HUI-24) -->
          <div class="reject-chips-tray" id="rejectChips_${p.id}">
            <div style="font-size:0.60rem; color:var(--text-dim); margin-bottom:2px;">Select Rejection Reason:</div>
            <button class="chip-btn" onclick="submitRejection('${p.id}', 'Lead time exceeds carrier SLA')">⏱ Lead time exceeds carrier SLA</button>
            <button class="chip-btn" onclick="submitRejection('${p.id}', 'Customs tariff & freight too high')">💰 Customs tariff &amp; freight too high</button>
            <button class="chip-btn" onclick="submitRejection('${p.id}', 'Gross margin drops below 44% floor')">📉 Gross margin drops below 44% floor</button>
            <button class="chip-btn" onclick="submitRejection('${p.id}', 'Awaiting direct OEM confirmation')">👤 Awaiting direct OEM confirmation</button>
          </div>
        </div>
      `).join('');
    }

    function toggleRejectChips(id) {
      const tray = document.getElementById(`rejectChips_${id}`);
      if (tray) tray.style.display = tray.style.display === "flex" ? "none" : "flex";
    }

    function approveDecision(id) {
      const idx = pendingApprovals.findIndex(p => p.id === id);
      if (idx === -1) return;

      const p = pendingApprovals.splice(idx, 1)[0];
      p.status = 'executed';
      p.approvedAt = new Date().toLocaleTimeString();

      undoLedger.unshift(p);
      actionEventStore.push(p);

      updateInboxBadge();
      renderInboxCards();
      updateUndoLedgerUI();
      dismissAlert();

      // Trust Ramp Check (HUI-90)
      if (p.stage) {
        consecutiveCleanApprovals[p.stage] = (consecutiveCleanApprovals[p.stage] || 0) + 1;
        if (consecutiveCleanApprovals[p.stage] >= 3 && enterpriseAutonomyPolicy[p.stage]?.level === 'C') {
          enterpriseAutonomyPolicy[p.stage].level = 'N';
          showToast(`📈 Trust Ramp: ${p.stage} promoted to Level N (Notify)`);
          logEvent(`[Trust Ramp] ${p.stage} promoted to Level N after 3 clean approvals.`, "ok");
          renderPolicyTable();
        }
      }

      showToast(`Approved: ${p.action} ($${(Math.abs(p.impact.money)/1000).toFixed(0)}k)`);
      logEvent(`[APPROVED] Human supervisor confirmed #${id}: ${p.action}. Dispatched to next enterprise node.`, "ok");

      if (!pendingApprovals.length) {
        setSystemBadge("running", "Running");
      }
      renderCanvas();
    }

    function submitRejection(id, reason) {
      const idx = pendingApprovals.findIndex(p => p.id === id);
      if (idx === -1) return;

      const p = pendingApprovals.splice(idx, 1)[0];
      p.status = 'rejected';
      p.rejectReason = reason;

      actionEventStore.push(p);
      updateInboxBadge();
      renderInboxCards();
      dismissAlert();

      // Trust Ramp demotion
      if (p.stage && enterpriseAutonomyPolicy[p.stage]) {
        enterpriseAutonomyPolicy[p.stage].level = 'C';
        consecutiveCleanApprovals[p.stage] = 0;
      }

      showToast(`Rejected: ${reason}`);
      logEvent(`[REJECTED] Supervisor rejected #${id}: ${reason}. Holding baseline buffer state.`, "warn");

      if (!pendingApprovals.length) {
        setSystemBadge("running", "Running");
      }
      renderCanvas();
    }

    async function askWhyDecision(id) {
      const p = pendingApprovals.find(x => x.id === id);
      if (!p) return;

      const card = document.getElementById(`card_${id}`);
      if (!card) return;

      let rBox = card.querySelector(".ai-reasoning-box");
      if (!rBox) {
        rBox = document.createElement("div");
        rBox.className = "ai-reasoning-box";
        rBox.style.background = "var(--bg-card)";
        rBox.style.border = "1px solid var(--accent-blue)";
        rBox.style.borderRadius = "4px";
        rBox.style.padding = "6px";
        rBox.style.fontSize = "0.68rem";
        rBox.style.color = "var(--text-main)";
        rBox.style.lineHeight = "1.35";
        card.appendChild(rBox);
      }

      rBox.innerHTML = `<em>✨ Querying Copilot (Groq LPU ~500 tok/s)...</em>`;

      const prompt = `Explain why the multi-enterprise value chain should approve: "${p.action}" with impact -$${(Math.abs(p.impact.money)/1000).toFixed(0)}k, SLA impact: ${p.impact.kpi_delta}. Give 2 concise bullet points focusing on customer penalty avoidance and line balancing.`;

      try {
        let text = "";
        if (typeof callGroqLpu === "function" && window.GROQ_API_KEY) {
          text = await callGroqLpu(prompt);
        } else {
          text = `• **SLA Safeguard**: Prevents Tier-1 SLA drop to 94.2% on OmniCloud compute clusters, averting $420k in contract delay penalties.\\n• **Line Balance**: Keeps Pegasus EMS SMT Line 3 utilization at optimal 91% without idle crew costs.`;
        }
        rBox.innerHTML = `<b>AI Rationale:</b><br>${text.replace(/\\n/g, '<br>')}`;
      } catch (e) {
        rBox.innerHTML = `<b>AI Rationale:</b><br>• Prevents SLA penalty on OmniCloud compute clusters ($420k breach).<br>• Maintains Pegasus EMS SMT Line 3 utilization at optimal 91%.`;
      }
    }

    function batchApproveLowRisk() {
      const lowRisk = pendingApprovals.filter(p => (p.confidence >= 0.85 && Math.abs(p.impact.money) <= 1000000));
      if (!lowRisk.length) {
        showToast("No low-risk pending decisions to batch.");
        return;
      }
      const ids = lowRisk.map(p => p.id);
      ids.forEach(id => approveDecision(id));
      showToast(`Batch Approved ${ids.length} decisions.`);
    }

    function updateUndoLedgerUI() {
      const list = document.getElementById("undoLedgerList");
      const countEl = document.getElementById("undoCount");
      const countTop = document.getElementById("undoCountTop");

      countEl.textContent = undoLedger.length;
      countTop.textContent = undoLedger.length;

      if (!undoLedger.length) {
        list.innerHTML = `<div style="text-align:center; padding:20px; color:var(--text-dim); font-size:0.72rem;">No executed actions in undo ledger.</div>`;
        return;
      }

      list.innerHTML = undoLedger.map(ev => `
        <div class="undo-card">
          <div style="display:flex; justify-content:space-between; font-weight:700;">
            <span>[${ev.stage}] ${ev.action}</span>
            <span style="color:var(--text-dim);">${ev.time}</span>
          </div>
          <div style="font-size:0.66rem; color:var(--text-muted);">${ev.why}</div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:3px;">
            <span style="font-family:var(--font-mono); font-weight:700; color:${ev.impact.money >= 0 ? '#059669' : '#e11d48'};">
              ${ev.impact.money >= 0 ? '+' : ''}$${(Math.abs(ev.impact.money)/1000).toFixed(0)}k
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
          impact: { money: Math.abs(ev.impact.money), units: ev.impact.units || 0 },
          reversible: false,
          level: "H",
          status: "executed"
        };
        actionEventStore.push(undoEv);
        updateUndoLedgerUI();
        logEvent(`[UNDO] Reverted ${ev.stage}: ${ev.action}. Baseline allocations restored.`, "warn");
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
      a.download = `inter_company_audit_log_${Date.now()}.json`;
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
      a.download = `inter_company_audit_log_${Date.now()}.csv`;
      a.click();
      showToast("Audit Log Exported (CSV)");
    }

    function generateAiDigest() {
      showToast("Generating Value Chain AI Brief...");
      document.getElementById("digestSurprises").innerHTML = `
        <b>Enterprise Copilot Synthesis:</b> 6-Enterprise Value Chain (SilicoFab ➔ MicroPCB ➔ Apex OEM ➔ Pegasus EMS ➔ TransGlobal 3PL ➔ OmniCloud) synchronized $135.0M gross pipeline into $28.4M firm commitments. 
        One supervisor approval handled (-$480k Apex OEM ➔ Pegasus EMS wafer reallocation), safeguarding OmniCloud SLA at 99.4% with zero liquidated damages. 
        All other tier-1/tier-2 handoffs executed autonomously under active policy.
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

    // Hook Canvas Rendering to include Human Gate Node on Level 4 (Value Chain) & Level 3 (Company)
    const origRenderCurrentCanvas = window.renderCurrentCanvas || renderCurrentCanvas;
    renderCurrentCanvas = function() {
      if (typeof origRenderCurrentCanvas === 'function') origRenderCurrentCanvas();
      
      const nl = document.getElementById("nodesLayer");
      if (!nl) return;

      if (hasHumanGateOnCanvas && currentLevel === 4) {
        const isWaiting = pendingApprovals.length > 0;
        const gateNode = document.createElement("div");
        gateNode.id = "node_gate_human_l4";
        gateNode.className = `canvas-node human-gate ${isWaiting ? 'waiting-approval' : ''}`;
        gateNode.style.left = "660px";
        gateNode.style.top = "130px";
        gateNode.innerHTML = `
          <div class="node-bar">
            <div class="node-title-wrap">
              <span class="node-badge-pill badge-level-C">GATE</span>
              <span style="color: var(--accent-amber); font-weight: 700;">👤 Human Gate</span>
            </div>
            <span class="node-autonomy-badge badge-level-C">${isWaiting ? 'HOLD' : 'ARMED'}</span>
          </div>
          <div class="node-content">
            <div class="node-role-label">Apex OEM ➔ Pegasus EMS Checkpoint</div>
            <div class="node-desc-text">Inter-company Level C approval on allocations &gt; $500k.</div>
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
        nl.appendChild(gateNode);

      } else if (hasHumanGateOnCanvas && currentLevel === 3) {
        const isWaiting = pendingApprovals.length > 0;
        const gateNode = document.createElement("div");
        gateNode.id = "node_gate_human_l3";
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
        nl.appendChild(gateNode);
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
      logEvent("Inter-Company Human Intervention UI initialized.", "ok");
      logEvent("Multi-Enterprise Autonomy Policy armed across 6 Companies & 6 Orgs.", "ok");
      logEvent("Active Guardrails: Spend Limit $500,000 | Min SLA 90.0% | Min Confidence 75%.", "ok");
    });
    """

    # Inject HUI JS right before </script>
    html = html.replace("</script>\n</body>", hui_js + "\n  </script>\n</body>")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully generated {OUTPUT_FILE} ({len(html)} bytes)!")

    with open(ALT_OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully generated {ALT_OUTPUT_FILE} ({len(html)} bytes)!")

if __name__ == "__main__":
    build()
