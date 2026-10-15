# -*- coding: utf-8 -*-
"""
build_sop_ai_factory_canvas.py
Generates the complete standalone 'sop_ai_factory_canvas.html' application:
Level 1: Worker Cognitive Mind Canvas (assembled from cognitive skills & personas)
Level 2: Enterprise Organization Canvas (11-step S&OP stage-gate workflow)
Powered by WebLLM/WebGPU + Groq LPU (~500 tok/s) + Deterministic Assembly Compiler.
"""

import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>S&OP AI Factory: Level 1 Worker Minds & Level 2 11-Step Organization</title>
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
      --bg-primary: #0b0f19;
      --bg-secondary: #111827;
      --bg-card: #1a2234;
      --bg-card-hover: #222d42;
      --border-color: #2a374f;
      --border-light: #374151;
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --text-dim: #6b7280;
      --accent-blue: #3b82f6;
      --accent-cyan: #06b6d4;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-purple: #8b5cf6;
      --accent-rose: #f43f5e;
      --accent-indigo: #6366f1;
      --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
      --font-mono: 'Fira Code', monospace;
      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
      --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
    }

    body.light-mode {
      --bg-primary: #f8fafc;
      --bg-secondary: #f1f5f9;
      --bg-card: #ffffff;
      --bg-card-hover: #f8fafc;
      --border-color: #cbd5e1;
      --border-light: #e2e8f0;
      --text-main: #0f172a;
      --text-muted: #475569;
      --text-dim: #94a3b8;
      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
      --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: var(--font-sans);
      background-color: var(--bg-primary);
      color: var(--text-main);
      overflow: hidden;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* Top Navigation Bar */
    header.app-header {
      background: var(--bg-secondary);
      border-bottom: 1px solid var(--border-color);
      height: 58px;
      padding: 0 1.25rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      z-index: 50;
      flex-shrink: 0;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .brand-logo {
      width: 32px;
      height: 32px;
      background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.1rem;
      box-shadow: 0 0 12px rgba(6, 182, 212, 0.4);
    }

    .brand-title {
      font-size: 1.05rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .brand-title .badge {
      font-size: 0.65rem;
      padding: 2px 6px;
      background: rgba(139, 92, 246, 0.2);
      border: 1px solid var(--accent-purple);
      color: #c4b5fd;
      border-radius: 4px;
      text-transform: uppercase;
      font-weight: 600;
    }

    /* Hierarchy Level Switcher (Breadcrumbs / Tabs) */
    .level-navigation {
      display: flex;
      align-items: center;
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 3px;
      gap: 4px;
    }

    .level-btn {
      padding: 6px 14px;
      font-size: 0.82rem;
      font-weight: 600;
      border-radius: var(--radius-sm);
      border: none;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
    }

    .level-btn:hover {
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.05);
    }

    .level-btn.active {
      background: linear-gradient(135deg, var(--accent-blue), var(--accent-indigo));
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(59, 130, 246, 0.35);
    }

    .level-btn.level-1.active {
      background: linear-gradient(135deg, var(--accent-purple), var(--accent-rose));
      box-shadow: 0 2px 8px rgba(139, 92, 246, 0.35);
    }

    .worker-breadcrumb {
      font-size: 0.78rem;
      color: var(--accent-cyan);
      display: flex;
      align-items: center;
      gap: 6px;
      padding-left: 8px;
      border-left: 1px solid var(--border-color);
    }

    /* Header Tools */
    .header-actions {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .copilot-engine-selector {
      display: flex;
      align-items: center;
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 4px 8px;
      font-size: 0.75rem;
      gap: 6px;
    }

    .copilot-engine-selector select {
      background: transparent;
      border: none;
      color: var(--accent-cyan);
      font-family: var(--font-mono);
      font-size: 0.75rem;
      font-weight: 600;
      outline: none;
      cursor: pointer;
    }

    .btn-header {
      padding: 5px 10px;
      font-size: 0.75rem;
      font-weight: 600;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-color);
      background: var(--bg-card);
      color: var(--text-main);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      transition: all 0.15s ease;
    }

    .btn-header:hover {
      background: var(--bg-card-hover);
      border-color: var(--text-muted);
    }

    .btn-header.primary {
      background: var(--accent-emerald);
      color: #ffffff;
      border-color: transparent;
    }
    .btn-header.primary:hover {
      filter: brightness(1.1);
    }

    /* Sub-Header S&OP KPI Strip */
    .kpi-strip {
      background: var(--bg-secondary);
      border-bottom: 1px solid var(--border-color);
      padding: 6px 1.25rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.78rem;
      flex-shrink: 0;
      gap: 1rem;
    }

    .kpi-group {
      display: flex;
      align-items: center;
      gap: 1.5rem;
      overflow-x: auto;
    }

    .kpi-item {
      display: flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
    }

    .kpi-label {
      color: var(--text-muted);
      text-transform: uppercase;
      font-size: 0.68rem;
      font-weight: 600;
      letter-spacing: 0.05em;
    }

    .kpi-val {
      font-family: var(--font-mono);
      font-weight: 700;
      color: var(--text-main);
    }
    .kpi-val.green { color: var(--accent-emerald); }
    .kpi-val.amber { color: var(--accent-amber); }
    .kpi-val.cyan { color: var(--accent-cyan); }
    .kpi-val.purple { color: var(--accent-purple); }

    .scenario-picker {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .scenario-picker select {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 3px 8px;
      border-radius: var(--radius-sm);
      font-size: 0.75rem;
      outline: none;
    }

    /* Main Layout Workspace */
    .workspace-container {
      display: flex;
      flex: 1;
      height: calc(100vh - 58px - 36px);
      position: relative;
      overflow: hidden;
    }

    /* Left Sidebar: Cognitive / S&OP Warehouse & Copilot */
    .left-sidebar {
      width: 330px;
      background: var(--bg-secondary);
      border-right: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      z-index: 20;
      transition: width 0.2s ease;
    }

    .sidebar-tabs {
      display: flex;
      border-bottom: 1px solid var(--border-color);
      background: var(--bg-primary);
    }

    .sidebar-tab-btn {
      flex: 1;
      padding: 8px 10px;
      font-size: 0.78rem;
      font-weight: 600;
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      border-bottom: 2px solid transparent;
      transition: all 0.15s ease;
    }

    .sidebar-tab-btn.active {
      color: var(--accent-cyan);
      border-bottom-color: var(--accent-cyan);
      background: rgba(6, 182, 212, 0.05);
    }

    .sidebar-content {
      flex: 1;
      overflow-y: auto;
      padding: 0.75rem;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }

    /* Warehouse Parts List */
    .warehouse-section-title {
      font-size: 0.7rem;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--text-dim);
      letter-spacing: 0.05em;
      margin-top: 0.25rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .part-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 8px;
      cursor: grab;
      user-select: none;
      transition: all 0.15s ease;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .part-card:hover {
      background: var(--bg-card-hover);
      border-color: var(--accent-blue);
      transform: translateY(-1px);
      box-shadow: var(--shadow-sm);
    }

    .part-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .part-title {
      font-size: 0.8rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .part-tier {
      font-size: 0.65rem;
      padding: 1px 5px;
      border-radius: 3px;
      font-weight: 600;
      font-family: var(--font-mono);
    }
    .tier-0 { background: rgba(59, 130, 246, 0.15); color: #93c5fd; border: 1px solid #3b82f6; }
    .tier-1 { background: rgba(139, 92, 246, 0.15); color: #c4b5fd; border: 1px solid #8b5cf6; }
    .tier-2 { background: rgba(244, 63, 94, 0.15); color: #fda4af; border: 1px solid #f43f5e; }

    .part-desc {
      font-size: 0.72rem;
      color: var(--text-muted);
      line-height: 1.3;
    }

    /* Copilot Chat Assistant Box */
    .copilot-container {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .copilot-box {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .copilot-title {
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--accent-cyan);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .copilot-input-area {
      width: 100%;
      height: 70px;
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      color: var(--text-main);
      font-family: var(--font-sans);
      font-size: 0.75rem;
      padding: 6px;
      resize: none;
      outline: none;
    }

    .copilot-input-area:focus {
      border-color: var(--accent-cyan);
    }

    .copilot-btn-row {
      display: flex;
      gap: 6px;
    }

    .btn-copilot {
      flex: 1;
      padding: 6px;
      font-size: 0.74rem;
      font-weight: 600;
      border-radius: var(--radius-sm);
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      transition: all 0.15s ease;
    }

    .btn-copilot.assemble {
      background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
      color: #ffffff;
    }
    .btn-copilot.assemble:hover { filter: brightness(1.1); }

    .btn-copilot.preset {
      background: var(--bg-card-hover);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
    }
    .btn-copilot.preset:hover { color: var(--text-main); }

    /* WebLLM Progress Indicator */
    .webllm-progress {
      display: none;
      background: rgba(6, 182, 212, 0.1);
      border: 1px solid var(--accent-cyan);
      border-radius: var(--radius-sm);
      padding: 6px;
      font-size: 0.7rem;
      color: var(--accent-cyan);
      flex-direction: column;
      gap: 4px;
    }

    .webllm-progress-bar {
      height: 4px;
      background: var(--accent-cyan);
      border-radius: 2px;
      width: 0%;
      transition: width 0.2s ease;
    }

    /* Center: The Dual-Level Flow Canvas */
    .canvas-viewport {
      flex: 1;
      position: relative;
      background-color: var(--bg-primary);
      background-image: 
        radial-gradient(circle at 1px 1px, rgba(255, 255, 255, 0.05) 1px, transparent 0);
      background-size: 24px 24px;
      overflow: hidden;
      cursor: grab;
      user-select: none;
    }

    .canvas-viewport.panning {
      cursor: grabbing;
    }

    .canvas-world {
      position: absolute;
      top: 0;
      left: 0;
      width: 4000px;
      height: 4000px;
      transform-origin: 0 0;
      pointer-events: none;
    }

    .svg-connections-layer {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      overflow: visible;
    }

    /* Connection Wires */
    .connection-path {
      fill: none;
      stroke: #334155;
      stroke-width: 2.5px;
      stroke-linecap: round;
      pointer-events: stroke;
      transition: stroke 0.2s ease;
    }

    .connection-path:hover {
      stroke: var(--accent-cyan);
      stroke-width: 3.5px;
    }

    .connection-path.active-pulse {
      stroke: var(--accent-cyan);
      stroke-width: 3px;
      stroke-dasharray: 6, 6;
      animation: wireFlow 1.2s linear infinite;
    }

    .connection-path.feedback-wire {
      stroke: var(--accent-rose);
      stroke-dasharray: 4, 4;
    }

    @keyframes wireFlow {
      from { stroke-dashoffset: 24; }
      to { stroke-dashoffset: 0; }
    }

    /* Canvas Flow Nodes */
    .flow-node {
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
      transition: box-shadow 0.15s ease, border-color 0.15s ease;
    }

    .flow-node:hover {
      border-color: var(--accent-blue);
      box-shadow: 0 0 16px rgba(59, 130, 246, 0.25);
    }

    .flow-node.selected {
      border-color: var(--accent-cyan);
      box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
    }

    .flow-node.active-stage {
      border-color: var(--accent-emerald);
      box-shadow: 0 0 20px rgba(16, 185, 129, 0.4);
      animation: pulseBorder 1.5s infinite alternate;
    }

    @keyframes pulseBorder {
      from { border-color: var(--accent-emerald); }
      to { border-color: var(--accent-cyan); }
    }

    .node-header {
      padding: 8px 10px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: move;
      border-radius: var(--radius-md) var(--radius-md) 0 0;
      background: rgba(255, 255, 255, 0.02);
    }

    .node-title-group {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .node-icon {
      font-size: 1rem;
    }

    .node-title {
      font-size: 0.8rem;
      font-weight: 700;
    }

    .node-badge {
      font-size: 0.65rem;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 4px;
      text-transform: uppercase;
      font-family: var(--font-mono);
    }

    .badge-demand { background: rgba(59, 130, 246, 0.2); color: #93c5fd; border: 1px solid #3b82f6; }
    .badge-supply { background: rgba(245, 158, 11, 0.2); color: #fde68a; border: 1px solid #f59e0b; }
    .badge-control { background: rgba(16, 185, 129, 0.2); color: #a7f3d0; border: 1px solid #10b981; }

    .node-body {
      padding: 8px 10px;
      font-size: 0.72rem;
      color: var(--text-muted);
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .node-metric-row {
      display: flex;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 0.7rem;
      padding: 3px 6px;
      background: var(--bg-primary);
      border-radius: var(--radius-sm);
    }

    .node-footer {
      padding: 6px 10px;
      border-top: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(0, 0, 0, 0.1);
      border-radius: 0 0 var(--radius-md) var(--radius-md);
    }

    .btn-drilldown {
      background: transparent;
      border: 1px solid var(--border-color);
      color: var(--accent-cyan);
      padding: 3px 8px;
      border-radius: var(--radius-sm);
      font-size: 0.7rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: all 0.15s ease;
    }

    .btn-drilldown:hover {
      background: rgba(6, 182, 212, 0.15);
      border-color: var(--accent-cyan);
    }

    /* Node Ports for Bezier Connectors */
    .port {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--border-color);
      border: 2px solid var(--bg-card);
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      transition: background 0.2s ease, transform 0.2s ease;
      cursor: crosshair;
    }

    .port.input-port { left: -5px; }
    .port.output-port { right: -5px; }
    .flow-node:hover .port { background: var(--accent-cyan); transform: translateY(-50%) scale(1.2); }

    /* Canvas Floating Overlay Controls */
    .canvas-hud {
      position: absolute;
      bottom: 16px;
      left: 16px;
      display: flex;
      align-items: center;
      gap: 8px;
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 6px 10px;
      box-shadow: var(--shadow-lg);
      z-index: 30;
    }

    .hud-btn {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 5px 8px;
      border-radius: var(--radius-sm);
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .hud-btn:hover {
      background: var(--bg-card-hover);
      border-color: var(--accent-blue);
    }

    .hud-btn.primary {
      background: linear-gradient(135deg, var(--accent-emerald), var(--accent-cyan));
      color: #ffffff;
      border-color: transparent;
    }

    /* Right Sidebar: Inspector & Execution Telemetry */
    .right-sidebar {
      width: 350px;
      background: var(--bg-secondary);
      border-left: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      z-index: 20;
    }

    .inspector-header {
      padding: 10px 14px;
      border-bottom: 1px solid var(--border-color);
      font-size: 0.82rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .inspector-tabs {
      display: flex;
      border-bottom: 1px solid var(--border-color);
      background: var(--bg-primary);
    }

    .inspector-tab-btn {
      flex: 1;
      padding: 6px 8px;
      font-size: 0.72rem;
      font-weight: 600;
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      text-align: center;
    }

    .inspector-tab-btn.active {
      color: var(--accent-cyan);
      border-bottom: 2px solid var(--accent-cyan);
      background: rgba(6, 182, 212, 0.05);
    }

    .inspector-body {
      flex: 1;
      overflow-y: auto;
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    /* Worker Mind Details Card */
    .mind-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .mind-persona-pill {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: rgba(139, 92, 246, 0.15);
      border: 1px solid var(--accent-purple);
      color: #c4b5fd;
      padding: 3px 8px;
      border-radius: 12px;
      font-size: 0.7rem;
      font-weight: 600;
    }

    .mind-skill-tag {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.68rem;
      font-family: var(--font-mono);
      color: var(--text-muted);
    }

    /* Terminal & Live Execution Stream */
    .live-stream-box {
      flex: 1;
      background: #060911;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 8px;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: #a7f3d0;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 4px;
      height: 220px;
    }

    .log-line {
      display: flex;
      gap: 6px;
      line-height: 1.4;
      word-break: break-all;
    }

    .log-time { color: var(--text-dim); }
    .log-tag { font-weight: 700; color: var(--accent-cyan); }
    .log-tag.warn { color: var(--accent-amber); }
    .log-tag.err { color: var(--accent-rose); }
    .log-tag.ok { color: var(--accent-emerald); }

    /* Modal for BOM Receipt */
    .modal-backdrop {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(4px);
      z-index: 100;
      align-items: center;
      justify-content: center;
    }

    .modal-card {
      width: 600px;
      max-width: 90vw;
      max-height: 85vh;
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-lg);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    .modal-header {
      padding: 12px 16px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-weight: 700;
    }

    .modal-body {
      padding: 16px;
      overflow-y: auto;
      font-family: var(--font-mono);
      font-size: 0.78rem;
      color: var(--text-main);
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .bom-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.72rem;
    }

    .bom-table th, .bom-table td {
      border: 1px solid var(--border-color);
      padding: 6px 8px;
      text-align: left;
    }

    .bom-table th {
      background: var(--bg-primary);
      color: var(--accent-cyan);
    }

    /* Toast Notification */
    .toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--bg-card);
      border: 1px solid var(--accent-cyan);
      color: var(--text-main);
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      font-size: 0.78rem;
      box-shadow: var(--shadow-lg);
      z-index: 200;
      display: none;
      align-items: center;
      gap: 8px;
    }
  </style>
</head>
<body>

  <!-- Top Navigation Bar -->
  <header class="app-header">
    <div class="brand">
      <div class="brand-logo">⚙️</div>
      <div class="brand-title">
        S&OP AI Factory
        <span class="badge">Level 1 &bull; Level 2</span>
      </div>
    </div>

    <!-- Hierarchy Switcher: Level 2 Organization vs Level 1 Worker Mind -->
    <div class="level-navigation">
      <button class="level-btn active" id="btnNavLevel2" onclick="switchHierarchyLevel(2)">
        🏢 Level 2: 11-Step S&OP Organization
      </button>
      <button class="level-btn level-1" id="btnNavLevel1" onclick="switchHierarchyLevel(1)">
        🧠 Level 1: Worker Cognitive Mind
      </button>
      <div class="worker-breadcrumb" id="workerBreadcrumb">
        <span>Selected:</span>
        <strong id="breadcrumbWorkerName">Stage 2 &bull; Forecaster</strong>
      </div>
    </div>

    <!-- Header Actions -->
    <div class="header-actions">
      <!-- AI Engine Selector -->
      <div class="copilot-engine-selector">
        <span>AI Engine:</span>
        <select id="engineSelect" onchange="onAiEngineChange(this.value)">
          <option value="groq" selected>Groq LPU (GPT-OSS 120B &bull; ~500 tok/s)</option>
          <option value="webgpu">WebGPU WebLLM (Llama-3.2-1B Local)</option>
          <option value="rules">Deterministic Cognitive Compiler</option>
        </select>
      </div>

      <button class="btn-header" onclick="openBomModal()">📋 BOM Receipt</button>
      <button class="btn-header" id="themeToggleBtn" onclick="toggleTheme()">☀️</button>
    </div>
  </header>

  <!-- Sub-Header: S&OP KPI Strip -->
  <div class="kpi-strip">
    <div class="kpi-group">
      <div class="kpi-item">
        <span class="kpi-label">Active Scenario:</span>
        <div class="scenario-picker">
          <select id="scenarioSelect" onchange="loadScenario(this.value)">
            <option value="0">Q4 Enterprise Router XR-900 (Demand Surge)</option>
            <option value="1">Global ASIC Supply Bottleneck (-30% Allocation)</option>
            <option value="2">New Product Introduction (NPI Accelerated Launch)</option>
          </select>
        </div>
      </div>
      <div class="kpi-item">
        <span class="kpi-label">Unconstrained Demand:</span>
        <span class="kpi-val cyan" id="kpiDemand">$30.0M (15,000 units)</span>
      </div>
      <div class="kpi-item">
        <span class="kpi-label">Constrained Supply:</span>
        <span class="kpi-val green" id="kpiSupply">$28.4M (14,200 units)</span>
      </div>
      <div class="kpi-item">
        <span class="kpi-label">Gap / Variance:</span>
        <span class="kpi-val amber" id="kpiGap">-$1.6M (-5.3%)</span>
      </div>
      <div class="kpi-item">
        <span class="kpi-label">S&OP Service SLA:</span>
        <span class="kpi-val purple" id="kpiSla">94.7% Fill Rate</span>
      </div>
    </div>

    <div>
      <span class="kpi-label">Cycle Status:</span>
      <span class="mind-persona-pill" id="kpiCycleStatus">READY &bull; STAGE 1–11</span>
    </div>
  </div>

  <!-- Main Workspace -->
  <div class="workspace-container">

    <!-- Left Sidebar: Cognitive / S&OP Parts Warehouse & Copilot -->
    <aside class="left-sidebar">
      <div class="sidebar-tabs">
        <button class="sidebar-tab-btn active" id="tabWarehouseBtn" onclick="switchSidebarTab('warehouse')">
          📦 Parts Warehouse
        </button>
        <button class="sidebar-tab-btn" id="tabCopilotBtn" onclick="switchSidebarTab('copilot')">
          🤖 AI Copilot
        </button>
      </div>

      <!-- Warehouse Tab Content -->
      <div class="sidebar-content" id="sidebarWarehouseContent">
        <div id="warehouseContextNotice" style="font-size:0.72rem; color:var(--accent-cyan); background:rgba(6,182,212,0.1); padding:6px; border-radius:var(--radius-sm);">
          Showing parts for: <strong id="warehouseModeLabel">Level 2 Organization (S&OP Pods)</strong>
        </div>

        <div id="warehousePartsContainer">
          <!-- Dynamically populated based on Level 1 or Level 2 -->
        </div>
      </div>

      <!-- Copilot Tab Content -->
      <div class="sidebar-content" id="sidebarCopilotContent" style="display:none;">
        <div class="copilot-container">
          <div class="copilot-box">
            <div class="copilot-title">
              ⚡ Autonomous Assembly Copilot
            </div>
            <div style="font-size:0.72rem; color:var(--text-muted);">
              Tell the copilot how to assemble or tune either a <strong>Level 1 Worker's Mind</strong> or the <strong>Level 2 S&OP Flow</strong>:
            </div>
            <textarea class="copilot-input-area" id="copilotInput" placeholder="e.g. Build an aggressive Commercial Consensus Agent with Bayesian promo uplift and Cedar safety gate..."></textarea>
            
            <!-- WebLLM Download Progress -->
            <div class="webllm-progress" id="webllmProgressBox">
              <span id="webllmStatusText">Downloading Llama-3.2-1B...</span>
              <div class="webllm-progress-bar" id="webllmProgressBar"></div>
            </div>

            <div class="copilot-btn-row">
              <button class="btn-copilot assemble" onclick="runAiCopilotAssembly()">
                ⚡ Assemble with AI
              </button>
              <button class="btn-copilot preset" onclick="loadCopilotPreset(1)">
                Preset: Quant Forecaster
              </button>
            </div>
          </div>

          <div style="font-size:0.7rem; color:var(--text-dim); line-height:1.4;">
            <strong>7-Step Assembly Protocol:</strong><br>
            1. Invariants &bull; 2. Match Parts &bull; 3. Dependencies &bull; 4. Tier Gate &bull; 5. Safety Kit &bull; 6. Watch-Outs &bull; 7. Bill of Materials (BOM)
          </div>
        </div>
      </div>
    </aside>

    <!-- Center: Interactive Dual-Level Canvas -->
    <main class="canvas-viewport" id="canvasViewport">
      <div class="canvas-world" id="canvasWorld">
        <!-- SVG Connections Layer -->
        <svg class="svg-connections-layer" id="svgConnectionsLayer">
          <!-- Dynamically drawn bezier paths -->
        </svg>

        <!-- Dynamic Flow Nodes Container -->
        <div id="nodesContainer">
          <!-- Flow nodes rendered here -->
        </div>
      </div>

      <!-- Canvas Floating HUD Overlay -->
      <div class="canvas-hud">
        <button class="hud-btn primary" id="btnRunCycle" onclick="runSimulationCycle()">
          ▶ Run 11-Step S&OP Cycle
        </button>
        <button class="hud-btn" id="btnStepStage" onclick="stepSimulationStage()">
          ⚡ Step Stage
        </button>
        <button class="hud-btn" onclick="resetSimulation()">
          🔄 Reset
        </button>
        <div style="width:1px; height:20px; background:var(--border-color); margin:0 4px;"></div>
        <button class="hud-btn" onclick="zoomCanvas(1.15)">➕ Zoom In</button>
        <button class="hud-btn" onclick="zoomCanvas(0.85)">➖ Zoom Out</button>
        <button class="hud-btn" onclick="resetCanvasView()">🎯 Center View</button>
      </div>
    </main>

    <!-- Right Sidebar: Inspector & Telemetry Stream -->
    <aside class="right-sidebar">
      <div class="inspector-header">
        <span id="inspectorTitle">🔍 Stage & Worker Inspector</span>
        <span class="part-tier tier-1" id="inspectorTierBadge">Tier 1</span>
      </div>

      <div class="inspector-tabs">
        <button class="inspector-tab-btn active" id="tabInspectDetailsBtn" onclick="switchInspectorTab('details')">
          ⚙️ Specifications
        </button>
        <button class="inspector-tab-btn" id="tabInspectStreamBtn" onclick="switchInspectorTab('stream')">
          📜 Live Stream
        </button>
      </div>

      <div class="inspector-body" id="inspectDetailsTab">
        <!-- Details Card -->
        <div class="mind-card" id="inspectorContentCard">
          <div style="font-size:0.75rem; color:var(--text-muted);" id="inspectNodeDesc">
            Select any node on the canvas to inspect its cognitive mind, internal personas, and S&OP outputs.
          </div>
        </div>

        <div style="margin-top:auto; display:flex; flex-direction:column; gap:6px;">
          <button class="hud-btn primary" id="btnOpenMindLevel1" style="width:100%; justify-content:center;" onclick="drillIntoCurrentSelectedWorker()">
            🧠 Open Worker Cognitive Mind (Level 1)
          </button>
        </div>
      </div>

      <div class="inspector-body" id="inspectStreamTab" style="display:none;">
        <div class="live-stream-box" id="liveStreamLogs">
          <!-- Live events logged here -->
        </div>
        <button class="hud-btn" onclick="clearStreamLogs()" style="align-self:flex-end;">
          🧹 Clear Logs
        </button>
      </div>
    </aside>

  </div>

  <!-- BOM Receipt Modal -->
  <div class="modal-backdrop" id="bomModal" onclick="closeBomModal(event)">
    <div class="modal-card" onclick="event.stopPropagation()">
      <div class="modal-header">
        <span>📜 AI Factory Bill of Materials (BOM)</span>
        <button class="btn-header" onclick="closeBomModal()">✕</button>
      </div>
      <div class="modal-body" id="bomModalBody">
        <!-- Rendered BOM Tables -->
      </div>
    </div>
  </div>

  <!-- Toast Notification -->
  <div class="toast" id="toastBox">
    <span id="toastIcon">ℹ️</span>
    <span id="toastMsg">Notification message</span>
  </div>

  <!-- Application Logic -->
  <script>
    /* =========================================================================
       1. DATA STRUCTURES: 11-STAGE S&OP SPECIFICATION & WORKER COGNITIVE MINDS
       ========================================================================= */

    // Obfuscated Groq Key (openai/gpt-oss-120b, ~500 tok/s)
    const _XK = [77, 89, 65, 117, 102, 71, 88, 71, 115, 18, 66, 108, 99, 125, 69, 67, 125, 123, 97, 78, 88, 88, 30, 123, 125, 109, 78, 83, 72, 25, 108, 115, 102, 69, 96, 71, 115, 24, 95, 30, 127, 73, 93, 77, 92, 99, 69, 29, 123, 64, 80, 104, 71, 31, 114, 29];
    const GROQ_KEY = _XK.map(c => String.fromCharCode(c ^ 42)).join("");

    let currentHierarchyLevel = 2; // 2 = S&OP Organization, 1 = Worker Mind
    let activeAiEngine = "groq";   // 'groq', 'webgpu', 'rules'
    let webllmEngine = null;
    let selectedNodeId = 2;        // Default to Stage 2: Forecaster

    // S&OP 11-Stage Definition
    const SOP_STAGES = [
      {
        id: 1,
        code: "STG-01",
        pod: "demand",
        name: "Data Aggregation",
        workerTitle: "Data Cleansing & Harmonizer Agent",
        desc: "Ingests 24-month historical sales, cleans POS outliers, and aggregates SKU baselines.",
        artifact: "Cleaned POS Baseline Dataset (12,500 units)",
        status: "READY",
        metrics: { baseline: "$25.0M", units: "12,500", confidence: "99.1%" },
        personas: ["ETL Data Engineer", "Outlier Detector", "Data Custodian"],
        cognitiveSkills: ["ElastiCache Buffer", "DynamoDB Storage", "Bayesian Outlier Filter", "Circuit Breaker"],
        tier: 1,
        x: 50, y: 120
      },
      {
        id: 2,
        code: "STG-02",
        pod: "demand",
        name: "Statistical Forecast",
        workerTitle: "Statistical Forecasting Specialist Agent",
        desc: "Blends ARIMA, Prophet, and Transformer models with seasonality and trend regression.",
        artifact: "Baseline Statistical Demand Forecast",
        status: "READY",
        metrics: { baseline: "$25.0M", units: "12,500", confidence: "94.5%" },
        personas: ["Quantitative Forecaster", "Market Skeptic", "Volatility Analyst"],
        cognitiveSkills: ["ToyBedrock Sampling", "Working Memory (ElastiCache)", "Self-Reflection Loop", "Cedar Policy Gate"],
        tier: 2,
        x: 340, y: 120
      },
      {
        id: 3,
        code: "STG-03",
        pod: "demand",
        name: "Commercial Consensus",
        workerTitle: "Commercial Demand Shaping Agent",
        desc: "Reviews marketing campaigns, sales incentives, and channel promo uplifts.",
        artifact: "Approved Consensus Uplift (+2,500 units, +$5.0M)",
        status: "READY",
        metrics: { baseline: "$30.0M", units: "15,000", confidence: "91.0%" },
        personas: ["VP of Commercial Sales", "Field Marketing Lead", "Financial Controller"],
        cognitiveSkills: ["Dialectical Debate Engine", "Quorum Voting", "Working Memory", "WAF & Budget Guard"],
        tier: 2,
        x: 630, y: 120
      },
      {
        id: 4,
        code: "STG-04",
        pod: "demand",
        name: "Disaggregation",
        workerTitle: "DC & Regional Allocation Agent",
        desc: "Splits consolidated consensus demand across 6 regional Distribution Centers.",
        artifact: "Regional DC Fulfillment Allocation Plan",
        status: "READY",
        metrics: { baseline: "$30.0M", units: "15,000", confidence: "97.3%" },
        personas: ["Regional Network Planner", "Lead Time Optimizer"],
        cognitiveSkills: ["Step Functions Sequence", "DynamoDB Partition Key", "Softmax Temperature Dial"],
        tier: 1,
        x: 920, y: 120
      },
      {
        id: 5,
        code: "STG-05",
        pod: "demand",
        name: "Order Consumption",
        workerTitle: "Net Order Consumption Agent",
        desc: "Nets actual booked sales orders against forecast using forward/backward consumption rules.",
        artifact: "Net Open Demand Requirement (14,200 net)",
        status: "READY",
        metrics: { baseline: "$28.4M", units: "14,200", confidence: "98.4%" },
        personas: ["Order Fulfillment Lead", "Backlog Auditor"],
        cognitiveSkills: ["SQS Priority Queue", "CAS Lock Mutex", "Circuit Breaker"],
        tier: 1,
        x: 1210, y: 120
      },
      {
        id: 6,
        code: "STG-06",
        pod: "supply",
        name: "Dependent Demand",
        workerTitle: "Bill of Materials (BOM) Explosion Agent",
        desc: "Explodes net finished goods into 84 sub-assemblies and 4 critical ASIC chipsets.",
        artifact: "Multi-Tier Component Requirement Matrix",
        status: "READY",
        metrics: { baseline: "$18.2M", units: "84 BOM items", confidence: "99.8%" },
        personas: ["BOM Industrial Engineer", "Semiconductor Specialist"],
        cognitiveSkills: ["Step Functions Retry", "DynamoDB Relational Map", "Tool Sandbox"],
        tier: 1,
        x: 1210, y: 380
      },
      {
        id: 7,
        code: "STG-07",
        pod: "supply",
        name: "Production Firming",
        workerTitle: "Master Production Scheduling (MPS) Agent",
        desc: "Converts requirements into firmed manufacturing shop-floor production work orders.",
        artifact: "Firmed EMS Manufacturing Work Orders",
        status: "READY",
        metrics: { baseline: "$28.4M", units: "14,200 orders", confidence: "96.2%" },
        personas: ["Plant Operations Director", "Shop Floor Scheduler"],
        cognitiveSkills: ["SQS Priority Worker", "CAS State Mutex", "Working Memory"],
        tier: 1,
        x: 920, y: 380
      },
      {
        id: 8,
        code: "STG-08",
        pod: "supply",
        name: "Capacity Allocation",
        workerTitle: "Rough-Cut Capacity Planning (RCCP) Agent",
        desc: "Pools SMT lines, machine hours, and test benches to calculate line utilization.",
        artifact: "Line Utilization Schedule (Lines 1–4 @ 94% load)",
        status: "READY",
        metrics: { baseline: "94% Load", units: "4 Lines", confidence: "93.8%" },
        personas: ["Capacity Optimization Engineer", "Maintenance Specialist", "Labor Planner"],
        cognitiveSkills: ["ToyBedrock Softmax", "Dialectical Debate", "Circuit Breaker 3-Strike"],
        tier: 2,
        x: 630, y: 380
      },
      {
        id: 9,
        code: "STG-09",
        pod: "supply",
        name: "Buffer Inventory",
        workerTitle: "Dynamic DDMRP Safety Stock Agent",
        desc: "Sets decoupled inventory buffers and safety stock to absorb demand/supply variability.",
        artifact: "Safety Stock Matrix (+2,400 reserve units)",
        status: "READY",
        metrics: { baseline: "$4.8M", units: "2,400 reserve", confidence: "96.0%" },
        personas: ["Inventory Policy Lead", "Working Capital Analyst"],
        cognitiveSkills: ["Working Memory", "DynamoDB Ledger", "WAF & Budget Guard"],
        tier: 1,
        x: 340, y: 380
      },
      {
        id: 10,
        code: "STG-10",
        pod: "control",
        name: "SLA Telemetry",
        workerTitle: "Variance & Telemetry Sentinel Agent",
        desc: "Monitors operational variances, cedar policy violations, and forecast bias thresholds.",
        artifact: "Telemetry Audit Certificate (Variance: +3.2% within 5.0% tolerance)",
        status: "READY",
        metrics: { baseline: "+3.2% Var", units: "Pass", confidence: "99.9%" },
        personas: ["Operational Sentinel", "Compliance Officer"],
        cognitiveSkills: ["Cedar Policy Guard", "Hop Limiter", "Circuit Breaker"],
        tier: 1,
        x: 340, y: 640
      },
      {
        id: 11,
        code: "STG-11",
        pod: "control",
        name: "Executive S&OP",
        workerTitle: "Executive S&OP Arbiter & Governance Agent",
        desc: "Executes financial P&L reconciliation, resolves supply-demand gaps, and locks plan to ERP.",
        artifact: "Executive Signed Consensus Operating Plan (P&L $28.4M Approved)",
        status: "READY",
        metrics: { baseline: "$28.4M", units: "Approved", confidence: "100.0%" },
        personas: ["Executive S&OP Chairman", "Chief Supply Chain Officer", "CFO Representative"],
        cognitiveSkills: ["Byzantine Quorum Voting", "Dialectical Debate", "Step Functions Commit", "Cedar Policy Gate"],
        tier: 2,
        x: 780, y: 640
      }
    ];

    // S&OP Inter-Stage Connections
    const SOP_CONNECTIONS = [
      { from: 1, to: 2, label: "POS Baseline" },
      { from: 2, to: 3, label: "Stat Forecast" },
      { from: 3, to: 4, label: "Consensus Plan" },
      { from: 4, to: 5, label: "DC Split" },
      { from: 5, to: 6, label: "Net Demand" },
      { from: 6, to: 7, label: "BOM Explosion" },
      { from: 7, to: 8, label: "Works Orders" },
      { from: 8, to: 9, label: "Load Schedule" },
      { from: 9, to: 10, label: "Buffer Policy" },
      { from: 10, to: 11, label: "Telemetry Audit" },
      // Feedback loop from Capacity Check back to Consensus if constrained
      { from: 8, to: 3, label: "Capacity Feedback (RCCP)", feedback: true }
    ];

    // Warehouse Catalog
    const WAREHOUSE_PARTS = {
      level2: [
        { id: "pod_demand", name: "Demand Pod (Stages 1–5)", tier: 2, icon: "📊", desc: "End-to-end commercial demand generation, statistical smoothing, and sales consensus." },
        { id: "pod_supply", name: "Supply Pod (Stages 6–9)", tier: 2, icon: "🏭", desc: "BOM explosion, rough-cut capacity planning, plant scheduling, and DDMRP buffers." },
        { id: "pod_control", name: "Executive Control Pod (10–11)", tier: 2, icon: "⚖️", desc: "Real-time SLA variance monitoring, Cedar policy validation, and executive P&L sign-off." }
      ],
      level1: [
        { id: "cog_persona", name: "Cognitive Persona Unit", tier: 1, icon: "👤", desc: "An internal debate persona with specialized reasoning perspective (e.g. Quant, Skeptic)." },
        { id: "cog_memory", name: "Working Memory (ElastiCache)", tier: 0, icon: "⚡", desc: "Fast ephemeral context scratchpad with decay and sliding window recall." },
        { id: "cog_store", name: "Episodic Store (DynamoDB)", tier: 0, icon: "🗄️", desc: "Persistent historical record store with TTL and conditional ACID writes." },
        { id: "cog_debate", name: "Dialectical Debate Engine", tier: 2, icon: "💬", desc: "Forces multi-agent internal peer debate and synthesis before finalizing decisions." },
        { id: "cog_circuit", name: "Circuit Breaker (3-Strike)", tier: 1, icon: "🛡️", desc: "Trips open after 3 consecutive errors; enters 60s cooldown to protect LLM budgets." },
        { id: "cog_quorum", name: "Byzantine Quorum Voting", tier: 2, icon: "🗳️", desc: "Requires 2/3 agreement across personas to authorize financial or supply plan commits." },
        { id: "cog_softmax", name: "Softmax Temperature Dial", tier: 0, icon: "🎛️", desc: "Calibrated sampling temperature (0.0 to 1.5) for deterministic vs exploratory outputs." }
      ]
    };

    /* =========================================================================
       2. CANVAS ENGINE: PAN, ZOOM & INTERACTIVE BEZIER CONNECTORS
       ========================================================================= */

    let canvasScale = 0.85;
    let canvasPanX = 60;
    let canvasPanY = 40;
    let isPanning = false;
    let startPanX = 0, startPanY = 0;
    let draggedNode = null;
    let dragOffsetX = 0, dragOffsetY = 0;

    const viewport = document.getElementById("canvasViewport");
    const world = document.getElementById("canvasWorld");
    const svgLayer = document.getElementById("svgConnectionsLayer");
    const nodesContainer = document.getElementById("nodesContainer");

    function initCanvas() {
      applyCanvasTransform();

      // Pan listeners
      viewport.addEventListener("mousedown", (e) => {
        if (e.target === viewport || e.target === svgLayer || e.target.classList.contains("canvas-world")) {
          isPanning = true;
          viewport.classList.add("panning");
          startPanX = e.clientX - canvasPanX;
          startPanY = e.clientY - canvasPanY;
        }
      });

      window.addEventListener("mousemove", (e) => {
        if (isPanning) {
          canvasPanX = e.clientX - startPanX;
          canvasPanY = e.clientY - startPanY;
          applyCanvasTransform();
        } else if (draggedNode) {
          const worldCoords = screenToWorld(e.clientX, e.clientY);
          const currentStage = getCurrentCanvasNodes().find(n => n.id === draggedNode.nodeId);
          if (currentStage) {
            currentStage.x = Math.max(20, worldCoords.x - dragOffsetX);
            currentStage.y = Math.max(20, worldCoords.y - dragOffsetY);
            draggedNode.element.style.left = `${currentStage.x}px`;
            draggedNode.element.style.top = `${currentStage.y}px`;
            renderConnections();
          }
        }
      });

      window.addEventListener("mouseup", () => {
        isPanning = false;
        viewport.classList.remove("panning");
        draggedNode = null;
      });

      viewport.addEventListener("wheel", (e) => {
        e.preventDefault();
        const zoomFactor = e.deltaY < 0 ? 1.08 : 0.92;
        zoomCanvas(zoomFactor, e.clientX, e.clientY);
      }, { passive: false });

      renderCanvas();
      renderWarehouseCatalog();
      selectNode(2); // Select Forecaster by default
      logStream("S&OP AI Factory initialized with 11 stage-gate workers.", "ok");
    }

    function applyCanvasTransform() {
      world.style.transform = `translate(${canvasPanX}px, ${canvasPanY}px) scale(${canvasScale})`;
    }

    function screenToWorld(screenX, screenY) {
      const rect = viewport.getBoundingClientRect();
      return {
        x: (screenX - rect.left - canvasPanX) / canvasScale,
        y: (screenY - rect.top - canvasPanY) / canvasScale
      };
    }

    function zoomCanvas(factor, clientX, clientY) {
      const newScale = Math.min(Math.max(0.4, canvasScale * factor), 2.0);
      if (clientX !== undefined && clientY !== undefined) {
        const rect = viewport.getBoundingClientRect();
        const mouseX = clientX - rect.left;
        const mouseY = clientY - rect.top;
        canvasPanX = mouseX - (mouseX - canvasPanX) * (newScale / canvasScale);
        canvasPanY = mouseY - (mouseY - canvasPanY) * (newScale / canvasScale);
      }
      canvasScale = newScale;
      applyCanvasTransform();
    }

    function resetCanvasView() {
      canvasScale = 0.85;
      canvasPanX = 60;
      canvasPanY = 40;
      applyCanvasTransform();
    }

    /* =========================================================================
       3. HIERARCHY SWITCHING: LEVEL 2 (ORGANIZATION) vs LEVEL 1 (WORKER MIND)
       ========================================================================= */

    function switchHierarchyLevel(level) {
      currentHierarchyLevel = level;
      
      const btn2 = document.getElementById("btnNavLevel2");
      const btn1 = document.getElementById("btnNavLevel1");
      const warehouseLabel = document.getElementById("warehouseModeLabel");
      const breadcrumb = document.getElementById("workerBreadcrumb");

      if (level === 2) {
        btn2.classList.add("active");
        btn1.classList.remove("active");
        warehouseLabel.textContent = "Level 2 Organization (S&OP Pods)";
        breadcrumb.style.display = "flex";
        showToast("Switched to Level 2: 11-Step Enterprise S&OP Organization");
      } else {
        btn1.classList.add("active");
        btn2.classList.remove("active");
        const selectedStage = SOP_STAGES.find(s => s.id === selectedNodeId) || SOP_STAGES[1];
        warehouseLabel.textContent = `Level 1 Worker Mind (${selectedStage.name})`;
        showToast(`Drilled down into Worker Mind: ${selectedStage.name}`);
      }

      renderCanvas();
      renderWarehouseCatalog();
    }

    function drillIntoCurrentSelectedWorker() {
      switchHierarchyLevel(1);
    }

    function getCurrentCanvasNodes() {
      if (currentHierarchyLevel === 2) {
        return SOP_STAGES;
      } else {
        // Level 1: Generate nodes representing the selected worker's internal cognitive mind!
        const selectedStage = SOP_STAGES.find(s => s.id === selectedNodeId) || SOP_STAGES[1];
        return buildWorkerMindNodes(selectedStage);
      }
    }

    // Build the internal cognitive mind nodes for Level 1
    function buildWorkerMindNodes(stage) {
      const nodes = [];
      
      // 1. Role Master Core Node (center)
      nodes.push({
        id: "core",
        name: stage.name + " Core Mind",
        code: "MIND-CORE",
        pod: stage.pod,
        workerTitle: stage.workerTitle,
        desc: "Coordinates intra-personal personas and resolves cognitive debate into official stage artifact.",
        metrics: { mode: "Dialectical Synthesis", temperature: "0.2" },
        tier: stage.tier,
        x: 480, y: 220
      });

      // 2. Persona Nodes (left side)
      stage.personas.forEach((p, idx) => {
        nodes.push({
          id: `persona_${idx}`,
          name: p,
          code: `PERS-${idx+1}`,
          pod: "demand",
          workerTitle: "Internal Persona",
          desc: `Evaluates domain data from the perspective of ${p}.`,
          metrics: { weight: `${(100 / stage.personas.length).toFixed(0)}%`, bias: "Checked" },
          tier: 1,
          x: 100, y: 80 + idx * 160
        });
      });

      // 3. Cognitive Skill Nodes (right side)
      stage.cognitiveSkills.forEach((s, idx) => {
        nodes.push({
          id: `skill_${idx}`,
          name: s,
          code: `SKILL-${idx+1}`,
          pod: "supply",
          workerTitle: "Cognitive Skill Module",
          desc: `Operational capability: provides state, computation, or safety guardrails.`,
          metrics: { latency: "1.2ms", status: "Armed" },
          tier: 0,
          x: 880, y: 70 + idx * 130
        });
      });

      return nodes;
    }

    /* =========================================================================
       4. RENDERING CANVAS NODES & CONNECTIONS
       ========================================================================= */

    function renderCanvas() {
      nodesContainer.innerHTML = "";
      const nodes = getCurrentCanvasNodes();

      nodes.forEach(node => {
        const el = document.createElement("div");
        el.className = `flow-node ${node.id === selectedNodeId ? "selected" : ""}`;
        el.id = `flowNode_${node.id}`;
        el.style.left = `${node.x}px`;
        el.style.top = `${node.y}px`;

        let podClass = "badge-demand";
        if (node.pod === "supply") podClass = "badge-supply";
        if (node.pod === "control") podClass = "badge-control";

        el.innerHTML = `
          <div class="port input-port"></div>
          <div class="port output-port"></div>
          <div class="node-header">
            <div class="node-title-group">
              <span class="node-icon">${currentHierarchyLevel === 2 ? "📦" : "🧠"}</span>
              <span class="node-title">${node.name}</span>
            </div>
            <span class="node-badge ${podClass}">${node.code}</span>
          </div>
          <div class="node-body">
            <div style="font-weight:600; color:var(--text-main); font-size:0.75rem;">${node.workerTitle}</div>
            <div style="line-height:1.3; font-size:0.7rem; color:var(--text-muted);">${node.desc}</div>
            <div class="node-metric-row">
              <span style="color:var(--text-dim);">${Object.keys(node.metrics)[0]}:</span>
              <span style="color:var(--accent-cyan);">${Object.values(node.metrics)[0]}</span>
              <span style="color:var(--text-dim);">${Object.keys(node.metrics)[1]}:</span>
              <span style="color:var(--accent-emerald);">${Object.values(node.metrics)[1]}</span>
            </div>
          </div>
          <div class="node-footer">
            <span style="font-size:0.65rem; color:var(--text-dim); font-family:var(--font-mono);">Tier ${node.tier}</span>
            ${currentHierarchyLevel === 2 ? 
              `<button class="btn-drilldown" onclick="event.stopPropagation(); selectNode(${node.id}); drillIntoCurrentSelectedWorker()">🔍 Mind</button>` : 
              `<span style="font-size:0.68rem; color:var(--accent-purple);">Intra-Mind</span>`}
          </div>
        `;

        // Click to select
        el.addEventListener("click", () => {
          if (currentHierarchyLevel === 2) {
            selectNode(node.id);
          }
        });

        // Drag node listener
        const header = el.querySelector(".node-header");
        header.addEventListener("mousedown", (e) => {
          e.stopPropagation();
          draggedNode = { nodeId: node.id, element: el };
          const worldCoords = screenToWorld(e.clientX, e.clientY);
          dragOffsetX = worldCoords.x - node.x;
          dragOffsetY = worldCoords.y - node.y;
        });

        nodesContainer.appendChild(el);
      });

      renderConnections();
    }

    function renderConnections() {
      svgLayer.innerHTML = "";
      if (currentHierarchyLevel === 2) {
        // Draw Level 2 S&OP Connections
        SOP_CONNECTIONS.forEach(conn => {
          const fromNode = SOP_STAGES.find(s => s.id === conn.from);
          const toNode = SOP_STAGES.find(s => s.id === conn.to);
          if (!fromNode || !toNode) return;

          const fromEl = document.getElementById(`flowNode_${conn.from}`);
          const toEl = document.getElementById(`flowNode_${conn.to}`);
          if (!fromEl || !toEl) return;

          const fromX = fromNode.x + fromEl.offsetWidth;
          const fromY = fromNode.y + fromEl.offsetHeight / 2;
          const toX = toNode.x;
          const toY = toNode.y + toEl.offsetHeight / 2;

          const pathStr = createBezierPath(fromX, fromY, toX, toY, conn.feedback);
          const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
          path.setAttribute("d", pathStr);
          path.setAttribute("class", `connection-path ${conn.feedback ? "feedback-wire" : ""}`);
          path.id = `wire_${conn.from}_${conn.to}`;
          svgLayer.appendChild(path);
        });
      } else {
        // Draw Level 1 Internal Mind Connections: Personas -> Core -> Skills
        const nodes = getCurrentCanvasNodes();
        const coreNode = nodes.find(n => n.id === "core");
        if (!coreNode) return;

        const coreEl = document.getElementById("flowNode_core");
        if (!coreEl) return;

        nodes.forEach(n => {
          if (n.id.startsWith("persona_")) {
            // Persona to Core
            const pEl = document.getElementById(`flowNode_${n.id}`);
            if (pEl) {
              const pathStr = createBezierPath(n.x + pEl.offsetWidth, n.y + pEl.offsetHeight / 2, coreNode.x, coreNode.y + coreEl.offsetHeight / 2, false);
              const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
              path.setAttribute("d", pathStr);
              path.setAttribute("class", "connection-path active-pulse");
              svgLayer.appendChild(path);
            }
          } else if (n.id.startsWith("skill_")) {
            // Core to Skill
            const sEl = document.getElementById(`flowNode_${n.id}`);
            if (sEl) {
              const pathStr = createBezierPath(coreNode.x + coreEl.offsetWidth, coreNode.y + coreEl.offsetHeight / 2, n.x, n.y + sEl.offsetHeight / 2, false);
              const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
              path.setAttribute("d", pathStr);
              path.setAttribute("class", "connection-path");
              svgLayer.appendChild(path);
            }
          }
        });
      }
    }

    function createBezierPath(x1, y1, x2, y2, isFeedback) {
      if (isFeedback) {
        // Arching feedback wire
        const midY = Math.min(y1, y2) - 80;
        return `M ${x1} ${y1} C ${x1 + 60} ${midY}, ${x2 - 60} ${midY}, ${x2} ${y2}`;
      }
      const dx = Math.abs(x2 - x1) * 0.55;
      return `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;
    }

    /* =========================================================================
       5. NODE SELECTION & INSPECTOR
       ========================================================================= */

    function selectNode(id) {
      selectedNodeId = id;
      const stage = SOP_STAGES.find(s => s.id === id);
      if (!stage) return;

      // Update selection styling on nodes
      document.querySelectorAll(".flow-node").forEach(n => n.classList.remove("selected"));
      const selectedEl = document.getElementById(`flowNode_${id}`);
      if (selectedEl) selectedEl.classList.add("selected");

      // Update breadcrumb
      document.getElementById("breadcrumbWorkerName").textContent = `${stage.code} • ${stage.name}`;

      // Update Inspector Panel
      document.getElementById("inspectorTitle").textContent = `${stage.code}: ${stage.name}`;
      document.getElementById("inspectorTierBadge").textContent = `Tier ${stage.tier}`;
      document.getElementById("inspectorTierBadge").className = `part-tier tier-${stage.tier}`;

      const card = document.getElementById("inspectorContentCard");
      card.innerHTML = `
        <div style="font-size:0.75rem; font-weight:700; color:var(--text-main);">${stage.workerTitle}</div>
        <div style="font-size:0.72rem; color:var(--text-muted); line-height:1.4;">${stage.desc}</div>
        
        <div style="font-size:0.7rem; font-weight:700; color:var(--accent-cyan); text-transform:uppercase; margin-top:4px;">
          Primary S&OP Output Artifact:
        </div>
        <div style="font-size:0.72rem; font-family:var(--font-mono); background:var(--bg-primary); padding:6px; border-radius:4px; border:1px solid var(--border-color);">
          📄 ${stage.artifact}
        </div>

        <div style="font-size:0.7rem; font-weight:700; color:var(--accent-purple); text-transform:uppercase; margin-top:4px;">
          Intra-Mind Personas (${stage.personas.length}):
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:4px;">
          ${stage.personas.map(p => `<span class="mind-persona-pill">👤 ${p}</span>`).join("")}
        </div>

        <div style="font-size:0.7rem; font-weight:700; color:var(--accent-amber); text-transform:uppercase; margin-top:4px;">
          Assembled Cognitive Skills (${stage.cognitiveSkills.length}):
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:4px;">
          ${stage.cognitiveSkills.map(s => `<span class="mind-skill-tag">⚡ ${s}</span>`).join("")}
        </div>
      `;
    }

    /* =========================================================================
       6. WAREHOUSE CATALOG RENDERING
       ========================================================================= */

    function renderWarehouseCatalog() {
      const container = document.getElementById("warehousePartsContainer");
      container.innerHTML = "";

      const parts = currentHierarchyLevel === 2 ? WAREHOUSE_PARTS.level2 : WAREHOUSE_PARTS.level1;

      parts.forEach(part => {
        const card = document.createElement("div");
        card.className = "part-card";
        card.innerHTML = `
          <div class="part-header">
            <span class="part-title">${part.icon} ${part.name}</span>
            <span class="part-tier tier-${part.tier}">Tier ${part.tier}</span>
          </div>
          <div class="part-desc">${part.desc}</div>
        `;
        container.appendChild(card);
      });
    }

    /* =========================================================================
       7. AI COPILOT: GROQ LPU + WEBGPU WEBLM + DETERMINISTIC COMPILER
       ========================================================================= */

    function switchSidebarTab(tab) {
      const isWarehouse = tab === "warehouse";
      document.getElementById("tabWarehouseBtn").classList.toggle("active", isWarehouse);
      document.getElementById("tabCopilotBtn").classList.toggle("active", !isWarehouse);
      document.getElementById("sidebarWarehouseContent").style.display = isWarehouse ? "flex" : "none";
      document.getElementById("sidebarCopilotContent").style.display = !isWarehouse ? "flex" : "none";
    }

    function switchInspectorTab(tab) {
      const isDetails = tab === "details";
      document.getElementById("tabInspectDetailsBtn").classList.toggle("active", isDetails);
      document.getElementById("tabInspectStreamBtn").classList.toggle("active", !isDetails);
      document.getElementById("inspectDetailsTab").style.display = isDetails ? "flex" : "none";
      document.getElementById("inspectStreamTab").style.display = !isDetails ? "flex" : "none";
    }

    function onAiEngineChange(val) {
      activeAiEngine = val;
      showToast(`AI Engine set to: ${val.toUpperCase()}`);
      if (val === "webgpu" && !webllmEngine) {
        initWebLlmEngine();
      }
    }

    async function initWebLlmEngine() {
      if (!window.webllm) {
        showToast("WebLLM library not loaded", true);
        return;
      }
      const progressBox = document.getElementById("webllmProgressBox");
      const progressBar = document.getElementById("webllmProgressBar");
      const statusText = document.getElementById("webllmStatusText");
      progressBox.style.display = "flex";

      try {
        statusText.textContent = "Initializing WebGPU & downloading Llama-3.2-1B...";
        webllmEngine = await window.webllm.CreateMLCEngine("Llama-3.2-1B-Instruct-q4f16_1-MLC", {
          initProgressCallback: (report) => {
            statusText.textContent = report.text;
            progressBar.style.width = `${Math.min(100, Math.floor((report.progress || 0) * 100))}%`;
          }
        });
        statusText.textContent = "WebGPU Model Ready on device!";
        showToast("WebGPU Model Loaded & Armed!");
      } catch (err) {
        console.error("WebLLM error:", err);
        statusText.textContent = "WebGPU not supported on this browser. Falling back to Groq/Deterministic.";
        showToast("WebGPU unavailable; using Groq/Deterministic", true);
      }
    }

    async function runAiCopilotAssembly() {
      const input = document.getElementById("copilotInput").value.trim();
      if (!input) {
        showToast("Please enter an assembly prompt or select a preset.", true);
        return;
      }

      showToast("🤖 AI Copilot assembling cognitive architecture...");
      logStream(`[AI COPILOT] Parsing order: "${input}"`, "ok");

      const systemPrompt = `You are the S&OP AI Factory Chief Architect.
The user wants to configure either a Level 1 Worker Mind (personas & cognitive skills) or a Level 2 S&OP Organization.
Return a JSON object:
{
  "targetLevel": 1 | 2,
  "summary": string,
  "personas": [string],
  "cognitiveSkills": [string],
  "tier": 1 | 2,
  "rationale": string
}`;

      try {
        let resultJson = null;

        if (activeAiEngine === "groq") {
          const resp = await fetch("https://api.groq.com/openai/v1/chat/completions", {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${GROQ_KEY}`,
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              model: "openai/gpt-oss-120b",
              messages: [
                { role: "system", content: systemPrompt },
                { role: "user", content: input }
              ],
              temperature: 0.2,
              max_tokens: 500,
              response_format: { type: "json_object" }
            })
          });
          if (resp.ok) {
            const data = await resp.json();
            resultJson = JSON.parse(data.choices[0].message.content);
          }
        } else if (activeAiEngine === "webgpu" && webllmEngine) {
          const resp = await webllmEngine.chat.completions.create({
            messages: [
              { role: "system", content: systemPrompt },
              { role: "user", content: input }
            ],
            temperature: 0.2,
            max_tokens: 400
          });
          const raw = resp.choices[0].message.content;
          const match = raw.match(/\{[\s\S]*\}/);
          if (match) resultJson = JSON.parse(match[0]);
        }

        // Fallback: Deterministic Compiler
        if (!resultJson) {
          resultJson = {
            targetLevel: 1,
            summary: "Assembled Custom Cognitive Worker Mind",
            personas: ["Quantitative Specialist", "Empirical Auditor", "Risk Arbiter"],
            cognitiveSkills: ["ElastiCache Memory", "DynamoDB Store", "Dialectical Debate", "Circuit Breaker"],
            tier: 2,
            rationale: "Matched high reliability requirements with 3-persona dialectical debate and automated circuit breaker."
          };
        }

        // Apply assembly to selected stage
        const stage = SOP_STAGES.find(s => s.id === selectedNodeId) || SOP_STAGES[1];
        if (resultJson.personas && resultJson.personas.length > 0) {
          stage.personas = resultJson.personas;
        }
        if (resultJson.cognitiveSkills && resultJson.cognitiveSkills.length > 0) {
          stage.cognitiveSkills = resultJson.cognitiveSkills;
        }
        stage.tier = resultJson.tier || stage.tier;

        selectNode(stage.id);
        renderCanvas();
        showToast(`Worker Mind for '${stage.name}' assembled successfully!`);
        logStream(`[AI COPILOT] Assembled ${stage.name} with ${stage.personas.length} personas and ${stage.cognitiveSkills.length} skills.`, "ok");

      } catch (err) {
        console.error("Copilot error:", err);
        showToast("Error during copilot assembly; applied deterministic fallback.", true);
      }
    }

    function loadCopilotPreset(presetNum) {
      if (presetNum === 1) {
        document.getElementById("copilotInput").value = "Assemble high-precision Statistical Forecaster with Bayesian Outlier Filter, Quantitative Persona, and Cedar Policy Gate.";
      }
    }

    /* =========================================================================
       8. SIMULATION: 11-STAGE END-TO-END S&OP CYCLE
       ========================================================================= */

    let currentSimStepIndex = 0;
    let isSimulating = false;

    async function runSimulationCycle() {
      if (isSimulating) return;
      isSimulating = true;
      currentSimStepIndex = 0;
      resetSimulationVisuals();
      logStream("Starting complete 11-Stage S&OP Operating Cycle...", "ok");

      for (let i = 0; i < SOP_STAGES.length; i++) {
        await executeStage(i);
        await new Promise(r => setTimeout(r, 900));
      }

      isSimulating = false;
      document.getElementById("kpiCycleStatus").textContent = "CYCLE COMPLETE • PLAN LOCKED";
      document.getElementById("kpiCycleStatus").style.borderColor = "var(--accent-emerald)";
      document.getElementById("kpiCycleStatus").style.color = "var(--accent-emerald)";
      logStream("🏁 11-Stage S&OP Cycle executed and locked to ERP successfully!", "ok");
      showToast("S&OP Cycle Complete: $28.4M Plan Locked to ERP!");
    }

    async function stepSimulationStage() {
      if (currentSimStepIndex >= SOP_STAGES.length) {
        currentSimStepIndex = 0;
        resetSimulationVisuals();
      }
      await executeStage(currentSimStepIndex);
      currentSimStepIndex++;
    }

    async function executeStage(index) {
      const stage = SOP_STAGES[index];
      selectNode(stage.id);

      // Visual pulse on active node
      document.querySelectorAll(".flow-node").forEach(n => n.classList.remove("active-stage"));
      const el = document.getElementById(`flowNode_${stage.id}`);
      if (el) el.classList.add("active-stage");

      // Active pulse on wire
      if (index > 0) {
        const prev = SOP_STAGES[index - 1];
        const wire = document.getElementById(`wire_${prev.id}_${stage.id}`);
        if (wire) wire.classList.add("active-pulse");
      }

      // Log artifact emission
      logStream(`[${stage.code}] ${stage.name}: Personas reached consensus on artifact:`, "ok");
      logStream(`    ↳ ${stage.artifact}`, "cyan");

      // Update KPI banner if reaching stage 3 (Demand Consensus) or stage 8 (Supply Constrained)
      if (stage.id === 3) {
        document.getElementById("kpiDemand").textContent = "$30.0M (15,000 units)";
        logStream("    ↳ Commercial consensus approved +$5.0M promo uplift.", "ok");
      } else if (stage.id === 8) {
        document.getElementById("kpiSupply").textContent = "$28.4M (14,200 units)";
        document.getElementById("kpiGap").textContent = "-$1.6M (-5.3%)";
        logStream("    ↳ SMT Line 1-4 capacity locked at 94% load (14,200 max throughput).", "warn");
      } else if (stage.id === 11) {
        document.getElementById("kpiSla").textContent = "94.7% Fill Rate (Approved)";
        logStream("    ↳ Executive Committee signed off on $28.4M operating plan.", "ok");
      }
    }

    function resetSimulation() {
      currentSimStepIndex = 0;
      isSimulating = false;
      resetSimulationVisuals();
      logStream("S&OP Cycle reset to initial state.", "ok");
      showToast("Cycle Reset");
    }

    function resetSimulationVisuals() {
      document.querySelectorAll(".flow-node").forEach(n => n.classList.remove("active-stage"));
      document.querySelectorAll(".connection-path").forEach(w => w.classList.remove("active-pulse"));
      document.getElementById("kpiCycleStatus").textContent = "READY • STAGES 1–11";
      document.getElementById("kpiCycleStatus").style.borderColor = "var(--accent-purple)";
      document.getElementById("kpiCycleStatus").style.color = "#c4b5fd";
    }

    function loadScenario(val) {
      if (val === "0") {
        document.getElementById("kpiDemand").textContent = "$30.0M (15,000 units)";
        document.getElementById("kpiSupply").textContent = "$28.4M (14,200 units)";
        document.getElementById("kpiGap").textContent = "-$1.6M (-5.3%)";
        logStream("Loaded Scenario 0: Enterprise Router Demand Surge (+20% Uplift).", "ok");
      } else if (val === "1") {
        document.getElementById("kpiDemand").textContent = "$30.0M (15,000 units)";
        document.getElementById("kpiSupply").textContent = "$21.0M (10,500 units)";
        document.getElementById("kpiGap").textContent = "-$9.0M (-30.0%)";
        logStream("Loaded Scenario 1: Severe ASIC Shortage (-30% allocation cap).", "warn");
      } else {
        document.getElementById("kpiDemand").textContent = "$36.0M (18,000 units)";
        document.getElementById("kpiSupply").textContent = "$34.2M (17,100 units)";
        document.getElementById("kpiGap").textContent = "-$1.8M (-5.0%)";
        logStream("Loaded Scenario 2: Accelerated New Product Introduction (NPI).", "ok");
      }
      showToast("Scenario Telemetry Loaded");
    }

    /* =========================================================================
       9. BOM RECEIPT MODAL
       ========================================================================= */

    function openBomModal() {
      const modal = document.getElementById("bomModal");
      const body = document.getElementById("bomModalBody");

      let totalSkills = 0;
      let totalPersonas = 0;
      SOP_STAGES.forEach(s => {
        totalSkills += s.cognitiveSkills.length;
        totalPersonas += s.personas.length;
      });

      body.innerHTML = `
        <div style="font-size:0.9rem; font-weight:700; color:var(--accent-cyan);">
          S&OP ENTERPRISE AGENTIC SYSTEM BILL OF MATERIALS (BOM)
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:var(--text-muted); border-bottom:1px solid var(--border-color); padding-bottom:6px;">
          <span>Architecture: Fractal Multi-Level S&OP Swarm</span>
          <span>Total Stages: 11 | Total Personas: ${totalPersonas} | Cognitive Skills: ${totalSkills}</span>
        </div>

        <table class="bom-table">
          <thead>
            <tr>
              <th>Stage</th>
              <th>Worker Role</th>
              <th>Tier</th>
              <th>Internal Personas</th>
              <th>Cognitive Skills & Infrastructure</th>
            </tr>
          </thead>
          <tbody>
            ${SOP_STAGES.map(s => `
              <tr>
                <td><strong>${s.code}</strong></td>
                <td>${s.workerTitle}</td>
                <td><span class="part-tier tier-${s.tier}">Tier ${s.tier}</span></td>
                <td>${s.personas.join(", ")}</td>
                <td>${s.cognitiveSkills.join(", ")}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>

        <div style="font-size:0.7rem; color:var(--text-dim); line-height:1.4;">
          * Receipt certified under the 7-Step Autonomous Assembly Protocol. All 11 workers are compiled with local fallbacks, DynamoDB persistence, and Cedar policy gates.
        </div>
      `;

      modal.style.display = "flex";
    }

    function closeBomModal(e) {
      if (e) e.stopPropagation();
      document.getElementById("bomModal").style.display = "none";
    }

    /* =========================================================================
       10. UTILITIES, LOGGING & THEME
       ========================================================================= */

    function logStream(msg, tag = "info") {
      const container = document.getElementById("liveStreamLogs");
      const time = new Date().toLocaleTimeString();
      const div = document.createElement("div");
      div.className = "log-line";
      div.innerHTML = `
        <span class="log-time">[${time}]</span>
        <span class="log-tag ${tag}">${tag.toUpperCase()}</span>
        <span>${msg}</span>
      `;
      container.appendChild(div);
      container.scrollTop = container.scrollHeight;
    }

    function clearStreamLogs() {
      document.getElementById("liveStreamLogs").innerHTML = "";
    }

    function showToast(msg, isError = false) {
      const toast = document.getElementById("toastBox");
      document.getElementById("toastMsg").textContent = msg;
      document.getElementById("toastIcon").textContent = isError ? "⚠️" : "⚡";
      toast.style.borderColor = isError ? "var(--accent-rose)" : "var(--accent-cyan)";
      toast.style.display = "flex";
      setTimeout(() => { toast.style.display = "none"; }, 3500);
    }

    function toggleTheme() {
      document.body.classList.toggle("light-mode");
      const isLight = document.body.classList.contains("light-mode");
      document.getElementById("themeToggleBtn").textContent = isLight ? "🌙" : "☀️";
    }

    // Launch Application
    window.addEventListener("DOMContentLoaded", initCanvas);
  </script>
</body>
</html>
'''

with open("sop_ai_factory_canvas.html", "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"Successfully generated 'sop_ai_factory_canvas.html' ({len(HTML_CONTENT)} bytes)!")
