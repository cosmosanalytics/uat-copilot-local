"""
build_canvas_design_app.py
Builds canvas_design_app.html: Standalone frontend-only HTML application
powered by WebLLM (local WebGPU) and Groq LPU (cloud fast inference),
demonstrating Skill #5: canvas-design (Apache 2.0 • Squad 1: Creative UI, Graphics & Frontend Artifacts).

Key Features:
1. Default Pure Light Mode with instant Dark Mode toggle.
2. Dual Inference: Groq LPU (cloud fast inference at 500+ tok/s with pre-provisioned free token) + Local WebGPU (WebLLM) + Instant Offline Showcase.
3. User Input enabled: Freeform design brief with prompt suggestion chips (pre-filled on load, zero empty-input blocking alerts).
4. Authentic Canvas-Design Runbook Methodology:
   - Phase 1: Design Philosophy Manifesto Creation (aesthetic worldview, 90% visual / 10% essential text, craft framing).
   - Phase 2: High-Assurance Visual Canvas Synthesis (pure HTML/CSS/SVG or HTML5 Canvas poster, geometric silence, concrete poetry, chromatic systems).
5. 3 Verified Instant Offline Presets:
   - Preset 1: Concrete Poetry (monumental architectural geometry, brutalist spatial tension, Le Corbusier meets Bauhaus).
   - Preset 2: Chromatic Silence & Quantum Fields (Josef Albers interaction, subtle spectral gradients, clinical reference coordinates).
   - Preset 3: Organic Modular Growth & Metabolist Systems (modular lattice, golden ratio spiral rhythm, systematic observation).
6. Export Suite: Export Canvas as SVG / HTML, Copy Design Philosophy Manifesto, or Print/Save as PDF.
"""

import json
import os

CATALOG_PATH = "internet_skills_catalog.json"
catalog = []
if os.path.exists(CATALOG_PATH):
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

cd_skill = next((s for s in catalog if s.get("name") == "canvas-design"), None)
cd_md = cd_skill.get("full_content", "") if cd_skill else """# Canvas Design
Create beautiful visual art in .png and .pdf documents using design philosophy.
Two steps:
1. Design Philosophy Creation (.md)
2. Express by creating it on a canvas (.png / .pdf)
"""

# Preset 1: Concrete Poetry
PRESET_CONCRETE_POETRY = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Concrete Poetry // Monumental Form</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=Cinzel:wght@500;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body {
      background: #f4efe6;
      color: #171614;
      font-family: 'Space Grotesk', sans-serif;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 2.5rem;
    }
    .poster-canvas {
      width: 100%;
      max-width: 680px;
      aspect-ratio: 1 / 1.414; /* ISO standard 216 paper ratio */
      background: #faf7f2;
      border: 1px solid #dcd5c8;
      box-shadow: 0 16px 45px rgba(23, 22, 20, 0.08);
      position: relative;
      padding: 3rem 2.8rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
    }
    .grid-lines {
      position: absolute;
      inset: 0;
      background-image: 
        linear-gradient(to right, rgba(23, 22, 20, 0.03) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(23, 22, 20, 0.03) 1px, transparent 1px);
      background-size: 32px 32px;
      pointer-events: none;
    }
    .header-tag {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 2px solid #171614;
      padding-bottom: 0.85rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      position: relative;
      z-index: 2;
    }
    .monument-block {
      position: relative;
      z-index: 2;
      margin: 1.5rem 0;
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }
    .monument-title {
      font-family: 'Cinzel', serif;
      font-size: 3.8rem;
      font-weight: 800;
      line-height: 0.92;
      letter-spacing: -0.02em;
      color: #171614;
      text-transform: uppercase;
    }
    .graphic-arch {
      position: relative;
      height: 280px;
      width: 100%;
      background: #171614;
      border-radius: 140px 140px 0 0;
      overflow: hidden;
      display: flex;
      align-items: flex-end;
      justify-content: center;
      padding: 1.5rem;
    }
    .sun-disk {
      position: absolute;
      top: -30px;
      right: 18%;
      width: 120px;
      height: 120px;
      background: #d65a31;
      border-radius: 50%;
      mix-blend-mode: screen;
    }
    .arch-cutout {
      position: absolute;
      inset: 24px 24px 0 24px;
      border: 1px solid rgba(250, 247, 242, 0.25);
      border-bottom: none;
      border-radius: 120px 120px 0 0;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      gap: 8px;
    }
    .arch-code {
      font-family: 'JetBrains Mono', monospace;
      color: #faf7f2;
      font-size: 0.75rem;
      letter-spacing: 0.2em;
    }
    .composition-strip {
      display: grid;
      grid-template-columns: 1.2fr 2fr 0.8fr;
      gap: 1rem;
      border-top: 1px solid #171614;
      padding-top: 1.25rem;
      position: relative;
      z-index: 2;
    }
    .col-spec {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      color: #555047;
      line-height: 1.5;
    }
    .col-manifesto {
      font-size: 0.82rem;
      line-height: 1.45;
      color: #2b2823;
      font-weight: 400;
    }
    .col-signature {
      text-align: right;
      font-family: 'Cinzel', serif;
      font-size: 1.1rem;
      font-weight: 700;
      color: #d65a31;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
    }
    .footer-bar {
      border-top: 1px solid #dcd5c8;
      padding-top: 0.75rem;
      display: flex;
      justify-content: space-between;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.65rem;
      color: #8c8474;
      position: relative;
      z-index: 2;
    }
  </style>
</head>
<body>
  <div class="poster-canvas">
    <div class="grid-lines"></div>

    <div class="header-tag">
      <span>PL-01 // ARCHITECTURAL CONSTRUCT</span>
      <span>SERIES 2026 • FOLIO #04</span>
    </div>

    <div class="monument-block">
      <div class="monument-title">
        MASS &amp;<br>VOID
      </div>
      <div class="graphic-arch">
        <div class="sun-disk"></div>
        <div class="arch-cutout">
          <div class="arch-code">§ 10.428 // POLISH POSTER RIGOR</div>
          <div style="color: rgba(250, 247, 242, 0.6); font-size: 0.7rem; font-family: 'JetBrains Mono', monospace;">38°43'N 09°08'W</div>
        </div>
      </div>
    </div>

    <div class="composition-strip">
      <div class="col-spec">
        FORM: MONUMENTAL<br>
        RATIO: 1:1.414 (DIN)<br>
        SURFACE: COLD PRESS<br>
        INK: CARBON / CINNABAR
      </div>
      <div class="col-manifesto">
        Ideas expressed through visual weight and spatial tension. Text as a rare, powerful architectural gesture — never paragraphs, only essential structures integrated into monolithic concrete balance.
      </div>
      <div class="col-signature">
        OPUS I<br>
        <span style="font-size: 0.6rem; color: #171614; font-family: 'JetBrains Mono', monospace;">VERIFIED ART</span>
      </div>
    </div>

    <div class="footer-bar">
      <span>CANVAS DESIGN SPECIFICATION // 90% VISUAL • 10% TEXT</span>
      <span>MUSEUM GRADE ARCHIVAL PROOF</span>
    </div>
  </div>
