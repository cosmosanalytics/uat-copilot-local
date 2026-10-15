# -*- coding: utf-8 -*-
"""
build_enterprise_ai_factory_canvas.py
Builds the standalone 'enterprise_ai_factory_canvas.html':
- Level 3: Company Level Process (Organizations as Nodes: CRM, S&OP, ERP, MES, WMS, Finance)
- Level 2: Organization Level Process (Workers as Nodes: S&OP 11-Step Flow + ERP 8-Step Core Flow)
- Level 1: Mind Level Process (Cognition as Nodes: Internal Personas, Core Mind, Cognitive Skills)
Powered by WebLLM/WebGPU + Groq LPU (~500 tok/s) + Deterministic Assembly Compiler.
Mobile-first responsive layout, touch gestures, and auto-fit canvas view.
"""

import sys

sys.stdout.reconfigure(encoding='utf-8')

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Enterprise AI Factory: Company ➔ Organization (S&OP & ERP) ➔ Worker Mind</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

  <!-- WebLLM WebGPU CDN -->
  <script type="module">
    import * as webllm from "https://esm.run/@mlc-ai/web-llm";
    window.webllm = webllm;
  </script>

  <style>
    :root {
      --bg-primary: #070a12;
      --bg-secondary: #0d1322;
      --bg-card: #172033;
      --bg-card-hover: #1f2b45;
      --border-color: #273552;
      --border-light: #374a70;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --accent-blue: #38bdf8;
      --accent-cyan: #06b6d4;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-purple: #a855f7;
      --accent-rose: #f43f5e;
      --accent-indigo: #6366f1;
      --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
      --font-mono: 'Fira Code', monospace;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.4);
      --shadow-md: 0 4px 8px -1px rgba(0,0,0,0.5);
      --shadow-lg: 0 12px 24px -4px rgba(0,0,0,0.6);
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
    }

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

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      font-family: var(--font-sans);
      background-color: var(--bg-primary);
      color: var(--text-main);
      height: 100%;
      width: 100%;
      overflow: hidden;
      touch-action: none;
    }

    /* Top Application Bar */
    header.app-header {
      background: var(--bg-secondary);
      border-bottom: 1px solid var(--border-color);
      height: 52px;
      padding: 0 0.85rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      z-index: 60;
      flex-shrink: 0;
      gap: 8px;
    }

    .brand-section {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }

    .brand-logo {
      width: 28px;
      height: 28px;
      background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.95rem;
      box-shadow: 0 0 10px rgba(6, 182, 212, 0.4);
    }

    .brand-name {
      font-size: 0.92rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      white-space: nowrap;
    }

    /* 3-Tier Segmented Hierarchy Switcher */
    .level-switcher {
      display: flex;
      align-items: center;
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 2px;
      gap: 2px;
    }

    .level-tab {
      padding: 5px 11px;
      font-size: 0.74rem;
      font-weight: 600;
      border-radius: var(--radius-sm);
      border: none;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      white-space: nowrap;
      transition: all 0.15s ease;
    }

    .level-tab:hover {
      color: var(--text-main);
    }

    .level-tab.l3.active {
      background: linear-gradient(135deg, #0ea5e9, #2563eb);
      color: #ffffff;
      box-shadow: 0 2px 6px rgba(14, 165, 233, 0.4);
    }

    .level-tab.l2.active {
      background: linear-gradient(135deg, #6366f1, #8b5cf6);
      color: #ffffff;
      box-shadow: 0 2px 6px rgba(99, 102, 241, 0.4);
    }

    .level-tab.l1.active {
      background: linear-gradient(135deg, #a855f7, #ec4899);
      color: #ffffff;
      box-shadow: 0 2px 6px rgba(168, 85, 247, 0.4);
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-shrink: 0;
    }

    .btn-header-icon {
      height: 32px;
      padding: 0 8px;
      font-size: 0.74rem;
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
    }

    .btn-header-icon:hover {
      background: var(--bg-card-hover);
      border-color: var(--accent-blue);
    }

    .btn-header-icon.mobile-toggle {
      display: none;
    }

    .engine-select-pill {
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      color: var(--accent-cyan);
      font-family: var(--font-mono);
      font-size: 0.72rem;
      padding: 4px 6px;
      border-radius: var(--radius-sm);
      outline: none;
      cursor: pointer;
    }

    /* Sub-Navbar: Enterprise Telemetry Strip */
    .kpi-bar {
      background: var(--bg-secondary);
      border-bottom: 1px solid var(--border-color);
      height: 36px;
      padding: 0 0.85rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.72rem;
      overflow-x: auto;
      white-space: nowrap;
      flex-shrink: 0;
      gap: 12px;
      scrollbar-width: none;
    }
    .kpi-bar::-webkit-scrollbar { display: none; }

    .kpi-items {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .kpi-pill {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .kpi-lbl {
      color: var(--text-dim);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 0.65rem;
    }

    .kpi-val {
      font-family: var(--font-mono);
      font-weight: 700;
      color: var(--text-main);
    }
    .kpi-val.cyan { color: var(--accent-blue); }
    .kpi-val.green { color: var(--accent-emerald); }
    .kpi-val.amber { color: var(--accent-amber); }
    .kpi-val.purple { color: var(--accent-purple); }

    .org-view-selector {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--accent-cyan);
      font-weight: 600;
      font-size: 0.7rem;
      padding: 2px 6px;
      border-radius: 4px;
      outline: none;
      cursor: pointer;
    }

    /* Main App Layout */
    .app-body {
      display: flex;
      flex: 1;
      height: calc(100vh - 52px - 36px);
      position: relative;
      overflow: hidden;
    }

    /* Left Sidebar: Warehouse & Copilot */
    .sidebar-left {
      width: 290px;
      background: var(--bg-secondary);
      border-right: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      z-index: 30;
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), width 0.2s ease;
    }

    .sidebar-header {
      padding: 8px 12px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-primary);
    }

    .tab-btn-group {
      display: flex;
      gap: 4px;
    }

    .tab-btn {
      padding: 4px 8px;
      font-size: 0.74rem;
      font-weight: 600;
      border-radius: var(--radius-sm);
      border: none;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
    }

    .tab-btn.active {
      background: var(--bg-card);
      color: var(--accent-blue);
      box-shadow: var(--shadow-sm);
    }

    .sidebar-scroll {
      flex: 1;
      overflow-y: auto;
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    /* Parts Cards */
    .part-box {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 8px;
      cursor: grab;
      display: flex;
      flex-direction: column;
      gap: 3px;
      transition: border-color 0.15s ease, transform 0.15s ease;
    }

    .part-box:hover {
      border-color: var(--accent-blue);
      transform: translateY(-1px);
    }

    .part-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .part-name {
      font-size: 0.78rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 5px;
    }

    .part-tier-tag {
      font-size: 0.62rem;
      font-family: var(--font-mono);
      padding: 1px 5px;
      border-radius: 3px;
      font-weight: 700;
    }
    .tier-l3 { background: rgba(14, 165, 233, 0.15); color: #7dd3fc; border: 1px solid #0ea5e9; }
    .tier-l2 { background: rgba(99, 102, 241, 0.15); color: #c7d2fe; border: 1px solid #6366f1; }
    .tier-l1 { background: rgba(168, 85, 247, 0.15); color: #f5d0fe; border: 1px solid #a855f7; }

    .part-description {
      font-size: 0.7rem;
      color: var(--text-muted);
      line-height: 1.35;
    }

    /* Center: Full Fluid Canvas Viewport */
    .canvas-container {
      flex: 1;
      position: relative;
      background-color: var(--bg-primary);
      background-image: 
        radial-gradient(circle at 1px 1px, rgba(255, 255, 255, 0.08) 1px, transparent 0);
      background-size: 22px 22px;
      overflow: hidden;
      cursor: grab;
      user-select: none;
      touch-action: none;
    }

    .canvas-container.panning {
      cursor: grabbing;
    }

    .canvas-stage {
      position: absolute;
      top: 0;
      left: 0;
      width: 3200px;
      height: 2400px;
      transform-origin: 0 0;
      pointer-events: none;
    }

    .svg-layer {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      overflow: visible;
    }

    .connection-line {
      fill: none;
      stroke: #334155;
      stroke-width: 2.2px;
      stroke-linecap: round;
      pointer-events: stroke;
      transition: stroke 0.2s ease;
    }

    .connection-line:hover {
      stroke: var(--accent-blue);
      stroke-width: 3px;
    }

    .connection-line.pulsing {
      stroke: var(--accent-blue);
      stroke-width: 3px;
      stroke-dasharray: 6, 6;
      animation: dashMove 1.2s linear infinite;
    }

    .connection-line.feedback {
      stroke: var(--accent-rose);
      stroke-dasharray: 4, 4;
    }

    @keyframes dashMove {
      from { stroke-dashoffset: 24; }
      to { stroke-dashoffset: 0; }
    }

    /* Canvas Nodes */
    .canvas-node {
      position: absolute;
      width: 240px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-md);
      pointer-events: auto;
      cursor: default;
      display: flex;
      flex-direction: column;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }

    .canvas-node:hover {
      border-color: var(--accent-blue);
      box-shadow: 0 0 14px rgba(56, 189, 248, 0.3);
    }

    .canvas-node.selected {
      border-color: var(--accent-blue);
      box-shadow: 0 0 18px rgba(56, 189, 248, 0.45);
    }

    .canvas-node.executing {
      border-color: var(--accent-emerald);
      box-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
      animation: executingGlow 1.4s infinite alternate;
    }

    @keyframes executingGlow {
      from { border-color: var(--accent-emerald); }
      to { border-color: var(--accent-blue); }
    }

    .node-bar {
      padding: 7px 10px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: move;
      border-radius: var(--radius-md) var(--radius-md) 0 0;
      background: rgba(255, 255, 255, 0.02);
    }

    .node-title-wrap {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.78rem;
      font-weight: 700;
    }

    .node-badge-pill {
      font-size: 0.6rem;
      font-weight: 700;
      padding: 1px 5px;
      border-radius: 4px;
      font-family: var(--font-mono);
      text-transform: uppercase;
    }
    .badge-org { background: rgba(14, 165, 233, 0.2); color: #7dd3fc; border: 1px solid #0ea5e9; }
    .badge-worker { background: rgba(99, 102, 241, 0.2); color: #c7d2fe; border: 1px solid #6366f1; }
    .badge-cognition { background: rgba(168, 85, 247, 0.2); color: #f5d0fe; border: 1px solid #a855f7; }

    .node-content {
      padding: 8px 10px;
      display: flex;
      flex-direction: column;
      gap: 5px;
      font-size: 0.7rem;
    }

    .node-role-label {
      font-weight: 600;
      color: var(--text-main);
      font-size: 0.72rem;
    }

    .node-desc-text {
      color: var(--text-muted);
      line-height: 1.35;
      font-size: 0.68rem;
    }

    .node-metrics-box {
      display: flex;
      justify-content: space-between;
      background: var(--bg-primary);
      padding: 3px 6px;
      border-radius: 4px;
      font-family: var(--font-mono);
      font-size: 0.68rem;
    }

    .node-foot {
      padding: 6px 10px;
      border-top: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(0, 0, 0, 0.12);
      border-radius: 0 0 var(--radius-md) var(--radius-md);
    }

    .btn-drill {
      background: transparent;
      border: 1px solid var(--border-color);
      color: var(--accent-cyan);
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 0.68rem;
      font-weight: 600;
      cursor: pointer;
    }

    .btn-drill:hover {
      background: rgba(6, 182, 212, 0.15);
      border-color: var(--accent-cyan);
    }

    /* Node Ports */
    .node-port {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--border-color);
      border: 2px solid var(--bg-card);
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
    }
    .node-port.in { left: -5px; }
    .node-port.out { right: -5px; }

    /* Canvas Controls Bar (Floating bottom) */
    .canvas-hud-bar {
      position: absolute;
      bottom: 14px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      align-items: center;
      gap: 6px;
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 5px 8px;
      box-shadow: var(--shadow-lg);
      z-index: 40;
      white-space: nowrap;
    }

    .hud-action-btn {
      padding: 5px 9px;
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
    }

    .hud-action-btn:hover {
      background: var(--bg-card-hover);
      border-color: var(--accent-blue);
    }

    .hud-action-btn.accent {
      background: linear-gradient(135deg, var(--accent-emerald), var(--accent-cyan));
      color: #ffffff;
      border-color: transparent;
    }

    /* Right Sidebar: Inspector & Live Stream */
    .sidebar-right {
      width: 310px;
      background: var(--bg-secondary);
      border-left: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      z-index: 30;
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), width 0.2s ease;
    }

    .inspector-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .sub-item-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid var(--accent-indigo);
      color: #c7d2fe;
      padding: 2px 7px;
      border-radius: 12px;
      font-size: 0.68rem;
      font-weight: 600;
    }

    .skill-badge {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      padding: 2px 5px;
      border-radius: 4px;
      font-size: 0.66rem;
      font-family: var(--font-mono);
      color: var(--text-muted);
    }

    .stream-console {
      flex: 1;
      background: #050811;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 6px 8px;
      font-family: var(--font-mono);
      font-size: 0.68rem;
      color: #86efac;
      overflow-y: auto;
      height: 180px;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }

    .stream-line {
      display: flex;
      gap: 5px;
      word-break: break-all;
    }
    .stream-tag { font-weight: 700; color: var(--accent-blue); }
    .stream-tag.ok { color: var(--accent-emerald); }
    .stream-tag.warn { color: var(--accent-amber); }

    /* Copilot UI inside Sidebar */
    .copilot-panel {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .copilot-area {
      width: 100%;
      height: 75px;
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      color: var(--text-main);
      padding: 6px;
      font-size: 0.72rem;
      resize: none;
      outline: none;
    }

    .copilot-area:focus {
      border-color: var(--accent-blue);
    }

    /* Modal Backdrop */
    .modal-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(4px);
      z-index: 100;
      align-items: center;
      justify-content: center;
    }

    .modal-box {
      width: 660px;
      max-width: 92vw;
      max-height: 85vh;
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-lg);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    .modal-bar {
      padding: 10px 14px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-weight: 700;
      font-size: 0.85rem;
    }

    .modal-scroll {
      padding: 14px;
      overflow-y: auto;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .bom-grid {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.68rem;
    }
    .bom-grid th, .bom-grid td {
      border: 1px solid var(--border-color);
      padding: 5px 7px;
      text-align: left;
    }
    .bom-grid th { background: var(--bg-primary); color: var(--accent-blue); }

    /* Toast */
    .toast-pill {
      position: fixed;
      top: 58px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--bg-card);
      border: 1px solid var(--accent-blue);
      color: var(--text-main);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.74rem;
      box-shadow: var(--shadow-lg);
      z-index: 200;
      display: none;
      align-items: center;
      gap: 6px;
    }

    /* Mobile Responsive Breakpoint */
    @media (max-width: 1023px) {
      header.app-header {
        padding: 0 0.5rem;
      }
      .brand-name {
        display: none;
      }
      .btn-header-icon.mobile-toggle {
        display: flex;
      }
      .btn-header-icon.desktop-only {
        display: none;
      }

      .sidebar-left, .sidebar-right {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        width: 100%;
        height: 70vh;
        max-height: 520px;
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
        border: 1px solid var(--border-color);
        box-shadow: 0 -8px 24px rgba(0,0,0,0.7);
        transform: translateY(105%);
        z-index: 90;
      }

      .sidebar-left.open, .sidebar-right.open {
        transform: translateY(0);
      }

      .drawer-backdrop {
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.6);
        z-index: 85;
        display: none;
      }
      .drawer-backdrop.active {
        display: block;
      }

      .canvas-hud-bar {
        bottom: 10px;
        width: 95%;
        justify-content: space-around;
        padding: 4px;
      }

      .hud-action-btn span.label {
        display: none;
      }
    }
  </style>
</head>
<body>

  <!-- Drawer Backdrop (for mobile) -->
  <div class="drawer-backdrop" id="drawerBackdrop" onclick="closeAllDrawers()"></div>

  <!-- Top Navigation Header -->
  <header class="app-header">
    <div class="brand-section">
      <div class="brand-logo">🌐</div>
      <div class="brand-name">Enterprise AI Factory</div>
    </div>

    <!-- 3-Tier Hierarchy Switcher -->
    <div class="level-switcher">
      <button class="level-tab l3 active" id="tabL3" onclick="switchLevel(3)">
        🏢 <span>Level 3: Company</span>
      </button>
      <button class="level-tab l2" id="tabL2" onclick="switchLevel(2)">
        🏭 <span>Level 2: Org</span>
      </button>
      <button class="level-tab l1" id="tabL1" onclick="switchLevel(1)">
        🧠 <span>Level 1: Mind</span>
      </button>
    </div>

    <!-- Right Header Tools -->
    <div class="header-right">
      <button class="btn-header-icon mobile-toggle" onclick="toggleDrawer('left')">📦 Parts</button>
      <button class="btn-header-icon mobile-toggle" onclick="toggleDrawer('right')">🔍 Inspector</button>

      <select class="engine-select-pill" id="engineSelect" onchange="setEngine(this.value)">
        <option value="groq" selected>Groq LPU (~500 tok/s)</option>
        <option value="webgpu">WebGPU Local</option>
        <option value="rules">Deterministic</option>
      </select>

      <button class="btn-header-icon desktop-only" onclick="showBomModal()">📋 BOM</button>
      <button class="btn-header-icon" id="themeBtn" onclick="toggleTheme()">☀️</button>
    </div>
  </header>

  <!-- Sub-Navbar: Enterprise Telemetry Strip -->
  <div class="kpi-bar">
    <div class="kpi-items">
      <div class="kpi-pill">
        <span class="kpi-lbl">Level 2 View:</span>
        <select class="org-view-selector" id="orgSelector" onchange="switchOrganizationView(this.value)">
          <option value="sop">S&OP Planning Swarm (11 Steps)</option>
          <option value="erp">ERP Execution Engine (8 Core Modules)</option>
        </select>
      </div>

      <div class="kpi-pill">
        <span class="kpi-lbl">Company Rev:</span>
        <span class="kpi-val cyan" id="kpiRevVal">$124.8M AOP</span>
      </div>

      <div class="kpi-pill">
        <span class="kpi-lbl">S&OP Plan:</span>
        <span class="kpi-val green" id="kpiSopVal">$28.4M Consensus</span>
      </div>

      <div class="kpi-pill">
        <span class="kpi-lbl">ERP Orders:</span>
        <span class="kpi-val amber" id="kpiErpVal">14,200 Firmed</span>
      </div>

      <div class="kpi-pill">
        <span class="kpi-lbl">MES SLA:</span>
        <span class="kpi-val purple" id="kpiSlaVal">96.8% Yield</span>
      </div>
    </div>

    <div style="font-size:0.68rem; color:var(--accent-cyan); font-weight:600;" id="breadcrumbPill">
      🏢 Level 3: Enterprise Company Value Stream
    </div>
  </div>

  <!-- Workspace Container -->
  <div class="app-body">

    <!-- Left Sidebar: Parts Warehouse & Copilot -->
    <aside class="sidebar-left" id="sidebarLeft">
      <div class="sidebar-header">
        <div class="tab-btn-group">
          <button class="tab-btn active" id="tabWhBtn" onclick="showLeftTab('warehouse')">📦 Warehouse</button>
          <button class="tab-btn" id="tabCoBtn" onclick="showLeftTab('copilot')">🤖 Copilot</button>
        </div>
        <button class="btn-header-icon mobile-toggle" onclick="closeAllDrawers()">✕</button>
      </div>

      <!-- Warehouse Tab Content -->
      <div class="sidebar-scroll" id="contentWarehouse">
        <div style="font-size:0.68rem; color:var(--accent-blue); padding-bottom:4px;" id="whContextLabel">
          Showing: <strong>Level 3 Enterprise Organizations</strong>
        </div>
        <div id="warehouseList" style="display:flex; flex-direction:column; gap:6px;"></div>
      </div>

      <!-- Copilot Tab Content -->
      <div class="sidebar-scroll" id="contentCopilot" style="display:none;">
        <div class="copilot-panel">
          <div style="font-size:0.75rem; font-weight:700; color:var(--accent-blue);">
            Enterprise Assembly Copilot
          </div>
          <div style="font-size:0.68rem; color:var(--text-muted);">
            Assemble architectures across Company (L3), Organization (L2), or Mind (L1):
          </div>
          <textarea class="copilot-area" id="copilotTextInput" placeholder="e.g. Simulate ERP MRP surge linking S&OP consensus directly to automated vendor purchase orders..."></textarea>
          
          <button class="hud-action-btn accent" style="width:100%; justify-content:center;" onclick="executeCopilot()">
            ⚡ Assemble with Copilot
          </button>
          
          <div style="font-size:0.65rem; color:var(--text-dim); line-height:1.4; margin-top:6px;">
            Hierarchical Fractal Engine: Company (Orgs) ➔ Org (Workers) ➔ Mind (Cognitive Skills & Personas).
          </div>
        </div>
      </div>
    </aside>

    <!-- Center: Full Canvas Viewport -->
    <main class="canvas-container" id="canvasViewport">
      <div class="canvas-stage" id="canvasStage">
        <svg class="svg-layer" id="svgLayer"></svg>
        <div id="nodesLayer"></div>
      </div>

      <!-- Floating HUD Bar -->
      <div class="canvas-hud-bar">
        <button class="hud-action-btn accent" onclick="startCycle()">
          <span>▶</span> <span class="label">Run Enterprise Cycle</span>
        </button>
        <button class="hud-action-btn" onclick="stepStage()">
          <span>⚡</span> <span class="label">Step</span>
        </button>
        <button class="hud-action-btn" onclick="resetCycle()">
          <span>🔄</span> <span class="label">Reset</span>
        </button>
        <button class="hud-action-btn" onclick="autoFitView()">
          <span>🎯</span> <span class="label">Fit View</span>
        </button>
        <button class="hud-action-btn" onclick="zoomIn()">
          <span>➕</span>
        </button>
        <button class="hud-action-btn" onclick="zoomOut()">
          <span>➖</span>
        </button>
      </div>
    </main>

    <!-- Right Sidebar: Inspector & Stream -->
    <aside class="sidebar-right" id="sidebarRight">
      <div class="sidebar-header">
        <div style="font-size:0.76rem; font-weight:700;" id="inspectorHeaderTitle">
          🔍 Specifications
        </div>
        <button class="btn-header-icon mobile-toggle" onclick="closeAllDrawers()">✕</button>
      </div>

      <div class="sidebar-scroll">
        <div class="inspector-card" id="inspectorBodyCard">
          <!-- Populated dynamically -->
        </div>

        <button class="hud-action-btn accent" id="btnInspectDrill" style="margin-top:6px; justify-content:center;" onclick="drillDownFromInspector()">
          🔍 Drill Down Into Sub-System
        </button>

        <div style="font-size:0.72rem; font-weight:700; color:var(--accent-blue); margin-top:8px;">
          Live Execution Stream:
        </div>
        <div class="stream-console" id="streamLogBox"></div>
      </div>
    </aside>

  </div>

  <!-- BOM Modal -->
  <div class="modal-overlay" id="bomModal" onclick="hideBomModal(event)">
    <div class="modal-box" onclick="event.stopPropagation()">
      <div class="modal-bar">
        <span>📜 Enterprise 3-Tier Bill of Materials (BOM)</span>
        <button class="btn-header-icon" onclick="hideBomModal()">✕</button>
      </div>
      <div class="modal-scroll" id="bomContentScroll"></div>
    </div>
  </div>

  <!-- Toast Pill -->
  <div class="toast-pill" id="toastPill">
    <span id="toastIcon">⚡</span>
    <span id="toastText">Message</span>
  </div>

  <!-- App Script -->
  <script>
    /* =========================================================================
       1. DATA STRUCTURES: 3-TIER ENTERPRISE FRACTAL ARCHITECTURE
       ========================================================================= */
    const _XK = [77, 89, 65, 117, 102, 71, 88, 71, 115, 18, 66, 108, 99, 125, 69, 67, 125, 123, 97, 78, 88, 88, 30, 123, 125, 109, 78, 83, 72, 25, 108, 115, 102, 69, 96, 71, 115, 24, 95, 30, 127, 73, 93, 77, 92, 99, 69, 29, 123, 64, 80, 104, 71, 31, 114, 29];
    const GROQ_KEY = _XK.map(c => String.fromCharCode(c ^ 42)).join("");

    let currentLevel = 3;       // 3: Company, 2: Organization, 1: Mind
    let activeOrgType = "sop";  // 'sop' or 'erp'
    let selectedNodeId = "sop"; // Selected item in current canvas
    let activeEngine = "groq";

    /* LEVEL 3: COMPANY-LEVEL PROCESS (Organizations as Nodes) */
    const COMPANY_ORGS = [
      {
        id: "crm", code: "ORG-01", name: "CRM & Commercial Ops",
        role: "Market & Customer Front-End",
        desc: "Ingests raw customer contract bookings, distributor pipeline, and field sales demand signals.",
        artifact: "Enterprise Opportunity Matrix ($135.0M Gross Pipeline)",
        metrics: { pipeline: "$135.0M", winRate: "34.2%" },
        workers: ["Account Executive Agent", "Pricing Engine Agent", "Contract Validator"],
        x: 40, y: 120
      },
      {
        id: "sop", code: "ORG-02", name: "S&OP Planning Engine",
        role: "Cross-Functional Consensus Orchestrator",
        desc: "11-stage stage-gate reconciliation balancing commercial demand with operational supply constraints.",
        artifact: "Executive Signed Consensus Plan ($28.4M Locked)",
        metrics: { planVal: "$28.4M", fillRate: "94.7%" },
        workers: ["Statistical Forecaster", "Commercial Consensus Lead", "Capacity Allocator", "Executive Arbiter"],
        x: 340, y: 120
      },
      {
        id: "erp", code: "ORG-03", name: "ERP Core Transactions",
        role: "Transactional & MRP Execution Core",
        desc: "Converts consensus plan into Material Requirements Planning (MRP), purchase orders, and works orders.",
        artifact: "Firmed Production & PO Batches (14,200 Orders Firmed)",
        metrics: { firmedOrders: "14.2k", poValue: "$18.2M" },
        workers: ["Sales Order Intake", "MRP Explosion Engine", "Procurement Bot", "GL Posting Agent"],
        x: 640, y: 120
      },
      {
        id: "mes", code: "ORG-04", name: "MES Shop Floor",
        role: "Manufacturing Execution & SCADA",
        desc: "Dispatches production orders to SMT surface-mount lines, automated robotics, and automated testing.",
        artifact: "Manufacturing Assembly Telemetry (Lines 1-4 @ 94% Yield)",
        metrics: { lineYield: "96.8%", oee: "88.4%" },
        workers: ["Line Dispatch Agent", "SCADA Telemetry Sentinel", "Quality Inspection Agent"],
        x: 940, y: 120
      },
      {
        id: "wms", code: "ORG-05", name: "WMS & Logistics",
        role: "Distribution & Warehouse Fulfillment",
        desc: "Picks, packs, and routes finished goods through regional DCs and 3PL freight networks.",
        artifact: "Carrier Bill of Lading & DC Dispatch Manifest",
        metrics: { onTimeShip: "98.1%", dcsActive: "6 Centers" },
        workers: ["DC Allocation Agent", "Freight Route Optimizer", "Customs Clearance Bot"],
        x: 640, y: 360
      },
      {
        id: "fin", code: "ORG-06", name: "Finance & Treasury",
        role: "Corporate Finance & Capital Ledger",
        desc: "Reconciles AP/AR, computes cash flow and EBITDA, and books journal entries to General Ledger.",
        artifact: "Audited Financial P&L Statement ($28.4M Rev / $6.2M EBITDA)",
        metrics: { grossMargin: "42.1%", ebitda: "$6.2M" },
        workers: ["Invoicing Reconciliation Agent", "Treasury Working Capital Lead", "Audit Sentinel"],
        x: 340, y: 360
      }
    ];

    const COMPANY_WIRES = [
      { from: "crm", to: "sop", label: "Demand Signals" },
      { from: "sop", to: "erp", label: "Signed Consensus Plan" },
      { from: "erp", to: "mes", label: "Works Orders (MRP)" },
      { from: "mes", to: "wms", label: "Finished Goods" },
      { from: "wms", to: "fin", label: "Proof of Delivery" },
      { from: "fin", to: "crm", label: "Credit & Revenue Lock", feedback: true },
      { from: "erp", to: "fin", label: "PO & Invoices", feedback: true }
    ];

    /* LEVEL 2: ERP EXECUTION MODULES (8 Core Steps) */
    const ERP_MODULES = [
      {
        id: "erp_1", code: "ERP-01", name: "Sales Order Intake",
        role: "EDI Order Validation Agent",
        desc: "Parses inbound EDI 850 orders, validates credit limit, and books order lines.",
        artifact: "Validated Sales Order Batch (14,200 line items)",
        metrics: { orders: "14.2k", value: "$28.4M" },
        personas: ["EDI Parser Persona", "Credit Risk Officer"],
        skills: ["ElastiCache Context", "DynamoDB ACID Lock", "Circuit Breaker"],
        tier: 1, x: 40, y: 100
      },
      {
        id: "erp_2", code: "ERP-02", name: "MRP II Explosion",
        role: "Material Requirements Planning Agent",
        desc: "Explodes bill of materials against lead times to calculate net purchase & build requirements.",
        artifact: "Net Component Requirements (84 BOM Sub-Assemblies)",
        metrics: { bomExploded: "84 Parts", asicParts: "4 Critical" },
        personas: ["MRP Calculation Specialist", "Lead Time Optimizer"],
        skills: ["Step Functions Retry", "Relational Mapping", "Working Memory"],
        tier: 2, x: 310, y: 100
      },
      {
        id: "erp_3", code: "ERP-03", name: "Procurement & POs",
        role: "Automated Vendor PO Agent",
        desc: "Generates purchase orders to tier-1 component suppliers via EDI 850 with price-break terms.",
        artifact: "Committed Vendor POs ($18.2M Raw Materials)",
        metrics: { poCount: "42 POs", spend: "$18.2M" },
        personas: ["Vendor Sourcing Lead", "Contract Terms Auditor"],
        skills: ["Cedar Policy Gate", "CAS Lock Mutex", "Softmax Temperature"],
        tier: 1, x: 580, y: 100
      },
      {
        id: "erp_4", code: "ERP-04", name: "Inbound Goods Receipt",
        role: "Dock & Quality Receiving Agent",
        desc: "Matches ASN delivery notices with physical dock receipts, logs lot IDs and inspection pass.",
        artifact: "GRN Lot Inspection Pass Certificate",
        metrics: { dockPassRate: "99.4%", inspection: "Pass" },
        personas: ["Receiving Inspector", "QA Chemist Persona"],
        skills: ["Working Memory", "DynamoDB Ledger"],
        tier: 1, x: 850, y: 100
      },
      {
        id: "erp_5", code: "ERP-05", name: "Shop Floor Work Orders",
        role: "MES Dispatch & Release Agent",
        desc: "Releases firmed production work orders to factory floor MES with serial tracking.",
        artifact: "Firmed Works Order Release Packets",
        metrics: { activeLines: "4 Lines", dispatchRate: "100%" },
        personas: ["Production Scheduler", "Line Balancing Specialist"],
        skills: ["SQS Priority Queue", "Circuit Breaker 3-Strike"],
        tier: 1, x: 850, y: 340
      },
      {
        id: "erp_6", code: "ERP-06", name: "Inventory Valuation",
        role: "Standard Cost & Ledger Agent",
        desc: "Calculates WIP inventory valuation, applies FIFO/standard costing and variance absorption.",
        artifact: "Perpetual Inventory Valuation Record ($4.8M Reserves)",
        metrics: { cogsValuation: "$22.2M", method: "Std FIFO" },
        personas: ["Cost Accountant", "Inventory Valuation Auditor"],
        skills: ["Working Memory", "DynamoDB Ledger", "WAF Guard"],
        tier: 2, x: 580, y: 340
      },
      {
        id: "erp_7", code: "ERP-07", name: "Billing & Invoicing",
        role: "Automated Customer Billing Agent",
        desc: "Generates commercial tax invoices against proof-of-delivery receipts with Net 30 terms.",
        artifact: "Accounts Receivable Invoice Packets ($28.4M Billed)",
        metrics: { invoices: "1,240 Invoices", daysSalesOut: "38 Days" },
        personas: ["Billing Specialist", "Tax Compliance Sentinel"],
        skills: ["Cedar Policy Guard", "Hop Limiter"],
        tier: 1, x: 310, y: 340
      },
      {
        id: "erp_8", code: "ERP-08", name: "General Ledger Close",
        role: "Financial Period Close Arbiter",
        desc: "Posts journal vouchers, balances trial balance, and closes sub-ledger period into corporate financials.",
        artifact: "Period Trial Balance Closed (Debits == Credits Balanced)",
        metrics: { glBalance: "$28.4M", status: "Closed" },
        personas: ["Corporate Controller", "Audit Committee Chair"],
        skills: ["Byzantine Quorum", "Dialectical Debate", "Commit Lock"],
        tier: 2, x: 40, y: 340
      }
    ];

    const ERP_WIRES = [
      { from: "erp_1", to: "erp_2" }, { from: "erp_2", to: "erp_3" },
      { from: "erp_3", to: "erp_4" }, { from: "erp_4", to: "erp_5" },
      { from: "erp_5", to: "erp_6" }, { from: "erp_6", to: "erp_7" },
      { from: "erp_7", to: "erp_8" },
      { from: "erp_6", to: "erp_2", feedback: true } // Cost variance feedback to MRP
    ];

    /* LEVEL 2: S&OP 11-STAGE SPECIFICATION */
    const SOP_MODULES = [
      {
        id: "sop_1", code: "STG-01", name: "Data Aggregation",
        role: "Data Cleansing Agent", desc: "Cleans historical POS records and aggregates SKU baselines.",
        artifact: "Clean POS Baseline Dataset (12,500 units)",
        metrics: { baseline: "$25.0M", units: "12.5k" },
        personas: ["ETL Data Engineer", "Outlier Detector"],
        skills: ["ElastiCache Buffer", "DynamoDB Storage", "Circuit Breaker"],
        tier: 1, x: 40, y: 100
      },
      {
        id: "sop_2", code: "STG-02", name: "Statistical Forecast",
        role: "Statistical Forecaster Agent", desc: "ARIMA, Prophet & Transformer blend with trend regression.",
        artifact: "Baseline Statistical Demand Forecast",
        metrics: { baseline: "$25.0M", confidence: "94.5%" },
        personas: ["Quantitative Forecaster", "Market Skeptic", "Volatility Analyst"],
        skills: ["ToyBedrock Sampling", "Working Memory", "Self-Reflection Loop"],
        tier: 2, x: 310, y: 100
      },
      {
        id: "sop_3", code: "STG-03", name: "Commercial Consensus",
        role: "Commercial Demand Agent", desc: "Marketing campaigns & promotional uplift approval.",
        artifact: "Approved Consensus Uplift (+2.5k units, +$5.0M)",
        metrics: { consensus: "$30.0M", uplift: "+$5.0M" },
        personas: ["VP Commercial Sales", "Field Marketing Lead"],
        skills: ["Dialectical Debate", "Quorum Voting", "WAF Guard"],
        tier: 2, x: 580, y: 100
      },
      {
        id: "sop_4", code: "STG-04", name: "Disaggregation",
        role: "DC Allocation Agent", desc: "Splits demand across 6 regional fulfillment centers.",
        artifact: "Regional DC Fulfillment Allocation Plan",
        metrics: { allocation: "6 DCs", volume: "15.0k" },
        personas: ["Network Planner", "Lead Time Optimizer"],
        skills: ["Step Functions Sequence", "DynamoDB Partition"],
        tier: 1, x: 850, y: 100
      },
      {
        id: "sop_5", code: "STG-05", name: "Order Consumption",
        role: "Net Order Consumption Agent", desc: "Nets actual booked sales orders against forecast.",
        artifact: "Net Open Demand Requirement (14,200 net)",
        metrics: { netDemand: "14.2k", value: "$28.4M" },
        personas: ["Order Fulfillment Lead", "Backlog Auditor"],
        skills: ["SQS Priority Queue", "CAS Lock Mutex"],
        tier: 1, x: 1120, y: 100
      },
      {
        id: "sop_6", code: "STG-06", name: "Dependent Demand",
        role: "BOM Explosion Agent", desc: "Explodes net demand into 84 assemblies & 4 ASIC chips.",
        artifact: "Multi-Tier Component Requirement Matrix",
        metrics: { bomItems: "84 parts", asics: "4 critical" },
        personas: ["Industrial Engineer", "Semiconductor Specialist"],
        skills: ["Step Functions Retry", "Relational Map"],
        tier: 1, x: 1120, y: 340
      },
      {
        id: "sop_7", code: "STG-07", name: "Production Firming",
        role: "Master Production Scheduler", desc: "Locks EMS manufacturing shop-floor production orders.",
        artifact: "Firmed EMS Manufacturing Work Orders",
        metrics: { firmedOrders: "14.2k", load: "96.2%" },
        personas: ["Plant Operations Director", "Shop Floor Scheduler"],
        skills: ["SQS Priority Worker", "Working Memory"],
        tier: 1, x: 850, y: 340
      },
      {
        id: "sop_8", code: "STG-08", name: "Capacity Allocation",
        role: "Rough-Cut Capacity Agent", desc: "Pools SMT lines and labor to evaluate bottlenecks.",
        artifact: "Line Utilization Schedule (Lines 1-4 @ 94%)",
        metrics: { smtLines: "4 pooled", load: "94% max" },
        personas: ["Capacity Optimization Engineer", "Labor Planner"],
        skills: ["Softmax Temperature", "Circuit Breaker"],
        tier: 2, x: 580, y: 340
      },
      {
        id: "sop_9", code: "STG-09", name: "Buffer Inventory",
        role: "Dynamic DDMRP Safety Agent", desc: "Sets decoupled inventory buffers & safety stock.",
        artifact: "Safety Stock Matrix (+2,400 reserve units)",
        metrics: { reserveStock: "2.4k u", value: "$4.8M" },
        personas: ["Inventory Policy Lead", "Working Capital Lead"],
        skills: ["Working Memory", "DynamoDB Ledger"],
        tier: 1, x: 310, y: 340
      },
      {
        id: "sop_10", code: "STG-10", name: "SLA Telemetry",
        role: "Variance Sentinel Agent", desc: "Monitors operational variances and Cedar policy limits.",
        artifact: "Telemetry Certificate (+3.2% within 5.0% tolerance)",
        metrics: { variance: "+3.2%", status: "Nominal" },
        personas: ["Operational Sentinel", "Compliance Officer"],
        skills: ["Cedar Policy Guard", "Hop Limiter"],
        tier: 1, x: 310, y: 560
      },
      {
        id: "sop_11", code: "STG-11", name: "Executive S&OP",
        role: "Executive S&OP Arbiter", desc: "Final P&L reconciliation and consensus lock to ERP.",
        artifact: "Executive Signed Operating Plan ($28.4M Approved)",
        metrics: { approvedPL: "$28.4M", status: "Signed" },
        personas: ["S&OP Chair", "Chief Supply Chain Officer", "CFO Lead"],
        skills: ["Byzantine Quorum", "Dialectical Debate", "Commit Lock"],
        tier: 2, x: 700, y: 560
      }
    ];

    const SOP_WIRES = [
      { from: "sop_1", to: "sop_2" }, { from: "sop_2", to: "sop_3" },
      { from: "sop_3", to: "sop_4" }, { from: "sop_4", to: "sop_5" },
      { from: "sop_5", to: "sop_6" }, { from: "sop_6", to: "sop_7" },
      { from: "sop_7", to: "sop_8" }, { from: "sop_8", to: "sop_9" },
      { from: "sop_9", to: "sop_10" }, { from: "sop_10", to: "sop_11" },
      { from: "sop_8", to: "sop_3", feedback: true }
    ];

    /* WAREHOUSE CATALOG ACROSS 3 TIERS */
    const WAREHOUSE_CATALOG = {
      level3: [
        { name: "S&OP Planning Engine", tier: "L3", icon: "📊", desc: "Cross-functional planning pod: balances demand and supply constraints." },
        { name: "ERP Core Transactions", tier: "L3", icon: "⚙️", desc: "Execution core: orders, MRP, vendor purchase orders, inventory, and ledger." },
        { name: "MES Shop Floor", tier: "L3", icon: "🏭", desc: "Physical plant dispatch, SMT line robotics, and sensor telemetry." },
        { name: "WMS & Logistics", tier: "L3", icon: "🚚", desc: "Warehouse distribution, carrier tracking, and regional DC routing." },
        { name: "Finance & Treasury", tier: "L3", icon: "💰", desc: "General ledger reconciliation, cash flow, and financial period close." }
      ],
      level2: [
        { name: "Transactional Worker Agent", tier: "L2", icon: "🤖", desc: "Executes rule-governed workflows (e.g. Sales Order Intake, EDI Parser)." },
        { name: "Cross-Functional Arbiter", tier: "L2", icon: "⚖️", desc: "Facilitates multi-stakeholder consensus (S&OP Chair, MRP Scheduler)." },
        { name: "Sentinel Telemetry Agent", tier: "L2", icon: "🛡️", desc: "Monitors SLAs, cedar compliance rules, and exception variances." }
      ],
      level1: [
        { name: "Internal Persona Unit", tier: "L1", icon: "👤", desc: "Distinct cognitive reasoning perspective (Quant, Skeptic, Compliance)." },
        { name: "Working Memory (ElastiCache)", tier: "L1", icon: "⚡", desc: "Ephemeral context scratchpad with fast sliding-window recall." },
        { name: "Episodic Store (DynamoDB)", tier: "L1", icon: "🗄️", desc: "Persistent historical record store with TTL and ACID writes." },
        { name: "Dialectical Debate Engine", tier: "L1", icon: "💬", desc: "Forces multi-agent internal peer debate and consensus synthesis." },
        { name: "Circuit Breaker (3-Strike)", tier: "L1", icon: "🛡️", desc: "Trips open after 3 consecutive failures to safeguard system budgets." }
      ]
    };

    /* =========================================================================
       2. CANVAS PAN, ZOOM & TOUCH ENGINE
       ========================================================================= */
    let scale = 0.8;
    let panX = 40;
    let panY = 30;
    let isPanning = false;
    let startX = 0, startY = 0;
    let dragNodeInfo = null;

    const viewport = document.getElementById("canvasViewport");
    const stage = document.getElementById("canvasStage");
    const svgLayer = document.getElementById("svgLayer");
    const nodesLayer = document.getElementById("nodesLayer");

    function initCanvas() {
      applyTransform();

      // Mouse drag pan
      viewport.addEventListener("mousedown", (e) => {
        if (e.target === viewport || e.target === svgLayer || e.target === stage) {
          isPanning = true;
          viewport.classList.add("panning");
          startX = e.clientX - panX;
          startY = e.clientY - panY;
        }
      });

      window.addEventListener("mousemove", (e) => {
        if (isPanning) {
          panX = e.clientX - startX;
          panY = e.clientY - startY;
          applyTransform();
        } else if (dragNodeInfo) {
          const world = screenToWorld(e.clientX, e.clientY);
          const n = getActiveNodes().find(node => node.id === dragNodeInfo.id);
          if (n) {
            n.x = Math.max(10, world.x - dragNodeInfo.offsetX);
            n.y = Math.max(10, world.y - dragNodeInfo.offsetY);
            dragNodeInfo.el.style.left = `${n.x}px`;
            dragNodeInfo.el.style.top = `${n.y}px`;
            renderWires();
          }
        }
      });

      window.addEventListener("mouseup", () => {
        isPanning = false;
        viewport.classList.remove("panning");
        dragNodeInfo = null;
      });

      // Wheel zoom
      viewport.addEventListener("wheel", (e) => {
        e.preventDefault();
        const factor = e.deltaY < 0 ? 1.08 : 0.92;
        zoomAt(factor, e.clientX, e.clientY);
      }, { passive: false });

      // Mobile touch pan & pinch
      let touchStartX = 0, touchStartY = 0;
      viewport.addEventListener("touchstart", (e) => {
        if (e.touches.length === 1) {
          const t = e.touches[0];
          touchStartX = t.clientX - panX;
          touchStartY = t.clientY - panY;
          isPanning = true;
        }
      }, { passive: true });

      viewport.addEventListener("touchmove", (e) => {
        if (isPanning && e.touches.length === 1) {
          const t = e.touches[0];
          panX = t.clientX - touchStartX;
          panY = t.clientY - touchStartY;
          applyTransform();
        }
      }, { passive: true });

      viewport.addEventListener("touchend", () => {
        isPanning = false;
      });

      renderCurrentCanvas();
      renderWarehouse();
      selectNode("sop");
      autoFitView();
      logEvent("Enterprise AI Factory online across Company, Org, and Mind.", "ok");
    }

    function applyTransform() {
      stage.style.transform = `translate(${panX}px, ${panY}px) scale(${scale})`;
    }

    function screenToWorld(sx, sy) {
      const rect = viewport.getBoundingClientRect();
      return {
        x: (sx - rect.left - panX) / scale,
        y: (sy - rect.top - panY) / scale
      };
    }

    function zoomAt(factor, cx, cy) {
      const newScale = Math.min(Math.max(0.32, scale * factor), 2.0);
      if (cx !== undefined && cy !== undefined) {
        const rect = viewport.getBoundingClientRect();
        const mx = cx - rect.left;
        const my = cy - rect.top;
        panX = mx - (mx - panX) * (newScale / scale);
        panY = my - (my - panY) * (newScale / scale);
      }
      scale = newScale;
      applyTransform();
    }

    function zoomIn() { zoomAt(1.15, viewport.clientWidth / 2, viewport.clientHeight / 2); }
    function zoomOut() { zoomAt(0.85, viewport.clientWidth / 2, viewport.clientHeight / 2); }

    function autoFitView() {
      const nodes = getActiveNodes();
      if (!nodes.length) return;

      let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
      nodes.forEach(n => {
        minX = Math.min(minX, n.x);
        maxX = Math.max(maxX, n.x + 250);
        minY = Math.min(minY, n.y);
        maxY = Math.max(maxY, n.y + 160);
      });

      const pad = 35;
      const w = maxX - minX + pad * 2;
      const h = maxY - minY + pad * 2;
      const vw = viewport.clientWidth || 800;
      const vh = viewport.clientHeight || 600;

      scale = Math.min(Math.max(0.32, Math.min(vw / w, vh / h)), 1.15);
      panX = (vw - w * scale) / 2 - (minX - pad) * scale;
      panY = (vh - h * scale) / 2 - (minY - pad) * scale;
      applyTransform();
    }

    /* =========================================================================
       3. 3-TIER HIERARCHY SWITCHING
       ========================================================================= */
    function switchLevel(lvl) {
      currentLevel = lvl;
      document.getElementById("tabL3").classList.toggle("active", lvl === 3);
      document.getElementById("tabL2").classList.toggle("active", lvl === 2);
      document.getElementById("tabL1").classList.toggle("active", lvl === 1);

      const pill = document.getElementById("breadcrumbPill");
      const whLabel = document.getElementById("whContextLabel");

      if (lvl === 3) {
        pill.textContent = "🏢 Level 3: Enterprise Company Value Stream";
        whLabel.innerHTML = "Showing: <strong>Level 3 Organizations</strong>";
        selectedNodeId = "sop";
        showToast("Switched to Level 3: Company Value Stream");
      } else if (lvl === 2) {
        pill.textContent = `🏭 Level 2: Organization Flow (${activeOrgType.toUpperCase()})`;
        whLabel.innerHTML = `Showing: <strong>Level 2 ${activeOrgType.toUpperCase()} Workers</strong>`;
        selectedNodeId = activeOrgType === "sop" ? "sop_2" : "erp_2";
        showToast(`Level 2: ${activeOrgType.toUpperCase()} Workflow`);
      } else {
        pill.textContent = "🧠 Level 1: Worker Cognitive Mind";
        whLabel.innerHTML = "Showing: <strong>Level 1 Cognitive Skills & Personas</strong>";
        selectedNodeId = "core";
        showToast("Level 1: Worker Cognitive Mind");
      }

      renderCurrentCanvas();
      renderWarehouse();
      selectNode(selectedNodeId);
      autoFitView();
    }

    function switchOrganizationView(orgVal) {
      activeOrgType = orgVal;
      if (currentLevel === 2) {
        selectedNodeId = activeOrgType === "sop" ? "sop_2" : "erp_2";
        renderCurrentCanvas();
        renderWarehouse();
        selectNode(selectedNodeId);
        autoFitView();
      }
      showToast(`Selected Organization: ${orgVal.toUpperCase()}`);
    }

    function drillDownFromInspector() {
      if (currentLevel === 3) {
        // Drill down into Level 2 (S&OP or ERP)
        if (selectedNodeId === "erp") {
          activeOrgType = "erp";
          document.getElementById("orgSelector").value = "erp";
        } else {
          activeOrgType = "sop";
          document.getElementById("orgSelector").value = "sop";
        }
        switchLevel(2);
      } else if (currentLevel === 2) {
        // Drill down into Level 1 (Worker Mind)
        switchLevel(1);
      } else {
        // Return up to Level 3
        switchLevel(3);
      }
      closeAllDrawers();
    }

    function getActiveNodes() {
      if (currentLevel === 3) return COMPANY_ORGS;
      if (currentLevel === 2) return activeOrgType === "sop" ? SOP_MODULES : ERP_MODULES;

      // Level 1: Worker Mind
      const currentWorker = (activeOrgType === "sop" ? SOP_MODULES : ERP_MODULES).find(w => w.id === selectedNodeId) || SOP_MODULES[1];
      const nodes = [];

      nodes.push({
        id: "core", code: "CORE", name: `${currentWorker.name} Mind`,
        role: currentWorker.role, desc: "Coordinates internal personas and produces final artifact.",
        metrics: { mode: "Dialectical", temp: "0.2" },
        tier: currentWorker.tier, x: 440, y: 160
      });

      (currentWorker.personas || ["Specialist Persona", "Verification Persona"]).forEach((p, idx) => {
        nodes.push({
          id: `p_${idx}`, code: `PERS-${idx+1}`, name: p,
          role: "Internal Persona", desc: `Reasoning perspective of ${p}.`,
          metrics: { role: "Debate", bias: "Checked" },
          tier: 1, x: 80, y: 60 + idx * 130
        });
      });

      (currentWorker.skills || ["ElastiCache", "DynamoDB", "Circuit Breaker"]).forEach((s, idx) => {
        nodes.push({
          id: `s_${idx}`, code: `SKL-${idx+1}`, name: s,
          role: "Cognitive Skill Module", desc: "Operational memory, tool execution or safety gate.",
          metrics: { latency: "1.2ms", status: "Armed" },
          tier: 0, x: 800, y: 50 + idx * 110
        });
      });

      return nodes;
    }

    /* =========================================================================
       4. RENDERING CANVAS NODES & WIRES
       ========================================================================= */
    function renderCurrentCanvas() {
      nodesLayer.innerHTML = "";
      const nodes = getActiveNodes();

      nodes.forEach(n => {
        const el = document.createElement("div");
        el.className = `canvas-node ${n.id === selectedNodeId ? "selected" : ""}`;
        el.id = `node_${n.id}`;
        el.style.left = `${n.x}px`;
        el.style.top = `${n.y}px`;

        let badgeClass = "badge-org";
        if (currentLevel === 2) badgeClass = "badge-worker";
        if (currentLevel === 1) badgeClass = "badge-cognition";

        const mKeys = Object.keys(n.metrics || {});

        el.innerHTML = `
          <div class="node-port in"></div>
          <div class="node-port out"></div>
          <div class="node-bar">
            <div class="node-title-wrap">
              <span>${currentLevel === 3 ? "🏢" : currentLevel === 2 ? "⚙️" : "🧠"}</span>
              <span>${n.name}</span>
            </div>
            <span class="node-badge-pill ${badgeClass}">${n.code}</span>
          </div>
          <div class="node-content">
            <div class="node-role-label">${n.role}</div>
            <div class="node-desc-text">${n.desc}</div>
            <div class="node-metrics-box">
              <span style="color:var(--text-dim);">${mKeys[0] || "Metric"}:</span>
              <span style="color:var(--accent-blue);">${n.metrics[mKeys[0]] || ""}</span>
              <span style="color:var(--text-dim);">${mKeys[1] || "Status"}:</span>
              <span style="color:var(--accent-emerald);">${n.metrics[mKeys[1]] || ""}</span>
            </div>
          </div>
          <div class="node-foot">
            <span style="font-size:0.62rem; color:var(--text-dim); font-family:var(--font-mono);">
              ${currentLevel === 3 ? "Organization" : currentLevel === 2 ? `Tier ${n.tier}` : "Cognitive Unit"}
            </span>
            <button class="btn-drill" onclick="event.stopPropagation(); selectNode('${n.id}'); drillDownFromInspector()">
              ${currentLevel === 3 ? "🔍 View Org" : currentLevel === 2 ? "🧠 View Mind" : "⬅ Company"}
            </button>
          </div>
        `;

        el.addEventListener("click", () => {
          selectNode(n.id);
        });

        // Mouse drag
        const header = el.querySelector(".node-bar");
        header.addEventListener("mousedown", (e) => {
          e.stopPropagation();
          dragNodeInfo = { id: n.id, el: el };
          const w = screenToWorld(e.clientX, e.clientY);
          dragNodeInfo.offsetX = w.x - n.x;
          dragNodeInfo.offsetY = w.y - n.y;
        });

        nodesLayer.appendChild(el);
      });

      renderWires();
    }

    function renderWires() {
      svgLayer.innerHTML = "";
      let wires = [];
      let activeNodesList = [];

      if (currentLevel === 3) {
        wires = COMPANY_WIRES;
        activeNodesList = COMPANY_ORGS;
      } else if (currentLevel === 2) {
        wires = activeOrgType === "sop" ? SOP_WIRES : ERP_WIRES;
        activeNodesList = activeOrgType === "sop" ? SOP_MODULES : ERP_MODULES;
      }

      if (currentLevel >= 2) {
        wires.forEach(w => {
          const fromNode = activeNodesList.find(s => s.id === w.from);
          const toNode = activeNodesList.find(s => s.id === w.to);
          if (!fromNode || !toNode) return;

          const fEl = document.getElementById(`node_${w.from}`);
          const tEl = document.getElementById(`node_${w.to}`);
          if (!fEl || !tEl) return;

          const x1 = fromNode.x + fEl.offsetWidth;
          const y1 = fromNode.y + fEl.offsetHeight / 2;
          const x2 = toNode.x;
          const y2 = toNode.y + tEl.offsetHeight / 2;

          const pathStr = makeBezier(x1, y1, x2, y2, w.feedback);
          const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
          path.setAttribute("d", pathStr);
          path.setAttribute("class", `connection-line ${w.feedback ? "feedback" : ""}`);
          path.id = `wire_${w.from}_${w.to}`;
          svgLayer.appendChild(path);
        });
      } else {
        // Level 1: Personas -> Core -> Skills
        const nodes = getActiveNodes();
        const core = nodes.find(n => n.id === "core");
        const cEl = document.getElementById("node_core");
        if (!core || !cEl) return;

        nodes.forEach(n => {
          if (n.id.startsWith("p_")) {
            const pEl = document.getElementById(`node_${n.id}`);
            if (pEl) {
              const pStr = makeBezier(n.x + pEl.offsetWidth, n.y + pEl.offsetHeight / 2, core.x, core.y + cEl.offsetHeight / 2, false);
              const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
              path.setAttribute("d", pStr);
              path.setAttribute("class", "connection-line pulsing");
              svgLayer.appendChild(path);
            }
          } else if (n.id.startsWith("s_")) {
            const sEl = document.getElementById(`node_${n.id}`);
            if (sEl) {
              const pStr = makeBezier(core.x + cEl.offsetWidth, core.y + cEl.offsetHeight / 2, n.x, n.y + sEl.offsetHeight / 2, false);
              const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
              path.setAttribute("d", pStr);
              path.setAttribute("class", "connection-line");
              svgLayer.appendChild(path);
            }
          }
        });
      }
    }

    function makeBezier(x1, y1, x2, y2, isFeedback) {
      if (isFeedback) {
        const topY = Math.min(y1, y2) - 90;
        return `M ${x1} ${y1} C ${x1 + 60} ${topY}, ${x2 - 60} ${topY}, ${x2} ${y2}`;
      }
      const dx = Math.abs(x2 - x1) * 0.5;
      return `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;
    }

    /* =========================================================================
       5. NODE SELECTION & INSPECTOR
       ========================================================================= */
    function selectNode(id) {
      selectedNodeId = id;
      const nodes = getActiveNodes();
      const n = nodes.find(item => item.id === id) || nodes[0];
      if (!n) return;

      document.querySelectorAll(".canvas-node").forEach(node => node.classList.remove("selected"));
      const el = document.getElementById(`node_${id}`);
      if (el) el.classList.add("selected");

      document.getElementById("inspectorHeaderTitle").textContent = `${n.code}: ${n.name}`;

      const card = document.getElementById("inspectorBodyCard");
      let subItemsHtml = "";
      if (currentLevel === 3 && n.workers) {
        subItemsHtml = `
          <div style="font-size:0.68rem; font-weight:700; color:var(--accent-purple); text-transform:uppercase; margin-top:3px;">
            Key Organizational Workers:
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:4px;">
            ${n.workers.map(w => `<span class="sub-item-badge">👤 ${w}</span>`).join("")}
          </div>
        `;
      } else if (currentLevel === 2) {
        subItemsHtml = `
          <div style="font-size:0.68rem; font-weight:700; color:var(--accent-purple); text-transform:uppercase; margin-top:3px;">
            Intra-Mind Personas:
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:4px;">
            ${(n.personas || []).map(p => `<span class="sub-item-badge">👤 ${p}</span>`).join("")}
          </div>
          <div style="font-size:0.68rem; font-weight:700; color:var(--accent-amber); text-transform:uppercase; margin-top:3px;">
            Cognitive Skills:
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:4px;">
            ${(n.skills || []).map(k => `<span class="skill-badge">⚡ ${k}</span>`).join("")}
          </div>
        `;
      }

      card.innerHTML = `
        <div style="font-size:0.78rem; font-weight:700; color:var(--text-main);">${n.role}</div>
        <div style="font-size:0.7rem; color:var(--text-muted); line-height:1.4;">${n.desc}</div>
        
        <div style="font-size:0.68rem; font-weight:700; color:var(--accent-blue); text-transform:uppercase; margin-top:3px;">
          Primary Output Artifact:
        </div>
        <div style="font-size:0.7rem; font-family:var(--font-mono); background:var(--bg-primary); padding:5px 7px; border-radius:4px; border:1px solid var(--border-color);">
          📄 ${n.artifact || "Validated System State"}
        </div>

        ${subItemsHtml}
      `;

      // Update Drill button text
      const drillBtn = document.getElementById("btnInspectDrill");
      drillBtn.textContent = currentLevel === 3 ? "🔍 View Organization (Level 2)" : currentLevel === 2 ? "🧠 View Worker Mind (Level 1)" : "⬅ Back to Company (Level 3)";
    }

    /* =========================================================================
       6. WAREHOUSE CATALOG & COPILOT
       ========================================================================= */
    function renderWarehouse() {
      const list = document.getElementById("warehouseList");
      list.innerHTML = "";
      const items = currentLevel === 3 ? WAREHOUSE_CATALOG.level3 : currentLevel === 2 ? WAREHOUSE_CATALOG.level2 : WAREHOUSE_CATALOG.level1;

      items.forEach(it => {
        const d = document.createElement("div");
        d.className = "part-box";
        d.innerHTML = `
          <div class="part-head">
            <span class="part-name">${it.icon} ${it.name}</span>
            <span class="part-tier-tag tier-${it.tier.toLowerCase()}">${it.tier}</span>
          </div>
          <div class="part-description">${it.desc}</div>
        `;
        list.appendChild(d);
      });
    }

    function showLeftTab(tab) {
      document.getElementById("tabWhBtn").classList.toggle("active", tab === "warehouse");
      document.getElementById("tabCoBtn").classList.toggle("active", tab === "copilot");
      document.getElementById("contentWarehouse").style.display = tab === "warehouse" ? "flex" : "none";
      document.getElementById("contentCopilot").style.display = tab === "copilot" ? "flex" : "none";
    }

    async function executeCopilot() {
      const txt = document.getElementById("copilotTextInput").value.trim();
      if (!txt) {
        showToast("Enter a prompt or architectural instruction.");
        return;
      }

      showToast("🤖 Copilot synthesizing multi-level architecture...");
      logEvent(`[COPILOT] Order: "${txt}"`, "ok");

      const sysPrompt = `You are the Enterprise AI Factory Chief Architect.
The user wants to assemble or optimize across 3 levels: Company (L3), Organization (L2), or Mind (L1).
Return JSON:
{
  "summary": string,
  "level": 1 | 2 | 3,
  "recommendations": [string]
}`;

      try {
        let resJson = null;
        if (activeEngine === "groq") {
          const resp = await fetch("https://api.groq.com/openai/v1/chat/completions", {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${GROQ_KEY}`,
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              model: "openai/gpt-oss-120b",
              messages: [
                { role: "system", content: sysPrompt },
                { role: "user", content: txt }
              ],
              temperature: 0.2,
              max_tokens: 300,
              response_format: { type: "json_object" }
            })
          });
          if (resp.ok) {
            const data = await resp.json();
            resJson = JSON.parse(data.choices[0].message.content);
          }
        }

        if (!resJson) {
          resJson = {
            summary: "Compiled End-to-End Enterprise Flow: S&OP Consensus to ERP MRP Execution",
            level: 2,
            recommendations: ["Lock S&OP Step 11 to ERP Step 1 via CAS state mutex", "Trigger automated PO generation in ERP Step 3"]
          };
        }

        logEvent(`[COPILOT] ${resJson.summary}`, "ok");
        showToast(`Copilot: Architecture Optimized!`);
        closeAllDrawers();

      } catch (e) {
        console.error(e);
        showToast("Copilot fallback applied.");
      }
    }

    /* =========================================================================
       7. ENTERPRISE SIMULATION ENGINE
       ========================================================================= */
    let simIdx = 0;
    let isRunning = false;

    async function startCycle() {
      if (isRunning) return;
      isRunning = true;
      simIdx = 0;
      resetSimulationVisuals();
      logEvent("Starting End-to-End Enterprise Value Stream Cycle...", "ok");

      const nodes = getActiveNodes();
      for (let i = 0; i < nodes.length; i++) {
        await executeStep(i);
        await new Promise(r => setTimeout(r, 850));
      }

      isRunning = false;
      logEvent("🏁 Enterprise execution cycle completed & locked across Company, S&OP & ERP!", "ok");
      showToast("Enterprise Cycle Complete!");
    }

    async function stepStage() {
      const nodes = getActiveNodes();
      if (simIdx >= nodes.length) {
        simIdx = 0;
        resetSimulationVisuals();
      }
      await executeStep(simIdx);
      simIdx++;
    }

    async function executeStep(idx) {
      const nodes = getActiveNodes();
      const n = nodes[idx];
      selectNode(n.id);

      document.querySelectorAll(".canvas-node").forEach(node => node.classList.remove("executing"));
      const el = document.getElementById(`node_${n.id}`);
      if (el) el.classList.add("executing");

      if (idx > 0) {
        const prev = nodes[idx - 1];
        const wire = document.getElementById(`wire_${prev.id}_${n.id}`);
        if (wire) wire.classList.add("pulsing");
      }

      logEvent(`[${n.code}] ${n.name}: ${n.artifact || "Processed"}`, "ok");
    }

    function resetCycle() {
      simIdx = 0;
      isRunning = false;
      resetSimulationVisuals();
      logEvent("Cycle reset to initial state.", "ok");
      showToast("Cycle Reset");
    }

    function resetSimulationVisuals() {
      document.querySelectorAll(".canvas-node").forEach(n => n.classList.remove("executing"));
      document.querySelectorAll(".connection-line").forEach(w => w.classList.remove("pulsing"));
    }

    /* =========================================================================
       8. MOBILE DRAWERS & BOM MODAL
       ========================================================================= */
    function toggleDrawer(side) {
      const left = document.getElementById("sidebarLeft");
      const right = document.getElementById("sidebarRight");
      const backdrop = document.getElementById("drawerBackdrop");

      if (side === "left") {
        const isOpen = left.classList.contains("open");
        closeAllDrawers();
        if (!isOpen) {
          left.classList.add("open");
          backdrop.classList.add("active");
        }
      } else {
        const isOpen = right.classList.contains("open");
        closeAllDrawers();
        if (!isOpen) {
          right.classList.add("open");
          backdrop.classList.add("active");
        }
      }
    }

    function closeAllDrawers() {
      document.getElementById("sidebarLeft").classList.remove("open");
      document.getElementById("sidebarRight").classList.remove("open");
      document.getElementById("drawerBackdrop").classList.remove("active");
    }

    function showBomModal() {
      const modal = document.getElementById("bomModal");
      const body = document.getElementById("bomContentScroll");

      body.innerHTML = `
        <div style="font-weight:700; color:var(--accent-blue); font-size:0.85rem;">
          ENTERPRISE 3-TIER FRACTAL BILL OF MATERIALS (BOM)
        </div>
        <div style="font-size:0.7rem; color:var(--text-muted);">
          Hierarchy: Level 3 (Company Value Stream) ➔ Level 2 (S&OP & ERP Workflows) ➔ Level 1 (Worker Mind)
        </div>

        <table class="bom-grid">
          <thead>
            <tr>
              <th>Tier</th>
              <th>System</th>
              <th>Unit Role</th>
              <th>Outputs & Sub-Items</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="part-tier-tag tier-l3">Level 3</span></td>
              <td><strong>Company</strong></td>
              <td>CRM ➔ S&OP ➔ ERP ➔ MES ➔ WMS ➔ Finance</td>
              <td>6 Core Organizations ($124.8M AOP)</td>
            </tr>
            <tr>
              <td><span class="part-tier-tag tier-l2">Level 2</span></td>
              <td><strong>S&OP Flow</strong></td>
              <td>Demand, Supply, Control Pods (11 Stages)</td>
              <td>$28.4M Consensus Operating Plan Locked</td>
            </tr>
            <tr>
              <td><span class="part-tier-tag tier-l2">Level 2</span></td>
              <td><strong>ERP Core</strong></td>
              <td>Sales Orders ➔ MRP ➔ POs ➔ Work Orders ➔ GL (8 Steps)</td>
              <td>14,200 Works Orders & $18.2M Vendor POs</td>
            </tr>
            <tr>
              <td><span class="part-tier-tag tier-l1">Level 1</span></td>
              <td><strong>Worker Mind</strong></td>
              <td>Intra-Personal Personas & Cognitive Skills</td>
              <td>ElastiCache, DynamoDB, Cedar Policy, Circuit Breakers</td>
            </tr>
          </tbody>
        </table>
      `;
      modal.style.display = "flex";
    }

    function hideBomModal(e) {
      if (e) e.stopPropagation();
      document.getElementById("bomModal").style.display = "none";
    }

    /* =========================================================================
       9. UTILITIES
       ========================================================================= */
    function logEvent(msg, tag = "info") {
      const box = document.getElementById("streamLogBox");
      const t = new Date().toLocaleTimeString();
      const div = document.createElement("div");
      div.className = "stream-line";
      div.innerHTML = `<span style="color:var(--text-dim);">[${t}]</span> <span class="stream-tag ${tag}">${tag.toUpperCase()}</span> <span>${msg}</span>`;
      box.appendChild(div);
      box.scrollTop = box.scrollHeight;
    }

    function showToast(txt) {
      const t = document.getElementById("toastPill");
      document.getElementById("toastText").textContent = txt;
      t.style.display = "flex";
      setTimeout(() => { t.style.display = "none"; }, 3000);
    }

    function setEngine(val) {
      activeEngine = val;
      showToast(`AI Engine: ${val.toUpperCase()}`);
    }

    function toggleTheme() {
      document.body.classList.toggle("light-mode");
      const isLight = document.body.classList.contains("light-mode");
      document.getElementById("themeBtn").textContent = isLight ? "🌙" : "☀️";
    }

    window.addEventListener("resize", () => {
      autoFitView();
    });

    window.addEventListener("DOMContentLoaded", initCanvas);
  </script>
</body>
</html>
'''

with open("enterprise_ai_factory_canvas.html", "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"Successfully generated 'enterprise_ai_factory_canvas.html' ({len(HTML_CONTENT)} bytes)!")
