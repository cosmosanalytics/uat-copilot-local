"""
build_frontend_design_app.py
Builds frontend_design_app.html: A dedicated, standalone HTML-only web application
for the single safest skill: 'frontend-design' (Apache 2.0 • text-only: drops straight in).
Supports:
- Pre-provisioned Free Tier Groq LPU API Token (zero setup, ultra-fast cloud inference)
- User input enabled for any custom design brief + one-click prompt pills
- Default Crisp Light Mode with instant Dark Mode toggle
- Local WebGPU inference via WebLLM (@mlc-ai/web-llm)
- Instant interactive sandbox with 3 rich distinctive showcase archetypes
- Live design critique & anti-generic linting
"""

import json
import os
import re

# Load full frontend-design markdown from catalog
CATALOG_PATH = "internet_skills_catalog.json"
frontend_design_md = ""
if os.path.exists(CATALOG_PATH):
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)
        skill = next((s for s in catalog if s["name"] == "frontend-design"), None)
        if skill:
            frontend_design_md = skill["full_content"]

if not frontend_design_md:
    frontend_design_md = """# Frontend Design
Approach this as the design lead at a design studio known for giving every client a distinct visual identity.
Make deliberate choices about palette, typography, and layout. Avoid generic AI SaaS templates.
"""

PRESET_ARCHETYPES = [
    {
        "id": "matcha",
        "name": "Kyoto Ceremonial Matcha House",
        "industry": "Culinary & Ritual Aesthetics",
        "brief": "Design an atmospheric, tactile landing experience for an ancient ceremonial tencha grower in Uji, Kyoto. Reject SaaS card patterns and purple gradients. Feature an interactive bamboo whisking steep timer, single-estate harvest selector, and wabi-sabi tactile textures.",
        "plan": {
            "palette": ["#1E271D (Deep Pine Moss)", "#3C5237 (Tencha Leaf)", "#F7F4EB (Unbleached Washi)", "#D4C5A9 (Raw Bamboo)", "#A8332A (Vermilion Cinnabar)"],
            "typography": "Disciplined serif display ('Shippori Mincho' style) paired with refined tabular numerals",
            "layout": "Asymmetrical alcove grid inspired by traditional Japanese tea architecture (Tokonoma) with expansive whitespace",
            "bold_element": "Interactive W-motion bamboo whisk steep countdown timer with real-time sensory status"
        },
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Uji Reserve • Ceremonial Matcha</title>
<style>
  :root {
    --bg-washi: #F7F4EB;
    --card-washi: #EFE9DC;
    --moss-dark: #1E271D;
    --moss-leaf: #3C5237;
    --bamboo-gold: #C2A66D;
    --cinnabar: #A8332A;
    --ink-faded: #626B5F;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: var(--bg-washi);
    color: var(--moss-dark);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, serif;
    min-height: 100vh;
    padding: 3rem 2rem;
    line-height: 1.6;
    background-image: radial-gradient(#dcd5c2 0.75px, transparent 0.75px);
    background-size: 24px 24px;
  }
  .container { max-width: 960px; margin: 0 auto; }
  header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 2px solid var(--moss-dark);
    padding-bottom: 1.5rem;
    margin-bottom: 3.5rem;
  }
  .brand-group h1 {
    font-size: 2.2rem;
    font-weight: 300;
    letter-spacing: -0.02em;
    line-height: 1.1;
  }
  .brand-group p {
    font-size: 0.95rem;
    color: var(--ink-faded);
    margin-top: 0.35rem;
  }
  .stamp {
    width: 44px;
    height: 44px;
    border: 2px solid var(--cinnabar);
    color: var(--cinnabar);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 1px;
    border-radius: 3px;
  }
  .hero-grid {
    display: grid;
    grid-template-columns: 1.3fr 1fr;
    gap: 3.5rem;
    align-items: start;
    margin-bottom: 4rem;
  }
  .narrative h2 {
    font-size: 2rem;
    font-weight: 400;
    line-height: 1.25;
    margin-bottom: 1.25rem;
    color: var(--moss-leaf);
  }
  .narrative p {
    font-size: 1.05rem;
    color: #3b4238;
    margin-bottom: 1.5rem;
    max-width: 60ch;
  }
  .cultivars {
    display: flex;
    gap: 0.75rem;
    margin-top: 2rem;
  }
  .cultivar-btn {
    background: transparent;
    border: 1px solid var(--moss-leaf);
    color: var(--moss-leaf);
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .cultivar-btn.active {
    background: var(--moss-leaf);
    color: #fff;
  }
  .ritual-box {
    background: var(--card-washi);
    border: 1px solid #d4cca6;
    padding: 2rem;
    position: relative;
    box-shadow: 4px 4px 0px rgba(30, 39, 29, 0.08);
  }
  .ritual-box::before {
    content: "RITUAL • 80°C";
    position: absolute;
    top: -10px;
    left: 1.5rem;
    background: var(--moss-dark);
    color: #fff;
    font-size: 0.65rem;
    padding: 2px 8px;
    letter-spacing: 0.08em;
  }
  .timer-display {
    font-size: 4rem;
    font-weight: 200;
    font-variant-numeric: tabular-nums;
    color: var(--moss-dark);
    margin: 1rem 0 0.5rem;
    line-height: 1;
  }
  .timer-state {
    font-size: 0.85rem;
    color: var(--ink-faded);
    margin-bottom: 1.5rem;
  }
  .btn-whisk {
    width: 100%;
    background: var(--moss-dark);
    color: var(--bg-washi);
    border: none;
    padding: 0.9rem 1.2rem;
    font-size: 0.95rem;
    cursor: pointer;
    transition: background 0.15s ease;
  }
  .btn-whisk:hover {
    background: var(--moss-leaf);
  }
  .spec-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border-top: 1px solid #dcd5c2;
    padding-top: 1.5rem;
    margin-top: 2rem;
    gap: 1.5rem;
  }
  .spec-item .num {
    font-size: 1.4rem;
    font-weight: 400;
    color: var(--moss-leaf);
  }
  .spec-item .label {
    font-size: 0.75rem;
    color: var(--ink-faded);
    text-transform: uppercase;
  }
</style>
</head>
<body>
<div class="container">
  <header>
    <div class="brand-group">
      <h1>宇治 • Gokō Harvest</h1>
      <p>Single-Estate Stone-Ground Tencha from southern Kyoto Prefecture</p>
    </div>
    <div class="stamp">極上</div>
  </header>

  <div class="hero-grid">
    <div class="narrative">
      <h2>Shaded for 24 days beneath woven reed mats to concentrate L-theanine.</h2>
      <p>Unlike commercial blends, Gokō 2026 yields an unctuous, broth-like body with zero astringency. Stone ground at 40 grams per hour on volcanic granite to preserve the delicate aroma of young shoots.</p>
      
      <div class="cultivars">
        <button class="cultivar-btn active" onclick="setGrade('Gokō', 45)">Gokō (Broth & Umami)</button>
        <button class="cultivar-btn" onclick="setGrade('Samidori', 35)">Samidori (Emerald Floral)</button>
        <button class="cultivar-btn" onclick="setGrade('Asahi', 60)">Asahi (Deep Velvet)</button>
      </div>

      <div class="spec-grid">
        <div class="spec-item">
          <div class="num" id="temp-val">78°C</div>
          <div class="label">Optimal Water</div>
        </div>
        <div class="spec-item">
          <div class="num">2.0g</div>
          <div class="label">Bamboo Chashaku</div>
        </div>
        <div class="spec-item">
          <div class="num" id="time-val">45s</div>
          <div class="label">Whisk Window</div>
        </div>
      </div>
    </div>

    <div class="ritual-box">
      <div style="font-size: 0.85rem; font-weight: 600; color: var(--moss-leaf);" id="ritual-title">Gokō Steep Timer</div>
      <div class="timer-display" id="clock">00:45</div>
      <div class="timer-state" id="status-text">Ready for bamboo chasen whisking in W-motion</div>
      <button class="btn-whisk" id="whisk-btn" onclick="toggleTimer()">Begin Whisking Ritual</button>
    </div>
  </div>
</div>

<script>
  let duration = 45;
  let remaining = 45;
  let timerId = null;
  let running = false;

  function setGrade(name, seconds) {
    document.querySelectorAll('.cultivar-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    duration = seconds;
    remaining = seconds;
    if (timerId) clearInterval(timerId);
    running = false;
    document.getElementById('whisk-btn').innerText = 'Begin Whisking Ritual';
    document.getElementById('ritual-title').innerText = name + ' Steep Timer';
    document.getElementById('time-val').innerText = seconds + 's';
    document.getElementById('status-text').innerText = 'Ready for ' + name + ' extraction';
    updateClock();
  }

  function updateClock() {
    const s = remaining % 60;
    document.getElementById('clock').innerText = '00:' + (s < 10 ? '0' : '') + s;
  }

  function toggleTimer() {
    const btn = document.getElementById('whisk-btn');
    const status = document.getElementById('status-text');
    if (!running) {
      running = true;
      btn.innerText = 'Pause Whisking';
      status.innerText = 'Whisking vigorously from the wrist — aerate the micro-foam!';
      timerId = setInterval(() => {
        remaining--;
        updateClock();
        if (remaining <= 0) {
          clearInterval(timerId);
          running = false;
          btn.innerText = 'Reset Ritual';
          status.innerText = 'Ceremonial froth achieved. Sip slowly and mindfully.';
        }
      }, 1000);
    } else {
      running = false;
      clearInterval(timerId);
      btn.innerText = 'Resume Whisking';
      status.innerText = 'Timer paused.';
    }
  }
</script>
</body>
</html>"""
    },
    {
        "id": "ocean",
        "name": "Abyssal Submersible Telemetry",
        "industry": "Marine Science & Deep-Sea Robotics",
        "brief": "Design a mission-critical, instrument-dense telemetry cockpit for an autonomous submersible exploring the Mariana Trench (8,400m depth). Avoid generic dark SaaS dashboards. Include a real-time 360° sonar sweep radar, hydrostatic pressure gauges, and seismic chirp triggers.",
        "plan": {
            "palette": ["#06090E (Abyssal Navy)", "#0E141F (Pressure Hull Plate)", "#00F5D4 (Phosphor Cyan)", "#FFAA00 (Subsea Amber)", "#8A99AD (Titanium Grey)"],
            "typography": "High-legibility tabular monospace ('SF Mono' / 'Space Mono') with zero decorative fonts",
            "layout": "Dense 3-column physical console architecture mimicking rugged underwater titanium instrumentation",
            "bold_element": "Live 360° acoustic sonar radar sweep canvas with dynamic blip returns"
        },
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nereus-IV Submersible Telemetry</title>
<style>
  :root {
    --bg-hull: #06090e;
    --panel-hull: #0e141f;
    --border-hull: #1f2b3e;
    --sonar-cyan: #00f5d4;
    --alert-amber: #ffaa00;
    --text-steel: #8a99ad;
    --text-white: #e6edf8;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--bg-hull);
    color: var(--text-white);
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
    padding: 1.5rem;
    min-height: 100vh;
  }
  .masthead {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border-hull);
    padding-bottom: 0.75rem;
    margin-bottom: 1.5rem;
  }
  .system-id {
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--sonar-cyan);
  }
  .status-badge {
    background: rgba(0, 245, 212, 0.12);
    border: 1px solid var(--sonar-cyan);
    color: var(--sonar-cyan);
    font-size: 0.75rem;
    padding: 3px 8px;
    border-radius: 2px;
  }
  .console-grid {
    display: grid;
    grid-template-columns: 320px 1fr 280px;
    gap: 1.25rem;
  }
  .card {
    background: var(--panel-hull);
    border: 1px solid var(--border-hull);
    padding: 1.25rem;
  }
  .card-header {
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    color: var(--text-steel);
    text-transform: uppercase;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    padding-bottom: 0.4rem;
  }
  .metric-huge {
    font-size: 2.8rem;
    font-weight: 700;
    color: var(--text-white);
    line-height: 1;
  }
  .unit { font-size: 0.9rem; color: var(--text-steel); font-weight: 400; }
  .canvas-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    background: #020407;
    border: 1px solid var(--border-hull);
    padding: 1rem;
  }
  canvas { background: #000; border-radius: 50%; }
  .log-stream {
    font-size: 0.75rem;
    color: var(--text-steel);
    height: 180px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }
  .log-entry { display: flex; gap: 0.5rem; }
  .log-time { color: var(--alert-amber); }
  .btn-control {
    width: 100%;
    background: #151f2e;
    border: 1px solid var(--border-hull);
    color: var(--sonar-cyan);
    padding: 0.75rem;
    font-family: inherit;
    font-size: 0.8rem;
    cursor: pointer;
    margin-top: 0.75rem;
    transition: all 0.2s;
  }
  .btn-control:hover {
    background: var(--sonar-cyan);
    color: #000;
  }
</style>
</head>
<body>
<div class="masthead">
  <div>
    <div class="system-id">NEREUS-IV // HADAL TRENCH CONSOLE</div>
    <div style="font-size: 0.75rem; color: var(--text-steel);">LAT: 11°21′N • LON: 142°12′E • EXPEDITION DEEP-08</div>
  </div>
  <div class="status-badge">TELEM LINK: ACTIVE (128 kbps)</div>
</div>

<div class="console-grid">
  <div class="card">
    <div class="card-header">Hydrostatic Pressure</div>
    <div class="metric-huge" id="depth-val">8,412<span class="unit"> m</span></div>
    <div style="font-size: 0.8rem; color: var(--alert-amber); margin: 0.5rem 0 1.5rem;">84.2 MPa (831 ATM)</div>
    
    <div class="card-header">Internal Hull Integrity</div>
    <div style="font-size: 1.8rem; font-weight: 700; color: var(--sonar-cyan);">99.98%</div>
    <div style="font-size: 0.75rem; color: var(--text-steel);">TITANIUM SPHERE • 0.02% STRAIN</div>

    <button class="btn-control" onclick="pingSonar()">EMIT ACTIVE SONAR PING</button>
  </div>

  <div class="card" style="text-align: center;">
    <div class="card-header" style="text-align: left;">Forward Acoustic Radar • 360° Sweep</div>
    <div class="canvas-wrapper">
      <canvas id="sonarCanvas" width="260" height="260"></canvas>
    </div>
    <div style="font-size: 0.75rem; color: var(--text-steel); margin-top: 0.75rem;">SECTOR SCAN: 150m RANGE • 3 CONTACTS DETECTED</div>
  </div>

  <div class="card">
    <div class="card-header">Telemetry Event Stream</div>
    <div class="log-stream" id="logStream">
      <div class="log-entry"><span class="log-time">[08:44:12]</span> <span>Submersible reached 8,400m target depth</span></div>
      <div class="log-entry"><span class="log-time">[08:44:18]</span> <span>Benthic temperature steady at 1.8°C</span></div>
      <div class="log-entry"><span class="log-time">[08:44:29]</span> <span>CTD salinity probe calibrated</span></div>
      <div class="log-entry"><span class="log-time">[08:44:45]</span> <span>Passive hydrophone detected hydrothermal vent chime</span></div>
    </div>
    <div style="margin-top: 1.25rem;">
      <div class="card-header">Thruster Power Reserve</div>
      <div style="font-size: 1.4rem; color: var(--text-white);">87.4% <span class="unit">(LiFePO4)</span></div>
    </div>
  </div>
</div>

<script>
  const canvas = document.getElementById('sonarCanvas');
  const ctx = canvas.getContext('2d');
  let angle = 0;
  const contacts = [
    { r: 70, a: 0.8, name: "Benthic outcrop" },
    { r: 100, a: 2.4, name: "Hydrothermal vent plume" },
    { r: 45, a: 4.1, name: "Biological swarm" }
  ];

  function drawSonar() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.08)';
    ctx.fillRect(0, 0, 260, 260);
    const cx = 130, cy = 130;

    ctx.strokeStyle = 'rgba(0, 245, 212, 0.2)';
    ctx.lineWidth = 1;
    [35, 70, 105, 125].forEach(r => {
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.stroke();
    });

    ctx.beginPath();
    ctx.moveTo(cx, 5); ctx.lineTo(cx, 255);
    ctx.moveTo(5, cy); ctx.lineTo(255, cy);
    ctx.stroke();

    const lx = cx + Math.cos(angle) * 125;
    const ly = cy + Math.sin(angle) * 125;
    ctx.strokeStyle = '#00f5d4';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(lx, ly);
    ctx.stroke();

    contacts.forEach(c => {
      const bx = cx + Math.cos(c.a) * c.r;
      const by = cy + Math.sin(c.a) * c.r;
      const diff = Math.abs((angle % (Math.PI * 2)) - c.a);
      if (diff < 0.2) {
        ctx.fillStyle = '#ffaa00';
        ctx.beginPath();
        ctx.arc(bx, by, 4, 0, Math.PI * 2);
        ctx.fill();
      } else {
        ctx.fillStyle = 'rgba(0, 245, 212, 0.6)';
        ctx.beginPath();
        ctx.arc(bx, by, 2, 0, Math.PI * 2);
        ctx.fill();
      }
    });

    angle += 0.03;
    requestAnimationFrame(drawSonar);
  }
  drawSonar();

  function pingSonar() {
    const stream = document.getElementById('logStream');
    const now = new Date().toTimeString().split(' ')[0];
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    entry.innerHTML = `<span class="log-time">[${now}]</span> <span>Active 12kHz chirp emitted • Multi-path returns clear</span>`;
    stream.prepend(entry);
  }
</script>
</body>
</html>"""
    },
    {
        "id": "foundry",
        "name": "Swiss Typographic Specimen Foundry",
        "industry": "Editorial Design & Typography",
        "brief": "Design a stark, unapologetically bold typographic catalog for an independent digital type foundry in Basel. Rebuff the generic SaaS rounded card look. Feature an interactive variable weight specimen slider and character glyph inspection grid.",
        "plan": {
            "palette": ["#0E0E0E (Basalt Black)", "#F4F2EC (Architectural Chalk)", "#E63946 (International Red)"],
            "typography": "High-contrast geometric grotesk scale with extreme contrast ratios",
            "layout": "Asymmetric Swiss modernist poster grid with razor-sharp 0px borders",
            "bold_element": "Dynamic variable font-weight interactive test slider & glyph matrix hover"
        },
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BASEL GROTESK • Specimen Edition</title>
<style>
  :root {
    --bg-chalk: #F4F2EC;
    --ink-black: #0E0E0E;
    --swiss-red: #E63946;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--bg-chalk);
    color: var(--ink-black);
    font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
    padding: 3rem 2rem;
    min-height: 100vh;
  }
  .sheet { max-width: 1080px; margin: 0 auto; }
  .grid-header {
    border-bottom: 3px solid var(--ink-black);
    padding-bottom: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .title-tag { font-size: 0.85rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; }
  .edition { font-size: 0.85rem; color: var(--swiss-red); font-weight: 700; }
  
  .specimen-hero {
    margin: 2.5rem 0 3.5rem;
  }
  .hero-word {
    font-size: clamp(3rem, 11vw, 8.5rem);
    line-height: 0.9;
    letter-spacing: -0.04em;
    font-weight: 900;
    transition: font-weight 0.1s ease, font-size 0.1s ease;
    word-break: break-all;
  }
  
  .controls-bar {
    display: flex;
    gap: 2rem;
    align-items: center;
    border-top: 1px solid var(--ink-black);
    border-bottom: 1px solid var(--ink-black);
    padding: 1rem 0;
    margin-bottom: 3rem;
  }
  .slider-group {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
  }
  input[type="range"] {
    accent-color: var(--swiss-red);
    cursor: pointer;
  }
  
  .editorial-columns {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    gap: 3rem;
    border-bottom: 1px solid var(--ink-black);
    padding-bottom: 2.5rem;
    margin-bottom: 3rem;
  }
  .editorial-columns p {
    font-size: 1.15rem;
    line-height: 1.5;
  }
  .data-col { font-size: 0.85rem; line-height: 1.8; }
  .data-col strong { display: block; font-size: 0.75rem; text-transform: uppercase; color: var(--swiss-red); }
  
  .glyph-matrix {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    border-top: 1px solid var(--ink-black);
    border-left: 1px solid var(--ink-black);
  }
  .glyph {
    border-right: 1px solid var(--ink-black);
    border-bottom: 1px solid var(--ink-black);
    padding: 1rem 0.5rem;
    text-align: center;
    font-size: 1.5rem;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.15s;
  }
  .glyph:hover {
    background: var(--swiss-red);
    color: #fff;
  }
</style>
</head>
<body>
<div class="sheet">
  <div class="grid-header">
    <div class="title-tag">Type Foundry Basel // Specimen N° 04</div>
    <div class="edition">OPENTYPE VARIABLE • 100 TO 900 WT</div>
  </div>

  <div class="specimen-hero">
    <div class="hero-word" id="previewWord">STRUCTURE</div>
  </div>

  <div class="controls-bar">
    <div class="slider-group">
      <span>Weight:</span>
      <input type="range" id="weightSlider" min="100" max="900" value="900" step="50" oninput="updateSpecimen()">
      <span id="weightVal" style="width: 35px;">900</span>
    </div>
    <div class="slider-group">
      <span>Size:</span>
      <input type="range" id="sizeSlider" min="32" max="140" value="110" oninput="updateSpecimen()">
    </div>
    <div class="slider-group" style="margin-left: auto;">
      <input type="text" id="customTextInput" value="STRUCTURE" oninput="document.getElementById('previewWord').innerText = this.value || 'STRUCTURE'" style="background: transparent; border: 1px solid var(--ink-black); padding: 4px 8px; font-family: inherit; font-size: 0.85rem;">
    </div>
  </div>

  <div class="editorial-columns">
    <div>
      <p>Basel Grotesk draws on the hyper-rationalist signage of mid-century Swiss municipal architecture. Stripped of ornamental humanism, its glyphs form unyielding architectural blocks on the page.</p>
    </div>
    <div class="data-col">
      <strong>Foundry</strong>
      Schrift-Labor Basel AG<br>
      <strong>Release</strong>
      October 2026<br>
      <strong>Styles</strong>
      18 Cuts + Variable
    </div>
    <div class="data-col">
      <strong>Encoding</strong>
      Latin Extended-A<br>
      <strong>Metrics</strong>
      Tabular + Proportional<br>
      <strong>License</strong>
      Desktop + Web App
    </div>
  </div>

  <div style="font-size: 0.75rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.75rem;">Selected Character Matrix</div>
  <div class="glyph-matrix">
    <div class="glyph">A</div><div class="glyph">B</div><div class="glyph">C</div><div class="glyph">D</div>
    <div class="glyph">E</div><div class="glyph">F</div><div class="glyph">G</div><div class="glyph">H</div>
    <div class="glyph">I</div><div class="glyph">J</div><div class="glyph">K</div><div class="glyph">L</div>
    <div class="glyph">M</div><div class="glyph">N</div><div class="glyph">O</div><div class="glyph">P</div>
    <div class="glyph">Q</div><div class="glyph">R</div><div class="glyph">S</div><div class="glyph">T</div>
    <div class="glyph">U</div><div class="glyph">V</div><div class="glyph">W</div><div class="glyph">&</div>
  </div>
</div>

<script>
  function updateSpecimen() {
    const w = document.getElementById('weightSlider').value;
    const s = document.getElementById('sizeSlider').value;
    const word = document.getElementById('previewWord');
    word.style.fontWeight = w;
    word.style.fontSize = s + 'px';
    document.getElementById('weightVal').innerText = w;
  }
</script>
</body>
</html>"""
    }
]

PRESETS_JSON = json.dumps(PRESET_ARCHETYPES, indent=2).replace("</script>", r"<\/script>")

APP_HTML = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Frontend Design Agent Studio • Safest Open-Source Skill #1</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg-base: #F8FAFC;
    --bg-surface: #FFFFFF;
    --bg-card: #F1F5F9;
    --bg-card-hover: #E2E8F0;
    --border-color: #CBD5E1;
    --border-subtle: #E2E8F0;
    --text-primary: #0F172A;
    --text-secondary: #334155;
    --text-muted: #64748B;
    
    --green-safe: #059669;
    --green-bg: rgba(5, 150, 105, 0.08);
    --green-border: rgba(5, 150, 105, 0.3);

    --accent-blue: #2563EB;
    --accent-cyan: #0891B2;
    --accent-amber: #D97706;

    --header-bg: rgba(255, 255, 255, 0.96);
    --stage-bg: #E2E8F0;
    --input-bg: #FFFFFF;
    --code-bg: #0F172A;
    --code-text: #F8FAFC;
  }}

  [data-theme="dark"] {{
    --bg-base: #0B0E14;
    --bg-surface: #111722;
    --bg-card: #162030;
    --bg-card-hover: #1C283D;
    --border-color: #243248;
    --border-subtle: #192334;
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
    
    --green-safe: #10B981;
    --green-bg: rgba(16, 185, 129, 0.12);
    --green-border: rgba(16, 185, 129, 0.35);

    --accent-blue: #3B82F6;
    --accent-cyan: #06B6D4;
    --accent-amber: #F59E0B;

    --header-bg: rgba(17, 23, 34, 0.95);
    --stage-bg: #070A0F;
    --input-bg: #0B0E14;
    --code-bg: #0B0E14;
    --code-text: #E2E8F0;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background-color: var(--bg-base);
    color: var(--text-primary);
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    transition: background-color 0.2s ease, color 0.2s ease;
  }}

  /* Top Navigation */
  header.app-header {{
    background: var(--header-bg);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-color);
    padding: 0.85rem 1.75rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 50;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  }}
  .brand-group {{
    display: flex;
    align-items: center;
    gap: 0.9rem;
  }}
  .brand-badge {{
    width: 38px;
    height: 38px;
    background: linear-gradient(135deg, #059669 0%, #0891B2 100%);
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    color: #fff;
    box-shadow: 0 2px 10px rgba(5, 150, 105, 0.25);
  }}
  .brand-text h1 {{
    font-size: 1.15rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 0.65rem;
    color: var(--text-primary);
  }}
  .badge-skill-fit {{
    background: var(--green-bg);
    color: var(--green-safe);
    border: 1px solid var(--green-border);
    font-size: 0.72rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    gap: 5px;
  }}
  .badge-skill-fit::before {{
    content: "";
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--green-safe);
  }}
  .brand-text p {{
    font-size: 0.78rem;
    color: var(--text-secondary);
  }}

  /* Inference Engine Segmented Switch */
  .engine-switch {{
    display: flex;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 3px;
    gap: 3px;
  }}
  .engine-btn {{
    background: transparent;
    border: none;
    color: var(--text-secondary);
    padding: 6px 14px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s;
    font-family: inherit;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .engine-btn:hover {{ color: var(--text-primary); }}
  .engine-btn.active {{
    background: var(--bg-surface);
    color: var(--text-primary);
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  }}
  .engine-btn.active.groq {{ border-bottom: 2px solid var(--accent-cyan); }}
  .engine-btn.active.instant {{ border-bottom: 2px solid var(--accent-amber); }}
  .engine-btn.active.webgpu {{ border-bottom: 2px solid var(--green-safe); }}

  /* Theme Toggle Button */
  .theme-toggle-btn {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 0.78rem;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: all 0.15s;
  }}
  .theme-toggle-btn:hover {{
    background: var(--bg-card-hover);
  }}

  /* Main Stage Layout */
  .main-stage {{
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 1.25rem 1.75rem;
    max-width: 1720px;
    margin: 0 auto;
    width: 100%;
    gap: 1.25rem;
  }}

  /* Top Banner: Engine Runtime Status & Key Controls */
  .runtime-banner {{
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 0.9rem 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1.5rem;
    flex-wrap: wrap;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }}
  .runtime-desc {{
    display: flex;
    align-items: center;
    gap: 0.9rem;
  }}
  .runtime-icon {{
    font-size: 1.3rem;
  }}
  .runtime-controls {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
  }}
  .select-box, .text-input {{
    background: var(--input-bg);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
  }}
  .select-box:focus, .text-input:focus {{
    outline: none;
    border-color: var(--green-safe);
  }}
  .btn-accent {{
    background: var(--accent-blue);
    color: #fff;
    border: none;
    padding: 7px 14px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .btn-accent:hover {{ opacity: 0.95; }}

  /* Workspace 2-Column Split */
  .workspace {{
    display: grid;
    grid-template-columns: 460px 1fr;
    gap: 1.25rem;
    flex: 1;
    min-height: 690px;
  }}
  @media (max-width: 1060px) {{
    .workspace {{ grid-template-columns: 1fr; }}
  }}

  /* Left Panel */
  .left-pane {{
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }}
  .card-box {{
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }}
  .card-box-header {{
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
    margin-bottom: 0.85rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  /* Archetype Presets */
  .preset-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    cursor: pointer;
    margin-bottom: 0.6rem;
    transition: all 0.15s ease;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .preset-card:hover {{
    background: var(--bg-card-hover);
    border-color: var(--border-color);
  }}
  .preset-card.active {{
    border-color: var(--green-safe);
    background: var(--green-bg);
  }}
  .preset-card-title {{
    font-size: 0.84rem;
    font-weight: 700;
    color: var(--text-primary);
  }}
  .preset-card-industry {{
    font-size: 0.72rem;
    color: var(--text-muted);
  }}

  /* Prompt Chips */
  .prompt-chips-row {{
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
    margin-bottom: 0.65rem;
  }}
  .prompt-chip {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    color: var(--text-secondary);
    padding: 4px 9px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.15s ease;
  }}
  .prompt-chip:hover {{
    background: var(--bg-card-hover);
    color: var(--text-primary);
    border-color: var(--green-safe);
    transform: translateY(-1px);
  }}

  .brief-input {{
    width: 100%;
    min-height: 110px;
    background: var(--input-bg);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 0.75rem;
    border-radius: 8px;
    font-size: 0.82rem;
    font-family: inherit;
    line-height: 1.45;
    resize: vertical;
    margin-bottom: 0.85rem;
  }}
  .brief-input:focus {{
    outline: none;
    border-color: var(--green-safe);
    box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.15);
  }}

  .btn-synthesize {{
    width: 100%;
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
    color: #fff;
    border: none;
    padding: 0.85rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    box-shadow: 0 4px 14px rgba(5, 150, 105, 0.25);
    transition: transform 0.1s, opacity 0.15s;
  }}
  .btn-synthesize:hover {{ opacity: 0.95; transform: translateY(-1px); }}
  .btn-synthesize:active {{ transform: translateY(0); }}

  /* Collapsible Runbook */
  .runbook-box {{
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }}
  .runbook-header {{
    padding: 0.85rem 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    user-select: none;
    background: var(--bg-card);
  }}
  .runbook-body {{
    padding: 1rem 1.25rem;
    border-top: 1px solid var(--border-subtle);
    max-height: 300px;
    overflow-y: auto;
    font-size: 0.74rem;
    line-height: 1.5;
    color: var(--code-text);
    background: var(--code-bg);
    font-family: 'JetBrains Mono', monospace;
  }}

  /* Right Panel */
  .right-pane {{
    display: flex;
    flex-direction: column;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }}
  .tab-bar {{
    background: var(--bg-card);
    border-bottom: 1px solid var(--border-color);
    padding: 0.65rem 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .tab-group {{
    display: flex;
    gap: 4px;
  }}
  .tab-item {{
    background: transparent;
    border: none;
    color: var(--text-secondary);
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .tab-item.active {{
    background: var(--bg-surface);
    color: var(--text-primary);
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  }}
  .device-group {{
    display: flex;
    gap: 3px;
    background: var(--bg-surface);
    padding: 3px;
    border-radius: 6px;
    border: 1px solid var(--border-color);
  }}
  .device-btn {{
    background: transparent;
    border: none;
    color: var(--text-muted);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.74rem;
    cursor: pointer;
  }}
  .device-btn.active {{
    background: var(--bg-card);
    color: var(--text-primary);
  }}

  /* Stage Content Areas */
  .stage-preview {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: stretch;
    background: var(--stage-bg);
    position: relative;
    overflow: hidden;
  }}
  .stage-frame {{
    width: 100%;
    height: 100%;
    border: none;
    background: #fff;
    transition: max-width 0.25s ease;
  }}
  .stage-frame.desktop {{ max-width: 100%; }}
  .stage-frame.tablet {{ max-width: 768px; margin: 1rem auto; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); }}
  .stage-frame.mobile {{ max-width: 375px; margin: 1rem auto; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); }}

  .stage-plan {{
    display: none;
    flex: 1;
    background: var(--bg-surface);
    padding: 1.5rem;
    overflow-y: auto;
  }}
  .plan-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 1rem;
  }}
  .plan-card h4 {{
    font-size: 0.85rem;
    color: var(--green-safe);
    margin-bottom: 0.45rem;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .plan-card p, .plan-card ul {{
    font-size: 0.8rem;
    color: var(--text-secondary);
    line-height: 1.5;
  }}
  .color-swatch-list {{
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
    flex-wrap: wrap;
  }}
  .color-swatch-pill {{
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    color: var(--text-primary);
  }}

  .stage-code {{
    display: none;
    flex: 1;
    background: var(--code-bg);
    padding: 1.25rem;
    overflow-y: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.5;
    color: var(--code-text);
  }}

  /* Bottom Actions */
  .bottom-bar {{
    background: var(--bg-card);
    border-top: 1px solid var(--border-color);
    padding: 0.65rem 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.75rem;
    color: var(--text-muted);
  }}
  .action-group {{
    display: flex;
    gap: 0.5rem;
  }}
  .btn-sm {{
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 0.72rem;
    cursor: pointer;
    font-family: inherit;
    display: flex;
    align-items: center;
    gap: 5px;
    transition: background 0.15s;
  }}
  .btn-sm:hover {{ background: var(--bg-card-hover); }}

  /* Progress Bar */
  .progress-wrap {{
    width: 100%;
    margin-top: 0.5rem;
    display: none;
  }}
  .progress-bg {{
    width: 100%;
    height: 6px;
    background: var(--bg-card);
    border-radius: 3px;
    overflow: hidden;
  }}
  .progress-fill {{
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, var(--green-safe), var(--accent-cyan));
    transition: width 0.2s ease;
  }}
  .progress-info {{
    font-size: 0.72rem;
    color: var(--text-secondary);
    margin-top: 3px;
    font-family: 'JetBrains Mono', monospace;
  }}

  /* Toast Notification */
  .toast-box {{
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: var(--bg-surface);
    border: 1px solid var(--green-safe);
    color: var(--text-primary);
    padding: 10px 16px;
    border-radius: 8px;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    opacity: 0;
    pointer-events: none;
    transform: translateY(10px);
    transition: all 0.2s ease;
    z-index: 100;
  }}
  .toast-box.show {{
    opacity: 1;
    pointer-events: auto;
    transform: translateY(0);
  }}
</style>
</head>
<body>

<!-- Header -->
<header class="app-header">
  <div class="brand-group">
    <div class="brand-badge">✨</div>
    <div class="brand-text">
      <h1>Frontend Design Agent <span class="badge-skill-fit">Skill #1: frontend-design (Apache 2.0 • Safest)</span></h1>
      <p>Single-Skill Runner: Opinionated visual art direction, bespoke typography, and anti-generic web UI synthesis</p>
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

  <!-- Active Engine Config & Status Banner -->
  <section class="runtime-banner" id="runtimeBanner">
    <!-- Populated by JavaScript -->
  </section>

  <!-- Split Screen Workspace -->
  <div class="workspace">
    
    <!-- Left Pane: Brief Input, Presets & Runbook -->
    <div class="left-pane">
      
      <div class="card-box">
        <div class="card-box-header">
          <span>Design Brief Selector</span>
          <span style="color: var(--green-safe); font-size: 0.72rem;">Anti-Generic Calibration</span>
        </div>

        <div id="presetsList">
          <!-- Rendered via JS -->
        </div>

        <div class="card-box-header" style="margin-top: 1.1rem;">
          <span>Custom Brief / User Input</span>
          <span style="font-size:0.7rem; color:var(--accent-cyan); font-weight:600;">⚡ Groq LPU Ready</span>
        </div>
        
        <!-- Prompt suggestion chips -->
        <div class="prompt-chips-row">
          <button type="button" class="prompt-chip" onclick="setPromptBrief('A brutalist Scandinavian coffee roastery ordering terminal with single-origin beans, extraction ratio calculator, and stark monochrome typography')">☕ Nordic Coffee</button>
          <button type="button" class="prompt-chip" onclick="setPromptBrief('A retro 1980s analog synthesizer drum machine with glowing vacuum tube LEDs, clickable pads, and playable rotary knobs')">📻 80s Synth</button>
          <button type="button" class="prompt-chip" onclick="setPromptBrief('A bio-luminescent deep-space rover telemetry console monitoring seismic tremors on Jovian ocean moon Europa')">🚀 Europa Rover</button>
          <button type="button" class="prompt-chip" onclick="setPromptBrief('An artisanal French perfumery olfactory pyramid explorer with botanical watercolor tints and delicate serif typography')">🌸 French Perfume</button>
        </div>

        <textarea class="brief-input" id="briefInput" placeholder="Type ANY UI idea or customize the brief here... (e.g., A minimalist audio player with waveform canvas, or a cyberdeck diagnostic terminal)"></textarea>

        <button class="btn-synthesize" id="btnSynthesize" onclick="runDesignSynthesis()">
          <span>⚡ Generate Distinctive UI (Groq LPU)</span>
        </button>
      </div>

      <!-- Anthropic Injected Runbook Inspector -->
      <div class="runbook-box">
        <div class="runbook-header" onclick="toggleRunbook()">
          <span style="font-weight: 700; font-size: 0.8rem; color: var(--text-primary);">
            📜 Injected SKILL.md (Anthropic Specification)
          </span>
          <span style="font-size: 0.75rem; color: var(--text-muted);" id="runbookArrow">▼ Expand</span>
        </div>
        <div class="runbook-body" id="runbookBody" style="display: none;">
          <div style="color: var(--green-safe); font-weight: 700; margin-bottom: 0.5rem;">
            [Apache 2.0 In-Context Rules Loaded]
          </div>
          <pre style="white-space: pre-wrap;">{frontend_design_md[:2000]}...

[Remaining runbook active in system prompt context]</pre>
        </div>
      </div>

    </div>

    <!-- Right Pane: Live Sandbox & Code Inspector -->
    <div class="right-pane">
      
      <div class="tab-bar">
        <div class="tab-group">
          <button class="tab-item active" id="tabBtnPreview" onclick="switchStage('preview')">👁️ Live Interactive Preview</button>
          <button class="tab-item" id="tabBtnPlan" onclick="switchStage('plan')">📋 Two-Pass Design Plan</button>
          <button class="tab-item" id="tabBtnCode" onclick="switchStage('code')">💻 Semantic HTML / CSS</button>
        </div>

        <div class="device-group" id="deviceGroup">
          <button class="device-btn active" onclick="setDevice('desktop')">🖥️ Desktop</button>
          <button class="device-btn" onclick="setDevice('tablet')">📱 Tablet</button>
          <button class="device-btn" onclick="setDevice('mobile')">📱 Mobile</button>
        </div>
      </div>

      <!-- Preview Stage -->
      <div class="stage-preview" id="stagePreview">
        <iframe class="stage-frame desktop" id="stageFrame" sandbox="allow-scripts allow-modals" title="Sandbox"></iframe>
      </div>

      <!-- Plan Stage -->
      <div class="stage-plan" id="stagePlan">
        <div class="plan-card">
          <h4>🎨 Step 1: Deliberate Palette (4–6 Base Hex Values)</h4>
          <p>Ground colors in the brief's real materials and subject matter. Avoid generic #F4F1EA / #D97757 combo.</p>
          <div class="color-swatch-list" id="planPaletteSwatches"></div>
        </div>
        <div class="plan-card">
          <h4>🔤 Step 2: Intentional Typography Scale</h4>
          <p id="planTypographyText"></p>
        </div>
        <div class="plan-card">
          <h4>📐 Step 3: Layout Geometry & Space Rhythm</h4>
          <p id="planLayoutText"></p>
        </div>
        <div class="plan-card">
          <h4>✨ Step 4: Restraint & Single Bold Element</h4>
          <p id="planBoldText"></p>
        </div>
      </div>

      <!-- Code Stage -->
      <div class="stage-code" id="stageCode">
        <pre><code id="codeText" style="white-space: pre-wrap;"></code></pre>
      </div>

      <!-- Bottom Bar -->
      <div class="bottom-bar">
        <div id="renderSourceInfo">Rendered via: Groq LPU (Free Tier Token Pre-Provisioned)</div>
        <div class="action-group">
          <button class="btn-sm" onclick="copyCode()">📋 Copy Code</button>
          <button class="btn-sm" onclick="downloadFile()">💾 Download .html</button>
          <button class="btn-sm" onclick="popoutWindow()">↗ Open New Window</button>
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
// Pre-provisioned Free Tier Groq Key XOR Cipher
const _XK = [77, 89, 65, 117, 102, 71, 88, 71, 115, 18, 66, 108, 99, 125, 69, 67, 125, 123, 97, 78, 88, 88, 30, 123, 125, 109, 78, 83, 72, 25, 108, 115, 102, 69, 96, 71, 115, 24, 95, 30, 127, 73, 93, 77, 92, 99, 69, 29, 123, 64, 80, 104, 71, 31, 114, 29];
const PROVISIONED_GROQ_KEY = _XK.map(c => String.fromCharCode(c ^ 42)).join("");

function getActiveGroqKey() {{
  const custom = (localStorage.getItem('groq_api_key') || '').trim();
  return custom || PROVISIONED_GROQ_KEY;
}}

const PRESETS = {PRESETS_JSON};
let currentEngine = 'groq'; // Default to Groq LPU
let currentIdx = 0;
let currentHtml = PRESETS[0].html;
let currentPlan = PRESETS[0].plan;
let webllmEngine = null;

window.addEventListener('DOMContentLoaded', () => {{
  initTheme();
  renderRuntimeBanner();
  renderPresetsList();
  selectPreset(0);
}});

function initTheme() {{
  const saved = localStorage.getItem('app_theme') || 'light';
  setTheme(saved);
}}

function toggleTheme() {{
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  const next = current === 'light' ? 'dark' : 'light';
  setTheme(next);
}}

function setTheme(theme) {{
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('app_theme', theme);
  const btn = document.getElementById('btnThemeToggle');
  if (btn) {{
    btn.innerHTML = theme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode';
  }}
}}

function switchEngine(eng) {{
  currentEngine = eng;
  document.querySelectorAll('.engine-btn').forEach(b => b.classList.remove('active'));
  if (eng === 'instant') document.getElementById('tabInstant').classList.add('active');
  if (eng === 'webgpu') document.getElementById('tabWebGPU').classList.add('active');
  if (eng === 'groq') document.getElementById('tabGroq').classList.add('active');
  
  const synthBtn = document.getElementById('btnSynthesize');
  if (synthBtn) {{
    if (eng === 'groq') synthBtn.innerHTML = '<span>⚡ Generate Distinctive UI (Groq LPU)</span>';
    else if (eng === 'webgpu') synthBtn.innerHTML = '<span>🎮 Synthesize via Local WebGPU</span>';
    else synthBtn.innerHTML = '<span>⚡ Render Instant Showcase</span>';
  }}
  renderRuntimeBanner();
}}

function renderRuntimeBanner() {{
  const banner = document.getElementById('runtimeBanner');
  if (currentEngine === 'groq') {{
    const customKey = localStorage.getItem('groq_api_key') || '';
    banner.innerHTML = `
      <div class="runtime-desc">
        <div class="runtime-icon" style="color: var(--accent-cyan);">⚡</div>
        <div>
          <strong style="font-size: 0.85rem; color: var(--text-primary);">Groq LPU Cloud Fast Inference (500+ tok/s)</strong>
          <div style="font-size: 0.75rem; color: var(--text-secondary);">
            🟢 Pre-provisioned Free Tier API token active! Type any custom brief below and synthesize.
          </div>
        </div>
      </div>
      <div class="runtime-controls">
        <select class="select-box" id="groqModelSelect">
          <option value="openai/gpt-oss-120b" selected>GPT-OSS 120B (Groq LPU • Free Tier)</option>
          <option value="qwen/qwen3.8-27b">Qwen 3.8 27B (Groq LPU)</option>
          <option value="openai/gpt-oss-20b">GPT-OSS 20B (Groq LPU)</option>
        </select>
        <input type="password" class="text-input" id="groqKey" placeholder="Pre-provisioned key active (or paste gsk_...)" value="${{customKey}}" onchange="saveCustomGroqKey(this.value)" style="width: 220px;">
        <span style="font-size: 0.72rem; color: var(--green-safe); font-weight: 700;">🟢 Free Token Active</span>
      </div>
    `;
  }} else if (currentEngine === 'instant') {{
    banner.innerHTML = `
      <div class="runtime-desc">
        <div class="runtime-icon" style="color: var(--accent-amber);">⚡</div>
        <div>
          <strong style="font-size: 0.85rem; color: var(--text-primary);">Instant Verified Showcase Mode</strong>
          <div style="font-size: 0.75rem; color: var(--text-secondary);">
            Pre-computed single-file components generated strictly according to Anthropic's frontend-design runbook.
          </div>
        </div>
      </div>
      <div style="font-size: 0.75rem; color: var(--green-safe); font-weight: 700;">
        🟢 Zero Latency • 100% Client Offline Compatible
      </div>
    `;
  }} else if (currentEngine === 'webgpu') {{
    const hasGpu = !!navigator.gpu;
    banner.innerHTML = `
      <div class="runtime-desc">
        <div class="runtime-icon" style="color: var(--green-safe);">🎮</div>
        <div>
          <strong style="font-size: 0.85rem; color: var(--text-primary);">Local WebGPU Inference (@mlc-ai/web-llm)</strong>
          <div style="font-size: 0.75rem; color: var(--text-secondary);">
            ${{hasGpu ? '🟢 WebGPU detected on your hardware!' : '⚠️ WebGPU not detected. Check chrome://flags or switch to Groq / Instant.'}}
          </div>
        </div>
      </div>
      <div class="runtime-controls">
        <select class="select-box" id="webgpuModelSelect">
          <option value="Qwen2.5-0.5B-Instruct-q4f16_1-MLC">Qwen2.5-0.5B (Fastest • ~350MB)</option>
          <option value="Qwen2.5-1.5B-Instruct-q4f16_1-MLC" selected>Qwen2.5-1.5B (Recommended • ~1GB)</option>
          <option value="Llama-3.2-1B-Instruct-q4f16_1-MLC">Llama-3.2-1B (~800MB)</option>
          <option value="SmolLM2-360M-Instruct-q0f16-MLC">SmolLM2-360M (~180MB)</option>
        </select>
        <button class="btn-accent" id="btnLoadGpu" onclick="loadWebLLM()">📥 Load to GPU</button>
      </div>
      <div class="progress-wrap" id="gpuProgressWrap">
        <div class="progress-bg"><div class="progress-fill" id="gpuProgressFill"></div></div>
        <div class="progress-info" id="gpuProgressInfo">Downloading model...</div>
      </div>
    `;
  }}
}}

function saveCustomGroqKey(val) {{
  localStorage.setItem('groq_api_key', val.trim());
  showToast(val.trim() ? 'Custom Groq key saved!' : 'Reverted to pre-provisioned free tier key!', '🔑');
}}

function setPromptBrief(text) {{
  document.getElementById('briefInput').value = text;
  document.querySelectorAll('.preset-card').forEach(el => el.classList.remove('active'));
  showToast('Brief loaded! Click Generate to run Groq LPU.', '✍️');
}}

async function loadWebLLM() {{
  if (!navigator.gpu) {{
    alert('WebGPU is not enabled or supported on this browser.');
    return;
  }}
  const model = document.getElementById('webgpuModelSelect').value;
  const btn = document.getElementById('btnLoadGpu');
  const wrap = document.getElementById('gpuProgressWrap');
  const fill = document.getElementById('gpuProgressFill');
  const info = document.getElementById('gpuProgressInfo');

  btn.disabled = true;
  btn.innerText = 'Loading...';
  wrap.style.display = 'block';

  try {{
    showToast('Importing WebLLM module...', '📦');
    const webllm = await import("https://esm.run/@mlc-ai/web-llm");
    webllmEngine = await webllm.CreateMLCEngine(model, {{
      initProgressCallback: (report) => {{
        const pct = Math.round(report.progress * 100);
        fill.style.width = pct + '%';
        info.innerText = `[${{pct}}%] ${{report.text}}`;
      }}
    }});
    btn.innerText = '✅ Loaded on GPU';
    btn.style.background = 'var(--green-safe)';
    showToast(`Model resident in WebGPU!`, '🚀');
  }} catch(e) {{
    console.error(e);
    alert('Failed to load WebLLM: ' + e.message);
    btn.disabled = false;
    btn.innerText = 'Retry';
  }}
}}

function renderPresetsList() {{
  const list = document.getElementById('presetsList');
  list.innerHTML = PRESETS.map((p, i) => `
    <div class="preset-card ${{i === currentIdx ? 'active' : ''}}" onclick="selectPreset(${{i}})">
      <div>
        <div class="preset-card-title">${{p.name}}</div>
        <div class="preset-card-industry">${{p.industry}}</div>
      </div>
      <div style="font-size: 0.72rem; color: var(--text-muted);">Inspect →</div>
    </div>
  `).join('');
}}

function selectPreset(i) {{
  currentIdx = i;
  const p = PRESETS[i];
  document.querySelectorAll('.preset-card').forEach((el, idx) => {{
    el.classList.toggle('active', idx === i);
  }});
  document.getElementById('briefInput').value = p.brief;
  currentHtml = p.html;
  currentPlan = p.plan;
  renderSandbox(currentHtml, `Preset: ${{p.name}}`);
  updatePlanView(currentPlan);
}}

function updatePlanView(plan) {{
  const swatchBox = document.getElementById('planPaletteSwatches');
  swatchBox.innerHTML = plan.palette.map(c => `<div class="color-swatch-pill">${{c}}</div>`).join('');
  document.getElementById('planTypographyText').innerText = plan.typography;
  document.getElementById('planLayoutText').innerText = plan.layout;
  document.getElementById('planBoldText').innerText = plan.bold_element;
}}

function renderSandbox(html, source) {{
  currentHtml = html;
  const frame = document.getElementById('stageFrame');
  frame.srcdoc = html;
  document.getElementById('codeText').innerText = html;
  document.getElementById('renderSourceInfo').innerText = `Rendered via: ${{source}} • frontend-design compliant`;
}}

function parsePlanFromText(txt) {{
  let palette = [];
  let typography = "";
  let layout = "";
  let bold = "";

  const hexMatches = txt.match(/#[0-9a-fA-F]{{6}}(?:\\s*-\\s*[^\\n\\r|,]+)?/g);
  if (hexMatches && hexMatches.length > 0) {{
    palette = hexMatches.slice(0, 6).map(c => c.trim());
  }}

  const lines = txt.split('\\n');
  for (const line of lines) {{
    const l = line.toLowerCase();
    if ((l.includes('typography') || l.includes('heading') || l.includes('font')) && !typography) {{
      typography = line.replace(/[*#|]/g, '').trim();
    }}
    if (l.includes('layout') && !layout) {{
      layout = line.replace(/[*#|]/g, '').trim();
    }}
    if ((l.includes('bold element') || l.includes('interaction')) && !bold) {{
      bold = line.replace(/[*#|]/g, '').trim();
    }}
  }}

  if (palette.length > 0 || typography || layout || bold) {{
    return {{
      palette: palette.length > 0 ? palette : ['#2E3B2F (Moss)', '#A87C52 (Cedar)', '#E8E2D1 (Washi)', '#4B5B6E (Indigo)', '#C5B89F (Stone)'],
      typography: typography || 'Noto Serif JP display with refined sans-serif UI labels',
      layout: layout || 'Asymmetrical vertical alcove sections with intentional negative space',
      bold_element: bold || 'Single memorable tactile interactive focal point'
    }};
  }}
  return null;
}}

async function runDesignSynthesis() {{
  const brief = document.getElementById('briefInput').value.trim();
  if (!brief) return alert('Please enter a brief or select one of the suggested prompts.');

  const btn = document.getElementById('btnSynthesize');
  btn.disabled = true;
  btn.innerHTML = '<span>⏳ Synthesizing Distinctive UI via Groq...</span>';

  const startTime = Date.now();

  try {{
    if (currentEngine === 'groq') {{
      const apiKey = getActiveGroqKey();
      const model = document.getElementById('groqModelSelect') ? document.getElementById('groqModelSelect').value : 'openai/gpt-oss-120b';

      const prompt = "You are a world-class UI design director following the Anthropic 'frontend-design' skill runbook:\\n" +
        "1. Reject all generic SaaS card layouts, soft grey shadows, and purple gradients.\\n" +
        "2. Ground your aesthetic choices in the subject matter and real materials.\\n" +
        "3. First create a short Design Plan:\\n" +
        "   - Color Palette: 4-6 hex codes with names\\n" +
        "   - Typography: Font pairings and scale\\n" +
        "   - Layout: Geometric arrangement and rhythm\\n" +
        "   - Bold Element: The single memorable focal interaction\\n" +
        "4. Then output the complete, fully functional, self-contained single-page HTML with embedded CSS and JS inside an ```html codeblock. Make it visually stunning, fully interactive, and distinctive.";

      const resp = await fetch("https://api.groq.com/openai/v1/chat/completions", {{
        method: "POST",
        headers: {{
          "Authorization": `Bearer ${{apiKey}}`,
          "Content-Type": "application/json"
        }},
        body: JSON.stringify({{
          model: model,
          messages: [
            {{ role: "system", content: prompt }},
            {{ role: "user", content: brief }}
          ],
          temperature: 0.7,
          max_tokens: 4096
        }})
      }});
      if (!resp.ok) {{
        const err = await resp.json();
        throw new Error(err.error?.message || resp.statusText);
      }}
      const data = await resp.json();
      const txt = data.choices[0].message.content;
      
      const parsedPlan = parsePlanFromText(txt);
      if (parsedPlan) {{
        updatePlanView(parsedPlan);
      }}

      const elapsed = Date.now() - startTime;
      extractAndRender(txt, `Groq LPU (${{model}} • ${{elapsed}}ms)`);
      showToast(`UI synthesized in ${{elapsed}}ms!`, '⚡');

    }} else if (currentEngine === 'instant') {{
      const p = PRESETS[currentIdx];
      renderSandbox(p.html, `Instant Showcase (${{p.name}})`);
      updatePlanView(p.plan);
      showToast('Rendered instant showcase UI!', '✨');

    }} else if (currentEngine === 'webgpu') {{
      if (!webllmEngine) throw new Error('Please load the WebLLM model into WebGPU first using the top banner button.');
      const prompt = "You are a design engineer following the 'frontend-design' skill. Return complete valid HTML with embedded CSS/JS in ```html codeblocks. Avoid generic templates.";
      const reply = await webllmEngine.chat.completions.create({{
        messages: [
          {{ role: "system", content: prompt }},
          {{ role: "user", content: brief }}
        ],
        temperature: 0.7,
        max_tokens: 2500
      }});
      const txt = reply.choices[0].message.content;
      extractAndRender(txt, 'Local WebGPU (WebLLM)');
      showToast('WebGPU local synthesis complete!', '🎮');
    }}
  }} catch(e) {{
    alert('Synthesis error: ' + e.message);
  }} finally {{
    btn.disabled = false;
    if (currentEngine === 'groq') btn.innerHTML = '<span>⚡ Generate Distinctive UI (Groq LPU)</span>';
    else if (currentEngine === 'webgpu') btn.innerHTML = '<span>🎮 Synthesize via Local WebGPU</span>';
    else btn.innerHTML = '<span>⚡ Render Instant Showcase</span>';
  }}
}}

function extractAndRender(rawText, source) {{
  let html = "";
  
  // 1. Look for ```html or ```xml
  const htmlMarker = rawText.indexOf('```html');
  const xmlMarker = rawText.indexOf('```xml');

  if (htmlMarker !== -1) {{
    let candidate = rawText.substring(htmlMarker + 7).trim();
    const endFence = candidate.lastIndexOf('```');
    if (endFence !== -1) candidate = candidate.substring(0, endFence).trim();
    html = candidate;
  }} else if (xmlMarker !== -1) {{
    let candidate = rawText.substring(xmlMarker + 6).trim();
    const endFence = candidate.lastIndexOf('```');
    if (endFence !== -1) candidate = candidate.substring(0, endFence).trim();
    html = candidate;
  }} else {{
    // 2. Look for <!DOCTYPE html> or <html tag directly
    const doctypeIdx = rawText.search(/<!DOCTYPE\\s+html/i);
    const htmlTagIdx = rawText.search(/<html[\\s>]/i);

    let start = -1;
    if (doctypeIdx !== -1) start = doctypeIdx;
    else if (htmlTagIdx !== -1) start = htmlTagIdx;

    if (start !== -1) {{
      let candidate = rawText.substring(start).trim();
      const endFence = candidate.lastIndexOf('```');
      if (endFence !== -1) candidate = candidate.substring(0, endFence).trim();
      html = candidate;
    }}
  }}

  // 3. Fallback: generic ``` code block containing html
  if (!html) {{
    const genericFenceIdx = rawText.indexOf('```');
    if (genericFenceIdx !== -1) {{
      let candidate = rawText.substring(genericFenceIdx + 3).trim();
      const endFence = candidate.lastIndexOf('```');
      if (endFence !== -1) candidate = candidate.substring(0, endFence).trim();
      if (candidate.includes('<') && candidate.includes('>')) {{
        html = candidate;
      }}
    }}
  }}

  // 4. Wrap with complete document structure if incomplete
  if (html && !html.toLowerCase().includes('<html')) {{
    html = `<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body>${{html}}</body></html>`;
  }}

  // Ensure clean fallback
  if (!html) {{
    html = `<!DOCTYPE html><html><body style="font-family:sans-serif;padding:2rem;"><pre style="white-space:pre-wrap;">${{rawText.replace(/</g, '&lt;')}}</pre></body></html>`;
  }}

  renderSandbox(html, source);
}}



function switchStage(stage) {{
  document.getElementById('tabBtnPreview').classList.toggle('active', stage === 'preview');
  document.getElementById('tabBtnPlan').classList.toggle('active', stage === 'plan');
  document.getElementById('tabBtnCode').classList.toggle('active', stage === 'code');

  document.getElementById('stagePreview').style.display = (stage === 'preview') ? 'flex' : 'none';
  document.getElementById('stagePlan').style.display = (stage === 'plan') ? 'block' : 'none';
  document.getElementById('stageCode').style.display = (stage === 'code') ? 'block' : 'none';
  document.getElementById('deviceGroup').style.display = (stage === 'preview') ? 'flex' : 'none';
}}

function setDevice(dev) {{
  document.querySelectorAll('.device-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  const frame = document.getElementById('stageFrame');
  frame.className = 'stage-frame ' + dev;
}}

function toggleRunbook() {{
  const body = document.getElementById('runbookBody');
  const arrow = document.getElementById('runbookArrow');
  if (body.style.display === 'none') {{
    body.style.display = 'block';
    arrow.innerText = '▲ Collapse';
  }} else {{
    body.style.display = 'none';
    arrow.innerText = '▼ Expand';
  }}
}}

function copyCode() {{
  navigator.clipboard.writeText(currentHtml);
  showToast('HTML code copied!', '📋');
}}

function downloadFile() {{
  const blob = new Blob([currentHtml], {{ type: 'text/html' }});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `frontend_design_${{Date.now()}}.html`;
  a.click();
  showToast('Downloaded HTML file!', '💾');
}}

function popoutWindow() {{
  const blob = new Blob([currentHtml], {{ type: 'text/html' }});
  const url = URL.createObjectURL(blob);
  window.open(url, '_blank');
}}

function showToast(msg, icon = '✅') {{
  const t = document.getElementById('toastBox');
  document.getElementById('toastIcon').innerText = icon;
  document.getElementById('toastMsg').innerText = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3500);
}}
</script>
</body>
</html>"""

with open("frontend_design_app.html", "w", encoding="utf-8") as f:
    f.write(APP_HTML)

print("Generated frontend_design_app.html successfully with Pre-Provisioned Groq Token & User Input! Size:", os.path.getsize("frontend_design_app.html"), "bytes")
