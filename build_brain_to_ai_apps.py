"""
build_brain_to_ai_apps.py
Builds 4 dedicated single-file HTML apps translating biological brain mechanisms to enterprise AI:
1. brain_to_ai_homeostasis.html  (Hypothalamic Homeostasis -> Autonomic Agent Regulation)
2. brain_to_ai_somatic_marker.html (Somatic Marker Hypothesis -> Dynamic Goal Weighting & Prioritization)
3. brain_to_ai_theory_of_mind.html (Theory of Mind -> Multi-Agent Negotiation & Intent Reading)
4. brain_to_ai_consolidation.html (Hippocampal Consolidation -> Episodic Plasticity & Long-Term Heuristic Recall)
"""

import os

# ==============================================================================
# APP 1: HYPOTHALAMIC HOMEOSTASIS -> AUTONOMIC AGENT REGULATION
# ==============================================================================
APP1_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Homeostasis AI: Hypothalamic Self-Regulation for Autonomous Agents</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Public+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg-page: #0A0E17;
    --bg-surface: #111827;
    --bg-card: #162032;
    --bg-subtle: #1E293B;
    --border: #2B3B52;
    --border-accent: #0D9488;
    --text-main: #F8FAFC;
    --text-muted: #94A3B8;
    --teal: #14B8A6;
    --teal-glow: rgba(20, 184, 166, 0.25);
    --gold: #F59E0B;
    --danger: #EF4444;
    --emerald: #10B981;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--bg-page);
    color: var(--text-main);
    font-family: 'Public Sans', sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }
  header {
    background: var(--bg-surface);
    border-bottom: 1px solid var(--border);
    padding: 14px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 50;
  }
  .brand { display: flex; align-items: center; gap: 12px; }
  .brand-icon {
    width: 38px; height: 38px; border-radius: 10px;
    background: linear-gradient(135deg, #0D9488, #047857);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; color: #fff;
    box-shadow: 0 4px 12px var(--teal-glow);
  }
  .brand h1 { font-family: 'Bricolage Grotesque', sans-serif; font-size: 18px; font-weight: 800; }
  .brand p { font-size: 11px; color: var(--text-muted); }
  .engine-bar { display: flex; align-items: center; gap: 8px; }
  .engine-pill {
    padding: 6px 12px; border-radius: 20px; font-size: 11px; font-weight: 600;
    background: var(--bg-subtle); border: 1px solid var(--border); color: var(--text-muted);
    cursor: pointer; transition: all 0.2s; user-select: none;
  }
  .engine-pill.active { background: var(--bg-card); border-color: var(--teal); color: var(--text-main); box-shadow: 0 0 10px var(--teal-glow); }
  .status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; background: var(--emerald); margin-right: 6px; }

  main { flex: 1; max-width: 1300px; width: 100%; margin: 0 auto; padding: 24px 28px; display: grid; grid-template-columns: 1fr; gap: 24px; }
  .neuro-banner {
    background: linear-gradient(135deg, rgba(13, 148, 136, 0.15) 0%, var(--bg-surface) 100%);
    border: 1px solid var(--border-accent); border-radius: 16px; padding: 20px 24px;
    display: grid; grid-template-columns: 1fr 1fr; gap: 24px;
  }
  @media (max-width: 860px) { .neuro-banner { grid-template-columns: 1fr; } }
  .neuro-col h2 { font-family: 'Bricolage Grotesque', sans-serif; font-size: 16px; font-weight: 800; color: var(--teal); margin-bottom: 6px; }
  .neuro-col p { font-size: 13px; color: var(--text-muted); line-height: 1.5; }

  .dashboard-grid { display: grid; grid-template-columns: 380px 1fr; gap: 24px; }
  @media (max-width: 960px) { .dashboard-grid { grid-template-columns: 1fr; } }

  .vitals-panel {
    background: var(--bg-surface); border: 1px solid var(--border); border-radius: 16px; padding: 20px;
    display: flex; flex-direction: column; gap: 16px;
  }
  .vital-gauge {
    background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 14px;
    display: flex; flex-direction: column; gap: 8px;
  }
  .gauge-top { display: flex; justify-content: space-between; font-size: 12px; font-weight: 700; }
  .gauge-bar-wrap { width: 100%; height: 8px; background: #0A0E17; border-radius: 4px; overflow: hidden; }
  .gauge-bar-fill { height: 100%; background: var(--teal); width: 40%; transition: width 0.4s ease, background 0.3s; }
  .gauge-bar-fill.warn { background: var(--gold); }
  .gauge-bar-fill.danger { background: var(--danger); }

  .action-box { display: flex; flex-direction: column; gap: 10px; margin-top: 8px; }
  .btn-primary {
    padding: 12px; border-radius: 10px; background: linear-gradient(135deg, var(--teal), #047857);
    border: none; color: #fff; font-weight: 800; font-size: 13px; cursor: pointer; transition: all 0.2s;
  }
  .btn-primary:hover { filter: brightness(1.15); transform: translateY(-1px); }
  .btn-secondary {
    padding: 10px; border-radius: 10px; background: var(--bg-subtle);
    border: 1px solid var(--border); color: var(--text-main); font-weight: 600; font-size: 12px; cursor: pointer;
  }
  .btn-secondary:hover { border-color: var(--teal); }

  .simulation-view {
    background: var(--bg-surface); border: 1px solid var(--border); border-radius: 16px; padding: 20px;
    display: flex; flex-direction: column; gap: 14px; min-height: 480px;
  }
  .stream-feed { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; max-height: 440px; }
  .event-card {
    background: var(--bg-card); border-radius: 10px; padding: 12px 14px; font-size: 12px; line-height: 1.5;
    border-left: 3px solid var(--border); animation: fadeIn 0.3s forwards;
  }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
  .event-card.normal { border-left-color: var(--teal); }
  .event-card.throttled { border-left-color: var(--gold); background: rgba(245, 158, 11, 0.05); }
  .event-card.compacted { border-left-color: var(--emerald); background: rgba(16, 185, 129, 0.06); }
  .event-card.crash { border-left-color: var(--danger); background: rgba(239, 68, 68, 0.08); color: #FCA5A5; }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="brand-icon">&#127915;</div>
      <div>
        <h1>Homeostasis AI: Autonomic Agent Regulation</h1>
        <p>Brainstem & Hypothalamic Homeostasis translated into Autonomous Rate, Context & Token Budgeting</p>
      </div>
    </div>
    <div class="engine-bar">
      <div class="engine-pill active" id="eng-det" onclick="setEng('det')"><span class="status-dot"></span>Deterministic Engine</div>
      <div class="engine-pill" id="eng-groq" onclick="setEng('groq')"><span class="status-dot" style="background:var(--gold);"></span>Groq LPU (~200ms)</div>
      <div class="engine-pill" id="eng-webllm" onclick="setEng('webllm')"><span class="status-dot" style="background:#3B82F6;"></span>WebGPU WebLLM</div>
    </div>
  </header>

  <main>
    <section class="neuro-banner">
      <div class="neuro-col">
        <h2>&#129504; Biological Brain: Hypothalamic Homeostasis</h2>
        <p>The human hypothalamus constantly regulates body temperature, arterial pH, glucose, and heart rate. Under physical exhaustion or dehydration, it induces fatigue and slows somatic output, protecting cells before a heart attack or systemic organ failure occurs.</p>
      </div>
      <div class="neuro-col">
        <h2>&#9881; AI Architecture: Autonomic Self-Regulation (+ Regulates)</h2>
        <p>Unregulated LLM agents blindly process tokens until hitting hard rate limits (HTTP 429) or memory overflow (128k context ceiling). Autonomic regulation measures token burn rate, compacts noisy logs, and throttles cadence <em>before</em> the hard circuit breaker has to trip.</p>
      </div>
    </section>

    <div class="dashboard-grid">
      <div class="vitals-panel">
        <h3 style="font-family:'Bricolage Grotesque', sans-serif; font-size:15px; font-weight:800;">Agent Internal Vitals (Metabolic State)</h3>

        <div class="vital-gauge">
          <div class="gauge-top"><span>Context Memory Pressure</span><span id="txt-mem">38% (48k / 128k)</span></div>
          <div class="gauge-bar-wrap"><div class="gauge-bar-fill" id="bar-mem" style="width:38%;"></div></div>
        </div>

        <div class="vital-gauge">
          <div class="gauge-top"><span>Token Burn Velocity</span><span id="txt-burn">1,400 tok/sec</span></div>
          <div class="gauge-bar-wrap"><div class="gauge-bar-fill" id="bar-burn" style="width:35%;"></div></div>
        </div>

        <div class="vital-gauge">
          <div class="gauge-top"><span>Autonomic Homeostasis Stress</span><span id="txt-stress">STABLE (0.24)</span></div>
          <div class="gauge-bar-wrap"><div class="gauge-bar-fill" id="bar-stress" style="width:24%;"></div></div>
        </div>

        <div class="action-box">
          <button class="btn-primary" onclick="injectBurstLoad()">&#9889; Inject Telemetry Burst Load (50,000 Events)</button>
          <button class="btn-secondary" onclick="runUnregulatedComparison()">&#10060; Compare with Unregulated Agent (Watch Crash)</button>
        </div>
      </div>

      <div class="simulation-view">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--border); padding-bottom:10px;">
          <strong style="font-size:13px; font-family:'JetBrains Mono';">Live Homeostatic Stream</strong>
          <span style="font-size:11px; color:var(--text-muted);" id="stream-status">Awaiting Telemetry Shock</span>
        </div>
        <div class="stream-feed" id="stream-feed">
          <div style="text-align:center; padding:80px 20px; color:var(--text-muted); font-size:13px;">
            Click <strong>Inject Telemetry Burst Load</strong> to observe hypothalamic self-regulation in real time.
          </div>
        </div>
      </div>
    </div>
  </main>

  <script>
    let activeEng = 'det';
    function setEng(e) {
      activeEng = e;
      document.querySelectorAll('.engine-pill').forEach(p => p.classList.remove('active'));
      document.getElementById('eng-' + e).classList.add('active');
    }

    async function injectBurstLoad() {
      const feed = document.getElementById('stream-feed');
      feed.innerHTML = '';
      document.getElementById('stream-status').innerText = 'Regulating Burst Stream...';

      const steps = [
        { mem: 62, burn: 3200, stress: 0.55, cls: 'normal', text: 'Telemetry Surge: 50,000 raw syslog lines received. Ingestion buffer climbing.' },
        { mem: 84, burn: 4800, stress: 0.82, cls: 'throttled', text: 'Hypothalamic Alarm: Memory pressure reached 84%. Rate limiter slowing dispatch cadence by 60%.' },
        { mem: 42, burn: 1800, stress: 0.32, cls: 'compacted', text: 'Homeostatic Compaction: Autonomously evicted 46,000 repetitive debug logs. Retained 4 core failure invariants.' },
        { mem: 38, burn: 1200, stress: 0.20, cls: 'normal', text: 'Equilibrium Restored: Executive context preserved at 38%. Zero HTTP 429 errors. Saved 78% token burn.' }
      ];

      for (let s of steps) {
        document.getElementById('bar-mem').style.width = s.mem + '%';
        document.getElementById('txt-mem').innerText = s.mem + '%';
        document.getElementById('bar-burn').style.width = (s.burn / 50) + '%';
        document.getElementById('txt-burn').innerText = s.burn + ' tok/sec';
        document.getElementById('bar-stress').style.width = (s.stress * 100) + '%';
        document.getElementById('txt-stress').innerText = s.stress > 0.7 ? 'HIGH STRESS' : 'STABLE (' + s.stress + ')';

        const card = document.createElement('div');
        card.className = 'event-card ' + s.cls;
        card.innerText = s.text;
        feed.appendChild(card);
        card.scrollIntoView({ behavior: 'smooth', block: 'end' });
        await new Promise(r => setTimeout(r, 700));
      }
      document.getElementById('stream-status').innerText = 'Homeostasis Maintained';
    }

    async function runUnregulatedComparison() {
      const feed = document.getElementById('stream-feed');
      feed.innerHTML = '';
      document.getElementById('stream-status').innerText = 'Unregulated Agent Running...';

      const steps = [
        { mem: 75, burn: 4500, stress: 0.75, cls: 'normal', text: 'Unregulated Ingestion: Dumping all raw 50,000 lines directly into LLM prompt.' },
        { mem: 96, burn: 7800, stress: 0.96, cls: 'throttled', text: 'Warning: Context window at 96% capacity (123,000 / 128,000 tokens).' },
        { mem: 100, burn: 9500, stress: 1.0, cls: 'crash', text: 'FATAL CRASH: HTTP 429 Rate Limit Exceeded & Out Of Memory. 14,800 tokens burned. System down for 15 minutes.' }
      ];

      for (let s of steps) {
        document.getElementById('bar-mem').style.width = s.mem + '%';
        document.getElementById('txt-mem').innerText = s.mem + '%';
        document.getElementById('bar-stress').style.width = (s.stress * 100) + '%';
        document.getElementById('txt-stress').innerText = 'CRITICAL OVERFLOW';
        const card = document.createElement('div');
        card.className = 'event-card ' + s.cls;
        card.innerText = s.text;
        feed.appendChild(card);
        card.scrollIntoView({ behavior: 'smooth', block: 'end' });
        await new Promise(r => setTimeout(r, 700));
      }
      document.getElementById('stream-status').innerText = 'Unregulated System Crashed';
    }
  </script>
</body>
</html>'''

# ==============================================================================
# APP 2: SOMATIC MARKER HYPOTHESIS -> DYNAMIC GOAL WEIGHTING (+ PRIORITIZES)
# ==============================================================================
APP2_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Somatic Marker AI: Emotion & Motivation Goal Weighting</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Public+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg-page: #080D1A;
    --bg-surface: #0F172A;
    --bg-card: #1E293B;
    --border: #334155;
    --accent: #2563EB;
    --accent-glow: rgba(37, 99, 235, 0.25);
    --gold: #F59E0B;
    --emerald: #10B981;
    --danger: #EF4444;
    --text-main: #F8FAFC;
    --text-muted: #94A3B8;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg-page); color: var(--text-main); font-family: 'Public Sans', sans-serif; min-height: 100vh; display: flex; flex-direction: column; }
  header { background: var(--bg-surface); border-bottom: 1px solid var(--border); padding: 14px 28px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 50; }
  .brand { display: flex; align-items: center; gap: 12px; }
  .brand-icon { width: 38px; height: 38px; border-radius: 10px; background: linear-gradient(135deg, #2563EB, #1D4ED8); display: flex; align-items: center; justify-content: center; font-size: 20px; box-shadow: 0 4px 12px var(--accent-glow); }
  .brand h1 { font-family: 'Bricolage Grotesque', sans-serif; font-size: 18px; font-weight: 800; }
  .brand p { font-size: 11px; color: var(--text-muted); }
  .engine-bar { display: flex; gap: 8px; }
  .engine-pill { padding: 6px 12px; border-radius: 20px; font-size: 11px; font-weight: 600; background: var(--bg-card); border: 1px solid var(--border); color: var(--text-muted); cursor: pointer; }
  .engine-pill.active { border-color: var(--accent); color: var(--text-main); box-shadow: 0 0 10px var(--accent-glow); }

  main { flex: 1; max-width: 1300px; width: 100%; margin: 0 auto; padding: 24px 28px; display: flex; flex-direction: column; gap: 24px; }
  .neuro-banner { background: linear-gradient(135deg, rgba(37, 99, 235, 0.15) 0%, var(--bg-surface) 100%); border: 1px solid var(--accent); border-radius: 16px; padding: 20px 24px; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  @media (max-width: 860px) { .neuro-banner { grid-template-columns: 1fr; } }
  .neuro-col h2 { font-family: 'Bricolage Grotesque', sans-serif; font-size: 16px; font-weight: 800; color: #60A5FA; margin-bottom: 6px; }
  .neuro-col p { font-size: 13px; color: var(--text-muted); line-height: 1.5; }

  .layout-grid { display: grid; grid-template-columns: 420px 1fr; gap: 24px; }
  @media (max-width: 960px) { .layout-grid { grid-template-columns: 1fr; } }

  .weights-card { background: var(--bg-surface); border: 1px solid var(--border); border-radius: 16px; padding: 20px; display: flex; flex-direction: column; gap: 16px; }
  .weight-slider-box { background: var(--bg-card); border-radius: 10px; padding: 12px 14px; border: 1px solid var(--border); display: flex; flex-direction: column; gap: 6px; }
  .weight-label { display: flex; justify-content: space-between; font-size: 12px; font-weight: 700; }
  .weight-val { font-family: 'JetBrains Mono', monospace; color: var(--gold); }
  .btn-run { padding: 12px; border-radius: 10px; background: linear-gradient(135deg, #2563EB, #1D4ED8); border: none; color: #fff; font-weight: 800; cursor: pointer; margin-top: 10px; }
  .btn-run:hover { filter: brightness(1.15); }

  .tree-card { background: var(--bg-surface); border: 1px solid var(--border); border-radius: 16px; padding: 20px; display: flex; flex-direction: column; gap: 12px; }
  .tree-node { background: var(--bg-card); border-radius: 10px; padding: 14px; border-left: 4px solid var(--border); font-size: 12px; line-height: 1.5; }
  .tree-node.pruned { border-left-color: var(--danger); text-decoration: line-through; opacity: 0.6; }
  .tree-node.promoted { border-left-color: var(--emerald); background: rgba(16, 185, 129, 0.08); }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="brand-icon">&#128203;</div>
      <div>
        <h1>Somatic Marker AI: Goal Weighting & Prioritization</h1>
        <p>Damasio's Somatic Marker Hypothesis translated into Dynamic Utility & Sub-Task Pruning</p>
      </div>
    </div>
    <div class="engine-bar">
      <div class="engine-pill active" id="eng-det"><span style="color:var(--emerald);">&#9679;</span> Deterministic Engine</div>
      <div class="engine-pill" id="eng-groq"><span style="color:var(--gold);">&#9679;</span> Groq LPU (~200ms)</div>
    </div>
  </header>

  <main>
    <section class="neuro-banner">
      <div class="neuro-col">
        <h2>&#129504; Biological Brain: Somatic Marker Hypothesis</h2>
        <p>Neurologist Antonio Damasio discovered that emotions (visceral somatic markers from the ventromedial prefrontal cortex) do not disrupt rationality—they <em>enable</em> it. Without emotional weighting, humans suffer analysis paralysis, evaluating hundreds of trivial options endlessly.</p>
      </div>
      <div class="neuro-col">
        <h2>&#9881; AI Architecture: Dynamic Goal Weighting (+ Prioritizes)</h2>
        <p>In autonomous agents, emotion translates to real-time utility re-weighting. When an emergency deadline approaches, the agent injects a "visceral urgency penalty," dropping low-value exploratory sub-tasks to guarantee mission SLA survival.</p>
      </div>
    </section>

    <div class="layout-grid">
      <div class="weights-card">
        <h3 style="font-family:'Bricolage Grotesque', sans-serif; font-size:15px; font-weight:800;">Urgency &amp; Somatic Vector Controls</h3>

        <div class="weight-slider-box">
          <div class="weight-label"><span>Safety SLA Urgency Weight</span><span class="weight-val" id="val-sla">0.95</span></div>
          <p style="font-size:11px; color:var(--text-muted);">Somatic fear response against breach</p>
        </div>

        <div class="weight-slider-box">
          <div class="weight-label"><span>Cost Optimization Weight</span><span class="weight-val" id="val-cost">0.20</span></div>
          <p style="font-size:11px; color:var(--text-muted);">Secondary resource thrift</p>
        </div>

        <div class="weight-slider-box">
          <div class="weight-label"><span>Exploration Curiosity Weight</span><span class="weight-val" id="val-curious">0.10</span></div>
          <p style="font-size:11px; color:var(--text-muted);">Suppressed under crisis urgency</p>
        </div>

        <button class="btn-run" onclick="runPrioritization()">&#9654; Evaluate &amp; Prune Execution Tree</button>
      </div>

      <div class="tree-card">
        <h3 style="font-family:'Bricolage Grotesque', sans-serif; font-size:15px; font-weight:800;">Execution Tree: Pruning Low-Value Sub-Tasks</h3>
        <div id="tree-container" style="display:flex; flex-direction:column; gap:10px;">
          <div class="tree-node">Task 1: Core Payload Encryption (Utility: 0.98) - Crucial safety invariant.</div>
          <div class="tree-node">Task 2: Secondary Cloud Region Benchmark (Utility: 0.22) - Exploratory background probe.</div>
          <div class="tree-node">Task 3: Historical Telemetry Deep Analysis (Utility: 0.15) - High token cost, low urgency.</div>
          <div class="tree-node">Task 4: Fast Failover Route Synthesis (Utility: 0.94) - Critical uptime path.</div>
        </div>
      </div>
    </div>
  </main>

  <script>
    function runPrioritization() {
      const container = document.getElementById('tree-container');
      container.innerHTML = `
        <div class="tree-node promoted"><strong>[PROMOTED &middot; WEIGHT 0.98]</strong> Task 1: Core Payload Encryption &mdash; Priority #1, immediate dispatch.</div>
        <div class="tree-node pruned"><strong>[DROPPED &middot; WEIGHT 0.22]</strong> Task 2: Secondary Cloud Region Benchmark &mdash; Somatic penalty applied; budget at risk.</div>
        <div class="tree-node pruned"><strong>[DROPPED &middot; WEIGHT 0.15]</strong> Task 3: Historical Telemetry Deep Analysis &mdash; Evicted to preserve token headroom.</div>
        <div class="tree-node promoted"><strong>[PROMOTED &middot; WEIGHT 0.94]</strong> Task 4: Fast Failover Route Synthesis &mdash; Priority #2, guaranteed SLA delivery.</div>
        <div style="background:rgba(16,185,129,0.1); border:1px solid var(--emerald); border-radius:10px; padding:12px; font-size:12px; color:var(--emerald);">
          <strong>Result:</strong> 2 non-essential tasks pruned. Execution latency reduced from 8.4s to 1.2s. Zero budget violation.
        </div>
      `;
    }
  </script>
</body>
</html>'''

# ==============================================================================
# APP 3: THEORY OF MIND -> MULTI-AGENT INTENT READING (+ READS INTENT)
# ==============================================================================
APP3_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Theory of Mind AI: Social Swarm Intent Reading</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Public+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg-page: #0C0A1A;
    --bg-surface: #15112B;
    --bg-card: #201A40;
    --border: #3B2F6E;
    --purple: #9333EA;
    --purple-glow: rgba(147, 51, 234, 0.25);
    --gold: #F59E0B;
    --emerald: #10B981;
    --danger: #EF4444;
    --text-main: #F8FAFC;
    --text-muted: #94A3B8;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg-page); color: var(--text-main); font-family: 'Public Sans', sans-serif; min-height: 100vh; display: flex; flex-direction: column; }
  header { background: var(--bg-surface); border-bottom: 1px solid var(--border); padding: 14px 28px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 50; }
  .brand { display: flex; align-items: center; gap: 12px; }
  .brand-icon { width: 38px; height: 38px; border-radius: 10px; background: linear-gradient(135deg, #9333EA, #6B21A8); display: flex; align-items: center; justify-content: center; font-size: 20px; box-shadow: 0 4px 12px var(--purple-glow); }
  .brand h1 { font-family: 'Bricolage Grotesque', sans-serif; font-size: 18px; font-weight: 800; }
  .brand p { font-size: 11px; color: var(--text-muted); }

  main { flex: 1; max-width: 1300px; width: 100%; margin: 0 auto; padding: 24px 28px; display: flex; flex-direction: column; gap: 24px; }
  .neuro-banner { background: linear-gradient(135deg, rgba(147, 51, 234, 0.15) 0%, var(--bg-surface) 100%); border: 1px solid var(--purple); border-radius: 16px; padding: 20px 24px; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  @media (max-width: 860px) { .neuro-banner { grid-template-columns: 1fr; } }
  .neuro-col h2 { font-family: 'Bricolage Grotesque', sans-serif; font-size: 16px; font-weight: 800; color: #C084FC; margin-bottom: 6px; }
  .neuro-col p { font-size: 13px; color: var(--text-muted); line-height: 1.5; }

  .duel-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  @media (max-width: 860px) { .duel-grid { grid-template-columns: 1fr; } }

  .agent-box { background: var(--bg-surface); border: 1px solid var(--border); border-radius: 16px; padding: 20px; display: flex; flex-direction: column; gap: 14px; }
  .agent-head { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
  .dialogue-log { display: flex; flex-direction: column; gap: 10px; min-height: 280px; }
  .bubble { padding: 10px 14px; border-radius: 10px; font-size: 12px; line-height: 1.5; background: var(--bg-card); }
  .bubble.intent { border-left: 3px solid #C084FC; background: rgba(192, 132, 252, 0.08); }
  .bubble.deadlock { border-left: 3px solid var(--danger); background: rgba(239, 68, 68, 0.08); color: #FCA5A5; }

  .btn-negotiate { padding: 14px; border-radius: 10px; background: linear-gradient(135deg, #9333EA, #6B21A8); border: none; color: #fff; font-weight: 800; font-size: 14px; cursor: pointer; }
  .btn-negotiate:hover { filter: brightness(1.15); }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="brand-icon">&#129504;</div>
      <div>
        <h1>Theory of Mind AI: Social Swarm Intent Reading</h1>
        <p>Temporoparietal Junction (TPJ) Mentalizing translated into Counterparty Constraint Inference</p>
      </div>
    </div>
  </header>

  <main>
    <section class="neuro-banner">
      <div class="neuro-col">
        <h2>&#129504; Biological Brain: Theory of Mind (Mentalizing)</h2>
        <p>In primates, the temporoparietal junction (TPJ) and medial prefrontal cortex model what other individuals secretly know, need, and intend. Human negotiations succeed because counterparties read implicit reservation prices rather than exchanging blind noise.</p>
      </div>
      <div class="neuro-col">
        <h2>&#9881; AI Architecture: Social Intent Reading (+ Reads Intent)</h2>
        <p>Naïve multi-agent systems exchange 10,000-token JSON dumps back and forth, hitting 14-round deadlocks. Theory of Mind inference predicts the other agent's reservation cost, formulating a win-win Pareto offer that locks consensus in 2 rounds.</p>
      </div>
    </section>

    <button class="btn-negotiate" onclick="runToM()">&#9889; Run Negotiation: Naïve Exchange vs. Theory of Mind Intent Reading</button>

    <div class="duel-grid">
      <div class="agent-box">
        <div class="agent-head">
          <strong style="color:var(--danger);">Naive System: Blind Data Dumps</strong>
          <span style="font-size:11px; color:var(--text-muted);">14 Rounds &middot; Deadlock</span>
        </div>
        <div class="dialogue-log" id="naive-log">
          <div class="bubble">Agent A: Sending 8,500-token full inventory payload...</div>
          <div class="bubble">Agent B: Rejected. Counter-proposing 7,900-token full ledger dump...</div>
          <div class="bubble deadlock">Round 14: Network message congestion. Deadlock timeout exceeded. Zero agreement reached.</div>
        </div>
      </div>

      <div class="agent-box">
        <div class="agent-head">
          <strong style="color:var(--emerald);">Theory of Mind: Implicit Intent Inference</strong>
          <span style="font-size:11px; color:var(--text-muted);">2 Rounds &middot; Pareto Consensus</span>
        </div>
        <div class="dialogue-log" id="tom-log">
          <div class="bubble intent">Agent A [Mentalizing]: Inferring Agent B reservation cost ($420/TEU) and SLA priority (Friday).</div>
          <div class="bubble">Agent A [Speech Act]: Proposing 40-word calibrated split at $435/TEU with guaranteed Friday slot.</div>
          <div class="bubble" style="border-left:3px solid var(--emerald); color:#86EFAC;">Agent B: Accepted in Round 2. Quorum locked. 85.7% less network traffic.</div>
        </div>
      </div>
    </div>
  </main>

  <script>
    function runToM() {
      // Trigger visual pulse
      document.getElementById('tom-log').style.animation = 'none';
      setTimeout(() => document.getElementById('tom-log').style.animation = '', 10);
    }
  </script>
</body>
</html>'''

# ==============================================================================
# APP 4: HIPPOCAMPAL CONSOLIDATION -> EPISODIC PLASTICITY (+ LEARNS)
# ==============================================================================
APP4_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Episodic Plasticity AI: Hippocampal-Neocortical Consolidation</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Public+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg-page: #071017;
    --bg-surface: #0E1A24;
    --bg-card: #152535;
    --border: #233B50;
    --amber: #F59E0B;
    --amber-glow: rgba(245, 158, 11, 0.25);
    --emerald: #10B981;
    --danger: #EF4444;
    --text-main: #F8FAFC;
    --text-muted: #94A3B8;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg-page); color: var(--text-main); font-family: 'Public Sans', sans-serif; min-height: 100vh; display: flex; flex-direction: column; }
  header { background: var(--bg-surface); border-bottom: 1px solid var(--border); padding: 14px 28px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 50; }
  .brand { display: flex; align-items: center; gap: 12px; }
  .brand-icon { width: 38px; height: 38px; border-radius: 10px; background: linear-gradient(135deg, #F59E0B, #D97706); display: flex; align-items: center; justify-content: center; font-size: 20px; box-shadow: 0 4px 12px var(--amber-glow); }
  .brand h1 { font-family: 'Bricolage Grotesque', sans-serif; font-size: 18px; font-weight: 800; }
  .brand p { font-size: 11px; color: var(--text-muted); }

  main { flex: 1; max-width: 1300px; width: 100%; margin: 0 auto; padding: 24px 28px; display: flex; flex-direction: column; gap: 24px; }
  .neuro-banner { background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, var(--bg-surface) 100%); border: 1px solid var(--amber); border-radius: 16px; padding: 20px 24px; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  @media (max-width: 860px) { .neuro-banner { grid-template-columns: 1fr; } }
  .neuro-col h2 { font-family: 'Bricolage Grotesque', sans-serif; font-size: 16px; font-weight: 800; color: var(--amber); margin-bottom: 6px; }
  .neuro-col p { font-size: 13px; color: var(--text-muted); line-height: 1.5; }

  .trials-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  @media (max-width: 860px) { .trials-grid { grid-template-columns: 1fr; } }

  .trial-card { background: var(--bg-surface); border: 1px solid var(--border); border-radius: 16px; padding: 20px; display: flex; flex-direction: column; gap: 14px; }
  .stat-badge { font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 800; padding: 4px 10px; border-radius: 6px; }
  .stat-badge.slow { background: rgba(239, 68, 68, 0.2); color: #F87171; }
  .stat-badge.fast { background: rgba(16, 185, 129, 0.2); color: #34D399; }

  .btn-consolidate { padding: 14px; border-radius: 10px; background: linear-gradient(135deg, #F59E0B, #D97706); border: none; color: #fff; font-weight: 800; font-size: 14px; cursor: pointer; }
  .btn-consolidate:hover { filter: brightness(1.15); }
</style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="brand-icon">&#129516;</div>
      <div>
        <h1>Episodic Plasticity AI: Memory Consolidation</h1>
        <p>Sharp-Wave Ripple Consolidation translated into Vector Heuristic Indexing & Zero-Shot Recovery</p>
      </div>
    </div>
  </header>

  <main>
    <section class="neuro-banner">
      <div class="neuro-col">
        <h2>&#129504; Biological Brain: Hippocampal-Neocortical Consolidation</h2>
        <p>During rest and sleep, the hippocampus fires sharp-wave ripples to replay waking episodes backwards and forwards. This transfers raw episodic shock memories into permanent neocortical schemas, turning yesterday's trauma into instant wisdom.</p>
      </div>
      <div class="neuro-col">
        <h2>&#9881; AI Architecture: Episodic Plasticity (+ Learns)</h2>
        <p>Traditional AI agents wake up with amnesia every session. Episodic plasticity indexes incident post-mortems into an immutable vector cache. When the exact same deadlock reoccurs tomorrow, the agent skips 28 brute-force steps, resolving in 180ms.</p>
      </div>
    </section>

    <div class="trials-grid">
      <div class="trial-card">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--border); padding-bottom:10px;">
          <strong>Incident Encounter #1 (First Trauma)</strong>
          <span class="stat-badge slow">11.2s &middot; Brute Force</span>
        </div>
        <p style="font-size:12px; color:var(--text-muted); line-height:1.5;">
          Encountered database deadlock cascade. Agent had zero stored heuristics. Tested 28 candidate causes across 11,200ms before discovering lock conflict.
        </p>
        <button class="btn-consolidate" onclick="consolidate()">&#129516; Consolidate Post-Mortem into Cortical Vector</button>
      </div>

      <div class="trial-card">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--border); padding-bottom:10px;">
          <strong>Incident Encounter #2 (With Consolidation)</strong>
          <span class="stat-badge fast" id="enc2-stat">Pending Consolidation</span>
        </div>
        <p style="font-size:12px; color:var(--text-muted); line-height:1.5;" id="enc2-desc">
          Click the consolidation button to index the invariant schema into long-term memory.
        </p>
      </div>
    </div>
  </main>

  <script>
    function consolidate() {
      document.getElementById('enc2-stat').innerText = '180ms · Zero-Shot Heuristic';
      document.getElementById('enc2-stat').className = 'stat-badge fast';
      document.getElementById('enc2-desc').innerHTML = `
        <strong>Cosine Similarity: 0.994</strong><br>
        Episodic plasticity retrieved consolidated invariant schema. Bypassed all 28 diagnostic branches. Solved in 180ms with zero repeated downtime.
      `;
    }
  </script>
</body>
</html>'''

def main():
    files = [
        ("brain_to_ai_homeostasis.html", APP1_HTML),
        ("brain_to_ai_somatic_marker.html", APP2_HTML),
        ("brain_to_ai_theory_of_mind.html", APP3_HTML),
        ("brain_to_ai_consolidation.html", APP4_HTML)
    ]
    for filename, content in files:
        path = os.path.join(r"c:\Users\richa\ai-engineering", filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"Generated {path} ({len(content)} bytes)")

if __name__ == "__main__":
    main()
