# -*- coding: utf-8 -*-
"""
Generates a stunning, intuitive, graphical, and fun One-Pager PDF:
"Capturing the World Invariant: The Foundation of Ground Truth"
Uses Playwright to print a crisp, pixel-perfect single-page PDF.
"""
import asyncio
import os
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Capturing the World Invariant — Ground Truth One-Pager</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    @page {
      size: letter portrait;
      margin: 0;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }

    body {
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      background: #ffffff;
      color: #0f172a;
      width: 8.5in;
      height: 11in;
      padding: 0.42in 0.45in;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    /* HEADER BANNER */
    .header {
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }
    .brand-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #eff6ff;
      color: #1d4ed8;
      border: 1px solid #bfdbfe;
      padding: 3px 9px;
      border-radius: 999px;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 6px;
    }
    h1 {
      font-size: 24px;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.02em;
      line-height: 1.15;
    }
    .subtitle {
      font-size: 11.5px;
      color: #475569;
      margin-top: 3px;
    }
    .header-badge {
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      padding: 6px 12px;
      border-radius: 8px;
      text-align: right;
    }
    .header-badge .label { font-size: 9px; text-transform: uppercase; color: #64748b; font-weight: 700; }
    .header-badge .val { font-size: 12px; font-weight: 800; color: #0284c7; }

    /* CORE THESIS CALLOUT */
    .thesis-card {
      background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
      border: 1.5px solid #a7f3d0;
      border-radius: 10px;
      padding: 10px 14px;
      display: flex;
      gap: 12px;
      align-items: center;
      margin: 10px 0;
    }
    .thesis-icon {
      font-size: 28px;
      flex-shrink: 0;
    }
    .thesis-text h2 {
      font-size: 12px;
      font-weight: 800;
      color: #065f46;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .thesis-text p {
      font-size: 10.5px;
      color: #047857;
      line-height: 1.45;
      margin-top: 2px;
    }

    /* THE THREE WORLDS SECTION */
    .section-title {
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #334155;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .worlds-grid {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 10px;
      margin-bottom: 10px;
    }
    .world-card {
      border: 1.5px solid #e2e8f0;
      border-radius: 10px;
      padding: 10px;
      background: #ffffff;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .world-card.literature { border-top: 4px solid #f59e0b; background: #fffdfa; }
    .world-card.security { border-top: 4px solid #3b82f6; background: #fbfdff; }
    .world-card.physics { border-top: 4px solid #10b981; background: #fbfffd; }
    
    .world-header {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 6px;
    }
    .world-icon { font-size: 18px; }
    .world-name { font-size: 11.5px; font-weight: 800; color: #1e293b; }
    .world-sub { font-size: 9px; color: #64748b; }
    
    .invariant-box {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 6px 8px;
      margin: 4px 0;
      font-size: 9.5px;
      line-height: 1.4;
    }
    .invariant-box strong { color: #0f172a; display: block; font-size: 9px; text-transform: uppercase; margin-bottom: 2px; }
    .invariant-box.law { background: #fef2f2; border-color: #fecaca; color: #991b1b; }
    .invariant-box.law strong { color: #b91c1c; }

    .agent-action {
      margin-top: auto;
      padding-top: 6px;
      border-top: 1px dashed #cbd5e1;
      font-size: 9px;
      color: #475569;
      line-height: 1.35;
    }
    .agent-action span { font-weight: 700; color: #1e293b; }

    /* HOW TO CAPTURE IT: THE 3 GOLDEN PRINCIPLES */
    .principles-grid {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 10px;
      margin-bottom: 10px;
    }
    .principle-card {
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 9px 10px;
    }
    .principle-num {
      display: inline-block;
      width: 18px;
      height: 18px;
      background: #0284c7;
      color: #ffffff;
      font-size: 10px;
      font-weight: 800;
      text-align: center;
      line-height: 18px;
      border-radius: 50%;
      margin-bottom: 4px;
    }
    .principle-title {
      font-size: 10.5px;
      font-weight: 800;
      color: #0f172a;
      margin-bottom: 3px;
    }
    .principle-desc {
      font-size: 9px;
      color: #475569;
      line-height: 1.4;
    }

    /* THE VISUAL PIPELINE */
    .pipeline-card {
      background: #f8fafc;
      border: 1.5px solid #cbd5e1;
      border-radius: 10px;
      padding: 10px 14px;
      margin-bottom: 10px;
    }
    .pipeline-flex {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin-top: 4px;
    }
    .pipe-step {
      flex: 1;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 6px 8px;
      text-align: center;
      box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .pipe-step .badge {
      font-size: 8px;
      font-weight: 800;
      text-transform: uppercase;
      padding: 2px 5px;
      border-radius: 4px;
      display: inline-block;
      margin-bottom: 3px;
    }
    .pipe-step .title { font-size: 9.5px; font-weight: 800; color: #1e293b; }
    .pipe-step .detail { font-size: 8px; color: #64748b; margin-top: 1px; }
    .pipe-arrow { font-size: 14px; color: #94a3b8; font-weight: 800; flex-shrink: 0; }

    /* FOOTER */
    .footer {
      border-top: 1.5px solid #e2e8f0;
      padding-top: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 9px;
      color: #64748b;
    }
    .footer-left { display: flex; gap: 12px; align-items: center; }
    .footer-tag { font-weight: 700; color: #0284c7; }
  </style>
</head>
<body>

  <!-- HEADER -->
  <div>
    <div class="header">
      <div>
        <div class="brand-pill">📘 GroundTruth Architecture Suite</div>
        <h1>Capturing the World Invariant</h1>
        <div class="subtitle">How to extract absolute environmental truths without imagining numbers or hallucinating rules.</div>
      </div>
      <div class="header-badge">
        <div class="label">Architecture Standard</div>
        <div class="val">Zero Hallucination</div>
      </div>
    </div>

    <!-- CORE THESIS CALLOUT -->
    <div class="thesis-card">
      <div class="thesis-icon">🧭</div>
      <div class="thesis-text">
        <h2>The Golden Principle of Ground Truth</h2>
        <p><strong>Capture the essentials of the text so that interpretation will never deviate away from the ground truth.</strong> Downstream interpretation naturally drifts into hallucination when unconstrained. Extracting irreducible world invariants creates an unbreakable contract that keeps agent reasoning permanently grounded.</p>
      </div>
    </div>

    <!-- THE THREE WORLDS SECTION -->
    <div class="section-title"><span>🌐</span> Ground Truth in Action: Three Different Worlds</div>
    <div class="worlds-grid">
      
      <!-- WORLD 1: LITERATURE -->
      <div class="world-card literature">
        <div class="world-header">
          <div class="world-icon">📖</div>
          <div>
            <div class="world-name">Literature / Fiction</div>
            <div class="world-sub">e.g., Where the Mountain Meets the Moon</div>
          </div>
        </div>
        <div class="invariant-box law">
          <strong>World Physics Invariant</strong>
          "Nothing grows on Fruitless Mountain, and birds and animals do not rest there."
        </div>
        <div class="invariant-box">
          <strong>Character Axiom</strong>
          Minli has a habit of quick thinking and impulsive action ("Too well," sighed her mother).
        </div>
        <div class="agent-action">
          <span>Agent Boundary:</span> Cannot invent farms on Fruitless Mountain; must route agent into a departure quest.
        </div>
      </div>

      <!-- WORLD 2: ENTERPRISE IT -->
      <div class="world-card security">
        <div class="world-header">
          <div class="world-icon">🛡️</div>
          <div>
            <div class="world-name">Enterprise IT Security</div>
            <div class="world-sub">e.g., SOC2 Production Access Policy</div>
          </div>
        </div>
        <div class="invariant-box law">
          <strong>Constitutional Invariant</strong>
          Hardware FIDO2 WebAuthn is strictly required; legacy SMS OTP is permanently revoked.
        </div>
        <div class="invariant-box">
          <strong>Time-Bound Ceilings</strong>
          Direct DB write lease max TTL: 4 hours. Emergency Break-Glass token hard cap: 2 hours.
        </div>
        <div class="agent-action">
          <span>Agent Boundary:</span> Auto-rejects peer approvals; triggers SOC2 alerts if break-glass exceeds 7,200s.
        </div>
      </div>

      <!-- WORLD 3: PHYSICAL CONTROL -->
      <div class="world-card physics">
        <div class="world-header">
          <div class="world-icon">⚙️</div>
          <div>
            <div class="world-name">Industrial Physics & MPC</div>
            <div class="world-sub">e.g., Model Predictive Control</div>
          </div>
        </div>
        <div class="invariant-box law">
          <strong>Physical Law Invariant</strong>
          Conservation of mass; process bounds dwell in [u_min, u_max] under bounded disturbances.
        </div>
        <div class="invariant-box">
          <strong>Receding Horizon Invariant</strong>
          Solves finite horizon [t, t+T]; executes only 1st step u(t); shifts horizon forward.
        </div>
        <div class="agent-action">
          <span>Agent Boundary:</span> If QP solver is infeasible, cannot guess an action—must trip emergency safe hold.
        </div>
      </div>

    </div>

    <!-- HOW TO CAPTURE IT: THE 3 GOLDEN PRINCIPLES -->
    <div class="section-title"><span>🔍</span> How to Extract Invariants (The 3 Golden Principles)</div>
    <div class="principles-grid">
      
      <div class="principle-card">
        <div class="principle-num">1</div>
        <div class="principle-title">Never Hallucinate Constants</div>
        <div class="principle-desc">
          If Wikipedia defines a cost function algebraically as J = ∑w(r-x)², <strong>do not fabricate a 42.0 kPa limit</strong>. Ground truth means expressing algebraic constraints when numbers are unspecified.
        </div>
      </div>

      <div class="principle-card">
        <div class="principle-num">2</div>
        <div class="principle-title">Environment Physics ≠ Agent Strategy</div>
        <div class="principle-desc">
          Separate what the <em>world enforces</em> from what an actor <em>chooses</em>. Policies can be negotiated; world invariants (gravity, expiration timers, barren soil) never bend for any prompt.
        </div>
      </div>

      <div class="principle-card">
        <div class="principle-num">3</div>
        <div class="principle-title">Every Invariant Needs a Tripwire</div>
        <div class="principle-desc">
          An invariant is useless as passive prose. It must be wired into the execution DAG as a <strong>circuit breaker</strong>: if an observed state crosses the boundary, execution freezes instantly.
        </div>
      </div>

    </div>

    <!-- THE GROUNDTRUTH REASONING PIPELINE -->
    <div class="section-title"><span>⚡</span> The GroundTruth Execution Pipeline</div>
    <div class="pipeline-card">
      <div class="pipeline-flex">
        
        <div class="pipe-step">
          <span class="badge" style="background:#e0f2fe; color:#0369a1;">Step 1: Ingest</span>
          <div class="title">Raw Source</div>
          <div class="detail">Novel, SOP, or API Route</div>
        </div>

        <div class="pipe-arrow">➔</div>

        <div class="pipe-step">
          <span class="badge" style="background:#fef3c7; color:#92400e;">Step 2: Filter</span>
          <div class="title">Absolutes & Negations</div>
          <div class="detail">"Never", "Prohibited", Limits</div>
        </div>

        <div class="pipe-arrow">➔</div>

        <div class="pipe-step">
          <span class="badge" style="background:#ede9fe; color:#6d28d9;">Step 3: Structure</span>
          <div class="title">5-Tier Policy Tree</div>
          <div class="detail">Root Invariants ➔ Bounds</div>
        </div>

        <div class="pipe-arrow">➔</div>

        <div class="pipe-step">
          <span class="badge" style="background:#fee2e2; color:#b91c1c;">Step 4: Guard</span>
          <div class="title">DAG Tripwire Gate</div>
          <div class="detail">Circuit Breaker Fallback</div>
        </div>

        <div class="pipe-arrow">➔</div>

        <div class="pipe-step">
          <span class="badge" style="background:#ecfdf5; color:#065f46;">Step 5: Verify</span>
          <div class="title">Reliable Agent</div>
          <div class="detail">100% Deterministic Safety</div>
        </div>

      </div>
    </div>
  </div>

  <!-- FOOTER -->
  <div class="footer">
    <div class="footer-left">
      <div><span class="footer-tag">GroundTruth Studio</span> • Systems Engineering for Agent Reliability</div>
      <div>•</div>
      <div>Client-Side WebGPU & Groq LPU Traceability</div>
    </div>
    <div>Live Hub: <strong>https://cosmosanalytics.github.io/Langchain-test/</strong></div>
  </div>

</body>
</html>
"""

async def generate():
    html_path = "scratch/world_invariant_one_pager.html"
    pdf_path = "scratch/world_invariant_one_pager.pdf"
    png_path = "scratch/world_invariant_one_pager.png"
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Wrote HTML to {html_path}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='chrome')
        page = await browser.new_page()
        await page.goto(f"file:///{os.path.abspath(html_path)}")
        await page.wait_for_timeout(1000)

        # Print PDF
        await page.pdf(
            path=pdf_path,
            format='Letter',
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
        )
        print(f"Generated PDF at {pdf_path}")

        # Capture high-res PNG preview
        await page.screenshot(path=png_path, full_page=True)
        print(f"Captured PNG preview at {png_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(generate())
