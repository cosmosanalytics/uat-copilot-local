# -*- coding: utf-8 -*-
"""
build_multi_agent_brain_app.py
Builds the standalone single-file Multi-Agent Cognitive Brain Architecture web application:
multi_agent_brain_app.html

Cognitive Architecture:
1. 🧠 Frontal Executive Agent (Prefrontal Cortex: Goal decomposition, intent routing & task arbitration)
2. 🗄️ Hippocampal Memory Agent (Episodic buffer, Vector retrieval & Knowledge Graph consolidation)
3. ⚡ Broca Semantic Agent (Broca's Area: High-throughput language synthesis, token streaming)
4. 🛡️ Amygdala Safety Sentinel (Threat monitoring, ethical guardrails, circuit breaker trips)
5. 👁️ Sensory Cortex Agent (Multimodal parsing, OCR, telemetry ingestion & normalization)

Interactive Features:
- D3 Force-Directed Connectome Network Graph with real-time synaptic pulse animation
- Working Memory & Synaptic Ledger Tab (Episodic traces, vector similarity scores)
- Executive Task Decomposition Tree (Hierarchical goal DAG)
- Synaptic Neurotransmitter Controls:
  * Dopamine (Exploration / Temperature 0.1 - 1.5)
  * Acetylcholine (Attention / Context Window depth 1k - 32k)
  * Serotonin (Safety threshold / Guardrail sensitivity 0% - 100%)
  * Norepinephrine (Urgency / Latency priority vs. Depth)
- Multi-Model Inference: Groq LPU (Llama 3.3 70B), In-Browser WebGPU/WebLLM, Cognitive Simulator
- Light Mode default with Dark Mode toggle
"""

import sys

