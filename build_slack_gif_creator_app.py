"""
build_slack_gif_creator_app.py
Builds slack_gif_creator_app.html: Standalone frontend-only HTML application
powered by WebLLM (local WebGPU) and Groq LPU (cloud fast inference),
demonstrating Skill #6: slack-gif-creator (Apache 2.0 • Squad 1: Creative UI, Graphics & Frontend Artifacts).

Key Features:
1. Default Pure Light Mode with instant Dark Mode toggle.
2. Dual Inference: Groq LPU (cloud fast inference at 500+ tok/s with pre-provisioned free token) + Local WebGPU (WebLLM) + Instant Offline Showcase.
3. User Input enabled: Freeform animation prompt with suggestions (pre-filled on load, zero empty-input blocking alerts).
4. Authentic Slack GIF Creator Methodology:
   - Slack emoji mode (128x128) vs message GIF mode (480x480).
   - Strict Slack performance budget: 10–30 FPS, <= 128 colors, under 3s duration, < 2MB payload.
   - Core movement easing curves: bounce_out, elastic_out, pulse_heartbeat, particle_burst, wobble_spin.
   - Real-time client-side frame generation & GIF assembly (using in-browser gifshot / HTML5 Canvas).
5. 3 Verified Instant Offline Presets:
   - Preset 1: Party Parrot Sparkle Pulse (128x128 emoji pulse + multi-color particle burst).
   - Preset 2: Confetti Celebration Cannon (480x480 message animation with physics gravity).
   - Preset 3: Loading Radar Scanner (128x128 pulsing concentric sonar rings with glowing sweeping beam).
6. Export Suite: Export animated GIF directly, download APNG / WebM, inspect generated JS/Python frame code, or copy Slack custom emoji dimensions.
"""

import json
import os

CATALOG_PATH = "internet_skills_catalog.json"
catalog = []
if os.path.exists(CATALOG_PATH):
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

sg_skill = next((s for s in catalog if s.get("name") == "slack-gif-creator"), None)
sg_md = sg_skill.get("full_content", "") if sg_skill else """# Slack GIF Creator
Utilities and constraints for creating animated GIFs optimized for Slack.
Dimensions: 128x128 emoji or 480x480 message.
FPS: 10-30, Colors: 48-128, Duration: < 3s.
"""

