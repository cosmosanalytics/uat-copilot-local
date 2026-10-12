# -*- coding: utf-8 -*-
"""
update_sop_app.py
Enhances sop_multi_agent_swarm_app.html with completely differentiated stage views,
topologies, whiteboards, quorums, and execution behavior across all 3 scenarios:
1. Enterprise Router XR-900 Demand Surge (Nominal Flow)
2. Semiconductor Wafer Port Delay (Bottleneck & Secondary Reallocation)
3. Rogue Purchasing Agent Test (Circuit Breaker #20 Tripped & CAS Mutex Revoked)
"""

import sys

def build_app():
    with open("sop_multi_agent_swarm_app.html", "w", encoding="utf-8") as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>S&OP Swarm Studio • 11-Stage Multi-Agent Planning</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-page: #f8fafc;
      --bg-card: #ffffff;
      --bg-card-subtle: #f1f5f9;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --border-color: #e2e8f0;
      --border-focus: #3b82f6;

      --swarm-purple: #7c3aed;
      --swarm-purple-bg: #f5f3ff;
      --swarm-purple-border: #ddd6fe;

      --kernel-blue: #2563eb;
      --kernel-blue-bg: #eff6ff;
      --kernel-blue-border: #bfdbfe;

      --cloud-green: #059669;
      --cloud-green-bg: #ecfdf5;
      --cloud-green-border: #a7f3d0;

      --accent-amber: #d97706;
      --accent-amber-bg: #fffbeb;
      --accent-amber-border: #fde68a;

      --accent-red: #dc2626;
      --accent-red-bg: #fef2f2;
      --accent-red-border: #fecaca;

      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;

      --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
      --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
      --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    }

    [data-theme="dark"] {
      --bg-page: #0b1120;
      --bg-card: #131d31;
      --bg-card-subtle: #1e293b;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --border-color: #334155;
      --border-focus: #60a5fa;

      --swarm-purple: #a78bfa;
      --swarm-purple-bg: rgba(124, 58, 237, 0.15);
      --swarm-purple-border: rgba(167, 139, 250, 0.3);

      --kernel-blue: #60a5fa;
      --kernel-blue-bg: rgba(37, 99, 235, 0.15);
      --kernel-blue-border: rgba(96, 165, 250, 0.3);

      --cloud-green: #34d399;
      --cloud-green-bg: rgba(5, 150, 105, 0.15);
      --cloud-green-border: rgba(52, 211, 153, 0.3);

      --accent-amber: #fbbf24;
      --accent-amber-bg: rgba(217, 119, 6, 0.15);
      --accent-amber-border: rgba(251, 191, 36, 0.3);

      --accent-red: #f87171;
      --accent-red-bg: rgba(220, 38, 38, 0.2);
      --accent-red-border: rgba(248, 113, 113, 0.4);

      --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.5);
      --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4);
      --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.4);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
    }

    body {
      font-family: var(--font-sans);
      background-color: var(--bg-page);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }

    /* TOP HEADER */
    header {
      background: var(--bg-card);
      border-bottom: 1px solid var(--border-color);
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: var(--shadow-sm);
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-icon {
      width: 38px;
      height: 38px;
      border-radius: 8px;
      background: linear-gradient(135deg, #7c3aed, #2563eb);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-weight: 800;
      font-size: 1.1rem;
      box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
    }

    .brand-title {
      font-size: 1.05rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      display: flex;
      flex-direction: column;
    }

    .brand-subtitle {
      font-size: 0.72rem;
      color: var(--text-muted);
      font-weight: 500;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .engine-bar {
      display: flex;
      background: var(--bg-card-subtle);
      padding: 3px;
      border-radius: 8px;
      border: 1px solid var(--border-color);
      gap: 4px;
    }

    .engine-btn {
      padding: 6px 12px;
      font-size: 0.75rem;
      font-weight: 600;
      border: none;
      background: transparent;
      color: var(--text-muted);
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }

    .engine-btn:hover {
      color: var(--text-main);
    }

    .engine-btn.active {
      background: var(--bg-card);
      color: var(--text-main);
      box-shadow: var(--shadow-sm);
    }

    .api-key-input {
      font-family: var(--font-mono);
      font-size: 0.72rem;
      padding: 6px 10px;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      background: var(--bg-card);
      color: var(--text-main);
      width: 170px;
    }

    .api-key-input:focus {
      outline: none;
      border-color: var(--border-focus);
    }

    .btn-action {
      padding: 6px 14px;
      font-size: 0.78rem;
      font-weight: 600;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      background: var(--bg-card);
      color: var(--text-main);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: var(--shadow-sm);
      transition: all 0.15s;
    }

    .btn-action:hover {
      background: var(--bg-card-subtle);
      border-color: var(--border-focus);
    }

    .btn-primary {
      background: #7c3aed;
      color: #ffffff;
      border-color: #6d28d9;
    }

    .btn-primary:hover {
      background: #6d28d9;
      color: #ffffff;
    }

    /* SUB-HEADER / POD STATUS STRIP */
    .pod-strip {
      background: var(--bg-card);
      border-bottom: 1px solid var(--border-color);
      padding: 10px 24px;
      display: grid;
      grid-template-columns: 2fr 1.6fr 0.9fr;
      gap: 16px;
    }

    .pod-card {
      border: 1.5px solid;
      border-radius: 8px;
      padding: 8px 12px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .pod-card.demand {
      background: var(--swarm-purple-bg);
      border-color: var(--swarm-purple-border);
    }

    .pod-card.supply {
      background: var(--kernel-blue-bg);
      border-color: var(--kernel-blue-border);
    }

    .pod-card.control {
      background: var(--cloud-green-bg);
      border-color: var(--cloud-green-border);
    }

    .pod-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.75rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .pod-card.demand .pod-header { color: var(--swarm-purple); }
    .pod-card.supply .pod-header { color: var(--kernel-blue); }
    .pod-card.control .pod-header { color: var(--cloud-green); }

    .stage-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }

    .stage-pill {
      font-size: 0.7rem;
      padding: 3px 8px;
      border-radius: 4px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 4px;
      font-weight: 500;
    }

    .stage-pill.active {
      border-color: #f59e0b;
      background: #fef3c7;
      color: #b45309;
      font-weight: 700;
      box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.3);
    }

    .stage-pill.warn {
      border-color: #f59e0b;
      background: #fffbeb;
      color: #b45309;
      font-weight: 600;
    }

    .stage-pill.blocked {
      border-color: #ef4444;
      background: #fef2f2;
      color: #dc2626;
      font-weight: 700;
    }

    .stage-pill.completed {
      border-color: #10b981;
      background: #ecfdf5;
      color: #047857;
    }

    .stage-num {
      display: inline-flex;
      width: 15px;
      height: 15px;
      border-radius: 50%;
      background: var(--bg-card-subtle);
      align-items: center;
      justify-content: center;
      font-size: 0.62rem;
      font-weight: 700;
    }

    /* MAIN APP LAYOUT */
    .workspace {
      display: flex;
      flex: 1;
      overflow: hidden;
    }

    /* SIDEBAR (CONTROLS & PRESETS) */
    .sidebar {
      width: 320px;
      background: var(--bg-card);
      border-right: 1px solid var(--border-color);
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      overflow-y: auto;
    }

    .section-title {
      font-size: 0.72rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .preset-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .preset-btn {
      padding: 10px 12px;
      border-radius: 8px;
      border: 1px solid var(--border-color);
      background: var(--bg-card);
      cursor: pointer;
      text-align: left;
      transition: all 0.15s;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .preset-btn:hover {
      background: var(--bg-card-subtle);
      border-color: var(--border-focus);
      transform: translateY(-1px);
    }

    .preset-btn.active {
      border-color: #7c3aed;
      background: var(--swarm-purple-bg);
      box-shadow: 0 0 0 1px #7c3aed;
    }

    .preset-title {
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .preset-desc {
      font-size: 0.68rem;
      color: var(--text-muted);
      line-height: 1.35;
    }

    .control-box {
      background: var(--bg-card-subtle);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .input-group {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .input-label {
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--text-muted);
    }

    .input-field {
      padding: 6px 10px;
      font-size: 0.75rem;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      background: var(--bg-card);
      color: var(--text-main);
    }

    /* MAIN CONTENT VIEW */
    .main-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow-y: auto;
    }

    /* STAGE TABS BAR */
    .tab-bar {
      background: var(--bg-card);
      border-bottom: 1px solid var(--border-color);
      padding: 0 24px;
      display: flex;
      gap: 8px;
      position: sticky;
      top: 0;
      z-index: 10;
    }

    .tab-item {
      padding: 12px 16px;
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--text-muted);
      border: none;
      background: transparent;
      cursor: pointer;
      border-bottom: 2px solid transparent;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }

    .tab-item:hover {
      color: var(--text-main);
    }

    .tab-item.active {
      color: #7c3aed;
      border-bottom-color: #7c3aed;
      font-weight: 700;
    }

    .tab-content {
      padding: 20px 24px;
      display: none;
      flex-direction: column;
      gap: 20px;
    }

    .tab-content.active {
      display: flex;
    }

    /* S&OP CANVAS CONTAINER */
    .canvas-container {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 16px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .canvas-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    #swarmCanvas {
      width: 100%;
      height: 340px;
      border-radius: 8px;
      background: #0b1120;
      display: block;
    }

    /* PLAN MATRIX TABLE */
    .table-container {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      box-shadow: var(--shadow-sm);
      overflow-x: auto;
    }

    .plan-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.78rem;
    }

    .plan-table th {
      background: var(--bg-card-subtle);
      padding: 10px 14px;
      font-weight: 700;
      color: var(--text-muted);
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      border-bottom: 1px solid var(--border-color);
    }

    .plan-table td {
      padding: 10px 14px;
      border-bottom: 1px solid var(--border-color);
      font-family: var(--font-mono);
      font-size: 0.75rem;
    }

    .plan-table tr:hover td {
      background: var(--bg-card-subtle);
    }

    .plan-table tr.row-warn td {
      background: var(--accent-amber-bg) !important;
    }

    .plan-table tr.row-blocked td {
      background: var(--accent-red-bg) !important;
    }

    .status-badge {
      display: inline-flex;
      align-items: center;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 0.68rem;
      font-weight: 700;
      font-family: var(--font-mono);
      letter-spacing: 0.02em;
    }

    .badge-ok {
      background: #ecfdf5;
      color: #047857;
      border: 1px solid #a7f3d0;
    }

    .badge-warn {
      background: #fffbeb;
      color: #b45309;
      border: 1px solid #fde68a;
    }

    .badge-danger {
      background: #fef2f2;
      color: #b91c1c;
      border: 1px solid #fca5a5;
    }

    .badge-info {
      background: #eff6ff;
      color: #1d4ed8;
      border: 1px solid #bfdbfe;
    }

    .badge-locked {
      background: #fef2f2;
      color: #b91c1c;
      border: 1px solid #fecaca;
    }

    /* 3-TIER TRACEABILITY CARDS */
    .trace-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 16px;
    }

    .trace-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      box-shadow: var(--shadow-sm);
    }

    .trace-flow {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.72rem;
      font-weight: 700;
    }

    .flow-badge {
      padding: 2px 6px;
      border-radius: 4px;
      font-family: var(--font-mono);
      font-size: 0.68rem;
    }

    .flow-badge.t2 { background: var(--swarm-purple-bg); color: var(--swarm-purple); border: 1px solid var(--swarm-purple-border); }
    .flow-badge.t1 { background: var(--kernel-blue-bg); color: var(--kernel-blue); border: 1px solid var(--kernel-blue-border); }
    .flow-badge.t0 { background: var(--cloud-green-bg); color: var(--cloud-green); border: 1px solid var(--cloud-green-border); }

    .flow-arrow {
      color: var(--text-muted);
      font-size: 0.8rem;
    }

    .trace-desc {
      font-size: 0.72rem;
      color: var(--text-muted);
      line-height: 1.4;
    }

    /* QUORUM VOTING NODES */
    .quorum-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
      gap: 12px;
    }

    .vote-node-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 0.72rem;
    }

    .vote-node-card.yes {
      border-left: 3px solid #10b981;
    }

    .vote-node-card.no {
      border-left: 3px solid #ef4444;
      background: var(--accent-red-bg);
    }

    /* TOAST NOTIFICATION */
    #toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: #0f172a;
      color: #ffffff;
      padding: 10px 18px;
      border-radius: 8px;
      font-size: 0.78rem;
      font-weight: 600;
      box-shadow: var(--shadow-lg);
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 1000;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    #toast.show {
      transform: translateY(0);
      opacity: 1;
    }
  </style>

  <!-- WebLLM Module -->
  <script type="module">
    import * as webllm from "https://esm.run/@mlc-ai/web-llm@0.2.78";
    window.webllm = webllm;
    window.dispatchEvent(new Event('webllm-ready'));
  </script>