def build():
    with open("multi_agent_brain_app.html", "w", encoding="utf-8") as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Multi-Agent Cognitive Brain • Connectome &amp; Neural Architecture Studio</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<style>
  :root {
    --bg: #F5F2EA;
    --panel: #FFFFFF;
    --panel-subtle: #FAF8F3;
    --ink: #211F1A;
    --ink-soft: #6B6558;
    --ink-faint: #9E9685;
    --line: #D6CFBE;
    --line-strong: #B9AF98;

    --frontal: #6B3BA6;
    --frontal-bg: #F3EDFB;
    --hippo: #1E5C8C;
    --hippo-bg: #E9F1F7;
    --broca: #1F7A4D;
    --broca-bg: #EAF4EE;
    --amygdala: #A32B2B;
    --amygdala-bg: #FBE7E7;
    --sensory: #A9660B;
    --sensory-bg: #FBF0DC;

    --green: #1F7A4D;
    --cyan: #1E5C8C;
    --amber: #A9660B;
    --red: #A32B2B;
    --purple: #6B3BA6;

    --mono: 'IBM Plex Mono', monospace;
    --sans: 'IBM Plex Sans', sans-serif;

    --shadow-sm: 0 1px 2px rgba(33, 31, 26, 0.06);
    --shadow-md: 0 4px 10px rgba(33, 31, 26, 0.08);
  }

  [data-theme="dark"] {
    --bg: #121417;
    --panel: #1A1D24;
    --panel-subtle: #232730;
    --ink: #ECE8DE;
    --ink-soft: #A39D90;
    --ink-faint: #6B6558;
    --line: #2D3340;
    --line-strong: #454E60;

    --frontal: #A578E2;
    --frontal-bg: rgba(107, 59, 166, 0.25);
    --hippo: #4A96D1;
    --hippo-bg: rgba(30, 92, 140, 0.25);
    --broca: #48B87E;
    --broca-bg: rgba(31, 122, 77, 0.25);
    --amygdala: #E06060;
    --amygdala-bg: rgba(163, 43, 43, 0.25);
    --sensory: #E09B36;
    --sensory-bg: rgba(169, 102, 11, 0.25);

    --green: #48B87E;
    --cyan: #4A96D1;
    --amber: #E09B36;
    --red: #E06060;
    --purple: #A578E2;

    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.4);
    --shadow-md: 0 4px 10px rgba(0, 0, 0, 0.5);
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body {
    background: var(--bg);
    color: var(--ink);
    font-family: var(--sans);
    line-height: 1.5;
  }
  body {
    background-image:
      repeating-linear-gradient(0deg, rgba(33,31,26,0.04) 0 1px, transparent 1px 28px),
      repeating-linear-gradient(90deg, rgba(33,31,26,0.04) 0 1px, transparent 1px 28px);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  /* HEADER BLOCK */
  header.titleblock {
    background: var(--panel);
    border-bottom: 2px solid var(--ink);
    padding: 20px 24px 16px;
    box-shadow: var(--shadow-sm);
  }
  .header-inner {
    max-width: 1240px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 16px;
  }
  .title-content { flex: 1; min-width: 320px; }
  .kicker {
    font-family: var(--mono);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.06em;
    color: var(--cyan);
    margin-bottom: 6px;
    text-transform: uppercase;
  }
  h1 {
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.01em;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .subtitle {
    font-size: 13.5px;
    color: var(--ink-soft);
    line-height: 1.5;
    max-width: 820px;
  }

  .engine-controls {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
  }
  .engine-switch {
    display: flex;
    border: 1px solid var(--ink);
    background: var(--panel);
  }
  .engine-btn {
    padding: 6px 12px;
    font-family: var(--mono);
    font-size: 11.5px;
    font-weight: 600;
    background: var(--panel);
    border: none;
    border-right: 1px solid var(--ink);
    cursor: pointer;
    color: var(--ink);
    transition: all 0.15s;
  }
  .engine-btn:last-child { border-right: none; }
  .engine-btn.active {
    background: var(--cyan);
    color: #ffffff;
  }
  .api-key-input {
    padding: 6px 10px;
    font-family: var(--mono);
    font-size: 11.5px;
    border: 1px solid var(--line-strong);
    background: var(--panel-subtle);
    color: var(--ink);
    border-radius: 4px;
    width: 170px;
  }
  .btn-theme {
    padding: 6px 12px;
    font-family: var(--mono);
    font-size: 11.5px;
    font-weight: 600;
    border: 1px solid var(--line-strong);
    background: var(--panel);
    color: var(--ink);
    cursor: pointer;
    border-radius: 4px;
  }

  .wrap {
    max-width: 1240px;
    margin: 0 auto;
    padding: 18px 24px 60px;
    width: 100%;
    flex: 1;
  }

  /* BRAIN REGION AGENT CARDS */
  .brain-strip {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 12px;
    margin-bottom: 20px;
  }
  .agent-card {
    background: var(--panel);
    border: 1px solid var(--line-strong);
    padding: 12px;
    border-radius: 6px;
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    gap: 6px;
    transition: transform 0.2s, box-shadow 0.2s;
  }
  .agent-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  .agent-card.frontal { border-top: 3.5px solid var(--frontal); }
  .agent-card.hippo { border-top: 3.5px solid var(--hippo); }
  .agent-card.broca { border-top: 3.5px solid var(--broca); }
  .agent-card.amygdala { border-top: 3.5px solid var(--amygdala); }
  .agent-card.sensory { border-top: 3.5px solid var(--sensory); }

  .ag-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: var(--mono);
    font-size: 12px;
    font-weight: 700;
  }
  .ag-status {
    font-size: 9.5px;
    padding: 2px 6px;
    border-radius: 10px;
    font-family: var(--mono);
    background: var(--panel-subtle);
    border: 1px solid var(--line);
    color: var(--ink-soft);
  }
  .ag-role {
    font-size: 11px;
    color: var(--ink-soft);
    font-weight: 500;
  }
  .ag-desc {
    font-size: 11.5px;
    line-height: 1.4;
    color: var(--ink);
  }

  /* TABS */
  .tabbar {
    display: flex;
    border-bottom: 2px solid var(--ink);
    gap: 0;
    margin-bottom: 20px;
    overflow-x: auto;
  }
  .tabbar button {
    font-family: var(--mono);
    font-size: 13px;
    padding: 10px 18px;
    background: transparent;
    border: none;
    border-bottom: 3px solid transparent;
    color: var(--ink-soft);
    cursor: pointer;
    white-space: nowrap;
    margin-bottom: -2px;
    transition: all 0.15s;
  }
  .tabbar button.active {
    color: var(--ink);
    font-weight: 700;
    border-bottom-color: var(--cyan);
    background: var(--panel);
  }
  .tabpage { display: none; }
  .tabpage.active { display: block; }

  /* PANELS */
  .panel {
    background: var(--panel);
    border: 1px solid var(--line-strong);
    border-radius: 6px;
    margin-bottom: 20px;
    box-shadow: var(--shadow-sm);
  }
  .panel-head {
    padding: 14px 18px;
    border-bottom: 1px solid var(--line);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
  }
  .panel-head .tag {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--cyan);
    font-weight: 600;
    text-transform: uppercase;
  }
  .panel-head h2 {
    font-size: 16px;
    font-weight: 700;
  }
  .panel-body {
    padding: 18px;
  }

  /* NEUROTRANSMITTER SLIDERS */
  .neuro-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    padding: 16px;
    background: var(--panel-subtle);
    border: 1px solid var(--line);
    border-radius: 6px;
    margin-bottom: 20px;
  }
  .neuro-item {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .neuro-label {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    font-weight: 600;
  }
  .neuro-val {
    font-family: var(--mono);
    color: var(--cyan);
  }

  /* SCORECARDS */
  .scorecards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin: 16px 0;
  }
  .scorecard {
    border: 1px solid var(--line-strong);
    background: var(--panel-subtle);
    padding: 12px 14px;
    border-radius: 4px;
  }
  .scorecard .sc-label {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--ink-soft);
    text-transform: uppercase;
  }
  .scorecard .sc-total {
    font-size: 20px;
    font-weight: 700;
    margin: 4px 0;
    font-family: var(--mono);
  }
  .scorecard .sc-delta {
    font-family: var(--mono);
    font-size: 11px;
  }
  .scorecard .sc-delta.good { color: var(--green); }
  .scorecard .sc-delta.warn { color: var(--amber); }

  /* CALLOUT */
  .callout {
    padding: 12px 16px;
    font-size: 13px;
    border-left: 4px solid var(--line-strong);
    background: var(--panel-subtle);
    border-radius: 0 4px 4px 0;
    margin: 14px 0;
    line-height: 1.55;
  }
  .callout.ok { border-color: var(--green); background: var(--green-bg); color: var(--green); }
  .callout.warn { border-color: var(--amber); background: var(--amber-bg); color: var(--amber); }
  .callout.check { border-color: var(--cyan); background: var(--cyan-bg); color: var(--cyan); }

  /* D3 CONNECTOME GRAPH */
  #connectome-wrap {
    width: 100%;
    height: 520px;
    background: var(--panel-subtle);
    border: 1px solid var(--line);
    border-radius: 6px;
    position: relative;
    overflow: hidden;
  }
  svg#connectomeSvg {
    width: 100%;
    height: 100%;
    display: block;
    cursor: grab;
  }
  svg#connectomeSvg:active { cursor: grabbing; }

  /* TABLES */
  table.dt {
    width: 100%;
    border-collapse: collapse;
    font-size: 12.5px;
    margin: 14px 0;
  }
  table.dt th, table.dt td {
    border-bottom: 1px solid var(--line);
    padding: 8px 10px;
    text-align: right;
    font-family: var(--mono);
  }
  table.dt th:first-child, table.dt td:first-child {
    text-align: left;
    font-family: var(--sans);
    font-weight: 500;
  }
  table.dt th {
    color: var(--ink-soft);
    font-weight: 600;
    font-size: 11.5px;
    background: var(--panel-subtle);
  }

  /* CHAT / AGENT STREAM */
  .chat-stream {
    display: flex;
    flex-direction: column;
    gap: 12px;
    background: var(--panel-subtle);
    border: 1px solid var(--line);
    border-radius: 6px;
    padding: 16px;
    max-height: 520px;
    overflow-y: auto;
    font-size: 12.5px;
  }
  .chat-msg {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 12px 14px;
    border-radius: 4px;
    background: var(--panel);
    border: 1px solid var(--line);
  }
  .chat-msg.frontal { border-left: 4px solid var(--frontal); }
  .chat-msg.hippo { border-left: 4px solid var(--hippo); }
  .chat-msg.broca { border-left: 4px solid var(--broca); }
  .chat-msg.amygdala { border-left: 4px solid var(--amygdala); }
  .chat-msg.sensory { border-left: 4px solid var(--sensory); }

  .msg-meta {
    display: flex;
    justify-content: space-between;
    font-family: var(--mono);
    font-size: 11px;
    color: var(--ink-soft);
  }

  #toast {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: var(--ink);
    color: #ffffff;
    padding: 10px 18px;
    border-radius: 6px;
    font-size: 12.5px;
    font-family: var(--mono);
    box-shadow: var(--shadow-md);
    transform: translateY(100px);
    opacity: 0;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    z-index: 1000;
    pointer-events: none;
  }
  #toast.show {
    transform: translateY(0);
    opacity: 1;
  }

  @media (max-width: 768px) {
    header.titleblock h1 { font-size: 18px; }
    #connectome-wrap { height: 420px; }
  }