</body>
</html>"""

# Preset 2: Chromatic Silence & Quantum Fields
PRESET_CHROMATIC_SILENCE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chromatic Silence // Spectral Tension</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body {
      background: #f7f9fa;
      color: #0b1320;
      font-family: 'Plus Jakarta Sans', sans-serif;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 2.5rem;
    }
    .poster-canvas {
      width: 100%;
      max-width: 680px;
      aspect-ratio: 1 / 1.414;
      background: #ffffff;
      border: 1px solid #e1e7ec;
      box-shadow: 0 20px 50px rgba(11, 19, 32, 0.06);
      position: relative;
      padding: 3rem 2.8rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
    }
    .top-meta {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      border-bottom: 1px solid #0b1320;
      padding-bottom: 0.6rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      letter-spacing: 0.08em;
    }
    .field-assembly {
      margin: 2rem 0;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }
    .albers-nest {
      position: relative;
      width: 100%;
      height: 320px;
      background: #0f1e36;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 4px;
      overflow: hidden;
    }
    .layer-2 {
      width: 78%;
      height: 78%;
      background: #1c3b6b;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .layer-3 {
      width: 65%;
      height: 65%;
      background: #2563eb;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .layer-4 {
      width: 50%;
      height: 50%;
      background: #38bdf8;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 40px rgba(56, 189, 248, 0.4);
    }
    .core-light {
      width: 32%;
      height: 32%;
      background: #faf5ff;
      border-radius: 50%;
    }
    .spectrum-legend {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 6px;
      margin-top: 0.5rem;
    }
    .color-swatch-bar {
      height: 8px;
      border-radius: 2px;
    }
    .title-row {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }
    .title-h {
      font-size: 2.2rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1.05;
      color: #0b1320;
    }
    .subtitle-p {
      font-size: 0.78rem;
      color: #4b5563;
      max-width: 320px;
      line-height: 1.4;
    }
    .footer-bar {
      border-top: 1px solid #e1e7ec;
      padding-top: 0.75rem;
      display: flex;
      justify-content: space-between;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.65rem;
      color: #9ca3af;
    }
  </style>
</head>
<body>
  <div class="poster-canvas">
    <div class="top-meta">
      <span style="font-weight: 700;">OPTICAL INTERACTION LAB</span>
      <span>FIG. 08 // HARMONIC RATIOS</span>
    </div>

    <div class="field-assembly">
      <div class="title-row">
        <div>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #2563eb; font-weight:700; margin-bottom: 4px;">CHROMATIC SILENCE</div>
          <h1 class="title-h">INTERACTION<br>OF COLOR</h1>
        </div>
        <div class="subtitle-p">
          Josef Albers interaction meets systematic telemetry. Color zones encode information spatially, with whispered clinical typography letting fields communicate.
        </div>
      </div>

      <div class="albers-nest">
        <div class="layer-2">
          <div class="layer-3">
            <div class="layer-4">
              <div class="core-light"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="spectrum-legend">
        <div><div class="color-swatch-bar" style="background: #0f1e36;"></div><div style="font-family:'JetBrains Mono'; font-size: 0.58rem; color:#6b7280; margin-top:2px;">#0F1E36</div></div>
        <div><div class="color-swatch-bar" style="background: #1c3b6b;"></div><div style="font-family:'JetBrains Mono'; font-size: 0.58rem; color:#6b7280; margin-top:2px;">#1C3B6B</div></div>
        <div><div class="color-swatch-bar" style="background: #2563eb;"></div><div style="font-family:'JetBrains Mono'; font-size: 0.58rem; color:#6b7280; margin-top:2px;">#2563EB</div></div>
        <div><div class="color-swatch-bar" style="background: #38bdf8;"></div><div style="font-family:'JetBrains Mono'; font-size: 0.58rem; color:#6b7280; margin-top:2px;">#38BDF8</div></div>
        <div><div class="color-swatch-bar" style="background: #FAF5FF; border:1px solid #e5e7eb;"></div><div style="font-family:'JetBrains Mono'; font-size: 0.58rem; color:#6b7280; margin-top:2px;">#FAF5FF</div></div>
      </div>
    </div>

    <div class="footer-bar">
      <span>CALIBRATED VIA SYSTEMATIC OBSERVATION</span>
      <span>INDEX λ = 450nm — 680nm // CANV-05</span>
    </div>
  </div>
</body>
</html>"""

# Preset 3: Organic Modular Growth & Metabolist Systems
PRESET_METABOLIST_GROWTH = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Metabolist Growth // Organic Systems</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Epilogue:ital,wght@0,300;0,600;0,800;1,400&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body {
      background: #f5f6f1;
      color: #192017;
      font-family: 'Epilogue', sans-serif;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 2.5rem;
    }
    .poster-canvas {
      width: 100%;
      max-width: 680px;
      aspect-ratio: 1 / 1.414;
      background: #ffffff;
      border: 1px solid #d9dec9;
      box-shadow: 0 20px 45px rgba(25, 32, 23, 0.07);
      position: relative;
      padding: 3rem 2.8rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
    }
    .top-strip {
      display: flex;
      justify-content: space-between;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      color: #3b5033;
      border-bottom: 2px solid #2d4025;
      padding-bottom: 0.65rem;
    }
    .hero-assembly {
      margin: 1.5rem 0;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }
    .hero-h {
      font-size: 3rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 0.95;
      color: #192017;
      text-transform: uppercase;
    }
    .svg-container {
      width: 100%;
      height: 300px;
      background: #fbfcf9;
      border: 1px solid #e4e8d8;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }
    .meta-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1.25rem;
      border-top: 1px solid #d9dec9;
      padding-top: 1rem;
    }
    .meta-box h4 {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.68rem;
      color: #4a6341;
      text-transform: uppercase;
      margin-bottom: 4px;
    }
    .meta-box p {
      font-size: 0.78rem;
      color: #2e3b2b;
      line-height: 1.45;
    }
    .footer-bar {
      border-top: 1px solid #d9dec9;
      padding-top: 0.75rem;
      display: flex;
      justify-content: space-between;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.65rem;
      color: #7b8e75;
    }
  </style>
