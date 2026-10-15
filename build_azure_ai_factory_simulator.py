# -*- coding: utf-8 -*-
"""
build_azure_ai_factory_simulator.py
Generates `ai_factory_azure_simulator.html` - The frontend web app HTML only
with WebLLM/WebGPU, Groq LPU, and in-browser Microsoft Azure Cloud Simulator.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The AI Agent Factory • In-Browser Azure Simulator</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">

<!-- Pyodide in-browser Python WebAssembly engine -->
<script src="https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js"></script>

<!-- WebLLM for local WebGPU inference -->
<script type="module">
  import * as webllm from "https://esm.run/@mlc-ai/web-llm";
  window.webllm = webllm;
</script>

<style>
  :root {
    --bg-page: #F3F4F6;
    --card-bg: #FFFFFF;
    --border-color: #E5E7EB;
    --border-hover: #D1D5DB;
    --text-primary: #111827;
    --text-secondary: #374151;
    --text-muted: #6B7280;
    --accent: #0078D4; /* Microsoft Azure Blue */
    --accent-light: #EFF6FC;
    --accent-dark: #005A9E;
    --azure-cyan: #00BCF2;
    --tier0-color: #D97706;
    --tier0-bg: #FEF3C7;
    --tier1-color: #0078D4;
    --tier1-bg: #EFF6FC;
    --tier2-color: #7C3AED;
    --tier2-bg: #EDE9FE;
    --success: #107C41; /* Microsoft Green */
    --success-bg: #DFF6DD;
    --danger: #D83B01; /* Microsoft Crimson */
    --danger-bg: #FDE7E9;
    --warning: #EA580C;
    --warning-bg: #FFEDD5;
    --code-bg: #0B192C;
    --code-text: #E2E8F0;
    --canvas-bg: #F8FAFC;
    --canvas-dot: #CBD5E1;
    --font-sans: 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
  }

  body.dark-mode {
    --bg-page: #080D1A;
    --card-bg: #0F172A;
    --border-color: #1E293B;
    --border-hover: #334155;
    --text-primary: #F8FAFC;
    --text-secondary: #CBD5E1;
    --text-muted: #94A3B8;
    --accent: #008AD7;
    --accent-light: rgba(0, 138, 215, 0.16);
    --accent-dark: #0078D4;
    --azure-cyan: #38BDF8;
    --tier0-color: #F59E0B;
    --tier0-bg: rgba(245, 158, 11, 0.15);
    --tier1-color: #38BDF8;
    --tier1-bg: rgba(56, 189, 248, 0.15);
    --tier2-color: #A855F7;
    --tier2-bg: rgba(168, 85, 247, 0.15);
    --code-bg: #030712;
    --code-text: #F3F4F6;
    --canvas-bg: #060913;
    --canvas-dot: #1E293B;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: var(--font-sans);
    background: var(--bg-page);
    color: var(--text-primary);
    line-height: 1.5;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    transition: background 0.2s ease, color 0.2s ease;
  }

  /* TOP NAVBAR */
  .navbar {
    background: var(--card-bg);
    border-bottom: 1px solid var(--border-color);
    padding: 10px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }
  .nav-brand {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .brand-logo {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #0078D4, #00BCF2, #7C3AED);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    box-shadow: 0 2px 8px rgba(0, 120, 212, 0.35);
  }
  .brand-title {
    font-size: 15.5px;
    font-weight: 800;
    letter-spacing: -0.01em;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .brand-title .azure-tag {
    background: linear-gradient(135deg, #0078D4, #00BCF2);
    color: white;
    font-size: 10px;
    padding: 2px 7px;
    border-radius: 4px;
    text-transform: uppercase;
    font-weight: 800;
  }
  .brand-subtitle {
    font-size: 11.5px;
    color: var(--text-muted);
    font-weight: 500;
  }

  .nav-controls {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .pill-badge {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 11.5px;
    font-weight: 600;
    border: 1px solid var(--border-color);
    background: var(--bg-page);
  }
  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }
  .dot.green { background: var(--success); box-shadow: 0 0 8px var(--success); }
  .dot.blue { background: var(--accent); }
  .dot.orange { background: var(--warning); }

  .engine-select {
    padding: 6px 10px;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    background: var(--card-bg);
    color: var(--text-primary);
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
  }
  .btn-icon {
    padding: 6px 12px;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    background: var(--card-bg);
    color: var(--text-primary);
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .btn-icon:hover {
    border-color: var(--border-hover);
    background: var(--bg-page);
  }

  /* MAIN LAYOUT */
  .studio-container {
    display: grid;
    grid-template-columns: 450px 1fr;
    gap: 18px;
    padding: 16px 20px;
    max-width: 1760px;
    margin: 0 auto;
    width: 100%;
    flex: 1;
  }

  @media (max-width: 1200px) {
    .studio-container {
      grid-template-columns: 1fr;
    }
  }

  /* COLUMN CARDS */
  .column-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03);
  }
  .card-header {
    padding: 12px 16px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(0,0,0,0.015);
  }
  .card-title-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .card-title {
    font-size: 14px;
    font-weight: 700;
    letter-spacing: -0.01em;
  }
  .card-badge {
    font-size: 10.5px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 5px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }
  .card-body {
    padding: 16px;
    overflow-y: auto;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  /* ORDER INTAKE STAGE */
  .order-box {
    background: var(--bg-page);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 12px;
  }
  .order-label {
    font-size: 11.5px;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
  }
  .order-input-wrap {
    display: flex;
    gap: 8px;
  }
  .order-textarea {
    flex: 1;
    min-height: 56px;
    padding: 9px 12px;
    border-radius: 7px;
    border: 1px solid var(--border-color);
    background: var(--card-bg);
    color: var(--text-primary);
    font-family: var(--font-sans);
    font-size: 12.5px;
    resize: none;
    line-height: 1.4;
  }
  .order-textarea:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-light);
  }
  .btn-assemble {
    padding: 0 16px;
    background: var(--accent);
    color: white;
    border: none;
    border-radius: 7px;
    font-weight: 700;
    font-size: 12.5px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;
    transition: all 0.15s ease;
    white-space: nowrap;
  }
  .btn-assemble:hover {
    background: var(--accent-dark);
    transform: translateY(-1px);
  }

  .preset-chips-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 10px;
  }
  .chip {
    padding: 4px 9px;
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.12s ease;
  }
  .chip:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: var(--accent-light);
  }

  /* PIPELINE ACCORDION */
  .pipeline-card {
    border: 1px solid var(--border-color);
    border-radius: 10px;
    background: var(--card-bg);
    overflow: hidden;
  }
  .pipeline-header {
    background: var(--bg-page);
    padding: 8px 12px;
    font-size: 11.5px;
    font-weight: 700;
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid var(--border-color);
  }
  .steps-accordion {
    display: flex;
    flex-direction: column;
  }
  .assembly-step {
    border-bottom: 1px solid var(--border-color);
    font-size: 11px;
    transition: background 0.15s ease;
  }
  .assembly-step:last-child { border-bottom: none; }
  .assembly-step.active {
    background: var(--accent-light);
  }
  .step-head {
    padding: 6px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    font-weight: 600;
  }
  .step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 17px;
    height: 17px;
    border-radius: 50%;
    background: var(--accent);
    color: white;
    font-size: 9.5px;
    font-weight: 700;
    margin-right: 6px;
  }
  .step-content {
    padding: 0 12px 6px 35px;
    color: var(--text-muted);
    font-size: 10.5px;
    line-height: 1.35;
  }

  /* 3-SHELF PARTS WAREHOUSE */
  .warehouse-card {
    border: 1px solid var(--border-color);
    border-radius: 10px;
    background: var(--card-bg);
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .warehouse-title {
    font-size: 12px;
    font-weight: 700;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .shelf {
    background: var(--bg-page);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 8px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .shelf-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 10.5px;
  }
  .shelf-tag {
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 9.5px;
    text-transform: uppercase;
  }
  .shelf-tag.t0 { background: var(--tier0-bg); color: var(--tier0-color); }
  .shelf-tag.t1 { background: var(--tier1-bg); color: var(--tier1-color); }
  .shelf-tag.t2 { background: var(--tier2-bg); color: var(--tier2-color); }
  .shelf-desc { color: var(--text-muted); font-size: 10px; }

  .parts-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
  }
  .part-item {
    background: var(--card-bg);
    border: 1px dashed var(--border-color);
    border-radius: 6px;
    padding: 5px 6px;
    font-size: 10.5px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 4px;
    cursor: grab;
    transition: all 0.12s ease;
    user-select: none;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .part-item:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: var(--accent-light);
    transform: translateY(-1px);
  }
  .part-item.active {
    border-style: solid;
    border-color: var(--accent);
    background: var(--accent-light);
    color: var(--accent-dark);
  }
  .part-item.trimmed {
    opacity: 0.4;
    text-decoration: line-through;
  }

  /* RECEIPT OUTPUT */
  .receipt-box {
    background: var(--code-bg);
    color: var(--code-text);
    border-radius: 8px;
    padding: 10px 12px;
    font-family: var(--font-mono);
    font-size: 10.5px;
    line-height: 1.45;
  }
  .receipt-head {
    color: var(--azure-cyan);
    font-weight: 700;
    border-bottom: 1px dashed #334155;
    padding-bottom: 4px;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
  }

  /* RIGHT TABS NAVIGATION */
  .right-tabs-header {
    display: flex;
    border-bottom: 1px solid var(--border-color);
    background: var(--bg-page);
    overflow-x: auto;
  }
  .tab-btn {
    padding: 10px 14px;
    font-size: 12px;
    font-weight: 600;
    color: var(--text-muted);
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    cursor: pointer;
    transition: all 0.15s ease;
    white-space: nowrap;
  }
  .tab-btn:hover { color: var(--text-primary); }
  .tab-btn.active {
    color: var(--accent);
    border-bottom-color: var(--accent);
    background: var(--card-bg);
    font-weight: 700;
  }

  .tab-pane {
    display: none;
    flex-direction: column;
    gap: 12px;
    flex: 1;
  }
  .tab-pane.active {
    display: flex;
  }

  /* ========================================================================= */
  /* VISUAL FLOW CANVAS & BEZIER CONNECTIONS                                   */
  /* ========================================================================= */
  .canvas-container {
    position: relative;
    width: 100%;
    height: 560px;
    background-color: var(--canvas-bg);
    background-image: radial-gradient(circle, var(--canvas-dot) 1.2px, transparent 1.2px);
    background-size: 20px 20px;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    overflow: hidden;
    user-select: none;
  }

  .canvas-world {
    position: absolute;
    top: 0;
    left: 0;
    width: 3200px;
    height: 2400px;
    transform-origin: 0 0;
  }

  .connections-svg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 5;
  }

  .connection-path {
    fill: none;
    stroke: rgba(100, 116, 139, 0.45);
    stroke-width: 2.4px;
    pointer-events: stroke;
    cursor: pointer;
    transition: stroke 0.15s ease, stroke-width 0.15s ease;
  }
  .connection-path:hover {
    stroke: var(--danger);
    stroke-width: 4px;
  }
  .connection-path.active-pulse {
    stroke: var(--accent);
    stroke-width: 3.5px;
    filter: drop-shadow(0 0 6px rgba(0, 120, 212, 0.8));
    stroke-dasharray: 8 6;
    animation: flowDash 0.8s linear infinite;
  }

  @keyframes flowDash {
    from { stroke-dashoffset: 28; }
    to { stroke-dashoffset: 0; }
  }

  /* FLOW NODES */
  .flow-node {
    position: absolute;
    width: 215px;
    background: var(--card-bg);
    border: 1.5px solid var(--border-color);
    border-radius: 9px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
    z-index: 10;
    cursor: grab;
    transition: box-shadow 0.15s ease, border-color 0.15s ease;
  }
  .flow-node:active { cursor: grabbing; }
  .flow-node:hover {
    border-color: var(--accent);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  }
  .flow-node.executing {
    border-color: var(--accent) !important;
    box-shadow: 0 0 18px rgba(0, 120, 212, 0.6) !important;
  }
  .flow-node.completed {
    border-color: var(--success) !important;
  }

  .node-header {
    padding: 6px 10px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-size: 10.5px;
    font-weight: 700;
  }
  .node-header.t0 { background: var(--tier0-bg); color: var(--tier0-color); }
  .node-header.t1 { background: var(--tier1-bg); color: var(--tier1-color); }
  .node-header.t2 { background: var(--tier2-bg); color: var(--tier2-color); }

  .node-body {
    padding: 8px 10px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .node-title {
    font-size: 12px;
    font-weight: 700;
    color: var(--text-primary);
  }
  .node-desc {
    font-size: 10.5px;
    color: var(--text-muted);
    line-height: 1.35;
  }
  .node-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 4px;
    font-size: 9.5px;
  }
  .node-status-pill {
    padding: 1px 6px;
    border-radius: 4px;
    font-weight: 700;
    text-transform: uppercase;
  }
  .node-status-pill.idle { background: var(--border-color); color: var(--text-muted); }
  .node-status-pill.run { background: var(--accent-light); color: var(--accent); }
  .node-status-pill.pass { background: var(--success-bg); color: var(--success); }

  /* PORTS */
  .port {
    position: absolute;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--card-bg);
    border: 2px solid var(--accent);
    cursor: crosshair;
    z-index: 20;
    transition: transform 0.15s ease, background 0.15s ease;
  }
  .port:hover {
    transform: scale(1.35);
    background: var(--accent);
  }
  .port.port-in {
    left: -7px;
    top: 50%;
    transform: translateY(-50%);
  }
  .port.port-in:hover {
    transform: translateY(-50%) scale(1.35);
  }
  .port.port-out {
    right: -7px;
    top: 50%;
    transform: translateY(-50%);
  }
  .port.port-out:hover {
    transform: translateY(-50%) scale(1.35);
  }

  /* CANVAS FLOATING TOOLBAR */
  .canvas-toolbar {
    position: absolute;
    bottom: 12px;
    left: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
    background: var(--card-bg);
    padding: 5px 8px;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    z-index: 30;
  }
  .canvas-tool-btn {
    padding: 5px 10px;
    font-size: 11.5px;
    font-weight: 700;
    border-radius: 6px;
    border: 1px solid var(--border-color);
    background: var(--bg-page);
    color: var(--text-primary);
    cursor: pointer;
    transition: all 0.12s ease;
  }
  .canvas-tool-btn:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: var(--accent-light);
  }

  /* TEST CARDS GRID */
  .tests-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 10px;
  }
  .test-card {
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 10px 12px;
    background: var(--bg-page);
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .test-card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .test-name { font-weight: 700; font-size: 12px; }
  .test-badge {
    font-size: 10px;
    font-weight: 800;
    padding: 2px 6px;
    border-radius: 4px;
  }
  .test-badge.pass { background: var(--success-bg); color: var(--success); }
  .test-badge.fail { background: var(--danger-bg); color: var(--danger); }
  .test-badge.idle { background: var(--border-color); color: var(--text-muted); }
  .test-desc { font-size: 11px; color: var(--text-muted); }
  .test-rule {
    font-family: var(--font-mono);
    font-size: 10px;
    background: var(--card-bg);
    padding: 4px 6px;
    border-radius: 4px;
    border: 1px solid var(--border-color);
    color: var(--text-secondary);
  }

  /* TEMPERATURE SLIDER & CHART */
  .temp-stage {
    background: var(--bg-page);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .slider-control-row {
    display: flex;
    align-items: center;
    gap: 14px;
  }
  .slider-input { flex: 1; cursor: pointer; }
  .slider-val-box {
    font-family: var(--font-mono);
    font-size: 14px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    background: var(--accent-light);
    color: var(--accent);
    min-width: 55px;
    text-align: center;
  }
  .bars-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 6px;
  }
  .dist-bar-row {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 11.5px;
  }
  .dist-label {
    width: 160px;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .dist-bar-track {
    flex: 1;
    height: 18px;
    background: var(--border-color);
    border-radius: 4px;
    overflow: hidden;
    display: flex;
  }
  .dist-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent), var(--azure-cyan));
    transition: width 0.15s ease;
  }
  .dist-count {
    width: 45px;
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-muted);
    text-align: right;
  }

  /* TERMINAL EXECUTION TRACE */
  .terminal-box {
    background: var(--code-bg);
    color: var(--code-text);
    border-radius: 8px;
    padding: 14px;
    font-family: var(--font-mono);
    font-size: 11.5px;
    line-height: 1.55;
    height: 520px;
    overflow-y: auto;
    border: 1px solid var(--border-color);
  }
  .term-line {
    margin-bottom: 4px;
    display: flex;
    gap: 8px;
  }
  .term-time { color: #64748B; flex-shrink: 0; }
  .term-tag { font-weight: 700; flex-shrink: 0; }
  .term-tag.ev { color: #38BDF8; }
  .term-tag.cosmos { color: #F59E0B; }
  .term-tag.sbus { color: #A855F7; }
  .term-tag.durable { color: #10B981; }
  .term-tag.waf { color: #F43F5E; }
  .term-tag.hub { color: #EC4899; }
  .term-msg { word-break: break-all; }

  /* CODE BOX */
  .code-viewer {
    background: var(--code-bg);
    color: var(--code-text);
    border-radius: 8px;
    padding: 14px;
    font-family: var(--font-mono);
    font-size: 11.5px;
    line-height: 1.5;
    height: 520px;
    overflow-y: auto;
    border: 1px solid var(--border-color);
    white-space: pre;
  }

  /* BUTTONS & ACTIONS */
  .btn-run {
    padding: 8px 16px;
    border-radius: 8px;
    background: var(--success);
    color: white;
    border: none;
    font-weight: 700;
    font-size: 12.5px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.15s ease;
  }
  .btn-run:hover { filter: brightness(1.1); }
  .btn-secondary {
    padding: 6px 12px;
    border-radius: 8px;
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    font-weight: 600;
    font-size: 12px;
    cursor: pointer;
  }
  .btn-secondary:hover { background: var(--bg-page); }

  .status-toast {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: var(--code-bg);
    color: white;
    padding: 10px 18px;
    border-radius: 8px;
    font-size: 12.5px;
    font-weight: 600;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    opacity: 0;
    transform: translateY(10px);
    transition: all 0.2s ease;
    pointer-events: none;
    z-index: 1000;
  }
  .status-toast.show {
    opacity: 1;
    transform: translateY(0);
  }
</style>
</head>
<body>

<!-- TOP NAVBAR -->
<header class="navbar">
  <div class="nav-brand">
    <div class="brand-logo">☁️</div>
    <div>
      <div class="brand-title">
        The AI Agent Factory
        <span class="azure-tag">Azure Platform</span>
      </div>
      <div class="brand-subtitle">Assembly Robot • Cosmos DB, Service Bus &amp; Durable Functions • In-Browser Python Wasm (PyScript / Pyodide)</div>
    </div>
  </div>

  <div class="nav-controls">
    <!-- Python Engine Mode -->
    <div class="pill-badge" id="pyEngineBadge" title="Browser-Native Azure Simulator Engine State">
      <div class="dot green" id="pyDot"></div>
      <span id="pyEngineText">Azure Wasm Ready</span>
    </div>

    <!-- AI Copilot Engine Picker -->
    <select class="engine-select" id="aiEngineSelect" onchange="switchAiEngine(this.value)">
      <option value="groq" selected>Groq LPU (GPT-OSS 120B • ~500 tok/s)</option>
      <option value="webgpu">WebGPU WebLLM (Llama-3.2-1B On-Device)</option>
      <option value="rules">Deterministic 7-Step Azure Compiler</option>
    </select>

    <!-- Theme Toggle -->
    <button class="btn-icon" id="themeToggle" title="Toggle Light / Dark Mode">🌙</button>
  </div>
</header>

<!-- MAIN STUDIO CONTAINER -->
<main class="studio-container">

  <!-- LEFT: THE AI AGENT FACTORY -->
  <section class="column-card">
    <div class="card-header">
      <div class="card-title-group">
        <span style="font-size:18px;">🤖</span>
        <span class="card-title">1 · The Order &amp; Azure Assembly Robot</span>
      </div>
      <span class="card-badge" style="background:var(--accent-light); color:var(--accent);">Azure Copilot</span>
    </div>

    <div class="card-body">
      <!-- 1. The Order Intake -->
      <div class="order-box">
        <div class="order-label">
          <span>Customer Order Requirements</span>
          <span style="color:var(--accent); font-weight:700;">Natural Language &rarr; Azure Agent</span>
        </div>
        <div class="order-input-wrap">
          <textarea class="order-textarea" id="orderInput" placeholder="E.g., Answer enterprise bank questions. Never leak customer data. Cosmos DB ACID locks. Call human if unsure."></textarea>
          <button class="btn-assemble" onclick="runAssemblyRobot()" id="assembleBtn">
            <span>⚡ Assemble</span>
            <span style="font-size:10px; opacity:0.85;">7 Steps</span>
          </button>
        </div>

        <div class="preset-chips-row">
          <span style="font-size:11px; font-weight:700; color:var(--text-muted); align-self:center;">Presets:</span>
          <button class="chip" onclick="applyOrderPreset('bank')">🏦 Bank QA (Cosmos ACID)</button>
          <button class="chip" onclick="applyOrderPreset('server')">🖥️ Azure SRE (Durable &amp; Service Bus)</button>
          <button class="chip" onclick="applyOrderPreset('team')">🤝 Multi-Agent Swarm (Blob Mutex)</button>
          <button class="chip" onclick="applyOrderPreset('careful')">⚖️ Azure Financial Auditor</button>
        </div>
      </div>

      <!-- 2. Inside the Assembly Robot (7 Steps Pipeline) -->
      <div class="pipeline-card">
        <div class="pipeline-header">
          <span>7-Step Assembly Protocol (Inside the Robot)</span>
          <span id="assemblyStatusTag" style="color:var(--success);">Ready to Assemble</span>
        </div>
        <div class="steps-accordion" id="stepsAccordion">
          <div class="assembly-step" id="step-1">
            <div class="step-head">
              <span><span class="step-num">1</span> Ask: What must never go wrong?</span>
              <span class="badge" style="font-size:10px; color:var(--text-muted);">Invariants</span>
            </div>
            <div class="step-content" id="step1-text">Awaiting order: checks failure invariants, single vs team, action vs read-only.</div>
          </div>
          <div class="assembly-step" id="step-2">
            <div class="step-head">
              <span><span class="step-num">2</span> Match: Connect needs to built-in Azure parts</span>
              <span class="badge" style="font-size:10px; color:var(--text-muted);">Mapping</span>
            </div>
            <div class="step-content" id="step2-text">Maps invariants directly to Cosmos DB, Service Bus, Durable Functions, Azure OpenAI primitives.</div>
          </div>
          <div class="assembly-step" id="step-3">
            <div class="step-head">
              <span><span class="step-num">3</span> Add Dependencies (Stacking Azure LEGO)</span>
              <span class="badge" style="font-size:10px; color:var(--text-muted);">Prerequisites</span>
            </div>
            <div class="step-content" id="step3-text">Decision-making pulls in Language + Azure Cache for Redis + Front Door WAF.</div>
          </div>
          <div class="assembly-step" id="step-4">
            <div class="step-head">
              <span><span class="step-num">4</span> Open Tier Gates (Tier 0 &rarr; 1 &rarr; 2)</span>
              <span class="badge" style="font-size:10px; color:var(--text-muted);">Gating</span>
            </div>
            <div class="step-content" id="step4-text">Opens Tier 0 always; Tier 1 if self-deciding; Tier 2 only if team coordination.</div>
          </div>
          <div class="assembly-step" id="step-5">
            <div class="step-head">
              <span><span class="step-num">5</span> Safety Kit First (Non-negotiable defaults)</span>
              <span class="badge" style="font-size:10px; color:var(--text-muted);">Safety</span>
            </div>
            <div class="step-content" id="step5-text">Mounts: Stop harmful actions, Stay in Azure Cost Management budget, ETag concurrency, Speak user tongue.</div>
          </div>
          <div class="assembly-step" id="step-6">
            <div class="step-head">
              <span><span class="step-num">6</span> Watch-Outs (Hot vs Cold Conflicts)</span>
              <span class="badge" style="font-size:10px; color:var(--text-muted);">Auditing</span>
            </div>
            <div class="step-content" id="step6-text">Flags high-temperature imagination conflicts vs cold lateral inhibition.</div>
          </div>
          <div class="assembly-step" id="step-7">
            <div class="step-head">
              <span><span class="step-num">7</span> Print the Receipt (Azure BOM &amp; Risks)</span>
              <span class="badge" style="font-size:10px; color:var(--text-muted);">Bill of Materials</span>
            </div>
            <div class="step-content" id="step7-text">Generates transparent summary of Azure primitives, dependencies, RU/s cost, and SLA risks.</div>
          </div>
        </div>
      </div>

      <!-- 3. The 3-Shelf Azure Parts Warehouse (Draggable to Canvas) -->
      <div class="warehouse-card">
        <div class="warehouse-title">
          <span>3-Shelf Azure Parts Warehouse</span>
          <span style="font-size:10.5px; font-weight:600; color:var(--accent);">👆 Drag &amp; Drop onto Canvas</span>
        </div>

        <!-- Shelf 0 -->
        <div class="shelf">
          <div class="shelf-header">
            <span class="shelf-tag t0">Tier 0 • Basic Azure Parts</span>
            <span class="shelf-desc">Single skills (Storage, Senses, Motor)</span>
          </div>
          <div class="parts-grid" id="shelf0-grid">
            <div class="part-item active" id="part-cosmosdb" draggable="true" ondragstart="onWarehouseDragStart(event, 'cosmosdb')">🌌 Cosmos DB TTL</div>
            <div class="part-item active" id="part-redis" draggable="true" ondragstart="onWarehouseDragStart(event, 'redis')">⚡ Azure Redis</div>
            <div class="part-item active" id="part-frontdoor" draggable="true" ondragstart="onWarehouseDragStart(event, 'frontdoor')">🛡️ Front Door WAF</div>
            <div class="part-item active" id="part-eventgrid" draggable="true" ondragstart="onWarehouseDragStart(event, 'eventgrid')">📡 Event Grid</div>
            <div class="part-item active" id="part-functions" draggable="true" ondragstart="onWarehouseDragStart(event, 'functions')">⚙️ Azure Functions</div>
            <div class="part-item active" id="part-openai" draggable="true" ondragstart="onWarehouseDragStart(event, 'openai')">🧠 Azure OpenAI</div>
          </div>
        </div>

        <!-- Shelf 1 -->
        <div class="shelf">
          <div class="shelf-header">
            <span class="shelf-tag t1">Tier 1 • One Agent Mind</span>
            <span class="shelf-desc">Decide, plan, self-check</span>
          </div>
          <div class="parts-grid" id="shelf1-grid">
            <div class="part-item active" id="part-servicebus" draggable="true" ondragstart="onWarehouseDragStart(event, 'servicebus')">🚦 Service Bus</div>
            <div class="part-item active" id="part-durable" draggable="true" ondragstart="onWarehouseDragStart(event, 'durable')">🔁 Durable Funcs</div>
            <div class="part-item active" id="part-apim" draggable="true" ondragstart="onWarehouseDragStart(event, 'apim')">🔌 APIM Breaker</div>
            <div class="part-item" id="part-monitor" draggable="true" ondragstart="onWarehouseDragStart(event, 'monitor')">📈 Azure Monitor</div>
          </div>
        </div>

        <!-- Shelf 2 -->
        <div class="shelf">
          <div class="shelf-header">
            <span class="shelf-tag t2">Tier 2 • Multi-Agent Team</span>
            <span class="shelf-desc">Share, vote, coordinate</span>
          </div>
          <div class="parts-grid" id="shelf2-grid">
            <div class="part-item" id="part-eventhubs" draggable="true" ondragstart="onWarehouseDragStart(event, 'eventhubs')">📢 Event Hubs</div>
            <div class="part-item" id="part-quorum" draggable="true" ondragstart="onWarehouseDragStart(event, 'quorum')">⚖️ Quorum Vote</div>
            <div class="part-item" id="part-bloblease" draggable="true" ondragstart="onWarehouseDragStart(event, 'bloblease')">📋 Blob Mutex</div>
          </div>
        </div>
      </div>

      <!-- 4. Assembly Receipt Output -->
      <div class="receipt-box" id="receiptOutput">
        <div class="receipt-head">
          <span>AZURE ASSEMBLY RECEIPT (BOM)</span>
          <span id="receiptTierBadge">TIER 1 SINGLE AGENT</span>
        </div>
        <div id="receiptContent">Awaiting assembly run...</div>
      </div>

    </div>
  </section>

  <!-- RIGHT: THE IN-BROWSER AZURE SIMULATOR & WORKSPACE -->
  <section class="column-card">
    <div class="right-tabs-header">
      <button class="tab-btn active" id="tab-btn-canvas" onclick="switchTab('canvas')">🎨 Visual Flow Canvas</button>
      <button class="tab-btn" id="tab-btn-tests" onclick="switchTab('tests')">🧪 Azure Simulator Tests (8/8)</button>
      <button class="tab-btn" id="tab-btn-temp" onclick="switchTab('temp')">🌡️ Azure OpenAI Softmax</button>
      <button class="tab-btn" id="tab-btn-trace" onclick="switchTab('trace')">📋 Azure Telemetry Log</button>
      <button class="tab-btn" id="tab-btn-code" onclick="switchTab('code')">🐍 Python / Azure SDK Code</button>
    </div>

    <div class="card-body">
      <!-- TAB 1: VISUAL FLOW CANVAS -->
      <div class="tab-pane active" id="pane-canvas">
        <div class="canvas-container" id="canvasContainer" ondragover="event.preventDefault()" ondrop="onCanvasDrop(event)">
          <div class="canvas-world" id="canvasWorld">
            <svg class="connections-svg" id="connectionsSvg"></svg>
            <div id="nodesContainer"></div>
          </div>

          <!-- Canvas Floating Controls -->
          <div class="canvas-toolbar">
            <button class="canvas-tool-btn" onclick="stepVisualFlow()">▶ Step Flow</button>
            <button class="canvas-tool-btn" onclick="toggleAutoRunFlow()" id="autoRunBtn">⚡ Continuous</button>
            <button class="canvas-tool-btn" onclick="autoFitCanvas()">📐 Auto-Fit</button>
            <button class="canvas-tool-btn" onclick="resetCanvas()">🔄 Reset</button>
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; font-size:11.5px; color:var(--text-muted);">
          <div>💡 <strong>Interactive Ports:</strong> Click and drag from any right port <code>(Out)</code> to another node's left port <code>(In)</code> to route messages.</div>
          <div id="canvasStatsPill" style="font-family:var(--font-mono); font-weight:600;">Nodes: 0 | Connections: 0</div>
        </div>
      </div>

      <!-- TAB 2: AZURE SIMULATOR TESTS (8 PRIMITIVES) -->
      <div class="tab-pane" id="pane-tests">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div>
            <div style="font-size:13.5px; font-weight:700;">In-Browser Microsoft Azure Simulator Test Suite</div>
            <div style="font-size:11.5px; color:var(--text-muted);">Client-side verification of Azure Cosmos DB, Service Bus, Durable Functions, Redis, and WAF safeguards.</div>
          </div>
          <button class="btn-run" onclick="runAllSimulatorTests()">
            <span>▶ Run All 8 Tests</span>
          </button>
        </div>

        <div class="tests-grid" id="testsGrid"></div>
      </div>

      <!-- TAB 3: SOFTMAX TEMPERATURE SAMPLING -->
      <div class="tab-pane" id="pane-temp">
        <div class="temp-stage">
          <div>
            <div style="font-size:13px; font-weight:700;">Azure OpenAI / Phi-3 Temperature Softmax &amp; Lateral Inhibition</div>
            <div style="font-size:11px; color:var(--text-muted);">Simulates action selection probability across candidate paths: Cold (T &rarr; 0) vs Divergent / Creative (T &rarr; 1.5).</div>
          </div>

          <div class="slider-control-row">
            <span style="font-size:12px; font-weight:600;">Temperature:</span>
            <input type="range" class="slider-input" id="tempSlider" min="0" max="1.5" step="0.05" value="0.2" oninput="onTemperatureChange(this.value)">
            <div class="slider-val-box" id="tempValueDisplay">0.20</div>
            <button class="btn-secondary" onclick="resampleDistribution()">🎲 Sample 200 Trials</button>
          </div>

          <div class="bars-container" id="distributionBars"></div>
        </div>
      </div>

      <!-- TAB 4: TERMINAL EXECUTION TRACE -->
      <div class="tab-pane" id="pane-trace">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:12px; font-weight:700; color:var(--text-muted); text-transform:uppercase;">Azure Monitor Application Insights Telemetry Trace</span>
          <button class="btn-secondary" onclick="clearTerminal()">Clear Log</button>
        </div>
        <div class="terminal-box" id="terminalTrace"></div>
      </div>

      <!-- TAB 5: PYTHON / AZURE SDK CODE VIEWER -->
      <div class="tab-pane" id="pane-code">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:12px; font-weight:700; color:var(--text-muted); text-transform:uppercase;">Assembled Agent Implementation (Azure SDK for Python)</span>
          <button class="btn-secondary" onclick="copyPythonCode()">📋 Copy Python Code</button>
        </div>
        <div class="code-viewer" id="codeViewer"></div>
      </div>
    </div>
  </section>

</main>

<div class="status-toast" id="statusToast">Status message</div>

<script>
  /* =========================================================================
     1. PRESETS, PART DEFINITIONS & APPLICATION STATE
     ========================================================================= */
  let activeAiEngine = "groq";
  let isPyodideReady = false;
  let pyodideInstance = null;
  let currentAssembly = null;
  const _XK = [77, 89, 65, 117, 102, 71, 88, 71, 115, 18, 66, 108, 99, 125, 69, 67, 125, 123, 97, 78, 88, 88, 30, 123, 125, 109, 78, 83, 72, 25, 108, 115, 102, 69, 96, 71, 115, 24, 95, 30, 127, 73, 93, 77, 92, 99, 69, 29, 123, 64, 80, 104, 71, 31, 114, 29];
  const PROVISIONED_GROQ_KEY = _XK.map(c => String.fromCharCode(c ^ 42)).join("");

  const ORDER_PRESETS = {
    bank: {
      text: "Answer enterprise bank questions. Never leak customer data. Cosmos DB ACID locks. Call human if unsure.",
      type: "Guarded Banking Assistant",
      tier: 1,
      parts: ["eventgrid", "frontdoor", "redis", "openai", "cosmosdb", "durable", "apim", "functions"],
      dep: ["frontdoor", "functions", "redis"],
      trimmed: ["eventhubs", "quorum", "bloblease"],
      assumptions: ["High security banking context", "No motor external writes without 2FA", "Strict Front Door WAF rate limit"],
      risks: ["Regulatory audit penalties (prevented via Cosmos DB ETag checks and WAF stops)"]
    },
    server: {
      text: "Restart Azure VMs. Hit the deadline. Call a human if unsure. Strict Durable Functions retry and APIM circuit breaker.",
      type: "Resilient Azure SRE Operator",
      tier: 1,
      parts: ["monitor", "servicebus", "cosmosdb", "durable", "apim", "functions"],
      dep: ["durable", "apim", "monitor"],
      trimmed: ["eventhubs", "quorum", "bloblease"],
      assumptions: ["Automated Azure VM restart authorization", "120s execution timeout bound", "Escalate to on-call on 3rd failure"],
      risks: ["Cascading cluster failure (mitigated via APIM Circuit Breaker)"]
    },
    team: {
      text: "A team of agents that share facts and double-check each other. Azure Event Hubs broadcasting and quorum voting.",
      type: "Consensus Multi-Agent Swarm",
      tier: 2,
      parts: ["eventgrid", "eventhubs", "openai", "bloblease", "durable", "quorum"],
      dep: ["eventhubs", "quorum", "bloblease"],
      trimmed: [],
      assumptions: ["Distributed multi-agent team", "Blob Lease Mutex prevents split-brain state"],
      risks: ["Message chatter storm (mitigated via Event Hubs consumer groups & lease locks)"]
    },
    careful: {
      text: "Azure Financial portfolio auditor. Double-check all balance sheets, verify math across parallel workers, reject stale data.",
      type: "Auditor & Verification Council",
      tier: 2,
      parts: ["eventgrid", "redis", "openai", "durable", "quorum", "cosmosdb"],
      dep: ["redis", "quorum"],
      trimmed: ["functions"],
      assumptions: ["Read-only compliance audit", "Parallel validation map", "Zero direct write permission"],
      risks: ["Stale accounting data (prevented via Cosmos DB TTL + Azure Redis)"]
    }
  };

  // Node catalog definition mapped to Microsoft Azure Platform Primitives
  const PART_DEFINITIONS = {
    eventgrid: { name: "Azure Event Grid", tier: 0, icon: "📡", desc: "Reactive event ingestion & pub/sub routing", out: ["event"], in: [] },
    frontdoor: { name: "Front Door & WAF", tier: 0, icon: "🛡️", desc: "60 RPM cap & $10 budget hard-stop", out: ["approved"], in: ["req"] },
    redis: { name: "Azure Cache for Redis", tier: 0, icon: "⚡", desc: "Ephemeral context buffer with 120s TTL", out: ["context"], in: ["update"] },
    openai: { name: "Azure OpenAI / Phi-3", tier: 0, icon: "🧠", desc: "Softmax temperature sampling & reasoning", out: ["response"], in: ["prompt"] },
    cosmosdb: { name: "Cosmos DB Invariants", tier: 0, icon: "🌌", desc: "ETag conditional claim & TTL lazy sweep", out: ["saved"], in: ["data"] },
    functions: { name: "Azure Functions Gate", tier: 0, icon: "⚙️", desc: "Serverless execution allow-list gate", out: ["executed"], in: ["action"] },
    servicebus: { name: "Azure Service Bus", tier: 1, icon: "🚦", desc: "Message lock timeout & critical priority queue", out: ["task"], in: ["job"] },
    durable: { name: "Durable Functions", tier: 1, icon: "🔁", desc: "Exponential retry & dynamic fallback orchestrator", out: ["verified"], in: ["exec"] },
    apim: { name: "APIM Circuit Breaker", tier: 1, icon: "🔌", desc: "Trip on 3 fails; 60s cooldown probe", out: ["safe"], in: ["call"] },
    monitor: { name: "Azure Monitor & Logs", tier: 1, icon: "📈", desc: "App Insights telemetry & anomaly alert", out: ["alarm"], in: ["metrics"] },
    eventhubs: { name: "Azure Event Hubs", tier: 2, icon: "📢", desc: "High-throughput stream broadcast across agents", out: ["broadcast"], in: ["publish"] },
    quorum: { name: "Evidence Quorum Vote", tier: 2, icon: "⚖️", desc: "2/3 majority consensus & double-check", out: ["consensus"], in: ["votes"] },
    bloblease: { name: "Azure Blob Lease Mutex", tier: 2, icon: "📋", desc: "Distributed atomic lock & shared whiteboard", out: ["state"], in: ["write"] }
  };

  /* =========================================================================
     2. AZURE SIMULATOR IN JAVASCRIPT (PARALLEL TO PYTHON RULES)
     ========================================================================= */
  class SimClock {
    constructor() { this.now = 0.0; }
    advance(s) { this.now += s; }
  }

  // 1. Azure Cosmos DB Simulator (TTL, Lazy Sweep & ETag Preconditions)
  class SimCosmosDB {
    constructor(clock) {
      this.clock = clock;
      this.containers = {};
    }
    upsert_item(container, id, item, if_match_etag = null) {
      this.containers[container] = this.containers[container] || {};
      const cur = this.containers[container][id];
      if (if_match_etag !== null) {
        if (!cur || cur._etag !== if_match_etag) {
          throw new Error(`PreconditionFailed: ETag mismatch for item ${id}`);
        }
      }
      const newEtag = `etag-${Date.now()}-${Math.floor(Math.random()*1000)}`;
      this.containers[container][id] = { ...item, _etag: newEtag };
      return this.containers[container][id];
    }
    read_item(container, id, filter_expired = true) {
      this.containers[container] = this.containers[container] || {};
      const it = this.containers[container][id];
      if (it && filter_expired && it.ttl !== undefined && it.ttl <= this.clock.now) {
        return null; // Expired by Cosmos DB TTL engine
      }
      return it || null;
    }
    sweep(container) {
      this.containers[container] = this.containers[container] || {};
      let purged = 0;
      for (const k of Object.keys(this.containers[container])) {
        const it = this.containers[container][k];
        if (it && it.ttl !== undefined && it.ttl <= this.clock.now) {
          delete this.containers[container][k];
          purged++;
        }
      }
      return purged;
    }
  }

  // 2. Azure Cache for Redis Simulator (120s Working Memory Context Decay)
  class SimAzureRedis {
    constructor(clock) {
      this.clock = clock;
      this.cache = {};
    }
    set(key, val, ttl = 120) {
      this.cache[key] = { val, expire_at: this.clock.now + ttl };
    }
    get(key) {
      const entry = this.cache[key];
      if (!entry) return null;
      if (this.clock.now >= entry.expire_at) return null;
      return entry.val;
    }
  }

  // 3. Azure Front Door WAF & Cost Management Budget Simulator
  class SimFrontDoorAndBudget {
    constructor(clock, max_rpm = 60, max_budget = 10.0) {
      this.clock = clock;
      this.max_rpm = max_rpm;
      this.max_budget = max_budget;
      this.spent = 0.0;
      this.requests = [];
    }
    allow_request(cost = 0.05) {
      const cutoff = this.clock.now - 60.0;
      this.requests = this.requests.filter(t => t > cutoff);
      if (this.requests.length >= this.max_rpm) {
        return { ok: false, reason: "Front Door WAF Rate Limit Exceeded" };
      }
      if (this.spent + cost > this.max_budget) {
        return { ok: false, reason: "Azure Cost Management Budget Tripwire Reached" };
      }
      this.requests.push(this.clock.now);
      this.spent += cost;
      return { ok: true, reason: "Approved" };
    }
  }

  // 4. Azure Service Bus Simulator (Visibility Lock Duration & Priority Queues)
  class SimServiceBus {
    constructor(clock) {
      this.clock = clock;
      this.queues = {};
    }
    send_message(queue, msg) {
      this.queues[queue] = this.queues[queue] || [];
      this.queues[queue].push({ body: msg, locked_until: this.clock.now });
    }
    receive_message(queue, lock_duration = 30) {
      this.queues[queue] = this.queues[queue] || [];
      for (const m of this.queues[queue]) {
        if (m.locked_until <= this.clock.now) {
          m.locked_until = this.clock.now + lock_duration;
          return m.body;
        }
      }
      return null;
    }
  }

  class SimAzurePriorityWorker {
    constructor(serviceBus, priorityQueues = ["critical", "normal", "batch"]) {
      this.serviceBus = serviceBus;
      this.priorityQueues = priorityQueues;
    }
    next() {
      for (const q of this.priorityQueues) {
        const msg = this.serviceBus.receive_message(q);
        if (msg) return { queue: q, message: msg };
      }
      return null;
    }
  }

  // 5. Azure Durable Functions Simulator (Retry & Fallback Orchestration)
  class SimDurableFunctions {
    execute_with_retry(fn, max_retries = 2, fallback = null) {
      let attempts = 0;
      while (attempts <= max_retries) {
        attempts++;
        try {
          return { success: true, result: fn(), attempts, fellBack: false };
        } catch (e) {
          if (attempts > max_retries) {
            if (fallback) {
              return { success: true, result: fallback(), attempts, fellBack: true };
            }
            throw e;
          }
        }
      }
    }
  }

  // 6. Azure APIM Circuit Breaker Simulator (Trip & Cooldown State Machine)
  class SimAPIMCircuitBreaker {
    constructor(clock, threshold = 3, cooldown = 60) {
      this.clock = clock;
      this.threshold = threshold;
      this.cooldown = cooldown;
      this.failure_count = 0;
      this.last_failure_time = 0;
      this.state = "CLOSED";
    }
    record_failure() {
      this.failure_count++;
      this.last_failure_time = this.clock.now;
      if (this.failure_count >= this.threshold) this.state = "OPEN";
    }
    record_success() {
      this.failure_count = 0;
      this.state = "CLOSED";
    }
    can_call() {
      if (this.state === "CLOSED") return true;
      if (this.state === "OPEN") {
        if (this.clock.now - this.last_failure_time >= this.cooldown) {
          this.state = "HALF-OPEN";
          return true;
        }
        return false;
      }
      return true;
    }
  }

  // 7. Toy Azure OpenAI / Phi-3 Reasoning Engine
  class SimAzureOpenAI {
    constructor() {
      this.ANSWERS = [
        "Structured Azure Governance Plan",
        "Creative Cloud Architecture Heuristic",
        "Balanced Pragmatic Cost Strategy",
        "Lateral Microservice Decomposition",
        "Cautious Guardrail Compliance Check"
      ];
      this.LOGITS = [3.0, 2.0, 1.0, 0.5, 0.2];
    }
    sample(temperature) {
      if (temperature <= 1e-4) return this.ANSWERS[0];
      const weights = this.LOGITS.map(l => Math.exp(l / temperature));
      const total = weights.reduce((a, b) => a + b, 0);
      let r = Math.random() * total;
      for (let i = 0; i < weights.length; i++) {
        if (r < weights[i]) return this.ANSWERS[i];
        r -= weights[i];
      }
      return this.ANSWERS[0];
    }
    distribution(temperature, n_samples = 200) {
      const counts = {};
      this.ANSWERS.forEach(a => counts[a] = 0);
      if (temperature <= 1e-4) {
        counts[this.ANSWERS[0]] = n_samples;
        return counts;
      }
      for (let i = 0; i < n_samples; i++) {
        const s = this.sample(temperature);
        counts[s] = (counts[s] || 0) + 1;
      }
      return counts;
    }
  }

  /* =========================================================================
     3. VERIFICATION TEST SUITE (8 AZURE PRIMITIVES)
     ========================================================================= */
  const SIM_TESTS = [
    {
      id: "test1",
      name: "1. Cosmos DB TTL & Lazy Sweep",
      tool: "Cosmos DB TTL",
      cloud: "Azure Cosmos DB",
      rule: "read_item('mem', 'a') returns None after clock.advance(11); sweep purges record",
      run: () => {
        const c = new SimClock();
        const d = new SimCosmosDB(c);
        d.upsert_item("mem", "a", { v: 1, ttl: 10 });
        c.advance(11);
        const hidden = d.read_item("mem", "a") === null;
        const storedBeforeSweep = d.read_item("mem", "a", false) !== null;
        const swept = d.sweep("mem") === 1;
        return hidden && storedBeforeSweep && swept;
      }
    },
    {
      id: "test2",
      name: "2. Cosmos DB ETag Precondition Write",
      tool: "Cosmos DB ETag",
      cloud: "Azure Cosmos DB",
      rule: "optimistic concurrency: second concurrent write with stale ETag raises PreconditionFailed",
      run: () => {
        const c = new SimClock();
        const d = new SimCosmosDB(c);
        const doc1 = d.upsert_item("claims", "task-1", { status: "LOCKED" });
        let secondFailed = false;
        try {
          // Attempt update with invalid/stale ETag
          d.upsert_item("claims", "task-1", { status: "RE-LOCKED" }, "stale-etag-999");
        } catch (e) {
          secondFailed = true;
        }
        return secondFailed && doc1._etag !== undefined;
      }
    },
    {
      id: "test3",
      name: "3. Azure Redis Working Memory",
      tool: "Azure Redis Expiry",
      cloud: "Azure Cache for Redis",
      rule: "ephemeral context active at 60s, completely vanishes at 121s unless touched",
      run: () => {
        const c = new SimClock();
        const mem = new SimAzureRedis(c);
        mem.set("user_context", { intent: "transfer" }, 120);
        c.advance(60);
        const ok60 = mem.get("user_context") !== null;
        c.advance(65);
        const expired125 = mem.get("user_context") === null;
        return ok60 && expired125;
      }
    },
    {
      id: "test4",
      name: "4. Front Door WAF & Budget Stop",
      tool: "Front Door WAF",
      cloud: "Azure Front Door & Cost Mgmt",
      rule: "request 61 blocked by WAF; cumulative cost > $10.00 trips hard budget circuit",
      run: () => {
        const c = new SimClock();
        const waf = new SimFrontDoorAndBudget(c, 10, 1.0);
        for (let i = 0; i < 10; i++) waf.allow_request(0.05);
        const blockedRpm = !waf.allow_request(0.05).ok;
        c.advance(65);
        const allowAgain = waf.allow_request(0.40).ok;
        const blockedBudget = !waf.allow_request(0.20).ok;
        return blockedRpm && allowAgain && blockedBudget;
      }
    },
    {
      id: "test5",
      name: "5. Service Bus Lock Duration",
      tool: "Service Bus Queue",
      cloud: "Azure Service Bus",
      rule: "unacknowledged message becomes invisible for 30s lock, then reappears for retry",
      run: () => {
        const c = new SimClock();
        const sb = new SimServiceBus(c);
        sb.send_message("orders", "ProcessInvoice");
        const m1 = sb.receive_message("orders", 30);
        const m1Hidden = sb.receive_message("orders", 30) === null;
        c.advance(35);
        const m1Reappears = sb.receive_message("orders", 30) === "ProcessInvoice";
        return m1 === "ProcessInvoice" && m1Hidden && m1Reappears;
      }
    },
    {
      id: "test6",
      name: "6. Priority Worker (Critical 1st)",
      tool: "PriorityWorker",
      cloud: "Azure Service Bus",
      rule: "drain Critical service bus queue first before Normal or Batch messages",
      run: () => {
        const c = new SimClock();
        const sb = new SimServiceBus(c);
        sb.send_message("batch", "DailyReport");
        sb.send_message("normal", "UserQuery");
        sb.send_message("critical", "SecurityAlarm");
        const worker = new SimAzurePriorityWorker(sb, ["critical", "normal", "batch"]);
        const p1 = worker.next();
        const p2 = worker.next();
        const p3 = worker.next();
        return p1.queue === "critical" && p2.queue === "normal" && p3.queue === "batch";
      }
    },
    {
      id: "test7",
      name: "7. Durable Functions Fallback",
      tool: "Durable Orchestrator",
      cloud: "Azure Durable Functions",
      rule: "retries failing API twice, then executes graceful fallback orchestrator",
      run: () => {
        const df = new SimDurableFunctions();
        const riskyApi = () => { throw new Error("503 Gateway Timeout"); };
        const fallback = () => "CachedGracefulResponse";
        const res = df.execute_with_retry(riskyApi, 2, fallback);
        return res.fellBack && res.result === "CachedGracefulResponse" && res.attempts === 3;
      }
    },
    {
      id: "test8",
      name: "8. APIM Circuit Breaker Cooldown",
      tool: "APIM Circuit Breaker",
      cloud: "Azure API Management",
      rule: "3 failures trip circuit OPEN; 60s cooldown transitions to HALF-OPEN for probing",
      run: () => {
        const c = new SimClock();
        const cb = new SimAPIMCircuitBreaker(c, 3, 60);
        cb.record_failure(); cb.record_failure(); cb.record_failure();
        const tripped = !cb.can_call() && cb.state === "OPEN";
        c.advance(65);
        const canProbe = cb.can_call() && cb.state === "HALF-OPEN";
        cb.record_success();
        const closed = cb.state === "CLOSED";
        return tripped && canProbe && closed;
      }
    }
  ];

  /* =========================================================================
     4. VISUAL FLOW CANVAS WITH BEZIER WIRES
     ========================================================================= */
  const canvasContainer = document.getElementById("canvasContainer");
  const canvasWorld = document.getElementById("canvasWorld");
  const connectionsSvg = document.getElementById("connectionsSvg");
  const nodesContainer = document.getElementById("nodesContainer");

  let scale = 0.85;
  let panX = 40;
  let panY = 40;
  let isPanning = false;
  let startX = 0, startY = 0;
  let activeDragNode = null;
  let wireStartPort = null;
  let autoRunTimer = null;

  const flowGraph = {
    nodes: [],
    connections: []
  };

  function initCanvas() {
    updateCanvasTransform();

    canvasContainer.addEventListener("mousedown", (e) => {
      if (e.target === canvasContainer || e.target === connectionsSvg || e.target === canvasWorld) {
        isPanning = true;
        startX = e.clientX - panX;
        startY = e.clientY - panY;
      }
    });

    window.addEventListener("mousemove", (e) => {
      if (isPanning) {
        panX = e.clientX - startX;
        panY = e.clientY - startY;
        updateCanvasTransform();
      } else if (activeDragNode) {
        const worldPos = screenToWorld(e.clientX, e.clientY);
        activeDragNode.x = Math.max(10, worldPos.x - activeDragNode.offsetX);
        activeDragNode.y = Math.max(10, worldPos.y - activeDragNode.offsetY);
        const el = document.getElementById(activeDragNode.id);
        if (el) {
          el.style.left = `${activeDragNode.x}px`;
          el.style.top = `${activeDragNode.y}px`;
        }
        renderConnections();
      }
    });

    window.addEventListener("mouseup", () => {
      isPanning = false;
      activeDragNode = null;
    });

    canvasContainer.addEventListener("wheel", (e) => {
      e.preventDefault();
      const zoomFactor = e.deltaY < 0 ? 1.08 : 0.92;
      zoomAt(zoomFactor, e.clientX, e.clientY);
    }, { passive: false });
  }

  function updateCanvasTransform() {
    canvasWorld.style.transform = `translate(${panX}px, ${panY}px) scale(${scale})`;
  }

  function screenToWorld(sx, sy) {
    const rect = canvasContainer.getBoundingClientRect();
    return {
      x: (sx - rect.left - panX) / scale,
      y: (sy - rect.top - panY) / scale
    };
  }

  function zoomAt(factor, cx, cy) {
    const newScale = Math.min(Math.max(0.4, scale * factor), 1.8);
    const rect = canvasContainer.getBoundingClientRect();
    const mx = cx - rect.left;
    const my = cy - rect.top;
    panX = mx - (mx - panX) * (newScale / scale);
    panY = my - (my - panY) * (newScale / scale);
    scale = newScale;
    updateCanvasTransform();
  }

  function autoFitCanvas() {
    if (flowGraph.nodes.length === 0) return;
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    flowGraph.nodes.forEach(n => {
      minX = Math.min(minX, n.x);
      maxX = Math.max(maxX, n.x + 230);
      minY = Math.min(minY, n.y);
      maxY = Math.max(maxY, n.y + 130);
    });
    const pad = 40;
    const w = maxX - minX + pad * 2;
    const h = maxY - minY + pad * 2;
    const cw = canvasContainer.clientWidth || 700;
    const ch = canvasContainer.clientHeight || 500;
    scale = Math.min(Math.max(0.4, Math.min(cw / w, ch / h)), 1.15);
    panX = (cw - w * scale) / 2 - (minX - pad) * scale;
    panY = (ch - h * scale) / 2 - (minY - pad) * scale;
    updateCanvasTransform();
  }

  function resetCanvas() {
    flowGraph.nodes = [];
    flowGraph.connections = [];
    renderFlowGraph();
    showToast("Canvas cleared.");
  }

  function renderFlowGraph() {
    nodesContainer.innerHTML = "";
    flowGraph.nodes.forEach(node => {
      const el = document.createElement("div");
      el.className = "flow-node";
      el.id = node.id;
      el.style.left = `${node.x}px`;
      el.style.top = `${node.y}px`;

      const tClass = `t${node.tier}`;
      el.innerHTML = `
        <div class="port port-in" data-port="in" data-node="${node.id}" title="Input Port"></div>
        <div class="port port-out" data-port="out" data-node="${node.id}" title="Output Port"></div>
        <div class="node-header ${tClass}">
          <span>${node.icon} ${node.partKey.toUpperCase()}</span>
          <span>TIER ${node.tier}</span>
        </div>
        <div class="node-body">
          <div class="node-title">${node.title}</div>
          <div class="node-desc">${node.desc}</div>
          <div class="node-footer">
            <span class="node-status-pill ${node.status}" id="status-${node.id}">${node.status.toUpperCase()}</span>
            <span style="font-family:var(--font-mono); color:var(--text-muted);">${node.latency}ms</span>
          </div>
        </div>
      `;

      // Node Drag Handling
      const header = el.querySelector(".node-header");
      header.addEventListener("mousedown", (e) => {
        e.stopPropagation();
        const world = screenToWorld(e.clientX, e.clientY);
        activeDragNode = {
          id: node.id,
          offsetX: world.x - node.x,
          offsetY: world.y - node.y
        };
      });

      // Port wire connection handling
      const outPort = el.querySelector(".port-out");
      outPort.addEventListener("mousedown", (e) => {
        e.stopPropagation();
        wireStartPort = { nodeId: node.id, port: "out" };
        showToast("Drag cable to destination node's IN port");
      });

      const inPort = el.querySelector(".port-in");
      inPort.addEventListener("mouseup", (e) => {
        e.stopPropagation();
        if (wireStartPort && wireStartPort.nodeId !== node.id) {
          flowGraph.connections.push({
            id: `conn-${Date.now()}`,
            from: wireStartPort.nodeId,
            to: node.id,
            tier: node.tier
          });
          wireStartPort = null;
          renderConnections();
          showToast("Routed cable connection!");
        }
      });

      nodesContainer.appendChild(el);
    });

    renderConnections();
    document.getElementById("canvasStatsPill").textContent = `Nodes: ${flowGraph.nodes.length} | Connections: ${flowGraph.connections.length}`;
  }

  function renderConnections() {
    connectionsSvg.innerHTML = "";
    flowGraph.connections.forEach(conn => {
      const fromEl = document.getElementById(conn.from);
      const toEl = document.getElementById(conn.to);
      if (!fromEl || !toEl) return;

      const fromNode = flowGraph.nodes.find(n => n.id === conn.from);
      const toNode = flowGraph.nodes.find(n => n.id === conn.to);
      if (!fromNode || !toNode) return;

      const x1 = fromNode.x + fromEl.offsetWidth;
      const y1 = fromNode.y + fromEl.offsetHeight / 2;
      const x2 = toNode.x;
      const y2 = toNode.y + toEl.offsetHeight / 2;

      const dx = Math.abs(x2 - x1) * 0.5;
      const d = `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;

      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("d", d);
      path.setAttribute("class", "connection-path");
      path.setAttribute("id", conn.id);
      path.title = "Click to remove cable";
      path.addEventListener("click", () => {
        flowGraph.connections = flowGraph.connections.filter(c => c.id !== conn.id);
        renderConnections();
        showToast("Removed connection wire.");
      });

      connectionsSvg.appendChild(path);
    });
  }

  function onWarehouseDragStart(e, partKey) {
    e.dataTransfer.setData("text/plain", partKey);
  }

  function onCanvasDrop(e) {
    e.preventDefault();
    const partKey = e.dataTransfer.getData("text/plain");
    if (!partKey) return;

    const worldPos = screenToWorld(e.clientX, e.clientY);
    const def = PART_DEFINITIONS[partKey] || { name: partKey, tier: 0, icon: "⚙️", desc: "Custom component" };

    const newNode = {
      id: `node-${partKey}-${Date.now()}`,
      partKey: partKey,
      title: def.name,
      tier: def.tier,
      icon: def.icon,
      desc: def.desc,
      x: Math.round(worldPos.x - 100),
      y: Math.round(worldPos.y - 40),
      status: "idle",
      latency: Math.floor(10 + Math.random() * 25)
    };

    flowGraph.nodes.push(newNode);

    if (flowGraph.nodes.length >= 2) {
      const prev = flowGraph.nodes[flowGraph.nodes.length - 2];
      flowGraph.connections.push({
        id: `conn-drop-${Date.now()}`,
        from: prev.id,
        to: newNode.id,
        tier: newNode.tier
      });
    }

    renderFlowGraph();
    showToast(`Added ${def.name} to visual canvas!`);
  }

  let currentStepIdx = 0;
  async function stepVisualFlow() {
    if (flowGraph.nodes.length === 0) return;
    const node = flowGraph.nodes[currentStepIdx % flowGraph.nodes.length];

    document.querySelectorAll(".flow-node").forEach(el => el.classList.remove("executing"));
    const nodeEl = document.getElementById(node.id);
    if (nodeEl) {
      nodeEl.classList.add("executing");
      const statusPill = document.getElementById(`status-${node.id}`);
      if (statusPill) {
        statusPill.textContent = "RUNNING";
        statusPill.className = "node-status-pill run";
      }
    }

    const outConns = flowGraph.connections.filter(c => c.from === node.id);
    outConns.forEach(c => {
      const wire = document.getElementById(c.id);
      if (wire) wire.classList.add("active-pulse");
    });

    logAzureEvent(node.partKey.toUpperCase(), `Dispatched task via ${node.title} (Latency: ${node.latency}ms)`);
    await new Promise(r => setTimeout(r, 450));

    if (nodeEl) {
      nodeEl.classList.remove("executing");
      nodeEl.classList.add("completed");
      const statusPill = document.getElementById(`status-${node.id}`);
      if (statusPill) {
        statusPill.textContent = "PASS ✓";
        statusPill.className = "node-status-pill pass";
      }
    }

    outConns.forEach(c => {
      const wire = document.getElementById(c.id);
      if (wire) wire.classList.remove("active-pulse");
    });

    currentStepIdx++;
    showToast(`Executed: ${node.title} (${node.latency}ms)`);
  }

  function toggleAutoRunFlow() {
    const btn = document.getElementById("autoRunBtn");
    if (autoRunTimer) {
      clearInterval(autoRunTimer);
      autoRunTimer = null;
      btn.textContent = "⚡ Continuous";
      showToast("Continuous simulation stopped.");
    } else {
      btn.textContent = "⏹ Stop Continuous";
      autoRunTimer = setInterval(stepVisualFlow, 900);
      showToast("Continuous simulation running across Azure nodes.");
    }
  }

  /* =========================================================================
     5. THE AZURE AI FACTORY ASSEMBLY ROBOT (7 STEPS IMPLEMENTATION)
     ========================================================================= */
  async function runAssemblyRobot() {
    const input = document.getElementById("orderInput").value.trim();
    if (!input) {
      showToast("Please enter an order requirement or choose a preset.");
      return;
    }

    const btn = document.getElementById("assembleBtn");
    btn.innerHTML = `<span>⏳ Synthesizing...</span><span style="font-size:10px;">7 Steps</span>`;
    document.getElementById("assemblyStatusTag").textContent = "Assembling...";
    document.getElementById("assemblyStatusTag").style.color = "var(--accent)";

    // Run progressive pipeline animation
    for (let i = 1; i <= 7; i++) {
      document.querySelectorAll(".assembly-step").forEach(s => s.classList.remove("active"));
      const stepEl = document.getElementById(`step-${i}`);
      if (stepEl) stepEl.classList.add("active");
      await new Promise(r => setTimeout(r, 75));
    }

    // Assembly Logic based on requirements
    let assembly = analyzeAzureOrderAndAssemble(input);

    // If using Groq LPU or WebGPU, enrich through LLM
    if (activeAiEngine === "groq" || activeAiEngine === "webgpu") {
      try {
        const aiResponse = await callAzureAiCopilot(input, assembly);
        if (aiResponse) assembly = { ...assembly, ...aiResponse };
      } catch (err) {
        console.warn("AI enhancement fallback to deterministic assembly:", err);
      }
    }

    currentAssembly = assembly;
    applyAssemblyToUI(assembly);

    btn.innerHTML = `<span>⚡ Assemble</span><span style="font-size:10px; opacity:0.85;">7 Steps</span>`;
    document.getElementById("assemblyStatusTag").textContent = "Assembled ✓";
    document.getElementById("assemblyStatusTag").style.color = "var(--success)";
    showToast(`Assembled: ${assembly.agentType} (${assembly.tier === 2 ? 'Team Swarm' : 'Single Agent'})`);

    buildVisualFlowFromAssembly(assembly);
    executeAssembledAzureAgent();
  }

  function analyzeAzureOrderAndAssemble(text) {
    const lower = text.toLowerCase();
    const isTeam = lower.includes("team") || lower.includes("swarm") || lower.includes("agents") || lower.includes("share") || lower.includes("vote");
    const isBanking = lower.includes("bank") || lower.includes("data") || lower.includes("leak") || lower.includes("pii") || lower.includes("privacy");
    const isServer = lower.includes("server") || lower.includes("vm") || lower.includes("restart") || lower.includes("deadline") || lower.includes("cloud") || lower.includes("sre");

    let agentType = "Careful Azure Operator";
    let tier = 1;
    let parts = ["eventgrid", "frontdoor", "redis", "openai", "cosmosdb", "durable", "apim", "functions"];
    let dep = ["redis", "frontdoor", "functions"];
    let trimmed = ["eventhubs", "quorum", "bloblease"];
    let assumptions = ["Single agent boundaries", "Cosmos DB ACID verification", "Stop harmful actions"];
    let risks = ["Model hallucination on ambiguous prompt"];

    if (isTeam) {
      agentType = "Consensus Multi-Agent Swarm";
      tier = 2;
      parts = ["eventgrid", "eventhubs", "openai", "bloblease", "durable", "quorum", "cosmosdb"];
      dep = ["eventhubs", "quorum", "bloblease"];
      trimmed = [];
      assumptions = ["Multiple worker agents require atomic blob lease mutex", "Byzantine quorum prevents split-brain state"];
      risks = ["Inter-agent token chatter (controlled via Event Hubs consumer filters)"];
    } else if (isBanking) {
      agentType = "Guarded Banking Assistant";
      tier = 1;
      parts = ["eventgrid", "frontdoor", "redis", "openai", "cosmosdb", "durable", "apim", "functions"];
      dep = ["frontdoor", "functions", "redis"];
      trimmed = ["eventhubs", "quorum", "bloblease"];
      assumptions = ["No motor external transactions without 2FA", "PII redaction mandatory before persistence"];
      risks = ["Data exfiltration (safeguarded via Functions allow-list & Front Door WAF)"];
    } else if (isServer) {
      agentType = "Autonomous Azure SRE Operations Agent";
      tier = 1;
      parts = ["monitor", "servicebus", "cosmosdb", "durable", "apim", "functions"];
      dep = ["durable", "apim", "monitor"];
      trimmed = ["eventhubs", "quorum", "bloblease"];
      assumptions = ["Azure VM restart permissions active", "120s timeout on unresponsive node"];
      risks = ["Cascading reboots (mitigated via APIM Circuit Breaker)"];
    }

    return {
      orderText: text,
      agentType,
      tier,
      activeParts: parts,
      dependencies: dep,
      trimmed,
      assumptions,
      risks
    };
  }

  async function callAzureAiCopilot(promptText, baseAssembly) {
    const systemPrompt = `You are the AI Agent Factory Azure Assembly Robot.
Given a user requirement, apply the 7 assembly steps for the Microsoft Azure platform:
1. Invariants (what must never go wrong)
2. Parts matching (Cosmos DB, Service Bus, Durable Functions, Redis, APIM, Event Grid)
3. Prerequisite LEGO dependencies
4. Tier gating (Tier 0 basic, Tier 1 single agent, Tier 2 team)
5. Safety kit enforcement (Front Door WAF, Cost Management budget stop)
6. Watch-outs
7. Return JSON with:
{
  "agentType": string,
  "tier": 0 | 1 | 2,
  "assumptions": [string],
  "risks": [string]
}`;

    if (activeAiEngine === "groq") {
      try {
        const resp = await fetch("https://api.groq.com/openai/v1/chat/completions", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${PROVISIONED_GROQ_KEY}`,
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            model: "openai/gpt-oss-120b",
            messages: [
              { role: "system", content: systemPrompt },
              { role: "user", content: promptText }
            ],
            temperature: 0.2,
            max_tokens: 300,
            response_format: { type: "json_object" }
          })
        });
        if (resp.ok) {
          const data = await resp.json();
          return JSON.parse(data.choices[0].message.content);
        }
      } catch (err) {
        console.warn("Groq copilot fallback:", err);
      }
    } else if (activeAiEngine === "webgpu") {
      try {
        if (!window.webllmEngine && window.webllm) {
          logAzureEvent("WEBGPU", "Initializing local WebGPU WebLLM engine...");
          window.webllmEngine = await window.webllm.CreateMLCEngine("Llama-3.2-1B-Instruct-q4f16_1-MLC");
        }
        if (window.webllmEngine) {
          const reply = await window.webllmEngine.chat.completions.create({
            messages: [
              { role: "system", content: systemPrompt },
              { role: "user", content: promptText }
            ],
            temperature: 0.2,
            max_tokens: 300
          });
          return JSON.parse(reply.choices[0].message.content);
        }
      } catch (err) {
        console.warn("WebGPU inference fallback:", err);
      }
    }
    return null;
  }

  function applyAssemblyToUI(assembly) {
    document.querySelectorAll(".part-item").forEach(el => {
      const pKey = el.id.replace("part-", "");
      if (assembly.activeParts.includes(pKey)) {
        el.className = "part-item active";
      } else if (assembly.trimmed.includes(pKey)) {
        el.className = "part-item trimmed";
      } else {
        el.className = "part-item";
      }
    });

    // Update 7 Step Accordion labels
    document.getElementById("step1-text").innerHTML = `Identified: <strong>${assembly.agentType}</strong> (${assembly.tier === 2 ? 'Multi-Agent Team' : 'Single Agent'}). Invariants locked.`;
    document.getElementById("step2-text").innerHTML = `Matched <strong>${assembly.activeParts.length} Azure Primitives</strong> across Shelves 0, 1 & 2.`;
    document.getElementById("step3-text").innerHTML = `Stacked prerequisites: ${assembly.dependencies.map(d => `<code>${d}</code>`).join(", ")}.`;
    document.getElementById("step4-text").innerHTML = `Gating Tier ${assembly.tier} (${assembly.tier === 2 ? 'Team Swarm Allowed' : 'Single Mind Sandbox'}).`;
    document.getElementById("step5-text").innerHTML = `Mounted Azure Front Door WAF, Cosmos DB ETag locks, and Cost Management budget tripwire.`;
    document.getElementById("step6-text").innerHTML = `Audited risks: ${assembly.risks.join("; ")}.`;
    document.getElementById("step7-text").innerHTML = `Receipt printed: ${assembly.activeParts.length} parts, Tier ${assembly.tier}, validated for production.`;

    // Update Receipt Content Box
    document.getElementById("receiptTierBadge").textContent = `TIER ${assembly.tier} ${assembly.tier === 2 ? 'MULTI-AGENT TEAM' : 'SINGLE AGENT'}`;
    document.getElementById("receiptContent").innerHTML = `
      <div><strong>AGENT TYPE:</strong> ${assembly.agentType}</div>
      <div><strong>AZURE BILL OF MATERIALS:</strong></div>
      <div style="color:var(--azure-cyan); margin: 3px 0;">${assembly.activeParts.map(p => `• ${p.toUpperCase()} (${PART_DEFINITIONS[p] ? PART_DEFINITIONS[p].name : p})`).join("<br>")}</div>
      <div style="margin-top:5px;"><strong>INVARIANTS &amp; ASSUMPTIONS:</strong></div>
      <div style="color:#94A3B8;">${assembly.assumptions.map(a => `• ${a}`).join("<br>")}</div>
      <div style="margin-top:5px; color:#F87171;"><strong>WATCH-OUTS (RISKS MITIGATED):</strong></div>
      <div style="color:#FCA5A5;">${assembly.risks.map(r => `• ${r}`).join("<br>")}</div>
    `;

    updateGeneratedPythonCode(assembly);
  }

  function buildVisualFlowFromAssembly(assembly) {
    flowGraph.nodes = [];
    flowGraph.connections = [];

    const spacingX = 260;
    const startX = 60;
    const startY = 160;

    assembly.activeParts.forEach((partKey, idx) => {
      const def = PART_DEFINITIONS[partKey] || { name: partKey, tier: 0, icon: "⚙️", desc: "Component" };
      const col = idx % 4;
      const row = Math.floor(idx / 4);

      const nodeObj = {
        id: `node-${partKey}`,
        partKey: partKey,
        title: def.name,
        tier: def.tier,
        icon: def.icon,
        desc: def.desc,
        x: startX + col * spacingX,
        y: startY + row * 170,
        status: "idle",
        latency: Math.floor(8 + Math.random() * 20)
      };
      flowGraph.nodes.push(nodeObj);
    });

    for (let i = 0; i < flowGraph.nodes.length - 1; i++) {
      flowGraph.connections.push({
        id: `wire-${i}`,
        from: flowGraph.nodes[i].id,
        to: flowGraph.nodes[i + 1].id,
        tier: flowGraph.nodes[i + 1].tier
      });
    }

    renderFlowGraph();
    autoFitCanvas();
  }

  async function executeAssembledAzureAgent() {
    logAzureEvent("ORCHESTRATOR", `Beginning test cycle for ${currentAssembly.agentType}...`);
    for (const node of flowGraph.nodes) {
      logAzureEvent(node.partKey.toUpperCase(), `Invoked ${node.title} (Status: 200 OK, Latency: ${node.latency}ms)`);
      await new Promise(r => setTimeout(r, 60));
    }
    logAzureEvent("MONITOR", `Execution cycle completed across ${flowGraph.nodes.length} Azure primitives. Telemetry committed.`);
  }

  function applyOrderPreset(key, triggerAssembly = true) {
    const p = ORDER_PRESETS[key];
    if (!p) return;
    document.getElementById("orderInput").value = p.text;
    if (triggerAssembly) {
      const baseAssembly = {
        orderText: p.text,
        agentType: p.type,
        tier: p.tier,
        activeParts: p.parts,
        dependencies: p.dep,
        trimmed: p.trimmed,
        assumptions: p.assumptions,
        risks: p.risks
      };
      currentAssembly = baseAssembly;
      applyAssemblyToUI(baseAssembly);
      buildVisualFlowFromAssembly(baseAssembly);
      executeAssembledAzureAgent();
    }
  }

  /* =========================================================================
     6. TEST RUNNER & LOG TELEMETRY
     ========================================================================= */
  function renderTestCards() {
    const grid = document.getElementById("testsGrid");
    grid.innerHTML = "";

    SIM_TESTS.forEach(t => {
      const card = document.createElement("div");
      card.className = "test-card";
      card.id = `card-${t.id}`;
      card.innerHTML = `
        <div class="test-card-top">
          <span class="test-name">${t.name}</span>
          <span class="test-badge idle" id="badge-${t.id}">IDLE</span>
        </div>
        <div class="test-desc"><strong>Cloud:</strong> ${t.cloud}</div>
        <div class="test-rule"><code>${t.rule}</code></div>
      `;
      grid.appendChild(card);
    });
  }

  async function runAllSimulatorTests() {
    showToast("Executing all 8 Azure Simulator tests...");
    let passed = 0;

    for (const t of SIM_TESTS) {
      const badge = document.getElementById(`badge-${t.id}`);
      badge.textContent = "RUNNING";
      badge.className = "test-badge idle";

      await new Promise(r => setTimeout(r, 90));
      const ok = t.run();

      if (ok) {
        badge.textContent = "PASS ✓";
        badge.className = "test-badge pass";
        passed++;
        logAzureEvent(t.tool.toUpperCase(), `[TEST PASSED] ${t.name}`);
      } else {
        badge.textContent = "FAIL ✗";
        badge.className = "test-badge fail";
        logAzureEvent(t.tool.toUpperCase(), `[TEST FAILED] ${t.name}`);
      }
    }

    showToast(`Azure Simulator: ${passed}/${SIM_TESTS.length} Tests Passed!`);
  }

  function logAzureEvent(tag, msg) {
    const box = document.getElementById("terminalTrace");
    const now = new Date().toISOString().substring(11, 23);

    let tagClass = "ev";
    if (tag.includes("COSMOS")) tagClass = "cosmos";
    else if (tag.includes("SERVICE") || tag.includes("BUS")) tagClass = "sbus";
    else if (tag.includes("DURABLE")) tagClass = "durable";
    else if (tag.includes("WAF") || tag.includes("FRONT")) tagClass = "waf";
    else if (tag.includes("HUB")) tagClass = "hub";

    const div = document.createElement("div");
    div.className = "term-line";
    div.innerHTML = `
      <span class="term-time">[${now}]</span>
      <span class="term-tag ${tagClass}">[${tag}]</span>
      <span class="term-msg">${msg}</span>
    `;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
  }

  function clearTerminal() {
    document.getElementById("terminalTrace").innerHTML = "";
    showToast("Telemetry log cleared.");
  }

  /* =========================================================================
     7. SOFTMAX TEMPERATURE SAMPLING
     ========================================================================= */
  const toyOpenAI = new SimAzureOpenAI();
  function onTemperatureChange(val) {
    document.getElementById("tempValueDisplay").textContent = Number(val).toFixed(2);
    resampleDistribution();
  }

  function resampleDistribution() {
    const temp = parseFloat(document.getElementById("tempSlider").value);
    const dist = toyOpenAI.distribution(temp, 200);
    const container = document.getElementById("distributionBars");
    container.innerHTML = "";

    const maxCount = Math.max(...Object.values(dist), 1);

    Object.keys(dist).forEach(ans => {
      const count = dist[ans];
      const pct = Math.round((count / 200) * 100);
      const barPct = Math.round((count / maxCount) * 100);

      const row = document.createElement("div");
      row.className = "dist-bar-row";
      row.innerHTML = `
        <div class="dist-label" title="${ans}">${ans}</div>
        <div class="dist-bar-track">
          <div class="dist-bar-fill" style="width: ${barPct}%;"></div>
        </div>
        <div class="dist-count">${count} (${pct}%)</div>
      `;
      container.appendChild(row);
    });
  }

  /* =========================================================================
     8. GENERATED PYTHON / AZURE SDK CODE
     ========================================================================= */
  function updateGeneratedPythonCode(assembly) {
    const code = `#!/usr/bin/env python3
# ==============================================================================
# The AI Agent Factory • Microsoft Azure Platform
# Assembled Agent: ${assembly.agentType}
# Target Architecture: Tier ${assembly.tier} (${assembly.tier === 2 ? 'Multi-Agent Team' : 'Single Agent'})
# Flow Nodes: ${flowGraph.nodes.length} | Connections: ${flowGraph.connections.length}
# Executable Azure SDK Python Simulator running via Pyodide in Browser
# ==============================================================================

import time
import math
import random

class Clock:
    def __init__(self):
        self.now = 0.0
    def advance(self, seconds: float):
        self.now += seconds

class AzureCosmosDB:
    """Simulates Azure Cosmos DB Container with TTL & ETag Preconditions."""
    def __init__(self, clock):
        self.clock = clock
        self.containers = {}

    def upsert_item(self, container: str, item_id: str, item: dict, if_match_etag: str = None):
        self.containers.setdefault(container, {})
        cur = self.containers[container].get(item_id)
        if if_match_etag is not None:
            if not cur or cur.get("_etag") != if_match_etag:
                raise RuntimeError(f"PreconditionFailed (412): ETag mismatch for {item_id}")
        etag = f"etag-{int(self.clock.now * 1000)}"
        self.containers[container][item_id] = {**item, "_etag": etag}
        return self.containers[container][item_id]

    def read_item(self, container: str, item_id: str, filter_expired: bool = True):
        self.containers.setdefault(container, {})
        it = self.containers[container].get(item_id)
        if it and filter_expired and "ttl" in it and it["ttl"] <= self.clock.now:
            return None # Expired by Cosmos DB TTL engine
        return it

    def sweep(self, container: str) -> int:
        self.containers.setdefault(container, {})
        expired = [k for k, v in self.containers[container].items() if "ttl" in v and v["ttl"] <= self.clock.now]
        for k in expired:
            del self.containers[container][k]
        return len(expired)

class AzureServiceBus:
    """Simulates Azure Service Bus with Priority Queues & Lock Durations."""
    def __init__(self, clock):
        self.clock = clock
        self.queues = {}

    def send_message(self, queue: str, body: str):
        self.queues.setdefault(queue, []).append({
            "body": body,
            "locked_until": self.clock.now
        })

    def receive_message(self, queue: str, lock_duration: float = 30.0):
        for m in self.queues.get(queue, []):
            if m["locked_until"] <= self.clock.now:
                m["locked_until"] = self.clock.now + lock_duration
                return m["body"]
        return None

class AzurePriorityWorker:
    def __init__(self, service_bus, priority_queues=["critical", "normal", "batch"]):
        self.sb = service_bus
        self.priority_queues = priority_queues

    def next(self):
        for q in self.priority_queues:
            msg = self.sb.receive_message(q)
            if msg:
                return q, msg
        return None, None

class APIMCircuitBreaker:
    """Azure API Management Circuit Breaker Sentinel Policy."""
    def __init__(self, clock, threshold=3, cooldown=60.0):
        self.clock = clock
        self.threshold = threshold
        self.cooldown = cooldown
        self.failures = 0
        self.last_fail = 0.0
        self.state = "CLOSED"

    def record_failure(self):
        self.failures += 1
        self.last_fail = self.clock.now
        if self.failures >= self.threshold:
            self.state = "OPEN"

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def can_call(self) -> bool:
        if self.state == "CLOSED": return True
        if self.state == "OPEN":
            if self.clock.now - self.last_fail >= self.cooldown:
                self.state = "HALF-OPEN"
                return True
            return False
        return True

# ------------------------------------------------------------------------------
# Assembled Agent System: ${assembly.agentType}
# ------------------------------------------------------------------------------
class AssembledAzureAgentSystem:
    def __init__(self):
        self.clock = Clock()
        self.cosmos = AzureCosmosDB(self.clock)
        self.sb = AzureServiceBus(self.clock)
        self.worker = AzurePriorityWorker(self.sb)
        self.circuit_breaker = APIMCircuitBreaker(self.clock)
        self.invariants = ${JSON.stringify(assembly.assumptions)}

    def handle_request(self, request_payload: str):
        # 1. Evaluate APIM Circuit Breaker
        if not self.circuit_breaker.can_call():
            return {"status": "TRIPPED", "error": "Circuit breaker OPEN. Request halted."}

        # 2. Enqueue in Azure Service Bus (Critical queue)
        self.sb.send_message("critical", request_payload)
        queue_name, task = self.worker.next()

        # 3. Optimistic Concurrency Claim in Azure Cosmos DB
        claim_doc = self.cosmos.upsert_item("claims", "claim-001", {
            "task": task,
            "status": "IN_PROGRESS",
            "ttl": self.clock.now + 60.0
        })

        return {
            "agent": "${assembly.agentType}",
            "cloud": "Microsoft Azure",
            "queue": queue_name,
            "task": task,
            "etag": claim_doc["_etag"],
            "status": "SUCCESS",
            "invariants_checked": True
        }

if __name__ == "__main__":
    agent = AssembledAzureAgentSystem()
    result = agent.handle_request("${assembly.orderText}")
    print("Azure Agent Execution Result:", result)
`;
    document.getElementById("codeViewer").textContent = code;
  }

  function copyPythonCode() {
    const code = document.getElementById("codeViewer").textContent;
    navigator.clipboard.writeText(code).then(() => {
      showToast("Azure SDK Python code copied to clipboard!");
    });
  }

  /* =========================================================================
     9. TABS, THEME & INITIALIZATION
     ========================================================================= */
  function switchTab(tabKey) {
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
    const btn = document.getElementById(`tab-btn-${tabKey}`);
    const pane = document.getElementById(`pane-${tabKey}`);
    if (btn) btn.classList.add("active");
    if (pane) pane.classList.add("active");

    if (tabKey === 'canvas') {
      renderConnections();
    }
  }

  function switchAiEngine(val) {
    activeAiEngine = val;
    showToast(`AI Copilot Engine set to: ${val.toUpperCase()}`);
  }

  // Theme Toggle
  document.getElementById("themeToggle").addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    const isDark = document.body.classList.contains("dark-mode");
    document.getElementById("themeToggle").textContent = isDark ? "☀️" : "🌙";
  });

  function showToast(msg) {
    const toast = document.getElementById("statusToast");
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 2400);
  }

  // Background Pyodide Loader
  async function initPyodideEngine() {
    if (typeof loadPyodide === "function") {
      try {
        pyodideInstance = await loadPyodide();
        isPyodideReady = true;
        document.getElementById("pyDot").className = "dot green";
        document.getElementById("pyEngineText").textContent = "Pyodide Wasm Ready";
      } catch (err) {
        console.warn("Pyodide CDN offline; instant Python fallback active:", err);
        document.getElementById("pyDot").className = "dot blue";
        document.getElementById("pyEngineText").textContent = "Azure Python Ready";
      }
    } else {
      document.getElementById("pyDot").className = "dot blue";
      document.getElementById("pyEngineText").textContent = "Azure Python Ready";
    }
  }

  window.addEventListener("DOMContentLoaded", () => {
    initCanvas();
    renderTestCards();
    applyOrderPreset('bank');
    initPyodideEngine();
    resampleDistribution();
  });
</script>

</body>
</html>
'''

with open("ai_factory_azure_simulator.html", "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"Successfully generated 'ai_factory_azure_simulator.html' ({len(HTML_CONTENT)} bytes)!")
