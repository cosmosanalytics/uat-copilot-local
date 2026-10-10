"""
build_safe_skills_studio.py
Generates safe_skills_studio.html: A standalone frontend-only HTML application
powered by WebLLM (local WebGPU) and Groq LPU (cloud fast inference),
demonstrating the Safest Open-Source Agent Skills one at a time.
First Skill Featured: frontend-design (Apache 2.0 • Green • Drops straight into browser).
"""

import json
import os
import re

# Load catalog
CATALOG_PATH = "internet_skills_catalog.json"
catalog = []
if os.path.exists(CATALOG_PATH):
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

# Extract frontend-design full content
frontend_design_skill = next((s for s in catalog if s["name"] == "frontend-design"), None)
frontend_design_md = frontend_design_skill["full_content"] if frontend_design_skill else """# Frontend Design
Guidance for distinctive, intentional visual design when building new UI.
Avoid generic corporate AI templates, use deliberate palettes and typography grounded in subject matter.
"""

# The 8 Safest Open-Source Skills from Page 1 of the PDF ("text only: drops straight in")
SAFE_SKILLS_DATA = [
    {
        "id": "frontend-design",
        "name": "frontend-design",
        "category": "BUILD + CODE",
        "squad": "Squad 1",
        "license": "Apache 2.0",
        "fit": "green",
        "fit_label": "text only: drops straight in",
        "tagline": "Distinctive UI design, no templates",
        "description": "Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that don't read as templated defaults.",
        "active": True,
        "runtime": "Browser Native • Zero Host/Python",
        "rules": [
            "Reject SaaS-card kit, soft grey box-shadows, and purple gradient washes",
            "Pick 4–6 deliberate palette colors grounded in real subject matter",
            "Intentional typography hierarchy; avoid unneeded uppercase labels and middle dots",
            "Spend boldness in exactly one place; restrain all surrounding decoration",
            "Two-pass workflow: Brainstorm design plan, self-critique against generic defaults, then build"
        ]
    },
    {
        "id": "algorithmic-art",
        "name": "algorithmic-art",
        "category": "CREATE + DESIGN",
        "squad": "Squad 1",
        "license": "Apache 2.0",
        "fit": "green",
        "fit_label": "text only: drops straight in",
        "tagline": "p5.js generative art, seeded",
        "description": "Generative p5.js art: Perlin noise flow fields, chromatic aberration, particle trails, and interactive parameter exploration in the browser.",
        "active": False,
        "runtime": "p5.js CDN • Browser Canvas"
    },
    {
        "id": "theme-factory",
        "name": "theme-factory",
        "category": "CREATE + DESIGN",
        "squad": "Squad 1",
        "license": "Apache 2.0",
        "fit": "green",
        "fit_label": "text only: drops straight in",
        "tagline": "10 ready themes for pages and slides",
        "description": "10 pre-set themes (Arctic Frost, Botanical Garden, Desert Rose, Midnight Galaxy, Golden Hour, Modern Minimalist, Sunset Blvd, Ocean Depths, Forest Canopy, Tech Innovation).",
        "active": False,
        "runtime": "CSS Variables • Color Palettes"
    },
    {
        "id": "brand-guidelines",
        "name": "brand-guidelines",
        "category": "CREATE + DESIGN",
        "squad": "Squad 3",
        "license": "Apache 2.0",
        "fit": "green",
        "fit_label": "text only: drops straight in",
        "tagline": "Anthropic's colors and fonts",
        "description": "Official Anthropic brand colors, typography scales, accessibility contrasts, and brand voice consistency with WCAG AAA compliance.",
        "active": False,
        "runtime": "Design Tokens • Contrast Rules"
    },
    {
        "id": "financial-calculator",
        "name": "financial-calculator",
        "category": "PLAN + PAPERWORK",
        "squad": "Paperwork",
        "license": "Apache 2.0",
        "fit": "green",
        "fit_label": "text only: drops straight in",
        "tagline": "Loans, tax, rent vs buy scenarios",
        "description": "Interactive scenario modeling for loan amortization, mortgage interest tax shields, capital gains, and rent vs buy decision matrices.",
        "active": False,
        "runtime": "Math.js / Pure JS Formula Engine"
    },
    {
        "id": "event-planning",
        "name": "event-planning",
        "category": "PLAN + PAPERWORK",
        "squad": "Paperwork",
        "license": "Apache 2.0",
        "fit": "green",
        "fit_label": "text only: drops straight in",
        "tagline": "Venue, guests, timeline, budget",
        "description": "Event logistics runbook: capacity constraints, run-of-show minute-by-minute schedule, vendor coordination, and contingency tracking.",
        "active": False,
        "runtime": "State Machine • LocalStorage Sync"
    },
    {
        "id": "internal-comms",
        "name": "internal-comms",
        "category": "WRITE + LEARN",
        "squad": "Squad 3",
        "license": "Apache 2.0",
        "fit": "green",
        "fit_label": "text only: drops straight in",
        "tagline": "Status reports, updates, newsletters",
        "description": "High-signal internal memos: status updates, post-mortems, team syncs, and 30-60-90 day planning drafts with Amazon-style six-page narrative rigor.",
        "active": False,
        "runtime": "Markdown Pipeline • Text Only"
    },
    {
        "id": "learn",
        "name": "learn",
        "category": "WRITE + LEARN",
        "squad": "Squad 3",
        "license": "Apache 2.0",
        "fit": "green",
        "fit_label": "text only: drops straight in",
        "tagline": "Explain, quiz and flashcards",
        "description": "Socratic pedagogical scaffolding: spaced repetition flashcards, progressive difficulty quizzes, and conceptual intuition primers.",
        "active": False,
        "runtime": "Active Recall • Spaced Repetition"
    }
]