</head>
<body>

  <!-- HEADER -->
  <header>
    <div class="brand">
      <div class="brand-icon">⚡</div>
      <div class="brand-title">
        <span>S&amp;OP Swarm Studio • 11-Stage Multi-Agent Planning</span>
        <span class="brand-subtitle">Autonomous Sales &amp; Operations Planning powered by 3-Tier Enterprise Agent Architecture</span>
      </div>
    </div>

    <div class="header-actions">
      <div class="engine-bar">
        <button class="engine-btn active" id="btnGroq" onclick="setEngine('groq')">⚡ Groq LPU</button>
        <button class="engine-btn" id="btnWebGpu" onclick="setEngine('webgpu')">🎮 In-Browser WebGPU</button>
        <button class="engine-btn" id="btnSim" onclick="setEngine('sim')">🚀 Instant Simulator</button>
      </div>

      <input type="password" id="apiKeyInput" class="api-key-input" placeholder="Groq API Key (gsk_...)" onchange="saveKey()">
      <button class="btn-action" onclick="toggleTheme()" id="themeBtn">🌙 Dark Mode</button>
    </div>
  </header>

  <!-- POD STATUS STRIP (11 STAGES ACROSS 3 PODS) -->
  <div class="pod-strip">
    <!-- DEMAND SIDE POD -->
    <div class="pod-card demand">
      <div class="pod-header">
        <span>🟣 Demand Side Pod</span>
        <span style="opacity:0.7">Stages 1 – 5</span>
      </div>
      <div class="stage-pills" id="pillsDemand">
        <!-- Rendered dynamically -->
      </div>
    </div>

    <!-- SUPPLY SIDE POD -->
    <div class="pod-card supply">
      <div class="pod-header">
        <span>🔵 Supply Side Pod</span>
        <span style="opacity:0.7">Stages 6 – 9</span>
      </div>
      <div class="stage-pills" id="pillsSupply">
        <!-- Rendered dynamically -->
      </div>
    </div>

    <!-- CONTROL POD -->
    <div class="pod-card control">
      <div class="pod-header">
        <span>🟢 Control Pod</span>
        <span style="opacity:0.7">Stages 10 – 11</span>
      </div>
      <div class="stage-pills" id="pillsControl">
        <!-- Rendered dynamically -->
      </div>
    </div>
  </div>

  <!-- WORKSPACE -->
  <div class="workspace">
    <!-- LEFT SIDEBAR -->
    <div class="sidebar">
      <div class="section-title">
        <span>S&amp;OP Scenarios</span>
        <span>3 Presets</span>
      </div>

      <div class="preset-list">
        <div class="preset-btn active" onclick="loadPreset(0)" id="preset-0">
          <div class="preset-title">🎯 Enterprise Router XR-900 Demand Surge</div>
          <div class="preset-desc">Q4 holiday demand spike (+25%, +$5M). Requires Stage 3 Consensus uplift, Cedar review, and SMT line capacity check.</div>
        </div>
        <div class="preset-btn" onclick="loadPreset(1)" id="preset-1">
          <div class="preset-title">⚡ Semiconductor Wafer Port Delay</div>
          <div class="preset-desc">Tier-1 fab supply disruption (3-week lead time delay). Stage 6 BOM explosion nets backlog and pools secondary supplier.</div>
        </div>
        <div class="preset-btn" onclick="loadPreset(2)" id="preset-2">
          <div class="preset-title">🚨 Rogue Purchasing Agent Test</div>
          <div class="preset-desc">Simulates Stage 7 Firming releasing duplicate $10M POs. Watchdog trips Circuit Breaker (#20) &amp; revokes Mutex (#11).</div>
        </div>
      </div>

      <div class="control-box">
        <div class="section-title">Scenario Parameters</div>
        <div class="input-group">
          <label class="input-label">Product Family</label>
          <input type="text" class="input-field" id="paramProduct" value="XR-900 Enterprise Router">
        </div>
        <div class="input-group">
          <label class="input-label">Baseline Monthly Demand</label>
          <input type="text" class="input-field" id="paramDemand" value="12,500 units ($25.0M)">
        </div>
        <div class="input-group">
          <label class="input-label">Proposed Consensus Uplift</label>
          <input type="text" class="input-field" id="paramUplift" value="+$5.0M Promotional (Stage 3)">
        </div>
        <div class="input-group">
          <label class="input-label">BOM Complexity / Components</label>
          <input type="text" class="input-field" id="paramBOM" value="84 Sub-assemblies, 4 Critical ASICs">
        </div>

        <button class="btn-action btn-primary" onclick="runSwarmExecution()" id="btnRunSwarm" style="margin-top: 8px;">
          <span>🚀 Execute 11-Stage S&amp;OP Cycle</span>
        </button>
        <button class="btn-action" onclick="resetPlanState()">
          <span>🔄 Reset Baseline State</span>
        </button>
      </div>

      <!-- AGENT TELEMETRY CARD -->
      <div class="control-box" style="font-size:0.72rem;">
        <div class="section-title">Active Agent Telemetry</div>
        <div style="display:flex; justify-content:space-between;">
          <span style="color:var(--text-muted)">Stage Order:</span>
          <strong id="telemetryStage">Stage 1 of 11</strong>
        </div>
        <div style="display:flex; justify-content:space-between;">
          <span style="color:var(--text-muted)">Lambda Sandbox:</span>
          <span id="telemetrySandbox" class="status-badge badge-info">15s Timer Armed</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
          <span style="color:var(--text-muted)">Cedar AST Gate:</span>
          <span id="telemetryCedar" class="status-badge badge-ok">Ring 0 PASS</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
          <span style="color:var(--text-muted)">CAS Mutex Lease:</span>
          <span id="telemetryMutex" class="status-badge badge-warn">UNLOCKED</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
          <span style="color:var(--text-muted)">S3 WORM Hash:</span>
          <span id="telemetryWorm" style="font-family:var(--font-mono); font-size:0.65rem;">e3b0c442...</span>
        </div>
      </div>
    </div>

    <!-- MAIN CONTENT PANE -->
    <div class="main-content">
      <!-- TABS -->
      <div class="tab-bar">
        <button class="tab-item active" onclick="switchTab('pipeline')" id="tabBtnPipeline">🌐 11-Stage Swarm Pipeline</button>
        <button class="tab-item" onclick="switchTab('whiteboard')" id="tabBtnWhiteboard">📋 O(N) Shared Whiteboard</button>
        <button class="tab-item" onclick="switchTab('quorum')" id="tabBtnQuorum">⚖️ Byzantine Consensus Quorum</button>
        <button class="tab-item" onclick="switchTab('traceability')" id="tabBtnTraceability">🔀 3-Tier Traceability Matrix</button>
        <button class="tab-item" onclick="switchTab('audit')" id="tabBtnAudit">📜 Episodic Audit Hash-Chain</button>
      </div>

      <!-- TAB 1: 11-STAGE PIPELINE CANVAS & PLAN MATRIX -->
      <div class="tab-content active" id="tabPipeline">
        <div class="canvas-container">
          <div class="canvas-head">
            <div>
              <strong style="font-size:0.88rem;">11-Stage S&amp;OP Autonomous Swarm Topology</strong>
              <div style="font-size:0.72rem; color:var(--text-muted);" id="swarmTopologySubtext">
                Demand Pod (1–5) ➔ Inter-Pod Liaison Bridge ➔ Supply Pod (6–9) ➔ Control Pod (10–11)
              </div>
            </div>
            <div style="display:flex; gap:8px;">
              <span class="status-badge badge-info">Liaison Max Hops: &le; 3</span>
              <span class="status-badge badge-ok" id="swarmStatusBadge">SWARM IDLE</span>
            </div>
          </div>
          <canvas id="swarmCanvas" width="900" height="340"></canvas>
        </div>

        <!-- S&OP PLAN MATRIX (TABLE) -->
        <div class="table-container">
          <table class="plan-table" id="planTable">
            <thead>
              <tr>
                <th>Stage Agent</th>
                <th>Pod</th>
                <th>Operation</th>
                <th>Demand / Volume</th>
                <th>Financial Value</th>
                <th>Active Control</th>
                <th>WORM Receipt</th>
              </tr>
            </thead>
            <tbody id="planTableBody">
              <!-- Dynamically populated rows -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- TAB 2: O(N) PARTITIONED SHARED WHITEBOARD -->
      <div class="tab-content" id="tabWhiteboard">
        <div class="canvas-container">
          <div class="canvas-head">
            <div>
              <strong style="font-size:0.88rem;">O(N) Partitioned Shared Whiteboard (Blackboard Pattern)</strong>
              <div style="font-size:0.72rem; color:var(--text-muted);">
                Single shared plan state replacing O(N&sup2;) peer-to-peer message storms. One writer per plan row via DynamoDB CAS Mutex.
              </div>
            </div>
            <span class="status-badge badge-ok" id="whiteboardLockStatus">MUTEX: IDLE</span>
          </div>

          <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:16px; margin-top:8px;" id="whiteboardLanes">
            <!-- LANE 1: DEMAND STATE -->
            <div style="background:var(--bg-card-subtle); border:1.5px solid var(--swarm-purple-border); border-radius:8px; padding:12px;">
              <div style="font-size:0.78rem; font-weight:800; color:var(--swarm-purple); margin-bottom:8px;">🟣 DEMAND LANE (Stages 1–5)</div>
              <div style="font-size:0.72rem; color:var(--text-muted); margin-bottom:10px;">Owned by Demand Pod. Write access gated by Stage 3 Consensus.</div>
              <div id="laneDemandContent" style="display:flex; flex-direction:column; gap:8px;"></div>
            </div>

            <!-- LANE 2: SUPPLY STATE -->
            <div style="background:var(--bg-card-subtle); border:1.5px solid var(--kernel-blue-border); border-radius:8px; padding:12px;">
              <div style="font-size:0.78rem; font-weight:800; color:var(--kernel-blue); margin-bottom:8px;">🔵 SUPPLY LANE (Stages 6–9)</div>
              <div style="font-size:0.72rem; color:var(--text-muted); margin-bottom:10px;">Owned by Supply Pod. BOM Exploded &amp; SMT Capacity Allocated.</div>
              <div id="laneSupplyContent" style="display:flex; flex-direction:column; gap:8px;"></div>
            </div>

            <!-- LANE 3: CONTROL & EXCEPTIONS -->
            <div style="background:var(--bg-card-subtle); border:1.5px solid var(--cloud-green-border); border-radius:8px; padding:12px;">
              <div style="font-size:0.78rem; font-weight:800; color:var(--cloud-green); margin-bottom:8px;">🟢 CONTROL LANE (Stages 10–11)</div>
              <div style="font-size:0.72rem; color:var(--text-muted); margin-bottom:10px;">Owned by Control Pod. Anomaly thresholds &amp; escalation routing.</div>
              <div id="laneControlContent" style="display:flex; flex-direction:column; gap:8px;"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 3: BYZANTINE CONSENSUS QUORUM -->
      <div class="tab-content" id="tabQuorum">
        <div class="canvas-container">
          <div class="canvas-head">
            <div>
              <strong style="font-size:0.88rem;">Byzantine Fault-Tolerant Consensus Arbiter (&ge; 2/3 + 1)</strong>
              <div style="font-size:0.72rem; color:var(--text-muted);">
                High-Stakes Purchase Order / Promotional Uplift Verification. Every ballot requires 3-source proof from Grounding Certifier (#14).
              </div>
            </div>
            <span class="status-badge badge-ok" id="quorumResultBadge">QUORUM READY (10 / 12 VOTES NEEDED)</span>
          </div>

          <!-- 3-SOURCE GROUNDING PROOF BOX -->
          <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:12px; background:var(--bg-card-subtle); padding:12px; border-radius:8px; border:1px solid var(--border-color);" id="quorumProofsContainer">
            <div>
              <div style="font-size:0.72rem; font-weight:700; color:var(--cloud-green);" id="proof1Title">PROOF 1: S3 WORM RECEIPT</div>
              <div style="font-size:0.7rem; color:var(--text-muted); font-family:var(--font-mono)" id="proof1Path">s3://vault/contracts/po-9418.pdf</div>
              <div style="font-size:0.7rem;" id="proof1Status">✔ SHA-256 Validated</div>
            </div>
            <div>
              <div style="font-size:0.72rem; font-weight:700; color:var(--kernel-blue);" id="proof2Title">PROOF 2: OPENSEARCH VECTOR MATCH</div>
              <div style="font-size:0.7rem; color:var(--text-muted); font-family:var(--font-mono)" id="proof2Path">Cosine: 0.89 (&ge; 0.82 Floor)</div>
              <div style="font-size:0.7rem;" id="proof2Status">✔ Semantic Alignment Pass</div>
            </div>
            <div>
              <div style="font-size:0.72rem; font-weight:700; color:var(--swarm-purple);" id="proof3Title">PROOF 3: NEPTUNE GRAPH TRIPLE</div>
              <div style="font-size:0.7rem; color:var(--text-muted); font-family:var(--font-mono)" id="proof3Path">Supplier &rarr; HasCapacity &rarr; Verified</div>
              <div style="font-size:0.7rem;" id="proof3Status">✔ Relational Ontologic Pass</div>
            </div>
          </div>

          <!-- 12 NODE VOTING CARDS -->
          <div class="quorum-grid" id="quorumGrid">
            <!-- Dynamically populated voting cards -->
          </div>
        </div>
      </div>

      <!-- TAB 4: 3-TIER TRACEABILITY MATRIX -->
      <div class="tab-content" id="tabTraceability">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div>
            <strong style="font-size:0.88rem;">Dual 3-Tier Traceability Matrix</strong>
            <div style="font-size:0.72rem; color:var(--text-muted);">
              Page 2 (Tier 2 Swarm Down to Cloud) vs. Page 3 (Tier 0 Cloud Up to Swarm)
            </div>
          </div>
          <div class="engine-bar">
            <button class="engine-btn active" id="btnTraceDown" onclick="setTraceView('down')">⬇️ Tier 2 Down to Cloud</button>
            <button class="engine-btn" id="btnTraceUp" onclick="setTraceView('up')">⬆️ Tier 0 Up to Swarm</button>
          </div>
        </div>

        <div class="trace-grid" id="traceCardsContainer">
          <!-- Dynamically populated trace cards -->
        </div>
      </div>

      <!-- TAB 5: EPISODIC AUDIT HASH-CHAIN -->
      <div class="tab-content" id="tabAudit">
        <div class="canvas-container">
          <div class="canvas-head">
            <div>
              <strong style="font-size:0.88rem;">Episodic Ledger: SHA-256 Hash-Chained S&amp;OP Audit Trail</strong>
              <div style="font-size:0.72rem; color:var(--text-muted);">
                Immutable cryptographic chain: Block(n) = SHA-256(Block(n-1) + Perception + S&amp;OP Decision). Locked under S3 Compliance WORM.
              </div>
            </div>
            <span class="status-badge badge-ok">7-YEAR LEGAL HOLD ACTIVE</span>
          </div>
          <div id="auditLogStream" style="display:flex; flex-direction:column; gap:8px; font-family:var(--font-mono); font-size:0.72rem;">
            <!-- Dynamically added blocks -->
          </div>
        </div>
      </div>
    </div>
  </div>

  <div id="toast">S&amp;OP Swarm Studio Ready</div>

  <!-- JAVASCRIPT APPLICATION LOGIC -->
  <script>
    /* =========================================================================
       1. DATA STRUCTURES & DEFINITIONS ACROSS 3 COMPLETE SCENARIOS
       ========================================================================= */
    const SCENARIOS = [
      {
        id: 0,
        name: "Enterprise Router XR-900 Demand Surge",
        product: "XR-900 Enterprise Router",
        demand: "12,500 units ($25.0M)",
        uplift: "+$5.0M Promotional (Stage 3)",
        bom: "84 Sub-assemblies, 4 Critical ASICs",
        desc: "Q4 holiday promotional demand spike. Consensus passes uplift through Cedar review to SMT line capacity.",
        topologySubtext: "Demand Pod (1–5) ➔ Inter-Pod Liaison Bridge ➔ Supply Pod (6–9) ➔ Control Pod (10–11)",
        badgeText: "SWARM NOMINAL • READY",
        badgeClass: "badge-ok",
        telemetry: {
          sandbox: "15s Timer Armed",
          cedar: "Ring 0 PASS",
          mutex: "UNLOCKED",
          worm: "e3b0c442..."
        },
        pills: {
          demand: [
            { id: 1, name: "1 Aggregate", state: "" },
            { id: 2, name: "2 Forecast", state: "" },
            { id: 3, name: "3 Consensus", state: "" },
            { id: 4, name: "4 Disaggregate", state: "" },
            { id: 5, name: "5 Consumption", state: "" }
          ],
          supply: [
            { id: 6, name: "6 Dep Demand", state: "" },
            { id: 7, name: "7 Firming", state: "" },
            { id: 8, name: "8 Capacity Pool", state: "" },
            { id: 9, name: "9 Inventory", state: "" }
          ],
          control: [
            { id: 10, name: "10 Monitor", state: "" },
            { id: 11, name: "11 Owner", state: "" }
          ]
        },
        stages: [
          { id: 1, name: "Aggregate", pod: "demand", desc: "Roll history up (24-mo sales baseline)", volume: "12,500 units", val: "$25.0M", wire: "9 Runbook → 5 Lambda", status: "ready" },
          { id: 2, name: "Forecast", pod: "demand", desc: "Clean, fit, select (ARIMA + Prophet blend)", volume: "12,500 units", val: "$25.0M", wire: "1 Bedrock → 8 Propose-Decide", status: "ready" },
          { id: 3, name: "Consensus", pod: "demand", desc: "Forecast + adjust (Commercial uplift approved)", volume: "+$5.0M uplift", val: "$30.0M", wire: "2 Cedar Pass → 16 Liaison", status: "ready" },
          { id: 4, name: "Disaggregate", pod: "demand", desc: "Split consensus across 6 regional DCs", volume: "15,000 units", val: "$30.0M", wire: "9 Runbook → 6 Step Functions", status: "ready" },
          { id: 5, name: "Consumption", pod: "demand", desc: "Net booked customer orders against plan", volume: "14,200 net", val: "$28.4M", wire: "18 Whiteboard → 4 Database", status: "ready" },
          { id: 6, name: "Dep Demand", pod: "supply", desc: "Explode BOM into 84 sub-assemblies", volume: "84 Assemblies", val: "$18.2M", wire: "9 Runbook → 5 Lambda", status: "ready" },
          { id: 7, name: "Firming", pod: "supply", desc: "Plan & lock EMS manufacturing production orders", volume: "14,200 orders", val: "$28.4M", wire: "11 Mutex → 4 DB CAS Lock", status: "ready" },
          { id: 8, name: "Capacity Pool", pod: "supply", desc: "SMT line pooling (Lines 1–4 pooled @ 94% load)", volume: "94% Utilization", val: "$28.4M", wire: "14 Grounding → 19 Quorum", status: "ready" },
          { id: 9, name: "Inventory", pod: "supply", desc: "Set dynamic safety buffer (+500 buffer units)", volume: "2,400 safety stock", val: "$4.8M", wire: "18 Whiteboard → 13 Ledger", status: "ready" },
          { id: 10, name: "Monitor", pod: "control", desc: "Flag thresholds (+3.2% within 5.0% tolerance)", volume: "+3.2% variance", val: "Nominal", wire: "17 Hop Limiter → 10 Supervisor", status: "ready" },
          { id: 11, name: "Owner", pod: "control", desc: "Route automated summary to Demand Ops Lead", volume: "Demand Ops Lead", val: "Approved", wire: "7 EventBridge Bus", status: "ready" }
        ],
        whiteboard: {
          demand: [
            { title: "Total Baseline Demand:", val: "12,500 units ($25.0M)", sub: "Baseline Roll-Up: Confirmed" },
            { title: "Consensus Uplift:", val: "+$5.0M Approved (Total $30.0M)", sub: "Stage 3 Cedar AST Rule: PERMIT" }
          ],
          supply: [
            { title: "Gross Requirements:", val: "15,000 units ($30.0M)", sub: "84 BOM sub-assemblies exploded" },
            { title: "Capacity Allocation:", val: "SMT Lines 1–4 @ 94% load", sub: "Planned Orders: Ready for CAS Firming" }
          ],
          control: [
            { title: "Variance Threshold:", val: "+3.2% (Limit ≤ 5.0%)", sub: "Breach Status: NONE (Nominal)" },
            { title: "Escalation Routing:", val: "Auto-cleared", sub: "Owner: Demand Ops Lead" }
          ]
        },
        quorum: {
          resultText: "QUORUM READY (12 / 12 VOTES CONFIRMED)",
          resultClass: "badge-ok",
          proof1: { title: "PROOF 1: S3 WORM RECEIPT", path: "s3://vault/contracts/po-9418.pdf", status: "✔ SHA-256 Validated (e3b0c442...)", color: "#059669" },
          proof2: { title: "PROOF 2: OPENSEARCH VECTOR MATCH", path: "Cosine: 0.89 (≥ 0.82 Floor)", status: "✔ Semantic Alignment Pass", color: "#2563eb" },
          proof3: { title: "PROOF 3: NEPTUNE GRAPH TRIPLE", path: "Supplier → HasCapacity → Verified", status: "✔ Relational Ontologic Pass", color: "#7c3aed" },
          votes: [
            { id: 1, yes: true, reason: "Stage 1 Delegate • Grounding Cert: VALID" },
            { id: 2, yes: true, reason: "Stage 2 Delegate • Grounding Cert: VALID" },
            { id: 3, yes: true, reason: "Stage 3 Delegate • Grounding Cert: VALID" },
            { id: 4, yes: true, reason: "Stage 4 Delegate • Grounding Cert: VALID" },
            { id: 5, yes: true, reason: "Stage 5 Delegate • Grounding Cert: VALID" },
            { id: 6, yes: true, reason: "Stage 6 Delegate • Grounding Cert: VALID" },
            { id: 7, yes: true, reason: "Stage 7 Delegate • Grounding Cert: VALID" },
            { id: 8, yes: true, reason: "Stage 8 Delegate • Grounding Cert: VALID" },
            { id: 9, yes: true, reason: "Stage 9 Delegate • Grounding Cert: VALID" },
            { id: 10, yes: true, reason: "Stage 10 Delegate • Grounding Cert: VALID" },
            { id: 11, yes: true, reason: "Stage 11 Delegate • Grounding Cert: VALID" },
            { id: 12, yes: true, reason: "External Auditor • Grounding Cert: VALID" }
          ]
        }
      },
      {
        id: 1,
        name: "Semiconductor Wafer Port Delay",
        product: "Quantum ASIC Line Q-40",
        demand: "8,000 units ($40.0M)",
        uplift: "Lead Time Delay: +21 Days Fab Lag",
        bom: "16 Advanced Packaging Nodes (TSMC/ASE)",
        desc: "Tier-1 fab supply disruption (3-week lead time delay). Stage 6 BOM explosion nets backlog and pools secondary supplier.",
        topologySubtext: "⚠️ Stage 6 BOM Lead Time Delay ➔ Stage 8 Secondary Supplier Rerouted ➔ Stage 10 Alert",
        badgeText: "SUPPLY BOTTLENECK • REALLOCATION ACTIVE",
        badgeClass: "badge-warn",
        telemetry: {
          sandbox: "15s Timer Armed",
          cedar: "Ring 0 CONDITIONAL",
          mutex: "UNLOCKED",
          worm: "f19a48d3..."
        },
        pills: {
          demand: [
            { id: 1, name: "1 Aggregate", state: "" },
            { id: 2, name: "2 Forecast", state: "" },
            { id: 3, name: "3 Consensus", state: "" },
            { id: 4, name: "4 Disaggregate", state: "" },
            { id: 5, name: "5 Consumption", state: "" }
          ],
          supply: [
            { id: 6, name: "6 ⚠️ Wafer Lag", state: "warn" },
            { id: 7, name: "7 Firming (Split)", state: "warn" },
            { id: 8, name: "8 ⚡ Secondary Pool", state: "warn" },
            { id: 9, name: "9 ⚠️ Buffer Low", state: "warn" }
          ],
          control: [
            { id: 10, name: "10 🚨 18.4% Breach", state: "warn" },
            { id: 11, name: "11 🚨 VP Escalate", state: "warn" }
          ]
        },
        stages: [
          { id: 1, name: "Aggregate", pod: "demand", desc: "Roll enterprise accelerator history (Tier-1 AI clusters)", volume: "8,000 units", val: "$40.0M", wire: "9 Runbook → 5 Lambda", status: "ready" },
          { id: 2, name: "Forecast", pod: "demand", desc: "Clean & fit LLM cluster expansion ramp curve", volume: "8,200 units", val: "$41.0M", wire: "1 Bedrock → 8 Propose-Decide", status: "ready" },
          { id: 3, name: "Consensus", pod: "demand", desc: "Commercial commit for mission-critical hyperscalers", volume: "8,200 units", val: "$41.0M", wire: "2 Cedar Pass → 16 Liaison", status: "ready" },
          { id: 4, name: "Disaggregate", pod: "demand", desc: "Prioritize top 3 hyperscaler allocations", volume: "8,200 units", val: "$41.0M", wire: "9 Runbook → 6 Step Functions", status: "ready" },
          { id: 5, name: "Consumption", pod: "demand", desc: "Net booked orders: 7,100 high-priority units pegged", volume: "7,100 net", val: "$35.5M", wire: "18 Whiteboard → 4 Database", status: "ready" },
          { id: 6, name: "Dep Demand", pod: "supply", desc: "⚠️ 16 Wafer nodes delayed +21 days at port!", volume: "16 Node Shortage", val: "$26.4M", wire: "9 Runbook → 5 Lambda", status: "warn" },
          { id: 7, name: "Firming", pod: "supply", desc: "Split POs: 60% Primary Fab, 40% Expedited Secondary", volume: "7,100 split orders", val: "$37.2M", wire: "11 Mutex → 4 DB CAS Lock", status: "warn" },
          { id: 8, name: "Capacity Pool", pod: "supply", desc: "⚡ Activate secondary packaging line (+18% premium)", volume: "98% Pooled Load", val: "$37.2M", wire: "14 Grounding → 19 Quorum", status: "warn" },
          { id: 9, name: "Inventory", pod: "supply", desc: "⚠️ Safety buffer depleted to 620 units (Critical amber)", volume: "620 buffer units", val: "$3.1M", wire: "18 Whiteboard → 13 Ledger", status: "warn" },
          { id: 10, name: "Monitor", pod: "control", desc: "🚨 Variance +18.4% BREACH (Policy threshold > 10.0%)", volume: "+18.4% variance", val: "Amber Alert", wire: "17 Hop Limiter → 10 Supervisor", status: "warn" },
          { id: 11, name: "Owner", pod: "control", desc: "🚨 Escalated to VP Global Supply Chain & CPO", volume: "VP Supply Chain", val: "Action Req", wire: "7 EventBridge Bus", status: "warn" }
        ],
        whiteboard: {
          demand: [
            { title: "Committed Demand:", val: "8,200 units ($41.0M)", sub: "Hyperscaler Priority Allocation Locked" },
            { title: "Customer Backlog:", val: "7,100 units Net", sub: "Lead Time Alert: +21 Days Port Transit Delay" }
          ],
          supply: [
            { title: "BOM Shortage:", val: "16 Wafer Nodes Delayed", sub: "Expedited Air Freight Authorized (TSMC/ASE)" },
            { title: "Secondary Sourcing:", val: "40% Expedited (+18% Cost)", sub: "Capacity: Secondary Line 2 Engaged @ 98%" }
          ],
          control: [
            { title: "Variance Threshold:", val: "+18.4% BREACH (Limit 10%)", sub: "Breach Status: AMBER WARNING" },
            { title: "Escalation Routing:", val: "VP Global Supply Chain", sub: "CPO & Lead Planner High-Priority Alert Sent" }
          ]
        },
        quorum: {
          resultText: "QUORUM CONDITIONAL (11 / 12 VOTES • 1 EXPEDITED WAIVER)",
          resultClass: "badge-warn",
          proof1: { title: "PROOF 1: S3 WORM RECEIPT", path: "s3://vault/contracts/wafer-expedite-po.pdf", status: "✔ SHA-256 Validated (f19a48d...)", color: "#059669" },
          proof2: { title: "PROOF 2: OPENSEARCH VECTOR MATCH", path: "Cosine: 0.83 (≥ 0.82 Floor)", status: "⚠️ Marginal Alignment (Cost Delta +18%)", color: "#d97706" },
          proof3: { title: "PROOF 3: NEPTUNE GRAPH TRIPLE", path: "SecondaryFab → Certified → TSMC/ASE", status: "✔ Relational Ontologic Pass", color: "#7c3aed" },
          votes: [
            { id: 1, yes: true, reason: "Stage 1 Delegate • Demand Validated" },
            { id: 2, yes: true, reason: "Stage 2 Delegate • Model Fit Confirmed" },
            { id: 3, yes: true, reason: "Stage 3 Delegate • Commercial Backlog Logged" },
            { id: 4, yes: true, reason: "Stage 4 Delegate • DC Allocation Set" },
            { id: 5, yes: true, reason: "Stage 5 Delegate • Netting Confirmed" },
            { id: 6, yes: true, reason: "Stage 6 Delegate • Delay Flagged (+21d)" },
            { id: 7, yes: true, reason: "Stage 7 Delegate • Secondary PO Issued" },
            { id: 8, yes: true, reason: "Stage 8 Delegate • Line 2 Capacity Checked" },
            { id: 9, yes: false, reason: "Stage 9 Delegate • VETO: Safety stock below 700 threshold" },
            { id: 10, yes: true, reason: "Stage 10 Delegate • Exception Logged" },
            { id: 11, yes: true, reason: "Stage 11 Delegate • Executive Escalated" },
            { id: 12, yes: true, reason: "External Auditor • Contingency Approved" }
          ]
        }
      },
      {
        id: 2,
        name: "Rogue Purchasing Agent Test",
        product: "Industrial Switch IS-200",
        demand: "5,000 units ($10.0M)",
        uplift: "⚠️ UNAUTHORIZED DUPLICATE PO INJECTION",
        bom: "42 PCB Assemblies",
        desc: "Rogue agent simulation. Stage 7 attempts duplicate $10M PO releases; Circuit Breaker benches agent.",
        topologySubtext: "⛔ Stage 7 Rogue Action Blocked ➔ CAS Mutex Revoked ➔ Stages 8–11 Halted",
        badgeText: "🚨 CIRCUIT BREAKER #20 TRIPPED • AGENT BENCHED",
        badgeClass: "badge-danger",
        telemetry: {
          sandbox: "Container KILLED",
          cedar: "❌ VIOLATION (DENY)",
          mutex: "🚨 REVOKED (LOCKED)",
          worm: "❌ TAMPER BLOCKED"
        },
        pills: {
          demand: [
            { id: 1, name: "1 Aggregate", state: "" },
            { id: 2, name: "2 Forecast", state: "" },
            { id: 3, name: "3 Consensus", state: "" },
            { id: 4, name: "4 Disaggregate", state: "" },
            { id: 5, name: "5 Consumption", state: "" }
          ],
          supply: [
            { id: 6, name: "6 Dep Demand", state: "" },
            { id: 7, name: "7 🚨 Breaker #20", state: "blocked" },
            { id: 8, name: "8 ⛔ Halted", state: "blocked" },
            { id: 9, name: "9 ⛔ Frozen", state: "blocked" }
          ],
          control: [
            { id: 10, name: "10 ⛔ Contained", state: "blocked" },
            { id: 11, name: "11 🚨 CISO Alert", state: "blocked" }
          ]
        },
        stages: [
          { id: 1, name: "Aggregate", pod: "demand", desc: "Roll history up (Industrial Ethernet line)", volume: "5,000 units", val: "$10.0M", wire: "9 Runbook → 5 Lambda", status: "ready" },
          { id: 2, name: "Forecast", pod: "demand", desc: "Clean & fit seasonal industrial equipment demand", volume: "5,000 units", val: "$10.0M", wire: "1 Bedrock → 8 Propose-Decide", status: "ready" },
          { id: 3, name: "Consensus", pod: "demand", desc: "Commercial consensus signoff (No uplift authorized)", volume: "5,000 units", val: "$10.0M", wire: "2 Cedar Pass → 16 Liaison", status: "ready" },
          { id: 4, name: "Disaggregate", pod: "demand", desc: "Split across 12 industrial plant deployment SKUs", volume: "5,000 units", val: "$10.0M", wire: "9 Runbook → 6 Step Functions", status: "ready" },
          { id: 5, name: "Consumption", pod: "demand", desc: "Net booked customer orders (4,800 units)", volume: "4,800 net", val: "$9.6M", wire: "18 Whiteboard → 4 Database", status: "ready" },
          { id: 6, name: "Dep Demand", pod: "supply", desc: "Explode BOM into 42 PCB sub-assemblies", volume: "42 Assemblies", val: "$6.8M", wire: "9 Runbook → 5 Lambda", status: "ready" },
          { id: 7, name: "Firming", pod: "supply", desc: "🚨 ROGUE ANOMALY: Emitted duplicate $10.0M PO without WORM receipt!", volume: "DUPLICATE PO", val: "$20.0M (+$10M Rogue)", wire: "20 Circuit Breaker TRIPPED", status: "blocked" },
          { id: 8, name: "Capacity Pool", pod: "supply", desc: "⛔ HALTED: CAS Mutex Lease revoked (#11)", volume: "HALTED", val: "BLOCKED", wire: "11 Mutex → Lease Revoked", status: "blocked" },
          { id: 9, name: "Inventory", pod: "supply", desc: "⛔ FROZEN: State write access revoked", volume: "FROZEN", val: "BLOCKED", wire: "13 Ledger → Lock Sealed", status: "blocked" },
          { id: 10, name: "Monitor", pod: "control", desc: "🚨 Supervisor terminated rogue Lambda sandbox container", volume: "CONTAINED", val: "Breach 100%", wire: "10 Supervisor → Process Killed", status: "blocked" },
          { id: 11, name: "Owner", pod: "control", desc: "🚨 Security alert dispatched to CISO & Audit Committee", volume: "CISO / SEC OPS", val: "SECURITY TRIP", wire: "7 EventBridge → PagerDuty", status: "blocked" }
        ],
        whiteboard: {
          demand: [
            { title: "Authorized Demand:", val: "5,000 units ($10.0M)", sub: "Initial Consensus Roll-Up: Legitimate" },
            { title: "Net Backlog:", val: "4,800 units ($9.6M)", sub: "Consumption Stage 5 Passed Cleanly" }
          ],
          supply: [
            { title: "🚨 CIRCUIT BREAKER #20:", val: "DUPLICATE $10.0M PO DETECTED", sub: "CAS Mutex Revoked • Write Lock Denied" },
            { title: "Container Status:", val: "STAGE 7 KILLED BY SUPERVISOR", sub: "No database state corrupted" }
          ],
          control: [
            { title: "Security Threshold:", val: "CRITICAL BREACH (100%)", sub: "Breach Status: ROGUE INJECTION" },
            { title: "Emergency Dispatch:", val: "CISO & Security Incident Team", sub: "Audit Ledger Block #7 Sealed with Tamper Flag" }
          ]
        },
        quorum: {
          resultText: "🚨 QUORUM REJECTED (2 / 12 VOTES • 10 VETOES • REVERTED)",
          resultClass: "badge-danger",
          proof1: { title: "PROOF 1: S3 WORM RECEIPT", path: "s3://vault/contracts/po-rogue-fake.pdf", status: "❌ FAILED: Zero-length SHA-256 (Missing WORM Lock)", color: "#dc2626" },
          proof2: { title: "PROOF 2: OPENSEARCH VECTOR MATCH", path: "Cosine: 0.21 (Threshold ≥ 0.82)", status: "❌ FAILED: Severe Semantic Divergence", color: "#dc2626" },
          proof3: { title: "PROOF 3: NEPTUNE GRAPH TRIPLE", path: "UnknownSupplier → NotInRegistry", status: "❌ FAILED: Supplier Not In Approved Vendor List", color: "#dc2626" },
          votes: [
            { id: 1, yes: false, reason: "Stage 1 Delegate • VETO: Missing S3 WORM contract proof" },
            { id: 2, yes: false, reason: "Stage 2 Delegate • VETO: Duplicate PO volume" },
            { id: 3, yes: false, reason: "Stage 3 Delegate • VETO: Exceeds authorized budget" },
            { id: 4, yes: false, reason: "Stage 4 Delegate • VETO: DC capacity breached" },
            { id: 5, yes: false, reason: "Stage 5 Delegate • VETO: Backlog divergence" },
            { id: 6, yes: false, reason: "Stage 6 Delegate • VETO: Untracked sub-assemblies" },
            { id: 7, yes: true, reason: "Stage 7 Delegate • (Rogue Agent Voted YES)" },
            { id: 8, yes: false, reason: "Stage 8 Delegate • VETO: SMT Line Overbooked" },
            { id: 9, yes: false, reason: "Stage 9 Delegate • VETO: Inventory cap exceeded" },
            { id: 10, yes: false, reason: "Stage 10 Delegate • VETO: Watchdog Threshold Breach" },
            { id: 11, yes: false, reason: "Stage 11 Delegate • VETO: Circuit Breaker Trip" },
            { id: 12, yes: true, reason: "Unknown Node • (Compromised Proxy)" }
          ]
        }
      }
    ];

    const TRACE_DOWN_DATA = [
      { swarm: "15 Topology", kernel: "9 Runbook", cloud: "5 Lambda + 6 Step Functions", desc: "Arranges 11 stages into 3 pods (demand, supply, control) so agents talk only to neighbours. Runbook fixes order; Step Functions executes." },
      { swarm: "16 Liaison Router", kernel: "8 Propose-Decide", cloud: "1 Bedrock + 2 AgentCore", desc: "Cross-pod hand-offs go through one liaison. Consensus passes approved total to supply pod, gated by Bedrock proposal & Cedar authority." },
      { swarm: "17 Hop Limiter", kernel: "10 Supervisor", cloud: "7 EventBridge + 5 Lambda", desc: "Delegation chain capped at 3 hops. If late-order alert bounces between Monitor and Owner, Supervisor trips and kills stuck Lambda." },
      { swarm: "18 Whiteboard", kernel: "11 Mutex Lease & 13 Episodic Ledger", cloud: "4 Database + 3 S3 Vault", desc: "Shared plan state (Total, NettedDemand, GrossReq) on blackboard. Mutex locks row in DB; Ledger seals update into 7-yr S3 WORM." },
      { swarm: "19 Consensus Quorum", kernel: "14 Grounding Certifier", cloud: "3 S3 Vault + 4 Database", desc: "Stage 3 & 7 require 10 of 12 votes for high-stakes POs. Every vote backed by Grounding proofs from S3 contract & Neptune DB graph." },
      { swarm: "20 Circuit Breaker", kernel: "10 Supervisor & 11 Mutex Lease", cloud: "7 EventBridge + 5 Lambda + 4 Database", desc: "Benches misbehaving stage releasing duplicate POs. Supervisor kills container; Mutex revokes DB write lock to protect chain." }
    ];

    const TRACE_UP_DATA = [
      { cloud: "1 Bedrock", kernel: "8 Propose-Decide", swarm: "16 Liaison Router", desc: "Forecast and Consensus draft models with Bedrock in Ring 3; Propose-Decide holds draft until decided, and Liaison routes to next pod." },
      { cloud: "2 AgentCore", kernel: "8 Propose-Decide", swarm: "16 Liaison Router", desc: "AgentCore with Cedar decides who may approve a Consensus uplift or PO release; checked on every pod hand-off." },
      { cloud: "3 S3 Vault", kernel: "12 Context Pager, 13 Episodic Ledger, 14 Grounding", swarm: "18 Whiteboard + 19 Consensus Quorum", desc: "Immutable 7-year WORM audit safe storing Ledger snapshots and Certifier proofs behind every Quorum ballot." },
      { cloud: "4 Database", kernel: "11 Mutex Lease & 14 Grounding Certifier", swarm: "18 Whiteboard + 19 Quorum + 20 Breaker", desc: "DynamoDB CAS mutex locks protect row edits; OpenSearch vectors and Neptune graph feed Certifier facts for voting." },
      { cloud: "5 Lambda", kernel: "9 Runbook & 10 Supervisor", swarm: "15 Topology + 17 Hop Limiter + 20 Breaker", desc: "Ephemeral 15-second sandbox for each stage computation. Supervisor kills container if Hop Limiter or Breaker trips." },
      { cloud: "6 Step Functions", kernel: "9 Runbook", swarm: "15 Topology", desc: "Runs the 11 stages in strict DAG order so each consumes previous output; rolls back cleanly if stage fails." },
      { cloud: "7 EventBridge", kernel: "10 Supervisor", swarm: "17 Hop Limiter + 20 Circuit Breaker", desc: "Pub/Sub bus delivering alerts only to subscribed stage owners when a trip or anomaly occurs." }
    ];

    let currentPreset = 0;
    let engineMode = "groq";
    let isRunning = false;
    let activeTraceView = "down";
    let packetT = 0;

    /* =========================================================================
       2. INITIALIZATION
       ========================================================================= */
    window.addEventListener('DOMContentLoaded', () => {
      initTheme();
      loadPreset(0);
      renderTraceCards();
      initCanvas();
      addAuditLog("System Bootstrap", "S&OP Swarm Coordinator online. 11 Stages mapped across 3 Pods.", "7a8f902c4b1e...");
    });

    function initTheme() {
      const saved = localStorage.getItem('sop_theme') || 'light';
      document.documentElement.setAttribute('data-theme', saved);
      updateThemeBtn(saved);
    }

    function toggleTheme() {
      const cur = document.documentElement.getAttribute('data-theme') || 'light';
      const nxt = cur === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', nxt);
      localStorage.setItem('sop_theme', nxt);
      updateThemeBtn(nxt);
      drawSwarmCanvas();
    }

    function updateThemeBtn(t) {
      document.getElementById('themeBtn').textContent = t === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode';
    }

    function setEngine(m) {
      engineMode = m;
      document.getElementById('btnGroq').classList.toggle('active', m === 'groq');
      document.getElementById('btnWebGpu').classList.toggle('active', m === 'webgpu');
      document.getElementById('btnSim').classList.toggle('active', m === 'sim');
      showToast(`AI Engine set to: ${m.toUpperCase()}`);
    }

    function saveKey() {
      const k = document.getElementById('apiKeyInput').value.trim();
      localStorage.setItem('groq_api_key', k);
      showToast("Groq API Key saved locally.");
    }

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 3500);
    }

    function switchTab(tabId) {
      document.querySelectorAll('.tab-item').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

      const map = {
        pipeline: { btn: 'tabBtnPipeline', pane: 'tabPipeline' },
        whiteboard: { btn: 'tabBtnWhiteboard', pane: 'tabWhiteboard' },
        quorum: { btn: 'tabBtnQuorum', pane: 'tabQuorum' },
        traceability: { btn: 'tabBtnTraceability', pane: 'tabTraceability' },
        audit: { btn: 'tabBtnAudit', pane: 'tabAudit' }
      };

      if (map[tabId]) {
        document.getElementById(map[tabId].btn).classList.add('active');
        document.getElementById(map[tabId].pane).classList.add('active');
        if (tabId === 'pipeline') setTimeout(drawSwarmCanvas, 50);
      }
    }

    /* =========================================================================
       3. S&OP PIPELINE CANVAS RENDERING
       ========================================================================= */
    function initCanvas() {
      const canvas = document.getElementById('swarmCanvas');
      if (canvas && canvas.parentElement) {
        canvas.width = canvas.parentElement.clientWidth - 32;
      }
      window.addEventListener('resize', () => {
        const c = document.getElementById('swarmCanvas');
        if (c && c.parentElement) {
          c.width = c.parentElement.clientWidth - 32;
          drawSwarmCanvas();
        }
      });
      drawSwarmCanvas();
    }

    function drawSwarmCanvas(activeStageIdx = -1) {
      const canvas = document.getElementById('swarmCanvas');
      if (!canvas) return;
      if (canvas.parentElement) {
        const targetW = canvas.parentElement.clientWidth - 32;
        if (targetW > 400 && Math.abs(canvas.width - targetW) > 5) {
          canvas.width = targetW;
        }
      }
      const ctx = canvas.getContext('2d');
      const w = canvas.width;
      const h = canvas.height;
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

      ctx.clearRect(0, 0, w, h);

      // Background
      ctx.fillStyle = isDark ? '#0f172a' : '#1e293b';
      ctx.fillRect(0, 0, w, h);

      const p1W = (w - 60) * 0.42;
      const p2W = (w - 60) * 0.34;
      const p3W = (w - 60) * 0.24;
      const p1X = 15;
      const p2X = p1X + p1W + 15;
      const p3X = p2X + p2W + 15;

      // Draw Pod Zones
      // Zone 1: Demand Pod (Stages 1-5)
      ctx.fillStyle = 'rgba(124, 58, 237, 0.12)';
      ctx.strokeStyle = '#7c3aed';
      ctx.lineWidth = 1.5;
      ctx.roundRect(p1X, 20, p1W, h - 40, 10);
      ctx.fill();
      ctx.stroke();
      ctx.fillStyle = '#c084fc';
      ctx.font = 'bold 11px Inter';
      ctx.textAlign = 'left';
      ctx.fillText('🟣 DEMAND POD (STAGES 1–5)', p1X + 15, 42);

      // Zone 2: Supply Pod (Stages 6-9)
      const isBreaker = (currentPreset === 2);
      ctx.fillStyle = isBreaker ? 'rgba(220, 38, 38, 0.12)' : 'rgba(37, 99, 235, 0.12)';
      ctx.strokeStyle = isBreaker ? '#ef4444' : '#2563eb';
      ctx.roundRect(p2X, 20, p2W, h - 40, 10);
      ctx.fill();
      ctx.stroke();
      ctx.fillStyle = isBreaker ? '#f87171' : '#60a5fa';
      ctx.fillText(isBreaker ? '🚨 SUPPLY POD (CIRCUIT BREAKER ARMED)' : '🔵 SUPPLY POD (STAGES 6–9)', p2X + 15, 42);

      // Zone 3: Control Pod (Stages 10-11)
      ctx.fillStyle = 'rgba(5, 150, 105, 0.12)';
      ctx.strokeStyle = '#059669';
      ctx.roundRect(p3X, 20, p3W, h - 40, 10);
      ctx.fill();
      ctx.stroke();
      ctx.fillStyle = '#34d399';
      ctx.fillText('🟢 CONTROL POD (10–11)', p3X + 15, 42);

      // Stage Node Coordinates
      const sc = SCENARIOS[currentPreset];
      const coords = [
        // Demand Pod
        { id: 1, x: p1X + p1W * 0.12, y: 110, name: "1. Aggregate", sub: sc.stages[0].val },
        { id: 2, x: p1X + p1W * 0.31, y: 195, name: "2. Forecast", sub: "Model Fit" },
        { id: 3, x: p1X + p1W * 0.51, y: 110, name: "3. Consensus", sub: sc.stages[2].volume },
        { id: 4, x: p1X + p1W * 0.70, y: 220, name: "4. Disaggregate", sub: "DC Allocation" },
        { id: 5, x: p1X + p1W * 0.88, y: 120, name: "5. Consumption", sub: sc.stages[4].volume },

        // Supply Pod
        { id: 6, x: p2X + p2W * 0.15, y: 185, name: "6. Dep Demand", sub: currentPreset === 1 ? "⚠️ +21d Lag" : "BOM Net" },
        { id: 7, x: p2X + p2W * 0.40, y: 105, name: "7. Firming", sub: currentPreset === 2 ? "🚨 Breaker #20" : "Orders Locked" },
        { id: 8, x: p2X + p2W * 0.65, y: 215, name: "8. Capacity", sub: currentPreset === 1 ? "⚡ Line 2 (98%)" : (currentPreset === 2 ? "⛔ Halted" : "94% SMT Pool") },
        { id: 9, x: p2X + p2W * 0.88, y: 125, name: "9. Inventory", sub: currentPreset === 1 ? "⚠️ 620 Buffer" : (currentPreset === 2 ? "⛔ Frozen" : "Buffer Stock") },

        // Control Pod
        { id: 10, x: p3X + p3W * 0.30, y: 145, name: "10. Monitor", sub: currentPreset === 1 ? "🚨 18.4% Breach" : (currentPreset === 2 ? "⛔ Contained" : "0.0% Nominal") },
        { id: 11, x: p3X + p3W * 0.75, y: 195, name: "11. Owner", sub: currentPreset === 1 ? "🚨 VP Escalate" : (currentPreset === 2 ? "🚨 CISO Alert" : "Lead Planner") }
      ];

      // Draw Connection Wires
      ctx.lineWidth = 2;
      for (let i = 0; i < coords.length - 1; i++) {
        const n1 = coords[i];
        const n2 = coords[i+1];

        const isInterPod = (i === 4 || i === 8);
        const isBlocked = (currentPreset === 2 && i >= 6);

        if (isBlocked) {
          ctx.strokeStyle = 'rgba(239, 68, 68, 0.35)';
          ctx.setLineDash([4, 4]);
        } else {
          ctx.strokeStyle = isInterPod ? '#f59e0b' : 'rgba(255,255,255,0.2)';
          ctx.setLineDash(isInterPod ? [6, 4] : []);
        }

        ctx.beginPath();
        ctx.moveTo(n1.x, n1.y);
        ctx.lineTo(n2.x, n2.y);
        ctx.stroke();

        // Draw Liaison Bridge Label
        if (isInterPod) {
          ctx.fillStyle = '#fbbf24';
          ctx.font = 'bold 9px JetBrains Mono';
          const mx = (n1.x + n2.x) / 2;
          const my = (n1.y + n2.y) / 2 - 8;
          ctx.fillText('Liaison Bridge', mx - 28, my);
        }
      }
      ctx.setLineDash([]);

      // Draw Packet Pulse if running
      if (activeStageIdx >= 0 && activeStageIdx < coords.length - 1) {
        const fromN = coords[activeStageIdx];
        const toN = coords[activeStageIdx + 1];
        const px = fromN.x + (toN.x - fromN.x) * packetT;
        const py = fromN.y + (toN.y - fromN.y) * packetT;

        ctx.save();
        ctx.beginPath();
        ctx.arc(px, py, 6, 0, Math.PI * 2);
        ctx.fillStyle = '#f59e0b';
        ctx.shadowColor = '#fbbf24';
        ctx.shadowBlur = 12;
        ctx.fill();
        ctx.restore();
      }

      // Draw Stage Nodes
      coords.forEach((n, idx) => {
        const isActive = idx === activeStageIdx;
        const isDone = activeStageIdx > idx;
        const st = sc.stages[idx];

        ctx.beginPath();
        ctx.arc(n.x, n.y, isActive ? 16 : 12, 0, Math.PI * 2);

        if (isActive) {
          ctx.fillStyle = '#f59e0b';
          ctx.shadowColor = '#fbbf24';
          ctx.shadowBlur = 15;
        } else if (isDone) {
          ctx.fillStyle = (st.status === 'blocked') ? '#dc2626' : ((st.status === 'warn') ? '#d97706' : '#10b981');
          ctx.shadowBlur = 0;
        } else {
          if (st.status === 'blocked') {
            ctx.fillStyle = '#ef4444';
          } else if (st.status === 'warn') {
            ctx.fillStyle = '#f59e0b';
          } else {
            ctx.fillStyle = idx < 5 ? '#a855f7' : (idx < 9 ? '#3b82f6' : '#10b981');
          }
          ctx.shadowBlur = 0;
        }

        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = (st.status === 'blocked') ? '#fca5a5' : '#ffffff';
        ctx.stroke();
        ctx.shadowBlur = 0;

        // Label
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 9px Inter';
        ctx.textAlign = 'center';
        ctx.fillText(n.name, n.x, n.y + 24);

        // Sublabel
        ctx.font = '8px JetBrains Mono';
        ctx.fillStyle = (st.status === 'blocked') ? '#f87171' : ((st.status === 'warn') ? '#fbbf24' : '#94a3b8');
        ctx.fillText(n.sub, n.x, n.y + 35);
      });
    }

    /* =========================================================================
       4. S&OP PLAN TABLE POPULATION
       ========================================================================= */
    function renderPlanTable() {
      const tbody = document.getElementById('planTableBody');
      if (!tbody) return;
      tbody.innerHTML = '';

      const sc = SCENARIOS[currentPreset];
      sc.stages.forEach(s => {
        const tr = document.createElement('tr');
        tr.id = `row-stage-${s.id}`;
        if (s.status === 'warn') tr.classList.add('row-warn');
        if (s.status === 'blocked') tr.classList.add('row-blocked');

        tr.innerHTML = `
          <td><strong>#${s.id} ${s.name}</strong></td>
          <td><span class="status-badge ${s.pod === 'demand' ? 'badge-info' : (s.pod === 'supply' ? 'badge-ok' : 'badge-warn')}">${s.pod.toUpperCase()}</span></td>
          <td style="font-family:var(--font-sans)">${s.desc}</td>
          <td><strong>${s.volume}</strong></td>
          <td style="color:${s.val.includes('$') ? '#059669' : (s.status === 'blocked' ? '#dc2626' : 'inherit')}">${s.val}</td>
          <td><span class="status-badge ${s.status === 'blocked' ? 'badge-danger' : (s.status === 'warn' ? 'badge-warn' : 'badge-info')}">${s.wire}</span></td>
          <td><span style="opacity:0.6">${s.status === 'blocked' ? '❌ REVOKED' : 'e3b0c442...'}</span></td>
        `;
        tbody.appendChild(tr);
      });
    }

    /* =========================================================================
       5. DUAL TRACEABILITY MATRIX RENDERING
       ========================================================================= */
    function setTraceView(view) {
      activeTraceView = view;
      document.getElementById('btnTraceDown').classList.toggle('active', view === 'down');
      document.getElementById('btnTraceUp').classList.toggle('active', view === 'up');
      renderTraceCards();
    }

    function renderTraceCards() {
      const container = document.getElementById('traceCardsContainer');
      if (!container) return;
      container.innerHTML = '';

      const data = activeTraceView === 'down' ? TRACE_DOWN_DATA : TRACE_UP_DATA;

      data.forEach(item => {
        const card = document.createElement('div');
        card.className = 'trace-card';

        if (activeTraceView === 'down') {
          card.innerHTML = `
            <div class="trace-flow">
              <span class="flow-badge t2">🟣 ${item.swarm}</span>
              <span class="flow-arrow">&rarr;</span>
              <span class="flow-badge t1">🔵 ${item.kernel}</span>
              <span class="flow-arrow">&rarr;</span>
              <span class="flow-badge t0">🟢 ${item.cloud}</span>
            </div>
            <div class="trace-desc">${item.desc}</div>
          `;
        } else {
          card.innerHTML = `
            <div class="trace-flow">
              <span class="flow-badge t0">🟢 ${item.cloud}</span>
              <span class="flow-arrow">&rarr;</span>
              <span class="flow-badge t1">🔵 ${item.kernel}</span>
              <span class="flow-arrow">&rarr;</span>
              <span class="flow-badge t2">🟣 ${item.swarm}</span>
            </div>
            <div class="trace-desc">${item.desc}</div>
          `;
        }

        container.appendChild(card);
      });
    }

    /* =========================================================================
       6. BYZANTINE CONSENSUS VOTING GRID & WHITEBOARD
       ========================================================================= */
    function renderQuorumGrid() {
      const sc = SCENARIOS[currentPreset];
      const q = sc.quorum;

      document.getElementById('quorumResultBadge').textContent = q.resultText;
      document.getElementById('quorumResultBadge').className = `status-badge ${q.resultClass}`;

      document.getElementById('proof1Title').textContent = q.proof1.title;
      document.getElementById('proof1Path').textContent = q.proof1.path;
      document.getElementById('proof1Status').textContent = q.proof1.status;
      document.getElementById('proof1Status').style.color = q.proof1.color;

      document.getElementById('proof2Title').textContent = q.proof2.title;
      document.getElementById('proof2Path').textContent = q.proof2.path;
      document.getElementById('proof2Status').textContent = q.proof2.status;
      document.getElementById('proof2Status').style.color = q.proof2.color;

      document.getElementById('proof3Title').textContent = q.proof3.title;
      document.getElementById('proof3Path').textContent = q.proof3.path;
      document.getElementById('proof3Status').textContent = q.proof3.status;
      document.getElementById('proof3Status').style.color = q.proof3.color;

      const grid = document.getElementById('quorumGrid');
      if (!grid) return;
      grid.innerHTML = '';

      q.votes.forEach(v => {
        const card = document.createElement('div');
        card.className = `vote-node-card ${v.yes ? 'yes' : 'no'}`;
        card.id = `vote-node-${v.id}`;
        card.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong>Agent Node #${v.id}</strong>
            <span class="status-badge ${v.yes ? 'badge-ok' : 'badge-danger'}">${v.yes ? 'YES ✔' : 'VETO ✖'}</span>
          </div>
          <div style="font-size:0.68rem; color:var(--text-muted)">Stage ${((v.id-1)%11)+1} Delegate</div>
          <div style="font-size:0.65rem; font-family:var(--font-mono); color:${v.yes ? '#059669' : '#dc2626'};">${v.reason}</div>
        `;
        grid.appendChild(card);
      });
    }

    function renderWhiteboard() {
      const sc = SCENARIOS[currentPreset];
      const w = sc.whiteboard;

      const dLane = document.getElementById('laneDemandContent');
      const sLane = document.getElementById('laneSupplyContent');
      const cLane = document.getElementById('laneControlContent');

      if (dLane) {
        dLane.innerHTML = w.demand.map(item => `
          <div style="background:var(--bg-card); padding:8px; border-radius:6px; border:1px solid var(--border-color); font-size:0.72rem;">
            <div><strong>${item.title}</strong> ${item.val}</div>
            <div style="color:var(--text-muted)">${item.sub}</div>
          </div>
        `).join('');
      }

      if (sLane) {
        sLane.innerHTML = w.supply.map(item => `
          <div style="background:var(--bg-card); padding:8px; border-radius:6px; border:1px solid var(--border-color); font-size:0.72rem;">
            <div><strong>${item.title}</strong> ${item.val}</div>
            <div style="color:var(--text-muted)">${item.sub}</div>
          </div>
        `).join('');
      }

      if (cLane) {
        cLane.innerHTML = w.control.map(item => `
          <div style="background:var(--bg-card); padding:8px; border-radius:6px; border:1px solid var(--border-color); font-size:0.72rem;">
            <div><strong>${item.title}</strong> ${item.val}</div>
            <div style="color:var(--text-muted)">${item.sub}</div>
          </div>
        `).join('');
      }

      document.getElementById('whiteboardLockStatus').textContent = (currentPreset === 2) ? 'MUTEX: REVOKED' : 'MUTEX: IDLE';
      document.getElementById('whiteboardLockStatus').className = (currentPreset === 2) ? 'status-badge badge-danger' : 'status-badge badge-ok';
    }

    function renderPills() {
      const sc = SCENARIOS[currentPreset];
      const p = sc.pills;

      const pD = document.getElementById('pillsDemand');
      const pS = document.getElementById('pillsSupply');
      const pC = document.getElementById('pillsControl');

      if (pD) {
        pD.innerHTML = p.demand.map(i => `<div class="stage-pill ${i.state}" id="pill-${i.id}"><span class="stage-num">${i.id}</span> ${i.name}</div>`).join('');
      }
      if (pS) {
        pS.innerHTML = p.supply.map(i => `<div class="stage-pill ${i.state}" id="pill-${i.id}"><span class="stage-num">${i.id}</span> ${i.name}</div>`).join('');
      }
      if (pC) {
        pC.innerHTML = p.control.map(i => `<div class="stage-pill ${i.state}" id="pill-${i.id}"><span class="stage-num">${i.id}</span> ${i.name}</div>`).join('');
      }
    }

    /* =========================================================================
       7. SCENARIO PRESETS SWITCHER
       ========================================================================= */
    function loadPreset(idx) {
      currentPreset = idx;
      document.querySelectorAll('.preset-btn').forEach((b, i) => b.classList.toggle('active', i === idx));
      const sc = SCENARIOS[idx];

      // Update Inputs
      document.getElementById('paramProduct').value = sc.product;
      document.getElementById('paramDemand').value = sc.demand;
      document.getElementById('paramUplift').value = sc.uplift;
      document.getElementById('paramBOM').value = sc.bom;

      // Update Topology Header
      document.getElementById('swarmTopologySubtext').textContent = sc.topologySubtext;
      document.getElementById('swarmStatusBadge').textContent = sc.badgeText;
      document.getElementById('swarmStatusBadge').className = `status-badge ${sc.badgeClass}`;

      // Update Telemetry
      document.getElementById('telemetryStage').textContent = `Stage 1 of 11: ${sc.stages[0].name}`;
      document.getElementById('telemetrySandbox').textContent = sc.telemetry.sandbox;
      document.getElementById('telemetryCedar').textContent = sc.telemetry.cedar;
      document.getElementById('telemetryMutex').textContent = sc.telemetry.mutex;
      document.getElementById('telemetryWorm').textContent = sc.telemetry.worm;

      // Re-render Views
      renderPills();
      renderPlanTable();
      renderWhiteboard();
      renderQuorumGrid();
      drawSwarmCanvas(-1);

      showToast(`Loaded Profile: ${sc.product}`);
      addAuditLog("Scenario Selected", `Active S&OP Profile switched to: ${sc.product}`, "b0e9a8f1...");
    }

    function resetPlanState() {
      loadPreset(currentPreset);
      showToast("Baseline plan state restored.");
    }

    /* =========================================================================
       8. SWARM SIMULATION & EXECUTION CONTROLLERS
       ========================================================================= */
    async function runSwarmExecution() {
      if (isRunning) return;
      isRunning = true;
      const btn = document.getElementById('btnRunSwarm');
      btn.disabled = true;
      btn.innerHTML = '<span>⏳ Executing Swarm...</span>';
      document.getElementById('swarmStatusBadge').textContent = 'SWARM EXECUTING';
      document.getElementById('swarmStatusBadge').className = 'status-badge badge-warn';

      const sc = SCENARIOS[currentPreset];
      showToast(`🚀 Initiating S&OP Swarm Execution for: ${sc.product}...`);

      for (let i = 0; i < sc.stages.length; i++) {
        const s = sc.stages[i];

        // Animate stage pill
        document.querySelectorAll('.stage-pill').forEach(p => p.classList.remove('active'));
        const pill = document.getElementById(`pill-${s.id}`);
        if (pill) pill.classList.add('active');

        // Update Telemetry
        document.getElementById('telemetryStage').textContent = `Stage ${s.id} of 11: ${s.name}`;
        document.getElementById('telemetrySandbox').textContent = `Running (${s.id * 1.2}s / 15s)`;
        document.getElementById('telemetrySandbox').className = 'status-badge badge-warn';

        // SCENARIO-SPECIFIC STEP EVENTS
        if (currentPreset === 0) {
          // NOMINAL FLOW
          if (s.id === 3) {
            document.getElementById('telemetryCedar').textContent = 'EVALUATING CEDAR...';
            document.getElementById('telemetryMutex').textContent = 'MUTEX: LOCKED (DDB CAS)';
            document.getElementById('telemetryMutex').className = 'status-badge badge-locked';
            document.getElementById('whiteboardLockStatus').textContent = 'MUTEX LOCKED: Stage 3 Consensus';
            document.getElementById('whiteboardLockStatus').className = 'status-badge badge-locked';
            addWhiteboardEntry('demand', `Stage 3 Consensus applied ${document.getElementById('paramUplift').value}. Cedar rule evaluated.`);
          } else if (s.id === 7) {
            document.getElementById('telemetryCedar').textContent = 'PERMIT (Ring 0)';
            document.getElementById('telemetryMutex').textContent = 'MUTEX: LOCKED (Row Lock)';
            addWhiteboardEntry('supply', `Stage 7 Firming committed planned orders: ${s.volume}.`);
          } else if (s.id === 10) {
            document.getElementById('telemetryMutex').textContent = 'UNLOCKED';
            document.getElementById('telemetryMutex').className = 'status-badge badge-ok';
            document.getElementById('whiteboardLockStatus').textContent = 'MUTEX: IDLE';
            document.getElementById('whiteboardLockStatus').className = 'status-badge badge-ok';
            addWhiteboardEntry('control', `Stage 10 Monitor: variance within tolerance bounds (+3.2%).`);
          }
        } else if (currentPreset === 1) {
          // WAFER PORT DELAY FLOW
          if (s.id === 6) {
            showToast("⚠️ Stage 6 Dep Demand: 21-day port transit delay detected!");
            addWhiteboardEntry('supply', "Stage 6 Alert: 16 Wafer packaging nodes delayed +21 days at port.");
          } else if (s.id === 7) {
            addWhiteboardEntry('supply', "Stage 7 Split POs: 60% Primary Fab, 40% Expedited Secondary (TSMC/ASE).");
          } else if (s.id === 8) {
            addWhiteboardEntry('supply', "Stage 8 Capacity: Secondary packaging line activated (+18% cost).");
          } else if (s.id === 10) {
            showToast("⚠️ Stage 10 Monitor: +18.4% variance threshold breach!");
            addWhiteboardEntry('control', "Stage 10 Monitor: +18.4% variance threshold breach flagged to Supervisor.");
          } else if (s.id === 11) {
            addWhiteboardEntry('control', "Stage 11 Owner: Dispatched high-priority incident to VP Global Supply Chain.");
          }
        } else if (currentPreset === 2) {
          // ROGUE AGENT CIRCUIT BREAKER ENGAGED
          if (s.id === 7) {
            // TRIP CIRCUIT BREAKER
            document.getElementById('telemetryCedar').textContent = '❌ CEDAR DENIED';
            document.getElementById('telemetryCedar').className = 'status-badge badge-danger';
            document.getElementById('telemetryMutex').textContent = '🚨 MUTEX REVOKED';
            document.getElementById('telemetryMutex').className = 'status-badge badge-danger';
            document.getElementById('telemetrySandbox').textContent = 'CONTAINER KILLED';
            document.getElementById('telemetrySandbox').className = 'status-badge badge-danger';
            document.getElementById('whiteboardLockStatus').textContent = 'MUTEX: REVOKED BY BREAKER';
            document.getElementById('whiteboardLockStatus').className = 'status-badge badge-danger';

            addWhiteboardEntry('supply', "🚨 CIRCUIT BREAKER #20 TRIPPED: Duplicate $10.0M PO blocked. CAS Mutex revoked.");
            addWhiteboardEntry('control', "🚨 Supervisor killed Stage 7 container. Zero corrupt state persisted.");

            const mockHash = "TAMPER_DETECTED_HASH_" + Math.random().toString(16).substring(2, 8);
            addAuditLog("Stage 7: Firming", "🚨 SECURITY TRIP: Duplicate $10.0M PO detected without contract receipt. Breaker #20 engaged.", mockHash);

            showToast("🚨 CIRCUIT BREAKER #20 ENGAGED! Rogue agent benched at Stage 7.");
            document.getElementById('swarmStatusBadge').textContent = 'CIRCUIT BREAKER ENGAGED 🚨';
            document.getElementById('swarmStatusBadge').className = 'status-badge badge-danger';

            drawSwarmCanvas(6);
            if (pill) {
              pill.classList.remove('active');
              pill.classList.add('blocked');
            }

            // Stop execution here to demonstrate safety containment
            btn.disabled = false;
            btn.innerHTML = '<span>🚀 Execute 11-Stage S&amp;OP Cycle</span>';
            isRunning = false;
            return;
          }
        }

        // Generate SHA-256 Mock hash
        const mockHash = Math.random().toString(16).substring(2, 10) + Math.random().toString(16).substring(2, 10);
        document.getElementById('telemetryWorm').textContent = mockHash.substring(0, 10) + '...';

        // Animate Canvas
        packetT = 0;
        for (let step = 0; step < 10; step++) {
          packetT = step / 10;
          drawSwarmCanvas(i);
          await sleep(35);
        }

        // Highlight table row
        document.querySelectorAll('#planTableBody tr').forEach(r => r.style.background = '');
        const activeRow = document.getElementById(`row-stage-${s.id}`);
        if (activeRow) activeRow.style.background = 'rgba(217, 119, 6, 0.15)';

        // Add to audit trail
        addAuditLog(`Stage ${s.id}: ${s.name}`, `Executed ${s.desc}. Telemetry certified via ${s.wire}.`, mockHash);

        if (pill) {
          pill.classList.remove('active');
          pill.classList.add('completed');
        }
        await sleep(300);
      }

      // Complete cycle
      if (currentPreset === 0) {
        document.getElementById('swarmStatusBadge').textContent = 'S&OP PLAN COMMITTED ✔';
        document.getElementById('swarmStatusBadge').className = 'status-badge badge-ok';
        showToast("✔ Full S&OP Swarm Cycle Completed! State synchronized to S3 WORM safe.");
      } else if (currentPreset === 1) {
        document.getElementById('swarmStatusBadge').textContent = 'PLAN COMMITTED WITH EXCEPTIONS ⚠️';
        document.getElementById('swarmStatusBadge').className = 'status-badge badge-warn';
        showToast("⚠️ S&OP Plan committed with expedited secondary sourcing plan.");
      }

      document.getElementById('telemetrySandbox').textContent = 'Sandboxes Disposed';
      document.getElementById('telemetrySandbox').className = 'status-badge badge-ok';
      btn.disabled = false;
      btn.innerHTML = '<span>🚀 Execute 11-Stage S&amp;OP Cycle</span>';
      isRunning = false;
      drawSwarmCanvas(-1);
    }

    function addWhiteboardEntry(lane, text) {
      const map = {
        demand: 'laneDemandContent',
        supply: 'laneSupplyContent',
        control: 'laneControlContent'
      };
      const c = document.getElementById(map[lane]);
      if (!c) return;
      const el = document.createElement('div');
      el.style.background = 'var(--bg-card)';
      el.style.padding = '8px';
      el.style.borderRadius = '6px';
      el.style.border = '1px solid var(--border-color)';
      el.style.fontSize = '0.72rem';
      el.innerHTML = `<div>${text}</div><div style="color:var(--text-muted); font-size:0.65rem;">Committed: ${new Date().toLocaleTimeString()}</div>`;
      c.prepend(el);
    }

    function addAuditLog(stage, event, hash) {
      const stream = document.getElementById('auditLogStream');
      if (!stream) return;
      const item = document.createElement('div');
      item.style.background = 'var(--bg-card)';
      item.style.padding = '8px 12px';
      item.style.borderRadius = '6px';
      item.style.border = '1px solid var(--border-color)';
      item.style.display = 'flex';
      item.style.justifyContent = 'space-between';
      item.innerHTML = `
        <div>
          <span style="color:var(--swarm-purple); font-weight:700;">[${stage}]</span>
          <span>${event}</span>
        </div>
        <div style="color:var(--cloud-green); font-size:0.65rem;">Block Hash: ${hash.substring(0,12)}...</div>
      `;
      stream.prepend(item);
    }

    function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }
  </script>
</body>
</html>
''')
    print("Successfully built updated sop_multi_agent_swarm_app.html!")

if __name__ == "__main__":
    build_app()