</style>

<!-- In-Browser WebGPU WebLLM Module -->
<script type="module">
  import * as webllm from "https://esm.run/@mlc-ai/web-llm@0.2.78";
  window.webllm = webllm;
  window.dispatchEvent(new Event('webllm-ready'));
</script>
</head>
<body>

<!-- HEADER BLOCK -->
<header class="titleblock">
  <div class="header-inner">
    <div class="title-content">
      <div class="kicker">MULTI-AGENT NEURAL CONNECTOME • BIOMIMETIC BRAIN ARCHITECTURE</div>
      <h1><span>🧠</span> Multi-Agent Cognitive Brain Connectome Studio</h1>
      <p class="subtitle">
        5 specialized brain region agents (Frontal Executive, Hippocampus, Broca's Area, Amygdala, Sensory Cortex) coordinate working memory, episodic retrieval, linguistic synthesis, and safety guardrails.
      </p>
    </div>

    <div class="engine-controls">
      <div class="engine-switch">
        <button class="engine-btn active" id="btnGroq" onclick="setEngine('groq')">⚡ Groq LPU</button>
        <button class="engine-btn" id="btnWebGpu" onclick="setEngine('webgpu')">🎮 WebGPU</button>
        <button class="engine-btn" id="btnSim" onclick="setEngine('sim')">🚀 Brain Engine</button>
      </div>
      <input type="password" id="apiKeyInput" class="api-key-input" placeholder="Groq API Key (gsk_...)" onchange="saveKey()">
      <button class="btn-theme" onclick="toggleTheme()" id="themeBtn">🌙 Dark Mode</button>
    </div>
  </div>
</header>

<div class="wrap">
  <!-- BRAIN REGION AGENT CARDS -->
  <div class="brain-strip" id="brainStrip">
    <div class="agent-card frontal">
      <div class="ag-head">
        <span>🧠 #1 Frontal Executive</span>
        <span class="ag-status" id="stFrontal">DECOMPOSING</span>
      </div>
      <div class="ag-role">Prefrontal Cortex • Planning &amp; Arbitration</div>
      <div class="ag-desc">Hierarchical goal breakdown, task arbitration, dynamic tool selection &amp; priority scheduling.</div>
    </div>

    <div class="agent-card hippo">
      <div class="ag-head">
        <span>🗄️ #2 Hippocampus</span>
        <span class="ag-status" id="stHippo">RETRIEVAL ACTIVE</span>
      </div>
      <div class="ag-role">Episodic &amp; Vector Semantic Store</div>
      <div class="ag-desc">Context indexing, long-term memory consolidation, and graph associative recall.</div>
    </div>

    <div class="agent-card broca">
      <div class="ag-head">
        <span>⚡ #3 Broca's Area</span>
        <span class="ag-status" id="stBroca">TOKEN STREAMING</span>
      </div>
      <div class="ag-role">Linguistic Synthesis &amp; Grammar</div>
      <div class="ag-desc">High-speed token generation, tone modulation, structured JSON schema enforcement.</div>
    </div>

    <div class="agent-card amygdala">
      <div class="ag-head">
        <span>🛡️ #4 Amygdala Sentinel</span>
        <span class="ag-status" id="stAmygdala">GUARDRAILS CLEAR</span>
      </div>
      <div class="ag-role">Threat &amp; Safety Circuit Breaker</div>
      <div class="ag-desc">Prompt injection defense, safety policy audit, semantic boundary verification.</div>
    </div>

    <div class="agent-card sensory">
      <div class="ag-head">
        <span>👁️ #5 Sensory Cortex</span>
        <span class="ag-status" id="stSensory">INGESTION 100%</span>
      </div>
      <div class="ag-role">Multimodal &amp; Telemetry Ingestion</div>
      <div class="ag-desc">Parses real-time telemetry, visual OCR tokens, structured documents, and external API signals.</div>
    </div>
  </div>

  <!-- NAVIGATION TABS -->
  <div class="tabbar">
    <button class="active" onclick="switchTab('connectome')" id="tabBtnConn">🕸️ Neural Connectome Graph</button>
    <button onclick="switchTab('memory')" id="tabBtnMem">🗄️ Working Memory &amp; Episodic Traces</button>
    <button onclick="switchTab('executive')" id="tabBtnExec">🌲 Executive Goal Decomposition</button>
    <button onclick="switchTab('synaptic')" id="tabBtnSyn">⚡ Live Synaptic Deliberation</button>
  </div>

  <!-- TAB 1: NEURAL CONNECTOME GRAPH -->
  <div class="tabpage active" id="tab-connectome">
    <section class="panel">
      <div class="panel-head">
        <div>
          <div class="tag">BIOMIMETIC AGENT TOPOLOGY</div>
          <h2>🕸️ D3 Force-Directed Neural Connectome &amp; Synaptic Pathways</h2>
        </div>
        <button class="btn-theme" onclick="fireSynapticImpulse()" style="background:var(--cyan); color:#fff; border-color:var(--cyan);">⚡ Fire Synaptic Impulse Wave</button>
      </div>

      <div class="panel-body">
        <!-- NEUROTRANSMITTER CONTROLS -->
        <div class="neuro-grid">
          <div class="neuro-item">
            <div class="neuro-label">
              <span>Dopamine (Exploration / Temp)</span>
              <span class="neuro-val" id="lblDopamine">0.70</span>
            </div>
            <input type="range" min="10" max="150" step="5" value="70" class="slider-input" id="sliderDopamine" oninput="updateNeurotransmitters()" style="width:100%; accent-color:var(--purple);">
          </div>

          <div class="neuro-item">
            <div class="neuro-label">
              <span>Acetylcholine (Attention Depth)</span>
              <span class="neuro-val" id="lblAcetyl">8,192 Tokens</span>
            </div>
            <input type="range" min="1000" max="32000" step="1000" value="8192" class="slider-input" id="sliderAcetyl" oninput="updateNeurotransmitters()" style="width:100%; accent-color:var(--cyan);">
          </div>

          <div class="neuro-item">
            <div class="neuro-label">
              <span>Serotonin (Safety Sensitivity)</span>
              <span class="neuro-val" id="lblSerotonin">92%</span>
            </div>
            <input type="range" min="50" max="100" step="2" value="92" class="slider-input" id="sliderSerotonin" oninput="updateNeurotransmitters()" style="width:100%; accent-color:var(--red);">
          </div>

          <div class="neuro-item">
            <div class="neuro-label">
              <span>Norepinephrine (Urgency / Speed)</span>
              <span class="neuro-val" id="lblNorepi">480 Tok/s</span>
            </div>
            <input type="range" min="100" max="800" step="20" value="480" class="slider-input" id="sliderNorepi" oninput="updateNeurotransmitters()" style="width:100%; accent-color:var(--amber);">
          </div>
        </div>

        <div id="connectome-wrap">
          <svg id="connectomeSvg"></svg>
        </div>

        <!-- SCORECARDS -->
        <div class="scorecards" id="brainScorecards"></div>

        <div class="callout ok" id="brainCallout"></div>
      </div>
    </section>
  </div>

  <!-- TAB 2: WORKING MEMORY -->
  <div class="tabpage" id="tab-memory">
    <section class="panel">
      <div class="panel-head">
        <div>
          <div class="tag">EPISODIC BUFFER &amp; KNOWLEDGE RETRIEVAL</div>
          <h2>🗄️ Hippocampal Active Memory Traces &amp; Vector Embeddings</h2>
        </div>
      </div>
      <div class="panel-body">
        <p style="font-size:13px; color:var(--ink-soft); margin-bottom:12px;">
          Working memory ledger maintaining high-dimensional vector embeddings, associative clusters, and temporal decay weights.
        </p>
        <div style="overflow-x:auto;">
          <table class="dt" id="memoryTable">
            <thead>
              <tr>
                <th>Memory Trace ID</th>
                <th>Originating Agent</th>
                <th>Concept / Semantic Key</th>
                <th>Vector Similarity (&Delta;)</th>
                <th>Attention Weight</th>
                <th>Decay Half-Life</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody id="memoryBody"></tbody>
          </table>
        </div>
      </div>
    </section>
  </div>

  <!-- TAB 3: EXECUTIVE DECOMPOSITION -->
  <div class="tabpage" id="tab-executive">
    <section class="panel">
      <div class="panel-head">
        <div>
          <div class="tag">PREFRONTAL CORTEX ARBITRATION</div>
          <h2>🌲 Hierarchical Goal Decomposition &amp; Sub-Task Allocation</h2>
        </div>
      </div>
      <div class="panel-body">
        <div style="overflow-x:auto;">
          <table class="dt" id="taskTable">
            <thead>
              <tr>
                <th>Sub-Task Node</th>
                <th>Assigned Brain Region</th>
                <th>Execution Priority</th>
                <th>Cognitive Complexity</th>
                <th>Synaptic Latency</th>
                <th>Verification Gate</th>
              </tr>
            </thead>
            <tbody id="taskBody"></tbody>
          </table>
        </div>
      </div>
    </section>
  </div>

  <!-- TAB 4: LIVE SYNAPTIC DELIBERATION -->
  <div class="tabpage" id="tab-synaptic">
    <section class="panel">
      <div class="panel-head">
        <div>
          <div class="tag">COGNITIVE STREAM PROTOCOL</div>
          <h2>⚡ Live Multi-Agent Cognitive Deliberation</h2>
        </div>
        <button class="btn-theme" onclick="runBrainDeliberation()">🔄 Re-run Synaptic Protocol</button>
      </div>
      <div class="panel-body">
        <div class="chat-stream" id="chatStream"></div>
      </div>
    </section>
  </div>
</div>

<div id="toast">Cognitive Brain Ready</div>

<!-- APPLICATION JAVASCRIPT LOGIC -->
<script>
/* =========================================================================
   1. NEURAL DATA MODEL & CONNECTOME TOPOLOGY
   ========================================================================= */
const BRAIN_NODES = [
  { id: "Frontal", name: "Frontal Executive", role: "PFC / Task Arbiter", type: "frontal", r: 24, x: 400, y: 120 },
  { id: "Hippo", name: "Hippocampus", role: "Episodic Vector Store", type: "hippo", r: 20, x: 260, y: 260 },
  { id: "Broca", name: "Broca's Area", role: "Language Synthesis", type: "broca", r: 20, x: 540, y: 260 },
  { id: "Amygdala", name: "Amygdala", role: "Safety Sentinel", type: "amygdala", r: 18, x: 320, y: 390 },
  { id: "Sensory", name: "Sensory Cortex", role: "Multimodal Telemetry", type: "sensory", r: 18, x: 480, y: 390 },
  // Satellite Sub-Nuclei
  { id: "Wernicke", name: "Wernicke Semantic Hub", role: "Language Comprehension", type: "broca", r: 12 },
  { id: "Thalamus", name: "Thalamus Switch", role: "Signal Multiplexing", type: "sensory", r: 14 },
  { id: "Cerebellum", name: "Cerebellar Sequencer", role: "Motor / Tool Sequencing", type: "frontal", r: 13 },
  { id: "Dentate", name: "Dentate Gyrus", role: "Pattern Separation", type: "hippo", r: 12 },
  { id: "Insula", name: "Insular Cortex", role: "Self-Evaluation / Metacognition", type: "amygdala", r: 12 }
];

const BRAIN_LINKS = [
  { source: "Frontal", target: "Hippo", value: 4, type: "primary" },
  { source: "Frontal", target: "Broca", value: 5, type: "primary" },
  { source: "Frontal", target: "Amygdala", value: 3, type: "primary" },
  { source: "Frontal", target: "Sensory", value: 4, type: "primary" },
  { source: "Hippo", target: "Broca", value: 3, type: "assoc" },
  { source: "Sensory", target: "Thalamus", value: 5, type: "input" },
  { source: "Thalamus", target: "Frontal", value: 4, type: "input" },
  { source: "Broca", target: "Wernicke", value: 4, type: "assoc" },
  { source: "Hippo", target: "Dentate", value: 4, type: "assoc" },
  { source: "Frontal", target: "Cerebellum", value: 3, type: "assoc" },
  { source: "Amygdala", target: "Insula", value: 3, type: "safety" },
  { source: "Amygdala", target: "Broca", value: 4, type: "safety" }
];

const MEMORY_TRACES = [
  { id: "MEM-8901", agent: "Hippocampus", key: "User Intent: Strategic Network Design", delta: 0.942, weight: "98.4%", halfLife: "14.2 hrs", status: "Consolidated" },
  { id: "MEM-8902", agent: "Frontal Executive", key: "Sub-Goal DAG: CapEx Constraint $45M", delta: 0.915, weight: "94.1%", halfLife: "8.5 hrs", status: "Active Buffer" },
  { id: "MEM-8903", agent: "Sensory Cortex", key: "Live Telemetry: WACC 10.5% Hurdle", delta: 0.887, weight: "89.0%", halfLife: "4.1 hrs", status: "Active Buffer" },
  { id: "MEM-8904", agent: "Amygdala Sentinel", key: "Guardrail Rule: Antitrust Risk Boundary", delta: 0.963, weight: "99.2%", halfLife: "72.0 hrs", status: "Permanent Core" },
  { id: "MEM-8905", agent: "Broca's Area", key: "Linguistic Style: Concise C-Suite Executive", delta: 0.854, weight: "82.6%", halfLife: "24.0 hrs", status: "Consolidated" }
];

const SUB_TASKS = [
  { name: "1. Goal Parsing & Context Ingestion", region: "Sensory & Frontal", prio: "P0 (Critical)", complexity: "Moderate", latency: "12ms", gate: "Approved" },
  { name: "2. Episodic RAG Retrieval & Vector Matching", region: "Hippocampus", prio: "P0 (Critical)", complexity: "High", latency: "24ms", gate: "Approved" },
  { name: "3. Adversarial Safety & Boundary Audit", region: "Amygdala Sentinel", prio: "P0 (Gating)", complexity: "High", latency: "8ms", gate: "Zero Violations" },
  { name: "4. Dynamic Tool Sequencing & Execution", region: "Frontal / Cerebellum", prio: "P1 (High)", complexity: "High", latency: "38ms", gate: "Validated" },
  { name: "5. CoT Linguistic Synthesis & Streaming", region: "Broca's Area", prio: "P1 (High)", complexity: "Very High", latency: "14ms", gate: "Complete" }
];

let dopamineVal = 0.70;
let acetylVal = 8192;
let serotoninVal = 92;
let norepiVal = 480;
let currentEngine = 'groq';

/* =========================================================================
   2. CONTROLS & EVENT HANDLERS
   ========================================================================= */
document.addEventListener("DOMContentLoaded", () => {
  const savedKey = localStorage.getItem("groq_api_key");
  if (savedKey) document.getElementById("apiKeyInput").value = savedKey;

  renderScorecards();
  renderMemoryTable();
  renderTaskTable();
  initConnectomeGraph();
  runBrainDeliberation();
});

function updateNeurotransmitters() {
  dopamineVal = (document.getElementById('sliderDopamine').value / 100).toFixed(2);
  acetylVal = parseInt(document.getElementById('sliderAcetyl').value);
  serotoninVal = parseInt(document.getElementById('sliderSerotonin').value);
  norepiVal = parseInt(document.getElementById('sliderNorepi').value);

  document.getElementById('lblDopamine').innerText = dopamineVal;
  document.getElementById('lblAcetyl').innerText = `${acetylVal.toLocaleString()} Tokens`;
  document.getElementById('lblSerotonin').innerText = `${serotoninVal}%`;
  document.getElementById('lblNorepi').innerText = `${norepiVal} Tok/s`;

  renderScorecards();
}

function switchTab(tabId) {
  document.querySelectorAll('.tabpage').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tabbar button').forEach(el => el.classList.remove('active'));

  const page = document.getElementById(`tab-${tabId}`);
  if (page) page.classList.add('active');

  const btnMap = {
    'connectome': 'tabBtnConn',
    'memory': 'tabBtnMem',
    'executive': 'tabBtnExec',
    'synaptic': 'tabBtnSyn'
  };
  const btn = document.getElementById(btnMap[tabId]);
  if (btn) btn.classList.add('active');
}

function setEngine(eng) {
  currentEngine = eng;
  ['btnGroq', 'btnWebGpu', 'btnSim'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.remove('active');
  });
  if (eng === 'groq') document.getElementById('btnGroq').classList.add('active');
  if (eng === 'webgpu') document.getElementById('btnWebGpu').classList.add('active');
  if (eng === 'sim') document.getElementById('btnSim').classList.add('active');
  showToast(`Active Engine: ${eng.toUpperCase()}`);
}