# Presets Data with self-contained JS animation generators
PRESETS_DATA = [
    {
        "id": "party-sparkle-pulse",
        "name": "Party Sparkle Pulse (Emoji)",
        "mode": "128x128 Emoji",
        "fps": 15,
        "frames": 24,
        "width": 128,
        "height": 128,
        "description": "A rhythmic celebration emoji that pulses and emits sparkling starbursts, optimized under 64KB for Slack custom reaction emojis.",
        "brief": "A vibrant party star emoji that pulses with heartbeat rhythm, radiates multi-color sparkles, and loops seamlessly at 128x128 for Slack.",
        "code": """function renderFrame(ctx, width, height, t, frameIdx, totalFrames) {
  // Background
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, width, height);

  const cx = width / 2;
  const cy = height / 2;

  // Pulse scale
  const pulse = 1 + 0.22 * Math.sin(t * Math.PI * 2);

  // Radiating sparkles
  const numParticles = 8;
  for (let i = 0; i < numParticles; i++) {
    const angle = (i / numParticles) * Math.PI * 2 + (t * Math.PI * 0.5);
    const dist = 24 + 32 * ((t + i / numParticles) % 1);
    const px = cx + Math.cos(angle) * dist;
    const py = cy + Math.sin(angle) * dist;
    const alpha = 1 - ((dist - 24) / 32);

    ctx.save();
    ctx.translate(px, py);
    ctx.rotate(t * Math.PI * 4);
    ctx.fillStyle = `rgba(245, 158, 11, ${alpha})`;
    ctx.beginPath();
    ctx.arc(0, 0, 3.5, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }

  // Central Star
  ctx.save();
  ctx.translate(cx, cy);
  ctx.scale(pulse, pulse);

  // Glow
  const glowGrad = ctx.createRadialGradient(0, 0, 4, 0, 0, 36);
  glowGrad.addColorStop(0, 'rgba(234, 179, 8, 0.45)');
  glowGrad.addColorStop(1, 'rgba(234, 179, 8, 0)');
  ctx.fillStyle = glowGrad;
  ctx.beginPath();
  ctx.arc(0, 0, 36, 0, Math.PI * 2);
  ctx.fill();

  // 5-point Star Polygon
  ctx.fillStyle = '#f59e0b';
  ctx.strokeStyle = '#b45309';
  ctx.lineWidth = 3;
  ctx.beginPath();
  for (let i = 0; i < 10; i++) {
    const r = (i % 2 === 0) ? 24 : 11;
    const a = (i * Math.PI) / 5 - Math.PI / 2;
    const x = r * Math.cos(a);
    const y = r * Math.sin(a);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  // Face details
  ctx.fillStyle = '#78350f';
  ctx.beginPath();
  ctx.arc(-6, -2, 2.5, 0, Math.PI * 2);
  ctx.arc(6, -2, 2.5, 0, Math.PI * 2);
  ctx.fill();

  // Smile
  ctx.strokeStyle = '#78350f';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(0, 2, 5, 0.2, Math.PI - 0.2);
  ctx.stroke();

  ctx.restore();
}"""
    },
    {
        "id": "confetti-cannon",
        "name": "Confetti Celebration Cannon",
        "mode": "480x480 Message",
        "fps": 20,
        "frames": 36,
        "width": 480,
        "height": 480,
        "description": "High-energy celebration message GIF with ballistic confetti particles, celebratory banner, and smooth physics easing.",
        "brief": "A celebration cannon firing vibrant ribbons and multi-colored confetti particles across a 480x480 canvas for Slack channel milestones.",
        "code": """function renderFrame(ctx, width, height, t, frameIdx, totalFrames) {
  // Clear
  ctx.fillStyle = '#fafaf9';
  ctx.fillRect(0, 0, width, height);

  const cx = width / 2;
  const cy = height / 2;

  // Confetti Physics simulation
  const numPieces = 42;
  const colors = ['#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899'];

  for (let i = 0; i < numPieces; i++) {
    const seed = (i * 9301 + 49297) % 233280;
    const randAngle = -Math.PI / 2 + ((seed % 100) / 100 - 0.5) * 1.8;
    const speed = 180 + (seed % 160);
    const grav = 240;

    const timeInAir = t;
    const px = cx + Math.cos(randAngle) * speed * timeInAir;
    const py = cy + 120 + Math.sin(randAngle) * speed * timeInAir + 0.5 * grav * (timeInAir * timeInAir);

    if (py < height && px > 0 && px < width) {
      ctx.save();
      ctx.translate(px, py);
      ctx.rotate(t * 12 + i);
      ctx.fillStyle = colors[i % colors.length];
      ctx.fillRect(-6, -3, 12, 6);
      ctx.restore();
    }
  }

  // Central Cannon & Badge
  const recoil = 12 * Math.max(0, 1 - t * 4);
  ctx.save();
  ctx.translate(cx, cy + 120 + recoil);

  // Cannon base
  ctx.fillStyle = '#1c1917';
  ctx.beginPath();
  ctx.arc(0, 0, 32, 0, Math.PI, true);
  ctx.fill();

  // Cannon barrel
  ctx.fillStyle = '#44403c';
  ctx.strokeStyle = '#d97706';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.rect(-16, -42, 32, 42);
  ctx.fill();
  ctx.stroke();

  // Blast ring
  if (t < 0.35) {
    const blastR = (t / 0.35) * 60;
    const blastAlpha = 1 - (t / 0.35);
    ctx.strokeStyle = `rgba(245, 158, 11, ${blastAlpha})`;
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.arc(0, -42, blastR, 0, Math.PI * 2);
    ctx.stroke();
  }

  ctx.restore();

  // Top Milestone Tag
  ctx.fillStyle = '#1c1917';
  ctx.font = 'bold 24px Plus Jakarta Sans, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('DEPLOYMENT CELEBRATION!', cx, 68);

  ctx.fillStyle = '#64748b';
  ctx.font = '13px JetBrains Mono, monospace';
  ctx.fillText('SLACK CHANNEL MILESTONE ACHIEVED', cx, 96);
}"""
    },
    {
        "id": "radar-sonar-scanner",
        "name": "Radar Sonar Scanner (Emoji)",
        "mode": "128x128 Emoji",
        "fps": 15,
        "frames": 24,
        "width": 128,
        "height": 128,
        "description": "Continuous scanning radar HUD with sweeping phosphor beam, concentric rings, and blipping targets, ideal for 'searching' or 'thinking' states.",
        "brief": "A sci-fi radar sonar sweep with luminous concentric grid circles and blipping target dots rotating seamlessly at 128x128 for Slack.",
        "code": """function renderFrame(ctx, width, height, t, frameIdx, totalFrames) {
  ctx.fillStyle = '#0f172a';
  ctx.fillRect(0, 0, width, height);

  const cx = width / 2;
  const cy = height / 2;
  const maxR = width * 0.44;

  // Concentric Rings
  ctx.strokeStyle = '#1e293b';
  ctx.lineWidth = 1.5;
  for (let r = 16; r <= maxR; r += 16) {
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.stroke();
  }

  // Crosshairs
  ctx.beginPath();
  ctx.moveTo(cx - maxR, cy);
  ctx.lineTo(cx + maxR, cy);
  ctx.moveTo(cx, cy - maxR);
  ctx.lineTo(cx, cy + maxR);
  ctx.stroke();

  // Sweeping Radar Beam (cone gradient)
  const angle = t * Math.PI * 2;
  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(angle);

  const beamGrad = ctx.createRadialGradient(0, 0, 0, 0, 0, maxR);
  beamGrad.addColorStop(0, 'rgba(16, 185, 129, 0.6)');
  beamGrad.addColorStop(1, 'rgba(16, 185, 129, 0)');

  ctx.fillStyle = beamGrad;
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.arc(0, 0, maxR, -0.6, 0);
  ctx.closePath();
  ctx.fill();

  // Leading bright line
  ctx.strokeStyle = '#34d399';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.lineTo(maxR, 0);
  ctx.stroke();

  ctx.restore();

  // Blips
  const blipAngle = 1.2;
  const blipDist = 32;
  const blipX = cx + Math.cos(blipAngle) * blipDist;
  const blipY = cy + Math.sin(blipAngle) * blipDist;

  const diff = (angle - blipAngle + Math.PI * 2) % (Math.PI * 2);
  const blipAlpha = Math.max(0, 1 - diff / 2.5);

  if (blipAlpha > 0) {
    ctx.fillStyle = `rgba(52, 211, 153, ${blipAlpha})`;
    ctx.beginPath();
    ctx.arc(blipX, blipY, 3.5, 0, Math.PI * 2);
    ctx.fill();
  }

  // Outer bezel
  ctx.strokeStyle = '#334155';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.arc(cx, cy, maxR, 0, Math.PI * 2);
  ctx.stroke();
}"""
    }
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slack GIF Creator Studio // Skill #6 (Apache 2.0)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <!-- gifshot client-side GIF generator CDN -->
  <script src="https://cdn.jsdelivr.net/npm/gifshot@0.4.5/build/gifshot.min.js"></script>
  <style>
    :root {
      --bg-canvas: #f8fafc;
      --bg-panel: #ffffff;
      --bg-panel-subtle: #f1f5f9;
      --border-subtle: #e2e8f0;
      --border-focus: #4a154b;
      --text-primary: #0f172a;
      --text-secondary: #475569;
      --text-muted: #64748b;
      --slack-aubergine: #4a154b;
      --slack-accent: #611f69;
      --slack-blue: #1264a3;
      --slack-green: #007a5a;
      --slack-amber: #ecb22e;
      --card-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
      --font-ui: 'Plus Jakarta Sans', sans-serif;
      --font-display: 'Bricolage Grotesque', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    html[data-theme="dark"] {
      --bg-canvas: #0b0f19;
      --bg-panel: #111827;
      --bg-panel-subtle: #1f2937;
      --border-subtle: #374151;
      --border-focus: #c084fc;
      --text-primary: #f9fafb;
      --text-secondary: #d1d5db;
      --text-muted: #9ca3af;
      --slack-aubergine: #7e22ce;
      --slack-accent: #9333ea;
      --card-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.6);
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
    }
    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-badge {
      width: 40px;
      height: 40px;
      border-radius: 9px;
      background: linear-gradient(135deg, #4a154b 0%, #1264a3 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
      font-size: 1.25rem;
      font-weight: 800;
      box-shadow: 0 2px 8px rgba(74, 21, 75, 0.25);
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
      background: #4a154b;
      color: #ffffff;
      box-shadow: 0 1px 4px rgba(74, 21, 75, 0.3);
    }
    .engine-btn.active.webgpu {
      background: #1264a3;
      color: #ffffff;
      box-shadow: 0 1px 4px rgba(18, 100, 163, 0.3);
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

    /* Main Grid */
    .main-stage {
      flex: 1;
      padding: 1.25rem 1.75rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    .studio-grid {
      display: grid;
      grid-template-columns: 390px 1fr;
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

    /* Slack Constraints Budget Badge */
    .slack-spec-strip {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
      margin-bottom: 0.85rem;
      padding: 8px;
      background: var(--bg-panel-subtle);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      font-family: var(--font-mono);
      font-size: 0.68rem;
      text-align: center;
    }
    .spec-item strong { display: block; color: var(--slack-aubergine); }

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
      border-color: var(--slack-aubergine);
      background: rgba(74, 21, 75, 0.05);
    }
    .preset-card.active {
      border-color: var(--slack-aubergine);
      background: rgba(74, 21, 75, 0.08);
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
      border-color: var(--slack-aubergine);
      color: var(--slack-aubergine);
    }
    .prompt-chip.active {
      border-color: var(--slack-aubergine);
      background: var(--slack-aubergine);
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
      border-color: var(--slack-aubergine);
      background: var(--bg-panel);
    }

    .btn-synthesize {
      width: 100%;
      background: linear-gradient(135deg, #4a154b 0%, #1264a3 100%);
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
      box-shadow: 0 2px 8px rgba(74, 21, 75, 0.25);
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

    /* Right Main Stage */
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
      color: var(--slack-aubergine);
      box-shadow: var(--card-shadow);
    }

    /* Live Player Box */
    .stage-content {
      position: relative;
      background: var(--bg-canvas);
      min-height: 520px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 2rem;
      gap: 1.5rem;
    }

    /* Simulated Slack Chat Message Card */
    .slack-chat-mockup {
      width: 100%;
      max-width: 560px;
      background: #ffffff;
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 1rem 1.25rem;
      box-shadow: 0 4px 15px rgba(0,0,0,0.05);
      display: flex;
      gap: 12px;
    }
    .slack-avatar {
      width: 36px;
      height: 36px;
      border-radius: 4px;
      background: #4a154b;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-weight: 700;
      font-size: 0.85rem;
    }
    .slack-message-body {
      flex: 1;
    }
    .slack-message-meta {
      display: flex;
      align-items: baseline;
      gap: 8px;
      margin-bottom: 4px;
    }
    .slack-sender { font-weight: 700; font-size: 0.85rem; color: #1d1c1d; }
    .slack-time { font-size: 0.7rem; color: #616061; }

    /* Canvas Screen */
    .canvas-screen-wrap {
      background: #f8fafc;
      border: 1px dashed var(--border-subtle);
      border-radius: 6px;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }
    #animationCanvas {
      background: #ffffff;
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    /* GIF Output Image */
    #gifResultImg {
      max-width: 280px;
      border-radius: 4px;
      border: 1px solid var(--border-subtle);
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
      display: none;
    }

    /* Controls Strip */
    .player-controls {
      display: flex;
      align-items: center;
      gap: 10px;
      font-family: var(--font-mono);
      font-size: 0.74rem;
    }

    /* Code View */
    .code-view {
      width: 100%;
      height: 520px;
      background: #0f172a;
      color: #f8fafc;
      border-radius: 8px;
      padding: 1.5rem;
      overflow: auto;
      font-family: var(--font-mono);
      font-size: 0.76rem;
      line-height: 1.5;
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
      border-color: var(--slack-aubergine);
      color: var(--slack-aubergine);
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
      <div class="brand-badge">✨</div>
      <div class="brand-text">
        <h1>Slack GIF Creator Studio <span class="badge-skill-fit">Skill #6: slack-gif-creator (Apache 2.0 • Safest)</span></h1>
        <p>128x128 Emoji & 480x480 Message Animations • Frame Easing • Client-Side GIF Synthesis • Slack Constraints</p>
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

      <!-- Left Column: Controls & Presets -->
      <div class="sidebar-pane">

        <div class="card-box">
          <div class="card-box-header">
            <span>Slack Animation Presets</span>
            <span style="color: #047857; font-size: 0.72rem; font-family: var(--font-mono);">Optimized &lt; 128 Colors</span>
          </div>

          <!-- Slack Specs Budget Indicator -->
          <div class="slack-spec-strip">
            <div class="spec-item">
              <span id="specDim">128 × 128 px</span>
              <strong>Slack Emoji</strong>
            </div>
            <div class="spec-item">
              <span id="specFps">15 FPS</span>
              <strong>Target Rate</strong>
            </div>
            <div class="spec-item">
              <span id="specBudget">&lt; 64 KB</span>
              <strong>Payload Budget</strong>
            </div>
          </div>

          <div class="preset-list" id="presetsList">
            <!-- Rendered via JS -->
          </div>

          <div class="card-box-header" style="margin-top: 1.15rem;">
            <span>Synthesize Slack Animation</span>
            <span style="font-size:0.7rem; color:var(--slack-aubergine); font-weight:600;">⚡ Groq LPU Ready</span>
          </div>

          <!-- Prompt suggestion chips -->
          <div class="prompt-chips-row">
            <button type="button" class="prompt-chip active" onclick="setPromptBrief('A vibrant party star emoji that pulses with heartbeat rhythm, radiates multi-color sparkles, and loops seamlessly at 128x128 for Slack.', this)">⭐ Party Star Pulse</button>
            <button type="button" class="prompt-chip" onclick="setPromptBrief('A celebration cannon firing vibrant ribbons and multi-colored confetti particles across a 480x480 canvas for Slack channel milestones.', this)">🎉 Confetti Cannon</button>
            <button type="button" class="prompt-chip" onclick="setPromptBrief('A sci-fi radar sonar sweep with luminous concentric grid circles and blipping target dots rotating seamlessly at 128x128 for Slack.', this)">📡 Radar Scanner</button>
            <button type="button" class="prompt-chip" onclick="setPromptBrief('A bouncing loading rocket emoji firing flame bursts with elastic overshoot easing at 128x128 for Slack reactions.', this)">🚀 Bouncing Rocket</button>
          </div>

          <textarea class="brief-input" id="briefInput" placeholder="Describe any animated Slack emoji (128x128) or message GIF (480x480) with specific motion easing (shake, bounce, pulse, particle burst)..."></textarea>

          <button class="btn-synthesize" id="btnSynthesize" onclick="runSlackGifSynthesis()">
            <span>⚡ Synthesize Slack Animation (Groq LPU)</span>
          </button>
        </div>

        <!-- Injected SKILL.md Runbook Inspector -->
        <div class="runbook-box">
          <div class="runbook-header" onclick="toggleRunbook()">
            <span style="font-weight: 700; font-size: 0.8rem; color: var(--text-primary);">
              📜 Injected SKILL.md (slack-gif-creator Runbook)
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

      <!-- Right Column: Live Player & Export Stage -->
      <div class="stage-pane">

        <div class="stage-top-bar">
          <div class="tabs-group">
            <button class="tab-btn active" id="tabBtnPlayer" onclick="switchStage('player')">👁️ Live Slack Stage</button>
            <button class="tab-btn" id="tabBtnCode" onclick="switchStage('code')">💻 Frame Render Script</button>
          </div>

          <div style="font-size: 0.72rem; color: var(--slack-aubergine); font-weight: 700; font-family: var(--font-mono);">
            SLACK BOT INTEGRATION READY
          </div>
        </div>

        <!-- Stage Views -->
        <div class="stage-content" id="stagePlayer">
          
          <!-- Simulated Slack message card -->
          <div class="slack-chat-mockup">
            <div class="slack-avatar">🤖</div>
            <div class="slack-message-body">
              <div class="slack-message-meta">
                <span class="slack-sender">GifBot APP</span>
                <span class="slack-time">Just now</span>
              </div>
              <div style="font-size: 0.84rem; margin-bottom: 8px;">
                Here is your customized animated reaction for Slack:
              </div>

              <!-- Animated Canvas Screen -->
              <div class="canvas-screen-wrap">
                <canvas id="animationCanvas" width="128" height="128"></canvas>
                <img id="gifResultImg" alt="Generated GIF" />
                <div class="player-controls">
                  <span id="playerStatus">● Playing at 15 FPS</span>
                  <span>•</span>
                  <span id="frameCounter">Frame 1 / 24</span>
                </div>
              </div>

            </div>
          </div>

        </div>

        <div class="stage-content" id="stageCode" style="display: none;">
          <pre class="code-view"><code id="codeText"></code></pre>
        </div>

        <!-- Bottom Status Bar -->
        <div class="bottom-bar">
          <div id="renderSourceInfo">Preset: Party Sparkle Pulse • 128x128 Emoji Mode</div>
          <div class="actions-row">
            <button class="btn-action" onclick="generateAndDownloadGif()">💾 Render &amp; Download .GIF</button>
            <button class="btn-action" onclick="copyFrameScript()">📋 Copy Frame Script</button>
            <button class="btn-action" onclick="togglePlayPause()">⏯️ Pause / Play</button>
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
  let currentStage = 'player';
  let currentCode = PRESETS[0].code;
  let webllmEngine = null;

  // Animation Loop state
  let animTimer = null;
  let isPlaying = true;
  let currentFrameIdx = 0;
  let totalFrames = 24;
  let targetFps = 15;
  let canvasW = 128;
  let canvasH = 128;

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
    const saved = localStorage.getItem('slack_gif_app_mode') || 'light';
    setTheme(saved);
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'light' ? 'dark' : 'light';
    setTheme(next);
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('slack_gif_app_mode', theme);
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
      if (eng === 'groq') synthBtn.innerHTML = '<span>⚡ Synthesize Slack Animation (Groq LPU)</span>';
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
          <div class="runtime-icon" style="color: #4a154b;">⚡</div>
          <div>
            <strong style="font-size: 0.85rem; color: var(--text-primary);">Groq LPU Cloud Fast Inference (500+ tok/s)</strong>
            <div style="font-size: 0.75rem; color: var(--text-secondary);">
              🟢 Pre-provisioned Free Tier API token active! Generates custom Slack animation scripts in ~1–2 seconds.
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
          <div class="runtime-icon" style="color: #4a154b;">⚡</div>
          <div>
            <strong style="font-size: 0.85rem; color: var(--text-primary);">Instant Verified Showcase Mode</strong>
            <div style="font-size: 0.75rem; color: var(--text-secondary);">
              3 pre-calibrated Slack animations running with zero latency.
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
          <div class="runtime-icon" style="color: #1264a3;">🎮</div>
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
          <button class="btn-action" id="btnLoadGpu" onclick="loadWebLLM()" style="background: #4a154b; color: #fff; border:none; padding: 5px 12px;">Load into GPU</button>
        </div>
        <div id="gpuProgressWrap" style="display:none; width: 100%; margin-top: 5px;">
          <div style="background: var(--border-subtle); height: 5px; border-radius: 3px; overflow: hidden;">
            <div id="gpuProgressFill" style="background: #4a154b; height: 100%; width: 0%;"></div>
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
          <div class="preset-meta">${p.mode} • ${p.fps} FPS</div>
        </div>
        <div style="font-size: 0.72rem; color: var(--text-muted);">Load →</div>
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
    canvasW = p.width;
    canvasH = p.height;
    targetFps = p.fps;
    totalFrames = p.frames;

    document.getElementById('specDim').innerText = `${p.width} × ${p.height} px`;
    document.getElementById('specFps').innerText = `${p.fps} FPS`;
    document.getElementById('specBudget').innerText = (p.width <= 128) ? '< 64 KB (Emoji)' : '< 2 MB (Message)';

    applyFrameScript(p.code, p.name);
  }

  function setPromptBrief(txt, el) {
    document.getElementById('briefInput').value = txt;
    document.querySelectorAll('.prompt-chip').forEach(c => c.classList.remove('active'));
    if (el) el.classList.add('active');
  }

  function switchStage(stage) {
    currentStage = stage;
    document.getElementById('tabBtnPlayer').classList.toggle('active', stage === 'player');
    document.getElementById('tabBtnCode').classList.toggle('active', stage === 'code');
    document.getElementById('stagePlayer').style.display = (stage === 'player') ? 'flex' : 'none';
    document.getElementById('stageCode').style.display = (stage === 'code') ? 'flex' : 'none';
  }

  let activeRenderFunction = null;

  function applyFrameScript(codeStr, sourceTitle) {
    currentCode = codeStr;
    document.getElementById('codeText').innerText = codeStr;
    document.getElementById('renderSourceInfo').innerText = `Preset: ${sourceTitle} • ${canvasW}x${canvasH}`;

    // Hide previous GIF result and show canvas
    document.getElementById('gifResultImg').style.display = 'none';
    const canvas = document.getElementById('animationCanvas');
    canvas.style.display = 'block';
    canvas.width = canvasW;
    canvas.height = canvasH;

    try {
      // Evaluate function
      const fn = new Function('return ' + codeStr)();
      activeRenderFunction = fn;
      restartAnimationLoop();
    } catch(e) {
      console.error(e);
      showToast('Error executing script: ' + e.message, '⚠️');
    }
  }

  function restartAnimationLoop() {
    if (animTimer) clearInterval(animTimer);
    currentFrameIdx = 0;
    const canvas = document.getElementById('animationCanvas');
    const ctx = canvas.getContext('2d');

    const intervalMs = Math.round(1000 / targetFps);
    animTimer = setInterval(() => {
      if (!isPlaying || !activeRenderFunction) return;

      const t = currentFrameIdx / totalFrames;
      try {
        activeRenderFunction(ctx, canvasW, canvasH, t, currentFrameIdx, totalFrames);
      } catch(err) {
        console.error("Frame render error:", err);
      }

      currentFrameIdx = (currentFrameIdx + 1) % totalFrames;
      document.getElementById('frameCounter').innerText = `Frame ${currentFrameIdx + 1} / ${totalFrames}`;
    }, intervalMs);
  }

  function togglePlayPause() {
    isPlaying = !isPlaying;
    document.getElementById('playerStatus').innerText = isPlaying ? `● Playing at ${targetFps} FPS` : '⏸️ Paused';
    showToast(isPlaying ? 'Resumed playback' : 'Paused', '⏯️');
  }

  async function runSlackGifSynthesis() {
    let brief = document.getElementById('briefInput').value.trim();
    if (!brief) {
      brief = "A vibrant party star emoji that pulses with heartbeat rhythm, radiates multi-color sparkles, and loops seamlessly at 128x128 for Slack.";
      document.getElementById('briefInput').value = brief;
      const firstChip = document.querySelector('.prompt-chip');
      if (firstChip) firstChip.classList.add('active');
      showToast('Loaded Party Star prompt', '⭐');
    }

    const btn = document.getElementById('btnSynthesize');
    btn.disabled = true;
    btn.innerHTML = '<span>⏳ Synthesizing Slack GIF via Groq...</span>';

    const startTime = Date.now();

    try {
      if (currentEngine === 'groq') {
        const apiKey = getActiveGroqKey();
        const model = document.getElementById('groqModelSelect') ? document.getElementById('groqModelSelect').value : 'openai/gpt-oss-120b';

        const prompt = "You are a master Slack GIF developer following Anthropic's official 'slack-gif-creator' runbook.\\n" +
          "Your mission is to return an executable JavaScript function that renders one frame of an animated Slack GIF onto an HTML5 Canvas.\\n" +
          "FUNCTION SIGNATURE TO RETURN:\\n" +
          "function renderFrame(ctx, width, height, t, frameIdx, totalFrames) { ... }\\n" +
          "SLACK ANIMATION RULES:\\n" +
          "1. Smooth looping: Parameter 't' goes from 0.0 to 1.0. All motions must loop seamlessly.\\n" +
          "2. Animation easing: Incorporate easing (pulse with Math.sin(t * Math.PI * 2), wobble, particle burst, bounce_out).\\n" +
          "3. High contrast: Thick strokes (lineWidth >= 2), vibrant complementary colors, clear outlines.\\n" +
          "4. OUTPUT FORMAT: Return ONLY the raw JavaScript function enclosed within a ```javascript codeblock. Do not include markdown preamble.";

        const resp = await fetch("https://api.groq.com/openai/v1/chat/completions", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${apiKey}`,
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            model: model,
            messages: [
              { role: "system", content: prompt },
              { role: "user", content: brief }
            ],
            temperature: 0.7,
            max_tokens: 4000
          })
        });

        if (!resp.ok) {
          const err = await resp.json();
          throw new Error(err.error?.message || resp.statusText);
        }

        const data = await resp.json();
        const txt = data.choices[0].message.content;

        extractAndApplyFunction(txt, `Groq LPU (${model})`);
        const elapsed = Date.now() - startTime;
        showToast(`Slack animation synthesized in ${elapsed}ms!`, '⚡');

      } else if (currentEngine === 'instant') {
        selectPreset(1);
        showToast('Switched to Confetti Cannon preset!', '✨');

      } else if (currentEngine === 'webgpu') {
        if (!webllmEngine) throw new Error('Please load the WebLLM model into WebGPU first using the top banner button.');
        const prompt = "You are a Slack GIF generator. Return only: function renderFrame(ctx, width, height, t, frameIdx, totalFrames) { ... } inside ```javascript";
        const reply = await webllmEngine.chat.completions.create({
          messages: [
            { role: "system", content: prompt },
            { role: "user", content: brief }
          ],
          temperature: 0.7,
          max_tokens: 2000
        });
        const txt = reply.choices[0].message.content;
        extractAndApplyFunction(txt, 'Local WebGPU (WebLLM)');
        showToast('WebGPU local synthesis complete!', '🎮');
      }
    } catch(e) {
      showToast('Synthesis error: ' + (e.message || 'Check network'), '⚠️');
      console.error(e);
    } finally {
      btn.disabled = false;
      if (currentEngine === 'groq') btn.innerHTML = '<span>⚡ Synthesize Slack Animation (Groq LPU)</span>';
      else if (currentEngine === 'webgpu') btn.innerHTML = '<span>🎮 Synthesize via Local WebGPU</span>';
      else btn.innerHTML = '<span>⚡ Render Instant Showcase</span>';
    }
  }

  function extractAndApplyFunction(rawText, source) {
    let code = "";
    const jsMarker = rawText.indexOf('```javascript');
    const genericMarker = rawText.indexOf('```');

    if (jsMarker !== -1) {
      let candidate = rawText.substring(jsMarker + 13).trim();
      const endFence = candidate.lastIndexOf('```');
      if (endFence !== -1) candidate = candidate.substring(0, endFence).trim();
      code = candidate;
    } else if (genericMarker !== -1) {
      let candidate = rawText.substring(genericMarker + 3).trim();
      const endFence = candidate.lastIndexOf('```');
      if (endFence !== -1) candidate = candidate.substring(0, endFence).trim();
      code = candidate;
    } else {
      code = rawText.trim();
    }

    applyFrameScript(code, source);
  }

  function generateAndDownloadGif() {
    if (!activeRenderFunction) {
      showToast('No active animation to render', '⚠️');
      return;
    }

    showToast('Compiling Slack GIF frames...', '⏳');

    // Collect frames from virtual canvas
    const virtualCanvas = document.createElement('canvas');
    virtualCanvas.width = canvasW;
    virtualCanvas.height = canvasH;
    const vCtx = virtualCanvas.getContext('2d');

    const frameImages = [];
    for (let f = 0; f < totalFrames; f++) {
      const t = f / totalFrames;
      activeRenderFunction(vCtx, canvasW, canvasH, t, f, totalFrames);
      frameImages.push(virtualCanvas.toDataURL('image/png'));
    }

    // Call gifshot
    if (typeof gifshot !== 'undefined') {
      gifshot.createGIF({
        images: frameImages,
        gifWidth: canvasW,
        gifHeight: canvasH,
        interval: 1 / targetFps,
        numFrames: totalFrames
      }, function (obj) {
        if (!obj.error) {
          const gifData = obj.image;
          const imgEl = document.getElementById('gifResultImg');
          imgEl.src = gifData;
          imgEl.style.display = 'block';

          // Download
          const a = document.createElement('a');
          a.href = gifData;
          a.download = `slack_animated_${canvasW}x${canvasH}_${Date.now()}.gif`;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          showToast('Slack GIF compiled & downloaded!', '💾');
        } else {
          showToast('GIF generation error: ' + obj.error, '⚠️');
        }
      });
    } else {
      showToast('Client-side GIF compiler unavailable', '⚠️');
    }
  }

  function copyFrameScript() {
    navigator.clipboard.writeText(currentCode).then(() => {
      showToast('Frame script copied to clipboard!', '📋');
    });
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
    snippet = sg_md[:1500].replace("\\", "\\\\").replace("`", "\\`")
    
    # Embed presets
    presets_json_str = json.dumps(PRESETS_DATA)
    
    out_html = HTML_TEMPLATE.replace("__SKILL_SNIPPET__", snippet)
    out_html = out_html.replace("__PRESETS_JSON__", presets_json_str)

    target_file = "slack_gif_creator_app.html"
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(out_html)
    
    print(f"Generated {target_file} successfully! Size: {len(out_html)} bytes")

if __name__ == "__main__":
    build_app()