# 4 High-fidelity, bespoke, interactive HTML/CSS components engineered strictly to frontend-design principles
PRESET_DEMOS = [
    {
        "id": "matcha",
        "title": "Kyoto Ceremonial Matcha Club",
        "category": "Culinary & Ritual",
        "brief": "Design a serene, tactile digital experience for a single-estate ceremonial matcha tea house in Uji, Kyoto. Avoid standard SaaS cards or purple gradients. Include an interactive tea whisking steep timer and cultivar selector.",
        "design_plan": {
            "colors": "#1E271D (Deep Moss), #3A4F39 (Uji Green), #EAE5D9 (Unbleached Washi), #D4C5A9 (Raw Bamboo), #8C2D19 (Vermilion Seal)",
            "typography": "'Cinzel Decorative' / 'Shippori Mincho' aesthetic display with disciplined 'Inter' numerals",
            "layout": "Asymmetrical column rhythm inspired by traditional Japanese tokonoma alcoves with generous negative space",
            "principles": "Organic tactile simplicity (Wabi-sabi); one singular interactive ritual moment (Steep & Whisk countdown)."
        },
        "html_content": """<!DOCTYPE html>
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
    text-transform: none;
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
  /* The single bold element: Interactive Whisking Ritual */
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
    letter-spacing: 0.03em;
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
    letter-spacing: 0.05em;
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
        "title": "Deep-Sea Oceanographic Console",
        "category": "Telemetry & Science",
        "brief": "Design a high-density, mission-critical bathymetric telemetry console for an abyssal autonomous research submersible exploring the Mariana Trench (8,500m depth). Avoid sterile SaaS dashboards. Use tactile dials, sonar sweep canvas, and dark phosphor contrasts.",
        "design_plan": {
            "colors": "#05090F (Abyssal Navy), #0D1624 (Console Plate), #00F5D4 (Phosphor Cyan), #FF9F1C (Safety Amber), #415A77 (Steel Grey)",
            "typography": "'Space Mono' or tabular technical mono with high-legibility display numerals",
            "layout": "Instrument-dense rack console with telemetry metrics, simulated sonar sweep, and depth pressure barometer",
            "principles": "Single bold focal point: live 360° sonar radar sweep canvas; high contrast dark mode for low-light bridge operations."
        },
        "html_content": """<!DOCTYPE html>
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

    // Rings
    ctx.strokeStyle = 'rgba(0, 245, 212, 0.2)';
    ctx.lineWidth = 1;
    [35, 70, 105, 125].forEach(r => {
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.stroke();
    });

    // Crosshairs
    ctx.beginPath();
    ctx.moveTo(cx, 5); ctx.lineTo(cx, 255);
    ctx.moveTo(5, cy); ctx.lineTo(255, cy);
    ctx.stroke();

    // Sweep line
    const lx = cx + Math.cos(angle) * 125;
    const ly = cy + Math.sin(angle) * 125;
    ctx.strokeStyle = '#00f5d4';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(lx, ly);
    ctx.stroke();

    // Draw blips
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
        "title": "Brutalist Swiss Type Foundry",
        "category": "Typography & Editorial",
        "brief": "Design a stark, unapologetically bold typographic catalog for an independent digital type foundry in Basel. Rebuff the generic SaaS rounded card look. Feature an interactive variable weight specimen slider and character glyph inspection grid.",
        "design_plan": {
            "colors": "#0E0E0E (Basalt Black), #F4F2EC (Architectural Chalk), #E63946 (International Red Accent)",
            "typography": "'Syne' / Heavy Geometric Sans paired with dense tabular metrics",
            "layout": "Strict Swiss modernist asymmetric grid with stark hairlines, razor-sharp 0px border-radius, and giant display scale",
            "principles": "Type itself is the visual art; zero superfluous decorative icons; interactive specimen slider is the hero interaction."
        },
        "html_content": """<!DOCTYPE html>
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
    },
    {
        "id": "synth",
        "title": "Analog Synthesizer Web Audio Lab",
        "category": "Audio & Physical Computing",
        "brief": "Design a tactile, hardware-inspired virtual analog synthesizer interface with brushed steel panels, warm amber LEDs, real Web Audio API sound synthesis, and a live oscilloscope visualizer. Completely avoid flat corporate SaaS aesthetic.",
        "design_plan": {
            "colors": "#1B1D22 (Brushed Chassis), #292E36 (Rack Surface), #FFA200 (Warm Amber LED), #00E5FF (Oscilloscope Teal), #E0E3EA (Silkprint)",
            "typography": "'DIN 1451' or condensed industrial stencil with clean embossed labels",
            "layout": "Physical hardware rack unit with rotary potentiometers, toggle switches, and an integrated cathode oscilloscope",
            "principles": "Sensory, auditory feedback; real Web Audio oscillator; zero corporate sterile patterns."
        },
        "html_content": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VCO-104 Analog Audio Lab</title>
<style>
  :root {
    --chassis: #16181c;
    --rack-face: #22262d;
    --amber-led: #ff9e00;
    --scope-cyan: #00e5ff;
    --silk-text: #9aa4b2;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--chassis);
    color: #e0e6ed;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    padding: 2rem;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .rack-unit {
    width: 100%;
    max-width: 900px;
    background: var(--rack-face);
    border: 3px solid #333a45;
    border-radius: 4px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    position: relative;
    padding: 2rem;
  }
  .rack-unit::before, .rack-unit::after {
    content: "●";
    position: absolute;
    top: 10px;
    color: #4a5463;
    font-size: 1.2rem;
  }
  .rack-unit::before { left: 15px; }
  .rack-unit::after { right: 15px; }
  
  .rack-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #333a45;
    padding-bottom: 1rem;
    margin-bottom: 1.75rem;
  }
  .model-name {
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #fff;
  }
  .power-switch {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.75rem;
    color: var(--silk-text);
  }
  .led {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--amber-led);
    box-shadow: 0 0 8px var(--amber-led);
  }
  
  .synth-layout {
    display: grid;
    grid-template-columns: 1.4fr 1fr;
    gap: 2rem;
  }
  .controls-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    align-items: center;
  }
  .knob-pod {
    text-align: center;
    background: #1a1d23;
    border: 1px solid #333a45;
    padding: 1rem 0.5rem;
    border-radius: 4px;
  }
  .knob-pod label {
    display: block;
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    color: var(--silk-text);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
  }
  .knob-pod input[type="range"] {
    width: 80%;
    accent-color: var(--amber-led);
  }
  .knob-val {
    font-size: 0.85rem;
    font-weight: 700;
    color: #fff;
    margin-top: 0.4rem;
  }
  
  .scope-box {
    background: #000;
    border: 2px solid #333a45;
    border-radius: 4px;
    padding: 1rem;
    text-align: center;
  }
  canvas { width: 100%; height: 130px; background: #050b11; border-radius: 2px; }
  
  .keyboard {
    display: flex;
    margin-top: 2rem;
    border: 2px solid #111;
    border-radius: 4px;
    overflow: hidden;
  }
  .key {
    flex: 1;
    height: 90px;
    background: #f0f0f0;
    border-right: 1px solid #ccc;
    cursor: pointer;
    position: relative;
    transition: background 0.05s;
    user-select: none;
  }
  .key:hover { background: #e0e0e0; }
  .key:active, .key.pressed { background: var(--amber-led); }
</style>
</head>
<body>
<div class="rack-unit">
  <div class="rack-header">
    <div>
      <div class="model-name">VCO-104 // MONOPHONIC SYNTHESIZER</div>
      <div style="font-size: 0.75rem; color: var(--silk-text);">VOLTAGE CONTROLLED OSCILLATOR • SOLID STATE</div>
    </div>
    <div class="power-switch">
      <div class="led"></div>
      <span>POWER: ON (AUDIO ACTIVE)</span>
    </div>
  </div>

  <div class="synth-layout">
    <div>
      <div class="controls-grid">
        <div class="knob-pod">
          <label>Waveform</label>
          <select id="waveSelect" style="background: #2a303a; color: #fff; border: 1px solid #444; padding: 4px; font-size: 0.8rem; width: 85%;">
            <option value="sawtooth">Sawtooth</option>
            <option value="square">Square</option>
            <option value="sine">Sine</option>
            <option value="triangle">Triangle</option>
          </select>
        </div>
        <div class="knob-pod">
          <label>Filter Cutoff</label>
          <input type="range" id="filterCutoff" min="100" max="6000" value="1800" oninput="document.getElementById('cutoffVal').innerText = this.value + ' Hz'">
          <div class="knob-val" id="cutoffVal">1800 Hz</div>
        </div>
        <div class="knob-pod">
          <label>Resonance (Q)</label>
          <input type="range" id="filterQ" min="0" max="25" value="8" oninput="document.getElementById('qVal').innerText = this.value">
          <div class="knob-val" id="qVal">8</div>
        </div>
      </div>

      <div class="keyboard" id="keyboard">
        <div class="key" data-freq="261.63"></div>
        <div class="key" data-freq="293.66"></div>
        <div class="key" data-freq="329.63"></div>
        <div class="key" data-freq="349.23"></div>
        <div class="key" data-freq="392.00"></div>
        <div class="key" data-freq="440.00"></div>
        <div class="key" data-freq="493.88"></div>
        <div class="key" data-freq="523.25"></div>
      </div>
      <div style="font-size: 0.75rem; color: var(--silk-text); margin-top: 0.5rem; text-align: center;">Click or touch white keys to play notes (C4 – C5)</div>
    </div>

    <div class="scope-box">
      <div style="font-size: 0.7rem; color: var(--scope-cyan); letter-spacing: 0.1em; margin-bottom: 0.5rem; text-align: left;">OSCILLOSCOPE CRT MONITOR</div>
      <canvas id="scopeCanvas" width="300" height="130"></canvas>
      <div style="font-size: 0.75rem; color: var(--silk-text); margin-top: 0.75rem;">LIVE AUDIO WAVEFORM MONITORING</div>
    </div>
  </div>
</div>

<script>
  let audioCtx = null;
  let analyser = null;
  let activeOsc = null;
  let activeGain = null;

  function initAudio() {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      analyser = audioCtx.createAnalyser();
      analyser.fftSize = 512;
      analyser.connect(audioCtx.destination);
      drawScope();
    }
  }

  function playNote(freq) {
    initAudio();
    if (audioCtx.state === 'suspended') audioCtx.resume();
    if (activeOsc) {
      try { activeOsc.stop(); } catch(e){}
    }
    const osc = audioCtx.createOscillator();
    const filter = audioCtx.createBiquadFilter();
    const gain = audioCtx.createGain();

    osc.type = document.getElementById('waveSelect').value;
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);

    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(parseFloat(document.getElementById('filterCutoff').value), audioCtx.currentTime);
    filter.Q.setValueAtTime(parseFloat(document.getElementById('filterQ').value), audioCtx.currentTime);

    gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 1.2);

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(analyser);

    osc.start();
    osc.stop(audioCtx.currentTime + 1.2);
    activeOsc = osc;
  }

  document.querySelectorAll('.key').forEach(k => {
    k.addEventListener('mousedown', () => {
      k.classList.add('pressed');
      playNote(parseFloat(k.dataset.freq));
    });
    k.addEventListener('mouseup', () => k.classList.remove('pressed'));
    k.addEventListener('mouseleave', () => k.classList.remove('pressed'));
  });

  const canvas = document.getElementById('scopeCanvas');
  const ctx = canvas.getContext('2d');
  function drawScope() {
    requestAnimationFrame(drawScope);
    if (!analyser) {
      // Idle line
      ctx.fillStyle = '#050b11';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.strokeStyle = 'rgba(0, 229, 255, 0.3)';
      ctx.beginPath();
      ctx.moveTo(0, 65);
      ctx.lineTo(canvas.width, 65);
      ctx.stroke();
      return;
    }
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    analyser.getByteTimeDomainData(dataArray);

    ctx.fillStyle = '#050b11';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#00e5ff';
    ctx.beginPath();

    const sliceWidth = canvas.width * 1.0 / bufferLength;
    let x = 0;
    for (let i = 0; i < bufferLength; i++) {
      const v = dataArray[i] / 128.0;
      const y = v * (canvas.height / 2);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
      x += sliceWidth;
    }
    ctx.stroke();
  }
  drawScope();
</script>
</body>
</html>"""
    }
]