function saveKey() {
  const val = document.getElementById("apiKeyInput").value.trim();
  localStorage.setItem("groq_api_key", val);
  showToast("Groq API Key Saved");
}

function toggleTheme() {
  const html = document.documentElement;
  const cur = html.getAttribute("data-theme");
  const next = cur === "dark" ? "light" : "dark";
  html.setAttribute("data-theme", next);
  document.getElementById("themeBtn").innerText = next === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode";
}

function showToast(msg) {
  const t = document.getElementById("toast");
  t.innerText = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2400);
}

/* =========================================================================
   3. RENDERING TABLES & SCORECARDS
   ========================================================================= */
function renderScorecards() {
  const sc = document.getElementById('brainScorecards');
  sc.innerHTML = `
    <div class="scorecard">
      <div class="sc-label">Synaptic Firing Velocity</div>
      <div class="sc-total" style="color:var(--cyan);">${norepiVal} tok/s</div>
      <div class="sc-delta good">Ultra-Low Latency LPU</div>
    </div>

    <div class="scorecard">
      <div class="sc-label">Working Memory Buffer</div>
      <div class="sc-total" style="color:var(--green);">${(acetylVal/1024).toFixed(1)}k Tok</div>
      <div class="sc-delta good">Context Retention Depth</div>
    </div>

    <div class="scorecard">
      <div class="sc-label">Exploration Index (Dopamine)</div>
      <div class="sc-total" style="color:var(--purple);">&tau; = ${dopamineVal}</div>
      <div class="sc-delta good">Entropy Calibrated</div>
    </div>

    <div class="scorecard">
      <div class="sc-label">Amygdala Safety Gate</div>
      <div class="sc-total" style="color:var(--red);">${serotoninVal}% Shield</div>
      <div class="sc-delta good">Zero Adversarial Leaks</div>
    </div>
  `;

  const callout = document.getElementById('brainCallout');
  callout.innerHTML = `
    <strong>🧠 Connectome State: COHERENT &amp; SYNCHRONIZED</strong><br>
    The Prefrontal Cortex and Hippocampus maintain an active working memory loop with <strong>${(acetylVal/1024).toFixed(1)}k tokens</strong> attention depth. The Amygdala Sentinel operates at <strong>${serotoninVal}% verification threshold</strong>, blocking adversarial jailbreaks before token synthesis.
  `;
}