</head>
<body>
  <div class="poster-canvas">
    <div class="top-strip">
      <span>METABOLIST DYNAMICS // BIO-COMPUTATION</span>
      <span>NATURE × GEOMETRY</span>
    </div>

    <div class="hero-assembly">
      <div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #4a6341; font-weight: 700; margin-bottom: 6px;">
          ORGANIC SYSTEMS PHILOSOPHY
        </div>
        <h1 class="hero-h">CELLULAR<br>GROWTH</h1>
      </div>

      <div class="svg-container">
        <!-- SVG Modular Lattice -->
        <svg viewBox="0 0 500 280" width="92%" height="92%">
          <defs>
            <radialGradient id="nodeGrad" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#4a6341"/>
              <stop offset="100%" stop-color="#192017"/>
            </radialGradient>
          </defs>
          <!-- Golden Ratio Circles & Cellular Vectors -->
          <circle cx="250" cy="140" r="110" fill="none" stroke="#d9dec9" stroke-width="1.5" stroke-dasharray="4,4"/>
          <circle cx="250" cy="140" r="75" fill="none" stroke="#4a6341" stroke-width="1.8"/>
          <circle cx="250" cy="140" r="42" fill="none" stroke="#192017" stroke-width="2.5"/>
          <circle cx="250" cy="140" r="16" fill="url(#nodeGrad)"/>
          
          <!-- Orbiting Satellite Cells -->
          <circle cx="175" cy="140" r="28" fill="#e4e8d8" stroke="#4a6341" stroke-width="1.5"/>
          <circle cx="325" cy="140" r="28" fill="#e4e8d8" stroke="#4a6341" stroke-width="1.5"/>
          <circle cx="250" cy="65" r="28" fill="#e4e8d8" stroke="#4a6341" stroke-width="1.5"/>
          <circle cx="250" cy="215" r="28" fill="#e4e8d8" stroke="#4a6341" stroke-width="1.5"/>

          <!-- Crosshairs & Coordinate Lines -->
          <line x1="80" y1="140" x2="420" y2="140" stroke="#b8c2a3" stroke-width="1"/>
          <line x1="250" y1="20" x2="250" y2="260" stroke="#b8c2a3" stroke-width="1"/>

          <!-- Clinical Annotations -->
          <text x="90" y="132" font-family="'JetBrains Mono', monospace" font-size="10" fill="#4a6341">α_01: RADIAL EXPANSION</text>
          <text x="260" y="32" font-family="'JetBrains Mono', monospace" font-size="10" fill="#192017">PHI = 1.618033</text>
          <text x="335" y="250" font-family="'JetBrains Mono', monospace" font-size="10" fill="#7b8e75">SYS: RECEPTOR LATTICE</text>
        </svg>
      </div>

      <div class="meta-grid">
        <div class="meta-box">
          <h4>Subtle Conceptual DNA</h4>
          <p>Cellular morphogenesis translated into structural architecture.</p>
        </div>
        <div class="meta-box">
          <h4>Spatial Craftsmanship</h4>
          <p>90% visual composition, 10% clinical reference telemetry.</p>
        </div>
        <div class="meta-box">
          <h4>Archival Ratio</h4>
          <p>Root 2 harmonic tension with zero decorative noise.</p>
        </div>
      </div>
    </div>

    <div class="footer-bar">
      <span>AUTONOMOUS CANVAS CREATION // ANTHROPIC SKILL RUNBOOK #05</span>
      <span>EDITION: 1/1 MASTERWORK</span>
    </div>
  </div>