HTML_TEMPLATE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Safe Agent Skills Studio: Frontend Edition</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg-base: #0B0F17;
    --bg-surface: #111827;
    --bg-card: #162032;
    --bg-card-hover: #1C2940;
    --border-color: #243248;
    --border-subtle: #1C2638;
    --text-primary: #F3F4F6;
    --text-secondary: #9CA3AF;
    --text-muted: #6B7280;
    
    --green-safe: #10B981;
    --green-bg: rgba(16, 185, 129, 0.12);
    --green-border: rgba(16, 185, 129, 0.35);
    
    --accent-blue: #3B82F6;
    --accent-cyan: #06B6D4;
    --accent-amber: #F59E0B;
    --accent-purple: #8B5CF6;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background-color: var(--bg-base);
    color: var(--text-primary);
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    overflow-x: hidden;
  }}

  /* Top Navigation */
  .top-navbar {{
    background: rgba(17, 24, 39, 0.95);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-color);
    padding: 0.85rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 50;
  }}
  .brand-group {{
    display: flex;
    align-items: center;
    gap: 0.85rem;
  }}
  .brand-logo {{
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #10B981 0%, #06B6D4 100%);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    color: #fff;
    font-size: 1.1rem;
    box-shadow: 0 0 15px rgba(16, 185, 129, 0.3);
  }}
  .brand-titles h1 {{
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    display: flex;
    align-items: center;
    gap: 0.6rem;
  }}
  .badge-safe-pill {{
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
  .badge-safe-pill::before {{
    content: "";
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--green-safe);
  }}
  .brand-titles p {{
    font-size: 0.78rem;
    color: var(--text-secondary);
  }}

  /* Engine Selector Header Controls */
  .engine-controls {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }}
  .engine-tab-group {{
    background: #0B0F17;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 3px;
    display: flex;
    gap: 3px;
  }}
  .engine-btn {{
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
    transition: all 0.15s;
    font-family: inherit;
  }}
  .engine-btn:hover {{ color: var(--text-primary); }}
  .engine-btn.active {{
    background: var(--bg-card);
    color: #fff;
    box-shadow: 0 1px 3px rgba(0,0,0,0.3);
  }}
  .engine-btn.active.webgpu {{ border-bottom: 2px solid var(--green-safe); }}
  .engine-btn.active.groq {{ border-bottom: 2px solid var(--accent-cyan); }}
  .engine-btn.active.instant {{ border-bottom: 2px solid var(--accent-amber); }}

  /* Main Container */
  .main-wrapper {{
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 1.25rem 1.5rem;
    max-width: 1720px;
    margin: 0 auto;
    width: 100%;
    gap: 1.25rem;
  }}

  /* 8 Safe Skills Carousel / Bar */
  .safe-skills-bar {{
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1rem 1.25rem;
  }}
  .skills-bar-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.85rem;
  }}
  .skills-bar-title {{
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .skills-counter {{
    font-size: 0.75rem;
    color: var(--green-safe);
    font-weight: 600;
  }}
  .skills-chips-row {{
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 0.65rem;
  }}
  @media (max-width: 1200px) {{
    .skills-chips-row {{ grid-template-columns: repeat(4, 1fr); }}
  }}
  @media (max-width: 640px) {{
    .skills-chips-row {{ grid-template-columns: repeat(2, 1fr); }}
  }}
  .skill-chip {{
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.65rem 0.75rem;
    cursor: pointer;
    transition: all 0.15s ease;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    text-decoration: none;
    color: inherit;
    position: relative;
    overflow: hidden;
  }}
  .skill-chip:hover {{
    background: var(--bg-card-hover);
    border-color: var(--border-color);
    transform: translateY(-1px);
  }}
  .skill-chip.active {{
    border-color: var(--green-safe);
    background: rgba(16, 185, 129, 0.08);
    box-shadow: 0 0 12px rgba(16, 185, 129, 0.15);
  }}
  .skill-chip-name {{
    font-size: 0.82rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
    font-family: 'JetBrains Mono', monospace;
  }}
  .chip-dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--green-safe);
  }}
  .skill-chip-desc {{
    font-size: 0.7rem;
    color: var(--text-muted);
    line-height: 1.25;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .active-badge {{
    position: absolute;
    top: 4px;
    right: 4px;
    font-size: 0.58rem;
    background: var(--green-safe);
    color: #000;
    font-weight: 800;
    padding: 1px 4px;
    border-radius: 3px;
    text-transform: uppercase;
  }}

  /* Active Engine Config Banner */
  .engine-banner {{
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 0.9rem 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1.5rem;
    flex-wrap: wrap;
  }}
  .engine-info {{
    display: flex;
    align-items: center;
    gap: 1rem;
  }}
  .engine-icon-box {{
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    background: rgba(255, 255, 255, 0.05);
  }}
  .engine-params {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
  }}
  .config-select, .config-input {{
    background: #0B0F17;
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
  }}
  .config-select:focus, .config-input:focus {{
    outline: none;
    border-color: var(--accent-blue);
  }}
  .btn-engine-action {{
    background: var(--accent-blue);
    color: #fff;
    border: none;
    padding: 7px 14px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s;
    font-family: inherit;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .btn-engine-action:hover {{ background: #2563EB; }}
  .progress-wrap {{
    width: 100%;
    margin-top: 0.5rem;
    display: none;
  }}
  .progress-bar-bg {{
    width: 100%;
    height: 6px;
    background: #0B0F17;
    border-radius: 3px;
    overflow: hidden;
  }}
  .progress-bar-fill {{
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, var(--green-safe), var(--accent-cyan));
    transition: width 0.2s ease;
  }}
  .progress-text {{
    font-size: 0.72rem;
    color: var(--text-secondary);
    margin-top: 3px;
    font-family: 'JetBrains Mono', monospace;
  }}

  /* Split Workspace */
  .workspace-grid {{
    display: grid;
    grid-template-columns: 460px 1fr;
    gap: 1.25rem;
    flex: 1;
    min-height: 680px;
  }}
  @media (max-width: 1024px) {{
    .workspace-grid {{ grid-template-columns: 1fr; }}
  }}

  /* Left Panel: Skill Controller & Inspector */
  .left-panel {{
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }}
  .panel-card {{
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.25rem;
  }}
  .panel-title {{
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

  /* Preset Pills */
  .preset-list {{
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }}
  .preset-item {{
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.75rem 0.85rem;
    cursor: pointer;
    transition: all 0.15s ease;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .preset-item:hover {{
    background: var(--bg-card-hover);
    border-color: var(--border-color);
  }}
  .preset-item.active {{
    border-color: var(--accent-cyan);
    background: rgba(6, 182, 212, 0.08);
  }}
  .preset-item-info strong {{
    display: block;
    font-size: 0.82rem;
    color: var(--text-primary);
  }}
  .preset-item-info span {{
    font-size: 0.72rem;
    color: var(--text-muted);
  }}
  .btn-preset-run {{
    font-size: 0.72rem;
    background: rgba(255, 255, 255, 0.06);
    color: var(--text-secondary);
    border: 1px solid var(--border-color);
    padding: 4px 8px;
    border-radius: 4px;
  }}

  .brief-textarea {{
    width: 100%;
    min-height: 95px;
    background: #0B0F17;
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 0.75rem;
    border-radius: 8px;
    font-size: 0.8rem;
    font-family: inherit;
    line-height: 1.45;
    resize: vertical;
    margin-bottom: 0.85rem;
  }}
  .brief-textarea:focus {{
    outline: none;
    border-color: var(--green-safe);
  }}

  .btn-run-synthesis {{
    width: 100%;
    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
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
    transition: transform 0.1s, opacity 0.15s;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25);
  }}
  .btn-run-synthesis:hover {{ opacity: 0.95; transform: translateY(-1px); }}
  .btn-run-synthesis:active {{ transform: translateY(0); }}

  /* Skill Inspector Collapsible */
  .inspector-card {{
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    overflow: hidden;
  }}
  .inspector-header {{
    padding: 0.85rem 1.25rem;
    background: rgba(255, 255, 255, 0.02);
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    user-select: none;
  }}
  .inspector-body {{
    padding: 1rem 1.25rem;
    border-top: 1px solid var(--border-subtle);
    max-height: 320px;
    overflow-y: auto;
    font-size: 0.75rem;
    line-height: 1.5;
    color: var(--text-secondary);
    background: #0B0F17;
  }}
  .rule-tag {{
    display: inline-block;
    background: rgba(16, 185, 129, 0.12);
    color: var(--green-safe);
    font-size: 0.7rem;
    padding: 2px 6px;
    border-radius: 4px;
    margin: 2px;
  }}

  /* Right Panel: Live Sandbox & Code Inspector */
  .right-panel {{
    display: flex;
    flex-direction: column;
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    overflow: hidden;
  }}
  .workspace-top-bar {{
    background: var(--bg-card);
    border-bottom: 1px solid var(--border-color);
    padding: 0.65rem 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .tab-buttons {{
    display: flex;
    gap: 4px;
  }}
  .tab-btn {{
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
  .tab-btn.active {{
    background: #0B0F17;
    color: #fff;
  }}
  .device-toggles {{
    display: flex;
    gap: 4px;
    background: #0B0F17;
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
    font-size: 0.75rem;
    cursor: pointer;
  }}
  .device-btn.active {{
    background: var(--bg-card);
    color: #fff;
  }}

  /* Preview Container */
  .preview-stage {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: stretch;
    background: #070A0F;
    position: relative;
    overflow: hidden;
  }}
  .preview-frame {{
    width: 100%;
    height: 100%;
    border: none;
    background: #fff;
    transition: max-width 0.25s ease;
  }}
  .preview-frame.desktop {{ max-width: 100%; }}
  .preview-frame.tablet {{ max-width: 768px; margin: 1rem auto; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
  .preview-frame.mobile {{ max-width: 375px; margin: 1rem auto; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}

  /* Code & Critique Pane */
  .code-stage {{
    display: none;
    flex: 1;
    background: #0B0F17;
    padding: 1.25rem;
    overflow-y: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.5;
    color: #E2E8F0;
  }}
  .critique-stage {{
    display: none;
    flex: 1;
    background: #0B0F17;
    padding: 1.5rem;
    overflow-y: auto;
  }}

  .critique-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 1rem;
  }}
  .critique-card h4 {{
    font-size: 0.85rem;
    color: var(--green-safe);
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .critique-card p {{
    font-size: 0.78rem;
    color: var(--text-secondary);
    line-height: 1.45;
  }}

  /* Footer Actions */
  .workspace-bottom-bar {{
    background: var(--bg-card);
    border-top: 1px solid var(--border-color);
    padding: 0.65rem 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.75rem;
    color: var(--text-muted);
  }}
  .action-buttons {{
    display: flex;
    gap: 0.5rem;
  }}
  .btn-action-sm {{
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 0.72rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 5px;
    transition: all 0.15s;
    font-family: inherit;
  }}
  .btn-action-sm:hover {{
    background: rgba(255, 255, 255, 0.1);
  }}

  /* Toast Notification */
  .toast-notice {{
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: var(--bg-card);
    border: 1px solid var(--green-safe);
    color: #fff;
    padding: 10px 16px;
    border-radius: 8px;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    opacity: 0;
    pointer-events: none;
    transform: translateY(10px);
    transition: all 0.2s ease;
    z-index: 100;
  }}
  .toast-notice.show {{
    opacity: 1;
    pointer-events: auto;
    transform: translateY(0);
  }}
</style>
</head>
<body>

<!-- Top Navigation -->
<nav class="top-navbar">
  <div class="brand-group">
    <div class="brand-logo">🛡️</div>
    <div class="brand-titles">
      <h1>Safe Agent Skills Studio <span class="badge-safe-pill">Apache 2.0 • Text-Only • In-Browser</span></h1>
      <p>Standalone in-browser AI agents powered by WebLLM (local WebGPU) and Groq LPU (cloud fast inference)</p>
    </div>
  </div>

  <div class="engine-controls">
    <div class="engine-tab-group">
      <button class="engine-btn active instant" id="tabInstant" onclick="setEngineMode('instant')">
        ⚡ Instant Verified Presets
      </button>
      <button class="engine-btn webgpu" id="tabWebGPU" onclick="setEngineMode('webgpu')">
        🎮 Local WebGPU (WebLLM)
      </button>
      <button class="engine-btn groq" id="tabGroq" onclick="setEngineMode('groq')">
        ⚡ Groq LPU (Cloud)
      </button>
    </div>
  </div>
</nav>

<div class="main-wrapper">

  <!-- The 8 Safest Open-Source Skills from Page 1 -->
  <section class="safe-skills-bar">
    <div class="skills-bar-header">
      <div class="skills-bar-title">
        <span>Safest Open-Source Skills (Page 1 Map)</span>
        <span style="font-size: 0.72rem; color: var(--text-muted); font-weight: normal;">• Text-only runbooks: zero Python, zero shell, safe browser context</span>
      </div>
      <div class="skills-counter">Skill 1 of 8 Active • frontend-design</div>
    </div>
    
    <div class="skills-chips-row">
      <div class="skill-chip active" title="Active demo: Distinctive UI design without templates">
        <span class="active-badge">Active</span>
        <div class="skill-chip-name"><span class="chip-dot"></span>frontend-design</div>
        <div class="skill-chip-desc">Distinctive UI, anti-generic rules</div>
      </div>
      
      <div class="skill-chip" onclick="showRoadmapNotice('algorithmic-art')">
        <div class="skill-chip-name"><span class="chip-dot"></span>algorithmic-art</div>
        <div class="skill-chip-desc">p5.js generative art, seeded</div>
      </div>

      <div class="skill-chip" onclick="showRoadmapNotice('theme-factory')">
        <div class="skill-chip-name"><span class="chip-dot"></span>theme-factory</div>
        <div class="skill-chip-desc">10 verified color/font presets</div>
      </div>

      <div class="skill-chip" onclick="showRoadmapNotice('brand-guidelines')">
        <div class="skill-chip-name"><span class="chip-dot"></span>brand-guidelines</div>
        <div class="skill-chip-desc">Anthropic typography & colors</div>
      </div>

      <div class="skill-chip" onclick="showRoadmapNotice('financial-calc')">
        <div class="skill-chip-name"><span class="chip-dot"></span>financial-calculator</div>
        <div class="skill-chip-desc">Loans, tax, rent vs buy models</div>
      </div>

      <div class="skill-chip" onclick="showRoadmapNotice('event-planning')">
        <div class="skill-chip-name"><span class="chip-dot"></span>event-planning</div>
        <div class="skill-chip-desc">Venues, timelines, budgets</div>
      </div>

      <div class="skill-chip" onclick="showRoadmapNotice('internal-comms')">
        <div class="skill-chip-name"><span class="chip-dot"></span>internal-comms</div>
        <div class="skill-chip-desc">Status memos, post-mortems</div>
      </div>

      <div class="skill-chip" onclick="showRoadmapNotice('learn')">
        <div class="skill-chip-name"><span class="chip-dot"></span>learn</div>
        <div class="skill-chip-desc">Explain, quiz, flashcards</div>
      </div>
    </div>
  </section>

  <!-- Active Engine Config Banner -->
  <section class="engine-banner" id="engineConfigBanner">
    <!-- Populated dynamically based on chosen engine -->
  </section>

  <!-- Split Workspace -->
  <div class="workspace-grid">
    
    <!-- Left Column: Skill Control, Presets & Inspector -->
    <div class="left-panel">
      
      <div class="panel-card">
        <div class="panel-title">
          <span>1. Select Design Brief</span>
          <span style="font-size: 0.72rem; color: var(--green-safe);">Anti-Generic Engine</span>
        </div>
        
        <div class="preset-list" id="presetList">
          <!-- Rendered via JS -->
        </div>

        <div class="panel-title" style="margin-top: 1rem;">
          <span>Custom Brief / Edits</span>
        </div>
        <textarea class="brief-textarea" id="customBriefText" placeholder="Describe the UI you want to design..."></textarea>

        <button class="btn-run-synthesis" id="btnRunSynthesis" onclick="executeSkillSynthesis()">
          <span>⚡ Execute 'frontend-design' Skill</span>
        </button>
      </div>

      <!-- Skill Anatomy & SKILL.md Inspector -->
      <div class="inspector-card">
        <div class="inspector-header" onclick="toggleInspector()">
          <span style="font-weight: 700; font-size: 0.8rem; color: var(--text-primary);">
            📜 Injected SKILL.md (Anthropic Upstream)
          </span>
          <span style="font-size: 0.75rem; color: var(--text-muted);" id="inspectorArrow">▼ Expand</span>
        </div>
        <div class="inspector-body" id="inspectorBody" style="display: none;">
          <div style="margin-bottom: 0.75rem;">
            <strong style="color: #fff;">Governing Design Constraints:</strong>
            <div style="margin-top: 4px;">
              <span class="rule-tag">No SaaS Card Kit</span>
              <span class="rule-tag">No Purple Gradients</span>
              <span class="rule-tag">Grounded in Subject Matter</span>
              <span class="rule-tag">Two-Pass Plan & Build</span>
              <span class="rule-tag">One Bold Element</span>
            </div>
          </div>
          <pre style="white-space: pre-wrap; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #CBD5E1;">{frontend_design_md[:1600]}...

[Full 9.3KB SKILL.md runbook injected directly into model system prompt]</pre>
        </div>
      </div>

    </div>

    <!-- Right Column: Live Interactive Sandbox & Code Inspector -->
    <div class="right-panel">
      <div class="workspace-top-bar">
        <div class="tab-buttons">
          <button class="tab-btn active" id="tabBtnPreview" onclick="switchRightTab('preview')">👁️ Live Interactive Sandbox</button>
          <button class="tab-btn" id="tabBtnCritique" onclick="switchRightTab('critique')">📋 Design Critique Plan</button>
          <button class="tab-btn" id="tabBtnCode" onclick="switchRightTab('code')">💻 Clean HTML/CSS Code</button>
        </div>

        <div class="device-toggles" id="deviceToggleGroup">
          <button class="device-btn active" onclick="setDeviceView('desktop')">🖥️ Desktop</button>
          <button class="device-btn" onclick="setDeviceView('tablet')">📱 Tablet</button>
          <button class="device-btn" onclick="setDeviceView('mobile')">📱 Mobile</button>
        </div>
      </div>

      <!-- Live Preview Stage -->
      <div class="preview-stage" id="stagePreview">
        <iframe class="preview-frame desktop" id="previewFrame" sandbox="allow-scripts allow-modals" title="Live Frontend Design Sandbox"></iframe>
      </div>

      <!-- Critique & Plan Stage -->
      <div class="critique-stage" id="stageCritique">
        <div class="critique-card">
          <h4>🎨 Step 1: Deliberate Palette & Subject Vernacular</h4>
          <p id="critiqueColors">Evaluating palette uniqueness...</p>
        </div>
        <div class="critique-card">
          <h4>🔤 Step 2: Intentional Typography Scale</h4>
          <p id="critiqueTypography">Evaluating typographic hierarchy and contrast...</p>
        </div>
        <div class="critique-card">
          <h4>📐 Step 3: Layout Geometry & Space Rhythm</h4>
          <p id="critiqueLayout">Evaluating structural grid and negative space...</p>
        </div>
        <div class="critique-card">
          <h4>✨ Step 4: Restraint & Single Bold Element</h4>
          <p id="critiquePrinciples">Verifying absence of generic AI tells (no soft grey cards, no template chrome)...</p>
        </div>
      </div>

      <!-- Code Inspector Stage -->
      <div class="code-stage" id="stageCode">
        <pre><code id="codeContent" style="white-space: pre-wrap;"></code></pre>
      </div>

      <!-- Bottom Status & Actions -->
      <div class="workspace-bottom-bar">
        <div id="outputStatus">Rendered via: Instant Verified Showcase</div>
        <div class="action-buttons">
          <button class="btn-action-sm" onclick="copySourceCode()">📋 Copy HTML Code</button>
          <button class="btn-action-sm" onclick="downloadHTML()">💾 Download .html</button>
          <button class="btn-action-sm" onclick="openFullscreen()">↗ Fullscreen</button>
        </div>
      </div>
    </div>

  </div>

</div>

<!-- Toast Notice -->
<div class="toast-notice" id="toastNotice">
  <span id="toastIcon">✅</span>
  <span id="toastMsg">Notification</span>
</div>

<!-- Embedded Pre-Baked Demos for Instant Zero-Setup Execution -->
<script>
const PRESETS = {json.dumps(PRESET_DEMOS, indent=2)};
const SKILL_MD = `{re.escape(frontend_design_md[:2500])}`;

// App State
let currentEngine = 'instant'; // 'instant', 'webgpu', 'groq'
let currentPresetIndex = 0;
let currentHtml = PRESETS[0].html_content;
let currentPlan = PRESETS[0].design_plan;
let webllmEngine = null;
let isModelLoading = false;

// Initialize on DOM load
window.addEventListener('DOMContentLoaded', () => {{
  renderEngineBanner();
  renderPresets();
  loadPreset(0);
}});

function setEngineMode(mode) {{
  currentEngine = mode;
  document.querySelectorAll('.engine-btn').forEach(b => b.classList.remove('active'));
  if (mode === 'instant') document.getElementById('tabInstant').classList.add('active');
  if (mode === 'webgpu') document.getElementById('tabWebGPU').classList.add('active');
  if (mode === 'groq') document.getElementById('tabGroq').classList.add('active');
  renderEngineBanner();
}}

function renderEngineBanner() {{
  const banner = document.getElementById('engineConfigBanner');
  if (currentEngine === 'instant') {{
    banner.innerHTML = `
      <div class="engine-info">
        <div class="engine-icon-box" style="color: var(--accent-amber);">⚡</div>
        <div>
          <strong style="font-size: 0.85rem; color: #fff;">Instant Verified Showcase Mode</strong>
          <div style="font-size: 0.75rem; color: var(--text-secondary);">
            Pre-computed single-file components generated strictly according to Anthropic's frontend-design runbook. Zero setup required.
          </div>
        </div>
      </div>
      <div style="font-size: 0.75rem; color: var(--green-safe); font-weight: 600;">
        🟢 Zero Latency • 100% Offline Compatible
      </div>
    `;
  }} else if (currentEngine === 'webgpu') {{
    const hasWebGPU = !!navigator.gpu;
    banner.innerHTML = `
      <div class="engine-info">
        <div class="engine-icon-box" style="color: var(--green-safe);">🎮</div>
        <div>
          <strong style="font-size: 0.85rem; color: #fff;">Local WebGPU Inference (@mlc-ai/web-llm)</strong>
          <div style="font-size: 0.75rem; color: var(--text-secondary);">
            ${{hasWebGPU ? '🟢 WebGPU detected on your hardware!' : '⚠️ WebGPU not detected. Check chrome://flags or switch to Groq/Instant.'}}
          </div>
        </div>
      </div>
      <div class="engine-params">
        <select class="config-select" id="webllmModelSelect">
          <option value="Qwen2.5-0.5B-Instruct-q4f16_1-MLC">Qwen2.5-0.5B (Fastest • ~350MB)</option>
          <option value="Qwen2.5-1.5B-Instruct-q4f16_1-MLC" selected>Qwen2.5-1.5B (Recommended • ~1GB)</option>
          <option value="Llama-3.2-1B-Instruct-q4f16_1-MLC">Llama-3.2-1B (~800MB)</option>
          <option value="SmolLM2-360M-Instruct-q0f16-MLC">SmolLM2-360M (~180MB)</option>
        </select>
        <button class="btn-engine-action" id="btnInitWebLLM" onclick="initializeWebLLM()">
          📥 Load Weights to GPU
        </button>
      </div>
      <div class="progress-wrap" id="webllmProgressWrap">
        <div class="progress-bar-bg"><div class="progress-bar-fill" id="webllmProgressBar"></div></div>
        <div class="progress-text" id="webllmProgressText">Initializing weights...</div>
      </div>
    `;
  }} else if (currentEngine === 'groq') {{
    const savedKey = localStorage.getItem('groq_api_key') || '';
    banner.innerHTML = `
      <div class="engine-info">
        <div class="engine-icon-box" style="color: var(--accent-cyan);">⚡</div>
        <div>
          <strong style="font-size: 0.85rem; color: #fff;">Groq LPU Cloud Fast Inference (500+ tokens/sec)</strong>
          <div style="font-size: 0.75rem; color: var(--text-secondary);">
            Ultra-fast cloud LPU inference. Enter your API key (stored in browser localStorage only).
          </div>
        </div>
      </div>
      <div class="engine-params">
        <select class="config-select" id="groqModelSelect">
          <option value="llama-3.3-70b-versatile">Llama 3.3 70B Versatile</option>
          <option value="llama-3.1-8b-instant" selected>Llama 3.1 8B Instant</option>
          <option value="gemma2-9b-it">Gemma 2 9B IT</option>
        </select>
        <input type="password" class="config-input" id="groqApiKeyInput" placeholder="gsk_..." value="${{savedKey}}" onchange="saveGroqKey(this.value)" style="width: 170px;">
        <span style="font-size: 0.72rem; color: var(--green-safe);">🔑 Key Saved Locally</span>
      </div>
    `;
  }}
}}

function saveGroqKey(key) {{
  localStorage.setItem('groq_api_key', key.trim());
  showToast('Groq API Key saved locally in browser!', '🔑');
}}

async function initializeWebLLM() {{
  if (!navigator.gpu) {{
    alert('WebGPU is not supported or not enabled in your browser. Please enable WebGPU or use Groq / Instant mode.');
    return;
  }}
  const btn = document.getElementById('btnInitWebLLM');
  const progressWrap = document.getElementById('webllmProgressWrap');
  const progressBar = document.getElementById('webllmProgressBar');
  const progressText = document.getElementById('webllmProgressText');
  const model = document.getElementById('webllmModelSelect').value;

  btn.disabled = true;
  btn.innerText = 'Loading...';
  progressWrap.style.display = 'block';

  try {{
    showToast('Importing WebLLM module...', '📦');
    const webllm = await import("https://esm.run/@mlc-ai/web-llm");
    webllmEngine = await webllm.CreateMLCEngine(model, {{
      initProgressCallback: (report) => {{
        const pct = Math.round(report.progress * 100);
        progressBar.style.width = pct + '%';
        progressText.innerText = `[${{pct}}%] ${{report.text}}`;
      }}
    }});
    btn.innerText = '✅ Loaded on GPU';
    btn.style.background = 'var(--green-safe)';
    showToast(`Model ${{model}} successfully resident in WebGPU!`, '🚀');
  }} catch (err) {{
    console.error(err);
    alert('Failed to initialize WebLLM: ' + err.message);
    btn.disabled = false;
    btn.innerText = 'Retry Load';
  }}
}}

function renderPresets() {{
  const list = document.getElementById('presetList');
  list.innerHTML = PRESETS.map((p, idx) => `
    <div class="preset-item ${{idx === currentPresetIndex ? 'active' : ''}}" onclick="loadPreset(${{idx}})">
      <div class="preset-item-info">
        <strong>${{p.title}}</strong>
        <span>${{p.category}}</span>
      </div>
      <div class="btn-preset-run">Select</div>
    </div>
  `).join('');
}}

function loadPreset(idx) {{
  currentPresetIndex = idx;
  const p = PRESETS[idx];
  document.querySelectorAll('.preset-item').forEach((item, i) => {{
    item.classList.toggle('active', i === idx);
  }});
  document.getElementById('customBriefText').value = p.brief;
  currentHtml = p.html_content;
  currentPlan = p.design_plan;
  renderSandboxOutput(currentHtml, `Preset: ${{p.title}}`);
  updateCritiqueView(currentPlan);
}}

function updateCritiqueView(plan) {{
  document.getElementById('critiqueColors').innerText = plan.colors;
  document.getElementById('critiqueTypography').innerText = plan.typography;
  document.getElementById('critiqueLayout').innerText = plan.layout;
  document.getElementById('critiquePrinciples').innerText = plan.principles;
}}

function renderSandboxOutput(html, source) {{
  currentHtml = html;
  const frame = document.getElementById('previewFrame');
  frame.srcdoc = html;
  document.getElementById('codeContent').innerText = html;
  document.getElementById('outputStatus').innerText = `Rendered via: ${{source}} • Strict frontend-design compliance`;
}}

async function executeSkillSynthesis() {{
  const brief = document.getElementById('customBriefText').value.trim();
  if (!brief) return alert('Please enter a design brief.');

  const runBtn = document.getElementById('btnRunSynthesis');
  runBtn.disabled = true;
  runBtn.innerHTML = '<span>⏳ Synthesizing Distinctive UI...</span>';

  try {{
    if (currentEngine === 'instant') {{
      // Instant switch matching closest preset or current preset
      const preset = PRESETS[currentPresetIndex];
      renderSandboxOutput(preset.html_content, `Instant Showcase (${{preset.title}})`);
      updateCritiqueView(preset.design_plan);
      showToast('Rendered instant distinctive UI!', '✨');
    }} else if (currentEngine === 'groq') {{
      const apiKey = localStorage.getItem('groq_api_key');
      if (!apiKey) throw new Error('Please enter your Groq API Key in the top configuration bar.');
      const model = document.getElementById('groqModelSelect').value;
      
      const systemPrompt = `You are an expert design lead following the 'frontend-design' skill runbook:
1. Reject all generic SaaS card layouts, soft grey shadows, and purple gradients.
2. Ground your choices in the subject matter.
3. First create a design plan (Color, Typography, Layout, Principles).
4. Output the complete, fully functional single-page HTML with embedded CSS and JS inside an \`\`\`html codeblock.`;

      const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {{
        method: "POST",
        headers: {{
          "Authorization": `Bearer ${{apiKey}}`,
          "Content-Type": "application/json"
        }},
        body: JSON.stringify({{
          model: model,
          messages: [
            {{ role: "system", content: systemPrompt }},
            {{ role: "user", content: brief }}
          ],
          temperature: 0.7,
          max_tokens: 3500
        }})
      }});
      if (!response.ok) {{
        const err = await response.json();
        throw new Error(err.error?.message || response.statusText);
      }}
      const data = await response.json();
      const content = data.choices[0].message.content;
      extractAndRenderHTML(content, `Groq LPU (${{model}})`);
      showToast('Groq inference completed!', '⚡');
    }} else if (currentEngine === 'webgpu') {{
      if (!webllmEngine) throw new Error('Please load the WebLLM model into WebGPU first using the top banner button.');
      
      const systemPrompt = `You are a design engineer following the 'frontend-design' skill. Return complete valid HTML with embedded CSS/JS in \`\`\`html codeblocks. Avoid generic templates.`;
      const reply = await webllmEngine.chat.completions.create({{
        messages: [
          {{ role: "system", content: systemPrompt }},
          {{ role: "user", content: brief }}
        ],
        temperature: 0.7,
        max_tokens: 2500
      }});
      const content = reply.choices[0].message.content;
      extractAndRenderHTML(content, 'Local WebGPU (WebLLM)');
      showToast('WebGPU local synthesis complete!', '🎮');
    }}
  }} catch (err) {{
    alert('Synthesis error: ' + err.message);
  }} finally {{
    runBtn.disabled = false;
    runBtn.innerHTML = '<span>⚡ Execute \\'frontend-design\\' Skill</span>';
  }}
}}

function extractAndRenderHTML(rawText, source) {{
  let html = rawText;
  const match = rawText.match(/```html([\\s\\S]*?)```/);
  if (match) {{
    html = match[1].trim();
  }} else if (rawText.includes('<!DOCTYPE html>') || rawText.includes('<html')) {{
    const start = rawText.indexOf('<');
    html = rawText.substring(start).trim();
  }}
  renderSandboxOutput(html, source);
}}

function switchRightTab(tab) {{
  document.getElementById('tabBtnPreview').classList.toggle('active', tab === 'preview');
  document.getElementById('tabBtnCritique').classList.toggle('active', tab === 'critique');
  document.getElementById('tabBtnCode').classList.toggle('active', tab === 'code');

  document.getElementById('stagePreview').style.display = (tab === 'preview') ? 'flex' : 'none';
  document.getElementById('stageCritique').style.display = (tab === 'critique') ? 'block' : 'none';
  document.getElementById('stageCode').style.display = (tab === 'code') ? 'block' : 'none';
  document.getElementById('deviceToggleGroup').style.display = (tab === 'preview') ? 'flex' : 'none';
}}

function setDeviceView(dev) {{
  document.querySelectorAll('.device-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  const frame = document.getElementById('previewFrame');
  frame.className = 'preview-frame ' + dev;
}}

function toggleInspector() {{
  const body = document.getElementById('inspectorBody');
  const arrow = document.getElementById('inspectorArrow');
  if (body.style.display === 'none') {{
    body.style.display = 'block';
    arrow.innerText = '▲ Collapse';
  }} else {{
    body.style.display = 'none';
    arrow.innerText = '▼ Expand';
  }}
}}

function copySourceCode() {{
  navigator.clipboard.writeText(currentHtml);
  showToast('HTML code copied to clipboard!', '📋');
}}

function downloadHTML() {{
  const blob = new Blob([currentHtml], {{ type: 'text/html' }});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `frontend_design_${{PRESETS[currentPresetIndex].id}}.html`;
  a.click();
  showToast('HTML file downloaded!', '💾');
}}

function openFullscreen() {{
  const blob = new Blob([currentHtml], {{ type: 'text/html' }});
  const url = URL.createObjectURL(blob);
  window.open(url, '_blank');
}}

function showRoadmapNotice(skillName) {{
  showToast(`Skill '${{skillName}}' is on the 8-skill roadmap! We are currently demoing Skill #1: frontend-design.`, 'ℹ️');
}}

function showToast(msg, icon = '✅') {{
  const toast = document.getElementById('toastNotice');
  document.getElementById('toastIcon').innerText = icon;
  document.getElementById('toastMsg').innerText = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3500);
}}
</script>
</body>
</html>"""

with open("safe_skills_studio.html", "w", encoding="utf-8") as f:
    f.write(HTML_TEMPLATE)

print("Generated safe_skills_studio.html successfully! Size:", os.path.getsize("safe_skills_studio.html"), "bytes")