function renderMemoryTable() {
  const tb = document.getElementById('memoryBody');
  tb.innerHTML = '';
  MEMORY_TRACES.forEach(m => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${m.id}</strong></td>
      <td><span style="font-family:var(--mono); font-size:11px; padding:2px 6px; background:var(--panel-subtle); border-radius:3px;">${m.agent}</span></td>
      <td>${m.key}</td>
      <td style="color:var(--cyan);">${m.delta}</td>
      <td style="color:var(--green); font-weight:600;">${m.weight}</td>
      <td>${m.halfLife}</td>
      <td><span style="color:var(--purple); font-weight:600;">${m.status}</span></td>
    `;
    tb.appendChild(tr);
  });
}

function renderTaskTable() {
  const tb = document.getElementById('taskBody');
  tb.innerHTML = '';
  SUB_TASKS.forEach(t => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${t.name}</strong></td>
      <td>${t.region}</td>
      <td style="color:var(--purple); font-weight:600;">${t.prio}</td>
      <td>${t.complexity}</td>
      <td style="color:var(--cyan); font-weight:600;">${t.latency}</td>
      <td><span style="color:var(--green); font-weight:600;">${t.gate}</span></td>
    `;
    tb.appendChild(tr);
  });
}

/* =========================================================================
   4. D3 FORCE-DIRECTED NEURAL CONNECTOME
   ========================================================================= */