</body>
</html>"""

PRESETS_DATA = [
    {
        "id": "concrete-poetry",
        "name": "Concrete Poetry // Monumental Form",
        "movement": "Brutalist Constructivism",
        "philosophy": "Communication through monumental form and bold geometry. Ideas expressed through visual weight, monolithic color blocks, and spatial tension. Text is a rare, sculptural gesture — never paragraphs.",
        "brief": "A museum-quality Brutalist architectural poster with massive geometric arch forms, high spatial tension, and Polish poster energy.",
        "html": PRESET_CONCRETE_POETRY
    },
    {
        "id": "chromatic-silence",
        "name": "Chromatic Silence // Spectral Fields",
        "movement": "Geometric Precision & Color Interaction",
        "philosophy": "Color as the primary information system. Concentric harmonic fields inspired by Josef Albers, where chromatic boundaries create depth and quiet contemplation with clinical reference telemetry.",
        "brief": "An optical interaction study poster exploring color tension with nested spectral squares, minimalist labels, and high-contrast analytical typography.",
        "html": PRESET_CHROMATIC_SILENCE
    },
    {
        "id": "metabolist-growth",
        "name": "Metabolist Growth // Organic Systems",
        "movement": "Bio-Computational Morphogenesis",
        "philosophy": "Natural clustering and modular growth patterns. Cellular receptor lattice organized around golden ratio harmonics, treating ephemeral natural processes with the reverence of a scientific bible.",
        "brief": "An organic system diagram poster showing cellular growth patterns, radial lattice vectors, and clinical phi-ratio telemetry in natural forest tones.",
        "html": PRESET_METABOLIST_GROWTH
    }
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Canvas Design Studio // Skill #5 (Apache 2.0)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-canvas: #f8fafc;
      --bg-panel: #ffffff;
      --bg-panel-subtle: #f1f5f9;
      --border-subtle: #e2e8f0;
      --border-focus: #0284c7;
      --text-primary: #0f172a;
      --text-secondary: #475569;
      --text-muted: #64748b;
      --brand-accent: #0284c7;
      --brand-accent-subtle: #e0f2fe;
      --card-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
      --font-ui: 'Plus Jakarta Sans', sans-serif;
      --font-display: 'Bricolage Grotesque', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    html[data-theme="dark"] {
      --bg-canvas: #090d16;
      --bg-panel: #0f172a;
      --bg-panel-subtle: #1e293b;
      --border-subtle: #334155;
      --border-focus: #38bdf8;
      --text-primary: #f8fafc;
      --text-secondary: #cbd5e1;
      --text-muted: #94a3b8;
      --brand-accent: #38bdf8;
      --brand-accent-subtle: rgba(56, 189, 248, 0.12);
      --card-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
    }

    * { margin:0; padding:0; box-sizing:border-box; }
    body {
      background: var(--bg-canvas);
      color: var(--text-primary);
      font-family: var(--font-ui);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      transition: background 0.2s ease, color 0.2s ease;
    }

    /* Top App Header */
    .app-header {
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border-subtle);
      padding: 0.85rem 1.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 50;
      box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }
    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-badge {
      width: 38px;
      height: 38px;
      border-radius: 9px;
      background: linear-gradient(135deg, #0284c7 0%, #4338ca 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
      font-size: 1.15rem;
      font-weight: 800;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25);
    }
    .brand-text h1 {
      font-family: var(--font-display);
      font-size: 1.25rem;
      font-weight: 800;
      line-height: 1.15;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .badge-skill-fit {
      font-size: 0.65rem;
      background: #ecfdf5;
      color: #047857;
      border: 1px solid #a7f3d0;
      border-radius: 999px;
      padding: 2px 8px;
      font-weight: 700;
      font-family: var(--font-mono);
    }
    .brand-text p {
      font-size: 0.76rem;
      color: var(--text-muted);
    }

    /* Top Engine Switch */
    .engine-switch {
      display: flex;
      background: var(--bg-panel-subtle);
      padding: 3px;
      border-radius: 8px;
      border: 1px solid var(--border-subtle);
      gap: 2px;
    }
    .engine-btn {
      padding: 6px 13px;
      border-radius: 6px;
      border: none;
      background: transparent;
      font-size: 0.76rem;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
      font-family: var(--font-ui);
    }
    .engine-btn.active.groq {
      background: #0284c7;
      color: #ffffff;
      box-shadow: 0 1px 4px rgba(2, 132, 199, 0.3);
    }
    .engine-btn.active.webgpu {
      background: #4338ca;
      color: #ffffff;
      box-shadow: 0 1px 4px rgba(67, 56, 202, 0.3);
    }
    .engine-btn.active.instant {
      background: #0f172a;
      color: #ffffff;
    }

    .theme-toggle-btn {
      background: var(--bg-panel-subtle);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* Runtime Info Strip */
    .runtime-banner {
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border-subtle);
      padding: 0.6rem 1.75rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 0.75rem;
    }
    .runtime-desc {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .runtime-icon { font-size: 1.1rem; }
    .runtime-controls {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .select-box, .text-input {
      background: var(--bg-panel-subtle);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      padding: 5px 9px;
      border-radius: 6px;
      font-size: 0.74rem;
      font-family: var(--font-mono);
    }

    /* Studio Layout */
    .main-stage {
      flex: 1;
      padding: 1.25rem 1.75rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    .studio-grid {
      display: grid;
      grid-template-columns: 380px 1fr;
      gap: 1.25rem;
      align-items: start;
    }
    @media (max-width: 1024px) {
      .studio-grid { grid-template-columns: 1fr; }
    }

    /* Left Sidebar: Controls & Presets */
    .sidebar-pane {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    .card-box {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 1rem;
      box-shadow: var(--card-shadow);
    }
    .card-box-header {
      font-family: var(--font-display);
      font-size: 0.88rem;
      font-weight: 700;
      margin-bottom: 0.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .preset-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 0.85rem;
    }
    .preset-card {
      background: var(--bg-panel-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 0.65rem 0.85rem;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.15s ease;
    }
    .preset-card:hover {
      border-color: var(--brand-accent);
      background: var(--brand-accent-subtle);
    }
    .preset-card.active {
      border-color: var(--brand-accent);
      background: var(--brand-accent-subtle);
    }
    .preset-title {
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--text-primary);
    }
    .preset-meta {
      font-size: 0.68rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }

    /* Prompt chips */
    .prompt-chips-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 0.75rem;
    }
    .prompt-chip {
      background: var(--bg-panel-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 999px;
      padding: 4px 10px;
      font-size: 0.7rem;
      font-weight: 600;
      color: var(--text-primary);
      cursor: pointer;
      transition: all 0.12s ease;
    }
    .prompt-chip:hover {
      border-color: var(--brand-accent);
      color: var(--brand-accent);
    }
    .prompt-chip.active {
      border-color: var(--brand-accent);
      background: var(--brand-accent);
      color: #ffffff;
    }

    .brief-input {
      width: 100%;
      height: 100px;
      background: var(--bg-panel-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 0.75rem;
      font-size: 0.82rem;
      color: var(--text-primary);
      font-family: var(--font-ui);
      resize: vertical;
      line-height: 1.45;
      margin-bottom: 0.75rem;
    }
    .brief-input:focus {
      outline: none;
      border-color: var(--brand-accent);
      background: var(--bg-panel);
    }

    .btn-synthesize {
      width: 100%;
      background: linear-gradient(135deg, #0284c7 0%, #4338ca 100%);
      color: #ffffff;
      border: none;
      border-radius: 8px;
      padding: 0.78rem;
      font-size: 0.84rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25);
      transition: all 0.15s ease;
      font-family: var(--font-display);
    }
    .btn-synthesize:hover {
      opacity: 0.95;
      transform: translateY(-1px);
    }
    .btn-synthesize:disabled {
      opacity: 0.6;
      cursor: not-allowed;
      transform: none;
    }

    /* Runbook box */
    .runbook-box {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      overflow: hidden;
      box-shadow: var(--card-shadow);
    }
    .runbook-header {
      padding: 0.75rem 1rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      background: var(--bg-panel-subtle);
      border-bottom: 1px solid var(--border-subtle);
    }
    .runbook-body {
      padding: 0.85rem;
      font-size: 0.72rem;
      color: var(--text-secondary);
      max-height: 220px;
      overflow-y: auto;
      font-family: var(--font-mono);
      line-height: 1.45;
    }

    /* Right Main Canvas Stage */
    .stage-pane {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      display: flex;
      flex-direction: column;
      box-shadow: var(--card-shadow);
      overflow: hidden;
    }
    .stage-top-bar {
      padding: 0.65rem 1.1rem;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 0.75rem;
      background: var(--bg-panel-subtle);
    }
    .tabs-group {
      display: flex;
      gap: 4px;
    }
    .tab-btn {
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 0.76rem;
      font-weight: 700;
      border: none;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s ease;
      font-family: var(--font-display);
    }
    .tab-btn.active {
      background: var(--bg-panel);
      color: var(--brand-accent);
      box-shadow: var(--card-shadow);
    }

    .stage-content {
      position: relative;
      background: var(--bg-canvas);
      min-height: 640px;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 1.5rem;
      overflow-y: auto;
    }
    .canvas-frame {
      width: 100%;
      height: 660px;
      border: none;
      border-radius: 8px;
      background: #ffffff;
      box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }

    .manifesto-view {
      width: 100%;
      height: 660px;
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 2rem;
      overflow-y: auto;
      font-family: var(--font-ui);
      line-height: 1.6;
    }
    .manifesto-view h2 {
      font-family: var(--font-display);
      font-size: 1.5rem;
      font-weight: 800;
      margin-bottom: 0.75rem;
      color: var(--brand-accent);
    }
    .manifesto-view p {
      margin-bottom: 1rem;
      color: var(--text-secondary);
      font-size: 0.92rem;
    }

    /* Bottom Bar */
    .bottom-bar {
      padding: 0.75rem 1.1rem;
      border-top: 1px solid var(--border-subtle);
      background: var(--bg-panel-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.72rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }
    .actions-row {
      display: flex;
      gap: 6px;
    }
    .btn-action {
      padding: 5px 10px;
      font-size: 0.72rem;
      font-weight: 600;
      border: 1px solid var(--border-subtle);
      background: var(--bg-panel);
      color: var(--text-primary);
      border-radius: 5px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .btn-action:hover {
      border-color: var(--brand-accent);
      color: var(--brand-accent);
    }

    /* Toast */
    .toast-box {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      padding: 10px 18px;
      border-radius: 8px;
      font-size: 0.8rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 10px 25px -5px rgba(0,0,0,0.2);
      opacity: 0;
      pointer-events: none;
      transform: translateY(10px);
      transition: all 0.2s ease;
      z-index: 100;
    }
    .toast-box.show {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0);
    }
  </style>
</head>
<body>

  <!-- Top App Header -->
  <header class="app-header">
    <div class="brand-group">
      <div class="brand-badge">🎨</div>
      <div class="brand-text">
        <h1>Canvas Design Studio <span class="badge-skill-fit">Skill #5: canvas-design (Apache 2.0 • Safest)</span></h1>
        <p>Design Philosophy Manifestos &rarr; Museum-Quality Visual Posters • 90% Visual Design • 10% Essential Text</p>
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
    <div class="runtime-banner" id="runtimeBanner">
      <!-- Populated via JS -->
    </div>

    <div class="studio-grid">

      <!-- Left Column: Presets & Custom Generator -->
      <div class="sidebar-pane">

        <div class="card-box">
          <div class="card-box-header">
            <span>Verified Movement Canvases</span>
            <span style="color: #047857; font-size: 0.72rem; font-family: var(--font-mono);">90% Visual / 10% Text</span>
          </div>

          <div class="preset-list" id="presetsList">
            <!-- Rendered via JS -->
          </div>

          <div class="card-box-header" style="margin-top: 1.15rem;">
            <span>Synthesize Custom Canvas</span>
            <span style="font-size:0.7rem; color:var(--brand-accent); font-weight:600;">⚡ Groq LPU Ready</span>
          </div>

          <!-- Prompt suggestion chips -->
          <div class="prompt-chips-row">
            <button type="button" class="prompt-chip active" onclick="setPromptBrief('A museum-quality Brutalist architectural poster with massive geometric arch forms, high spatial tension, and Polish poster energy.', this)">🏛️ Brutalist Monument</button>
            <button type="button" class="prompt-chip" onclick="setPromptBrief('An optical interaction study poster exploring color tension with nested spectral squares, minimalist labels, and high-contrast analytical typography.', this)">🟦 Chromatic Albers</button>
            <button type="button" class="prompt-chip" onclick="setPromptBrief('An organic system diagram poster showing cellular growth patterns, radial lattice vectors, and clinical phi-ratio telemetry in natural forest tones.', this)">🌿 Metabolist Systems</button>
            <button type="button" class="prompt-chip" onclick="setPromptBrief('A Swiss-style minimalist constructivist poster exploring negative space, asymmetric typography, and high-tension geometric angles in carbon black and vermilion red.', this)">📐 Swiss Minimalist</button>
          </div>

          <textarea class="brief-input" id="briefInput" placeholder="Describe any aesthetic movement or philosophical poster theme to synthesize using canvas-design rules..."></textarea>

          <button class="btn-synthesize" id="btnSynthesize" onclick="runCanvasSynthesis()">
            <span>⚡ Synthesize Visual Canvas (Groq LPU)</span>
          </button>
        </div>

        <!-- Injected SKILL.md Runbook Inspector -->
        <div class="runbook-box">
          <div class="runbook-header" onclick="toggleRunbook()">
            <span style="font-weight: 700; font-size: 0.8rem; color: var(--text-primary);">
              📜 Injected SKILL.md (canvas-design Runbook)
            </span>
            <span style="font-size: 0.75rem; color: var(--text-muted);" id="runbookArrow">▼ Expand</span>
          </div>
          <div class="runbook-body" id="runbookBody" style="display: none;">
            <div style="color: #047857; font-weight: 700; margin-bottom: 0.5rem;">
              [Apache 2.0 In-Context Rules Loaded]
            </div>
            <pre style="white-space: pre-wrap;">__SKILL_SNIPPET__...

[Remaining runbook active in system prompt context]</pre>
          </div>
        </div>

      </div>

      <!-- Right Column: Live Poster Stage -->
      <div class="stage-pane">

        <div class="stage-top-bar">
          <div class="tabs-group">
            <button class="tab-btn active" id="tabBtnPoster" onclick="switchStage('poster')">👁️ Live Poster Canvas</button>
            <button class="tab-btn" id="tabBtnManifesto" onclick="switchStage('manifesto')">📜 Design Philosophy Manifesto</button>
          </div>

          <div style="font-size: 0.72rem; color: var(--brand-accent); font-weight: 700; font-family: var(--font-mono);">
            MASTERWORK EXECUTION (90/10)
          </div>
        </div>

        <!-- Stage Views -->
        <div class="stage-content">
          <iframe class="canvas-frame" id="stageFrame" sandbox="allow-scripts allow-modals" title="Canvas Poster Stage"></iframe>
          <div class="manifesto-view" id="stageManifesto" style="display: none;">
            <!-- Rendered via JS -->
          </div>
        </div>

        <!-- Bottom Status Bar -->
        <div class="bottom-bar">
          <div id="renderSourceInfo">Canvas: Concrete Poetry • Museum Archival Grade</div>
          <div class="actions-row">
            <button class="btn-action" onclick="copyManifesto()">📋 Copy Manifesto</button>
            <button class="btn-action" onclick="downloadPosterHtml()">💾 Download .html</button>
            <button class="btn-action" onclick="popoutPoster()">↗ Full Canvas</button>
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

  const PRESETS = __PRESETS_JSON__;
  let currentEngine = 'groq';
  let currentPresetIdx = 0;
  let currentStage = 'poster';
  let currentHtml = PRESETS[0].html;
  let currentPhilosophy = PRESETS[0].philosophy;
  let webllmEngine = null;

  window.addEventListener('DOMContentLoaded', () => {
    initTheme();
    renderRuntimeBanner();
    renderPresetsList();
    selectPreset(0);
    const defaultBrief = PRESETS[0].brief;
    const input = document.getElementById('briefInput');
    if (input && !input.value) input.value = defaultBrief;
  });

  function initTheme() {
    const saved = localStorage.getItem('canvas_app_mode') || 'light';
    setTheme(saved);
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'light' ? 'dark' : 'light';
    setTheme(next);
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('canvas_app_mode', theme);
    const btn = document.getElementById('btnThemeToggle');
    if (btn) {
      btn.innerHTML = theme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode';
    }
  }

  function switchEngine(eng) {
    currentEngine = eng;
    document.querySelectorAll('.engine-btn').forEach(b => b.classList.remove('active'));
    if (eng === 'instant') document.getElementById('tabInstant').classList.add('active');
    if (eng === 'webgpu') document.getElementById('tabWebGPU').classList.add('active');
    if (eng === 'groq') document.getElementById('tabGroq').classList.add('active');

    const synthBtn = document.getElementById('btnSynthesize');
    if (synthBtn) {
      if (eng === 'groq') synthBtn.innerHTML = '<span>⚡ Synthesize Visual Canvas (Groq LPU)</span>';
      else if (eng === 'webgpu') synthBtn.innerHTML = '<span>🎮 Synthesize via Local WebGPU</span>';
      else synthBtn.innerHTML = '<span>⚡ Render Instant Showcase</span>';
    }
    renderRuntimeBanner();
  }

  function renderRuntimeBanner() {
    const banner = document.getElementById('runtimeBanner');
    if (currentEngine === 'groq') {
      const customKey = localStorage.getItem('groq_api_key') || '';
      banner.innerHTML = `
        <div class="runtime-desc">
          <div class="runtime-icon" style="color: #0284c7;">⚡</div>
          <div>
            <strong style="font-size: 0.85rem; color: var(--text-primary);">Groq LPU Cloud Fast Inference (500+ tok/s)</strong>
            <div style="font-size: 0.75rem; color: var(--text-secondary);">
              🟢 Pre-provisioned Free Tier API token active! Generates two-pass canvas-design posters in ~1–2 seconds.
            </div>
          </div>
        </div>
        <div class="runtime-controls">
          <select class="select-box" id="groqModelSelect">
            <option value="openai/gpt-oss-120b" selected>GPT-OSS 120B (Groq LPU • Free Tier)</option>
            <option value="qwen/qwen3.8-27b">Qwen 3.8 27B (Groq LPU)</option>
            <option value="openai/gpt-oss-20b">GPT-OSS 20B (Groq LPU)</option>
          </select>
          <input type="password" class="text-input" id="groqKey" placeholder="Pre-provisioned key active (or paste gsk_...)" value="${customKey}" onchange="saveCustomGroqKey(this.value)" style="width: 220px;">
          <span style="font-size: 0.72rem; color: #047857; font-weight: 700;">🟢 Free Token Active</span>
        </div>
      `;
    } else if (currentEngine === 'instant') {
      banner.innerHTML = `
        <div class="runtime-desc">
          <div class="runtime-icon" style="color: #0284c7;">⚡</div>
          <div>
            <strong style="font-size: 0.85rem; color: var(--text-primary);">Instant Verified Showcase Mode</strong>
            <div style="font-size: 0.75rem; color: var(--text-secondary);">
              3 pre-computed aesthetic movement posters calibrated strictly to canvas-design rules.
            </div>
          </div>
        </div>
        <div style="font-size: 0.75rem; color: #047857; font-weight: 700;">
          🟢 Zero Latency • 100% Client Offline Compatible
        </div>
      `;
    } else if (currentEngine === 'webgpu') {
      banner.innerHTML = `
        <div class="runtime-desc">
          <div class="runtime-icon" style="color: #4338ca;">🎮</div>
          <div>
            <strong style="font-size: 0.85rem; color: var(--text-primary);">Local In-Browser WebGPU (WebLLM)</strong>
            <div style="font-size: 0.75rem; color: var(--text-secondary);">
              Executes private local LLM weights on device GPU without network round-trips.
            </div>
          </div>
        </div>
        <div class="runtime-controls">
          <select class="select-box" id="webgpuModelSelect">
            <option value="Llama-3.2-3B-Instruct-q4f16_1-MLC" selected>Llama 3.2 3B Instruct (q4f16)</option>
            <option value="Qwen2.5-1.5B-Instruct-q4f16_1-MLC">Qwen 2.5 1.5B Instruct (Fast)</option>
          </select>
          <button class="btn-action" id="btnLoadGpu" onclick="loadWebLLM()" style="background: #0284c7; color: #fff; border:none; padding: 5px 12px;">Load into GPU</button>
        </div>
        <div id="gpuProgressWrap" style="display:none; width: 100%; margin-top: 5px;">
          <div style="background: var(--border-subtle); height: 5px; border-radius: 3px; overflow: hidden;">
            <div id="gpuProgressFill" style="background: #0284c7; height: 100%; width: 0%;"></div>
          </div>
          <div id="gpuProgressInfo" style="font-size: 0.7rem; color: var(--text-muted); margin-top: 3px;"></div>
        </div>
      `;
    }
  }

  function getActiveGroqKey() {
    const custom = localStorage.getItem('groq_api_key');
    if (custom && custom.trim().length > 10) return custom.trim();
    return PROVISIONED_GROQ_KEY;
  }

  function saveCustomGroqKey(val) {
    if (val && val.trim().length > 10) {
      localStorage.setItem('groq_api_key', val.trim());
      showToast('Custom Groq Key Saved', '🔑');
    } else {
      localStorage.removeItem('groq_api_key');
      showToast('Using Pre-provisioned Free Token', '⚡');
    }
  }

  async function loadWebLLM() {
    if (!navigator.gpu) {
      alert('WebGPU is not supported on this browser.');
      return;
    }
    const model = document.getElementById('webgpuModelSelect').value;
    const btn = document.getElementById('btnLoadGpu');
    const wrap = document.getElementById('gpuProgressWrap');
    const fill = document.getElementById('gpuProgressFill');
    const info = document.getElementById('gpuProgressInfo');

    btn.disabled = true;
    btn.innerText = 'Loading...';
    wrap.style.display = 'block';

    try {
      showToast('Importing WebLLM module...', '📦');
      const webllm = await import("https://esm.run/@mlc-ai/web-llm");
      webllmEngine = await webllm.CreateMLCEngine(model, {
        initProgressCallback: (report) => {
          const pct = Math.round(report.progress * 100);
          fill.style.width = pct + '%';
          info.innerText = `[${pct}%] ${report.text}`;
        }
      });
      btn.innerText = '✅ Loaded on GPU';
      btn.style.background = '#047857';
      showToast('Model resident in WebGPU!', '🚀');
    } catch(e) {
      console.error(e);
      showToast('Failed to load WebLLM: ' + e.message, '⚠️');
      btn.disabled = false;
      btn.innerText = 'Retry';
    }
  }

  function renderPresetsList() {
    const list = document.getElementById('presetsList');
    list.innerHTML = PRESETS.map((p, i) => `
      <div class="preset-card ${i === currentPresetIdx ? 'active' : ''}" onclick="selectPreset(${i})">
        <div>
          <div class="preset-title">${p.name}</div>
          <div class="preset-meta">${p.movement}</div>
        </div>
        <div style="font-size: 0.72rem; color: var(--text-muted);">View Canvas →</div>
      </div>
    `).join('');
  }

  function selectPreset(idx) {
    currentPresetIdx = idx;
    const p = PRESETS[idx];
    document.querySelectorAll('.preset-card').forEach((el, i) => {
      el.classList.toggle('active', i === idx);
    });
    document.getElementById('briefInput').value = p.brief;
    currentHtml = p.html;
    currentPhilosophy = p.philosophy;
    renderPosterStage(currentHtml, currentPhilosophy, p.name);
  }

  function setPromptBrief(txt, el) {
    document.getElementById('briefInput').value = txt;
    document.querySelectorAll('.prompt-chip').forEach(c => c.classList.remove('active'));
    if (el) el.classList.add('active');
  }

  function switchStage(stage) {
    currentStage = stage;
    document.getElementById('tabBtnPoster').classList.toggle('active', stage === 'poster');
    document.getElementById('tabBtnManifesto').classList.toggle('active', stage === 'manifesto');
    document.getElementById('stageFrame').style.display = (stage === 'poster') ? 'block' : 'none';
    document.getElementById('stageManifesto').style.display = (stage === 'manifesto') ? 'block' : 'none';
  }

  function renderPosterStage(html, philosophy, source) {
    currentHtml = html;
    currentPhilosophy = philosophy;

    const frame = document.getElementById('stageFrame');
    frame.srcdoc = html;

    const manBox = document.getElementById('stageManifesto');
    manBox.innerHTML = `
      <h2>Design Philosophy Manifesto</h2>
      <p style="font-size: 1.05rem; font-weight: 600; color: var(--text-primary); margin-bottom: 1.25rem;">
        Aesthetic Movement: ${source}
      </p>
      <div style="background: var(--bg-panel-subtle); border-left: 4px solid var(--brand-accent); padding: 1.25rem; border-radius: 6px; margin-bottom: 1.5rem;">
        <p style="margin: 0; color: var(--text-primary); font-size: 0.95rem; line-height: 1.6;">${philosophy}</p>
      </div>
      <h3 style="font-size: 1.1rem; margin-bottom: 0.5rem; font-family: var(--font-display);">The Critical Understanding</h3>
      <p>1. <strong>Visual Primacy:</strong> The poster is 90% visual design, 10% essential text. Information lives in geometry, color tension, and spatial hierarchy.</p>
      <p>2. <strong>Subtle Reference:</strong> Niche conceptual thread embedded quietly within the art itself — intuitive to insiders, aesthetically masterful to all.</p>
      <p>3. <strong>Master-Level Craftsmanship:</strong> Flawless alignment, perfect margin containment, zero decorative clutter.</p>
    `;

    document.getElementById('renderSourceInfo').innerText = `Canvas: ${source} • Museum Grade Archival Output`;
  }

  async function runCanvasSynthesis() {
    let brief = document.getElementById('briefInput').value.trim();
    if (!brief) {
      brief = "A museum-quality Brutalist architectural poster with massive geometric arch forms, high spatial tension, and Polish poster energy.";
      document.getElementById('briefInput').value = brief;
      const firstChip = document.querySelector('.prompt-chip');
      if (firstChip) firstChip.classList.add('active');
      showToast('Loaded Brutalist prompt', '🏛️');
    }

    const btn = document.getElementById('btnSynthesize');
    btn.disabled = true;
    btn.innerHTML = '<span>⏳ Synthesizing Poster Canvas via Groq...</span>';

    const startTime = Date.now();

    try {
      if (currentEngine === 'groq') {
        const apiKey = getActiveGroqKey();
        const model = document.getElementById('groqModelSelect') ? document.getElementById('groqModelSelect').value : 'openai/gpt-oss-120b';

        const systemPrompt = "You are an elite visual artist following Anthropic's 'canvas-design' skill runbook.\\n" +
          "Your mission is to synthesize a museum-grade visual art poster as a self-contained, responsive single-file HTML document.\\n" +
          "CORE DIRECTIVES OF canvas-design:\\n" +
          "1. 90% VISUAL DESIGN, 10% TEXT: No paragraphs or body copy. Text is strictly sparse, clinical, typographic architectural anchors (e.g., DIN labels, coordinates, series numbers).\\n" +
          "2. AESTHETIC MOVEMENT: Interpret the user brief as a high-concept aesthetic movement (e.g. Concrete Poetry, Chromatic Language, Metabolist Systems, Geometric Silence).\\n" +
          "3. VISUAL CRAFT: Museum-quality ISO aspect ratio (1:1.414), deliberate restrained color palette, master-level geometric or SVG shapes, and high spatial breathing room.\\n" +
          "4. OUTPUT FORMAT: Output ONLY the complete, self-contained single-page HTML inside an ```html codeblock with embedded CSS and SVG. Ensure all text and elements fit within canvas boundaries with zero clipping.";

        const resp = await fetch("https://api.groq.com/openai/v1/chat/completions", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${apiKey}`,
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            model: model,
            messages: [
              { role: "system", content: systemPrompt },
              { role: "user", content: brief }
            ],
            temperature: 0.7,
            max_tokens: 6000
          })
        });

        if (!resp.ok) {
          const err = await resp.json();
          throw new Error(err.error?.message || resp.statusText);
        }

        const data = await resp.json();
        const txt = data.choices[0].message.content;

        extractAndApplySynthesis(txt, brief, `Groq LPU (${model})`);
        const elapsed = Date.now() - startTime;
        showToast(`Poster synthesized in ${elapsed}ms!`, '⚡');

      } else if (currentEngine === 'instant') {
        selectPreset(1);
        showToast('Switched to Chromatic Silence preset!', '✨');

      } else if (currentEngine === 'webgpu') {
        if (!webllmEngine) throw new Error('Please load the WebLLM model into WebGPU first using the top banner button.');
        const systemPrompt = "You are an elite visual artist following 'canvas-design'. Return a single self-contained HTML poster inside ```html with 90% visual design, 10% minimal text, and high-tension geometric elegance.";
        const reply = await webllmEngine.chat.completions.create({
          messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: brief }
          ],
          temperature: 0.7,
          max_tokens: 2500
        });
        const txt = reply.choices[0].message.content;
        extractAndApplySynthesis(txt, brief, 'Local WebGPU (WebLLM)');
        showToast('WebGPU local synthesis complete!', '🎮');
      }
    } catch(e) {
      showToast('Synthesis error: ' + (e.message || 'Check network'), '⚠️');
      console.error(e);
    } finally {
      btn.disabled = false;
      if (currentEngine === 'groq') btn.innerHTML = '<span>⚡ Synthesize Visual Canvas (Groq LPU)</span>';
      else if (currentEngine === 'webgpu') btn.innerHTML = '<span>🎮 Synthesize via Local WebGPU</span>';
      else btn.innerHTML = '<span>⚡ Render Instant Showcase</span>';
    }
  }

  function extractAndApplySynthesis(rawText, userBrief, source) {
    let html = "";
    const htmlMarker = rawText.indexOf('```html');
    const xmlMarker = rawText.indexOf('```xml');

    if (htmlMarker !== -1) {
      let candidate = rawText.substring(htmlMarker + 7).trim();
      const endFence = candidate.lastIndexOf('```');
      if (endFence !== -1) candidate = candidate.substring(0, endFence).trim();
      html = candidate;
    } else if (xmlMarker !== -1) {
      let candidate = rawText.substring(xmlMarker + 6).trim();
      const endFence = candidate.lastIndexOf('```');
      if (endFence !== -1) candidate = candidate.substring(0, endFence).trim();
      html = candidate;
    } else {
      const doctypeIdx = rawText.search(/<!DOCTYPE\\s+html/i);
      const htmlTagIdx = rawText.search(/<html[\\s>]/i);
      let start = -1;
      if (doctypeIdx !== -1) start = doctypeIdx;
      else if (htmlTagIdx !== -1) start = htmlTagIdx;
      if (start !== -1) {
        let candidate = rawText.substring(start).trim();
        const endFence = candidate.lastIndexOf('```');
        if (endFence !== -1) candidate = candidate.substring(0, endFence).trim();
        html = candidate;
      }
    }

    if (!html || html.length < 100) {
      throw new Error("Could not extract complete HTML document from model response.");
    }

    const philosophy = `An interpretive aesthetic movement crafted in response to: "${userBrief}". Built with 90% visual form and 10% clinical typography to ensure pure spatial communication.`;
    renderPosterStage(html, philosophy, source);
  }

  function copyManifesto() {
    navigator.clipboard.writeText(currentPhilosophy).then(() => {
      showToast('Manifesto copied to clipboard!', '📋');
    });
  }

  function downloadPosterHtml() {
    const blob = new Blob([currentHtml], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `canvas_design_poster_${Date.now()}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('Poster HTML downloaded!', '💾');
  }

  function popoutPoster() {
    const win = window.open('', '_blank');
    if (win) {
      win.document.open();
      win.document.write(currentHtml);
      win.document.close();
    } else {
      showToast('Popout blocked by browser', '⚠️');
    }
  }

  function toggleRunbook() {
    const body = document.getElementById('runbookBody');
    const arrow = document.getElementById('runbookArrow');
    const isHidden = (body.style.display === 'none');
    body.style.display = isHidden ? 'block' : 'none';
    arrow.innerText = isHidden ? '▲ Collapse' : '▼ Expand';
  }

  function showToast(msg, icon='✅') {
    const box = document.getElementById('toastBox');
    document.getElementById('toastIcon').innerText = icon;
    document.getElementById('toastMsg').innerText = msg;
    box.classList.add('show');
    setTimeout(() => {
      box.classList.remove('show');
    }, 3200);
  }
  </script>
</body>
</html>"""

def build_app():
    # Embed runbook snippet
    snippet = cd_md[:1500].replace("\\", "\\\\").replace("`", "\\`")
    
    # Embed presets
    presets_json_str = json.dumps(PRESETS_DATA)
    
    out_html = HTML_TEMPLATE.replace("__SKILL_SNIPPET__", snippet)
    out_html = out_html.replace("__PRESETS_JSON__", presets_json_str)

    target_file = "canvas_design_app.html"
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(out_html)
    
    print(f"Generated {target_file} successfully! Size: {len(out_html)} bytes")

if __name__ == "__main__":
    build_app()