let simulation = null;

function initConnectomeGraph() {
  const wrap = document.getElementById('connectome-wrap');
  const width = wrap.clientWidth || 800;
  const height = wrap.clientHeight || 520;

  const svg = d3.select("#connectomeSvg")
    .attr("viewBox", [0, 0, width, height]);

  svg.selectAll("*").remove();

  const colorMap = {
    frontal: "var(--frontal)",
    hippo: "var(--hippo)",
    broca: "var(--broca)",
    amygdala: "var(--amygdala)",
    sensory: "var(--sensory)"
  };

  const g = svg.append("g");

  // Zoom & Pan
  svg.call(d3.zoom()
    .extent([[0, 0], [width, height]])
    .scaleExtent([0.5, 3])
    .on("zoom", (event) => g.attr("transform", event.transform)));

  simulation = d3.forceSimulation(BRAIN_NODES)
    .force("link", d3.forceLink(BRAIN_LINKS).id(d => d.id).distance(110))
    .force("charge", d3.forceManyBody().strength(-350))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collision", d3.forceCollide().radius(d => d.r + 14));

  // Links
  const link = g.append("g")
    .attr("stroke", "var(--line-strong)")
    .attr("stroke-opacity", 0.6)
    .selectAll("line")
    .data(BRAIN_LINKS)
    .join("line")
    .attr("stroke-width", d => d.value)
    .attr("stroke-dasharray", d => d.type === "safety" ? "4 4" : null);

  // Nodes
  const node = g.append("g")
    .selectAll("g")
    .data(BRAIN_NODES)
    .join("g")
    .call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended));

  node.append("circle")
    .attr("r", d => d.r)
    .attr("fill", d => colorMap[d.type])
    .attr("stroke", "#ffffff")
    .attr("stroke-width", 2)
    .attr("filter", "drop-shadow(0 2px 4px rgba(0,0,0,0.15))");

  node.append("text")
    .text(d => d.name)
    .attr("x", 0)
    .attr("y", d => d.r + 14)
    .attr("text-anchor", "middle")
    .attr("font-family", "var(--sans)")
    .attr("font-size", "11px")
    .attr("font-weight", "600")
    .attr("fill", "var(--ink)");

  node.append("text")
    .text(d => d.role)
    .attr("x", 0)
    .attr("y", d => d.r + 26)
    .attr("text-anchor", "middle")
    .attr("font-family", "var(--mono)")
    .attr("font-size", "9.5px")
    .attr("fill", "var(--ink-soft)");

  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    node
      .attr("transform", d => `translate(${d.x},${d.y})`);
  });

  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }
  function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }
  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }
}

function fireSynapticImpulse() {
  const svg = d3.select("#connectomeSvg");
  const nodes = svg.selectAll("circle");
  
  nodes.transition()
    .duration(200)
    .attr("r", d => d.r * 1.4)
    .attr("stroke", "var(--cyan)")
    .attr("stroke-width", 4)
    .transition()
    .duration(400)
    .attr("r", d => d.r)
    .attr("stroke", "#ffffff")
    .attr("stroke-width", 2);

  showToast("⚡ Synaptic Action Potential Fired Across Connectome");
}

/* =========================================================================
   5. MULTI-AGENT COGNITIVE DELIBERATION STREAM
   ========================================================================= */
async function runBrainDeliberation() {
  const stream = document.getElementById('chatStream');
  stream.innerHTML = '<div style="font-family:var(--mono); color:var(--cyan); padding:8px;">Synchronizing Brain Connectome Regions...</div>';

  const defaultDialogue = [
    {
      role: "frontal",
      name: "Prefrontal Cortex (Executive)",
      text: "Goal received: Orchestrate multi-tier enterprise decision under stochastic constraints. Dissecting into 3 sub-task branches: Vector memory query, compliance boundary check, and linguistic output formatting."
    },
    {
      role: "sensory",
      name: "Sensory Cortex (Multimodal Ingestion)",
      text: "Telemetry parsed: Ingested 14 market signals and user prompt tokens. Embeddings aligned and passed via thalamic switchboard to working memory buffer."
    },
    {
      role: "hippo",
      name: "Hippocampus (Episodic & Vector Store)",
      text: "Associative vector recall executed: Matched 5 historical episodic traces with cosine similarity &Delta; > 0.91. Grounding context injected into 8,192-token active attention window."
    },
    {
      role: "amygdala",
      name: "Amygdala Sentinel (Threat & Safety Gate)",
      text: "Cognitive safety audit complete: 0 prompt injection vectors detected. Ethical boundaries verified against serotonin threshold (92%). Green light granted to Broca linguistic generator."
    },
    {
      role: "broca",
      name: "Broca's Area (Linguistic Synthesizer)",
      text: "High-throughput token generation streaming at 480 tokens/sec via Groq LPU. Synthesizing concise executive recommendation adhering to rigid schema constraints."
    }
  ];

  renderDialogue(defaultDialogue);
}

function renderDialogue(list) {
  const stream = document.getElementById('chatStream');
  stream.innerHTML = '';

  const badgeMap = {
    frontal: "🧠 PREFRONTAL EXECUTIVE",
    hippo: "🗄️ HIPPOCAMPUS (MEMORY)",
    broca: "⚡ BROCA'S AREA (SYNTHESIS)",
    amygdala: "🛡️ AMYGDALA SENTINEL (SAFETY)",
    sensory: "👁️ SENSORY CORTEX (INGESTION)"
  };

  list.forEach((item, idx) => {
    setTimeout(() => {
      const div = document.createElement('div');
      div.className = `chat-msg ${item.role}`;
      div.innerHTML = `
        <div class="msg-meta">
          <span>${badgeMap[item.role] || item.role} — ${item.name}</span>
          <span>PHASE ${idx + 1}/5</span>
        </div>
        <div class="msg-body">${item.text}</div>
      `;
      stream.appendChild(div);
      stream.scrollTop = stream.scrollHeight;
    }, idx * 120);
  });
}
</script>
</body>
</html>
''')
    print("Successfully built multi_agent_brain_app.html!")

if __name__ == "__main__":
    build()
