# -*- coding: utf-8 -*-
"""
Generates an executive-grade, simple, intuitive, graphical, and fun 1-pager PDF:
"Ensuring Text-Based Invariants: How to Turn Prose into Unbreakable Guardrails"
Exactly 1 page, crisp light mode, visual diagrams, and fun analogies!
"""
import sys
import os
from playwright.sync_api import sync_playwright
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Ensuring Text-Based Invariants — Ground Truth One-Pager</title>
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
      padding: 0.38in 0.42in;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    /* HEADER BANNER */
    .header {
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }
    .brand-pill {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: #eff6ff;
      color: #1d4ed8;
      border: 1px solid #bfdbfe;
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 9.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 4px;
    }
    h1 {
      font-size: 21.5px;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.02em;
      line-height: 1.15;
    }
    .subtitle {
      font-size: 11px;
      color: #475569;
      margin-top: 2px;
    }
    .header-badge {
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      padding: 5px 10px;
      border-radius: 8px;
      text-align: right;
    }
    .header-badge .label { font-size: 8.5px; text-transform: uppercase; color: #64748b; font-weight: 700; }
    .header-badge .val { font-size: 11.5px; font-weight: 800; color: #0284c7; }

    /* CORE GOLDEN AXIOM BANNER */
    .axiom-banner {
      background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
      border: 1.5px solid #f59e0b;
      border-radius: 8px;
      padding: 8px 12px;
      margin: 8px 0;
      display: flex;
      gap: 10px;
      align-items: center;
    }
    .axiom-icon { font-size: 24px; flex-shrink: 0; }
    .axiom-title { font-size: 10.5px; font-weight: 800; color: #b45309; text-transform: uppercase; }
    .axiom-quote { font-size: 11.5px; font-weight: 800; color: #0f172a; margin-top: 1px; }
    .axiom-sub { font-size: 9.5px; color: #78350f; margin-top: 1px; }

    /* THE FUN ANALOGY CARD (PROMPT VS FENCE) */
    .analogy-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 8px;
    }
    .analogy-card {
      border-radius: 8px;
      padding: 8px 10px;
      border: 1.5px solid #e2e8f0;
      display: flex;
      gap: 8px;
      align-items: flex-start;
    }
    .analogy-card.bad {
      background: #fef2f2;
      border-color: #fca5a5;
    }
    .analogy-card.good {
      background: #f0fdf4;
      border-color: #86efac;
    }
    .analogy-emoji { font-size: 22px; flex-shrink: 0; }
    .analogy-text h3 { font-size: 11px; font-weight: 800; margin-bottom: 2px; }
    .analogy-card.bad h3 { color: #dc2626; }
    .analogy-card.good h3 { color: #16a34a; }
    .analogy-text p { font-size: 9.5px; line-height: 1.4; color: #334155; }

    /* SECTION TITLE */
    .section-title {
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #334155;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 5px;
    }

    /* 4-PILLAR MECHANISMS GRID */
    .pillars-grid {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr 1fr;
      gap: 8px;
      margin-bottom: 8px;
    }
    .pillar-card {
      border: 1.5px solid #e2e8f0;
      border-radius: 8px;
      padding: 8px;
      background: #ffffff;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .pillar-card.p1 { border-top: 3.5px solid #0284c7; }
    .pillar-card.p2 { border-top: 3.5px solid #10b981; }
    .pillar-card.p3 { border-top: 3.5px solid #f59e0b; }
    .pillar-card.p4 { border-top: 3.5px solid #ef4444; }

    .pillar-badge {
      font-size: 8px;
      font-weight: 800;
      text-transform: uppercase;
      padding: 1px 5px;
      border-radius: 4px;
      display: inline-block;
      margin-bottom: 4px;
    }
    .p1 .pillar-badge { background: #e0f2fe; color: #0369a1; }
    .p2 .pillar-badge { background: #dcfce7; color: #15803d; }
    .p3 .pillar-badge { background: #fef3c7; color: #b45309; }
    .p4 .pillar-badge { background: #fee2e2; color: #b91c1c; }

    .pillar-title { font-size: 10.5px; font-weight: 800; color: #0f172a; margin-bottom: 3px; }
    .pillar-desc { font-size: 8.8px; color: #475569; line-height: 1.4; flex: 1; }
    .pillar-code {
      font-family: 'JetBrains Mono', monospace;
      font-size: 7.8px;
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      padding: 3px 5px;
      border-radius: 4px;
      color: #0f172a;
      margin-top: 5px;
      white-space: pre-wrap;
    }

    /* VISUAL DAG GUARDRAIL DIAGRAM */
    .dag-box {
      border: 1.5px solid #cbd5e1;
      border-radius: 8px;
      background: #f8fafc;
      padding: 8px 12px;
      margin-bottom: 8px;
    }
    .dag-flex {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      margin-top: 4px;
    }
    .dag-node {
      flex: 1;
      background: #ffffff;
      border: 1.5px solid #cbd5e1;
      border-radius: 6px;
      padding: 6px 8px;
      text-align: center;
    }
    .dag-node.start { border-color: #0284c7; background: #f0f9ff; }
    .dag-node.diamond { border-color: #d97706; background: #fffbeb; transform: rotate(-0.5deg); }
    .dag-node.tripwire { border-color: #ef4444; background: #fef2f2; }
    .dag-node.pass { border-color: #10b981; background: #f0fdf4; }

    .dag-node .tag { font-size: 7.5px; font-weight: 800; text-transform: uppercase; margin-bottom: 2px; }
    .start .tag { color: #0284c7; }
    .diamond .tag { color: #b45309; }
    .tripwire .tag { color: #dc2626; }
    .pass .tag { color: #16a34a; }

    .dag-node .txt { font-size: 9px; font-weight: 800; color: #0f172a; }
    .dag-node .sub { font-size: 7.8px; color: #64748b; margin-top: 1px; }
    .dag-arrow { font-size: 13px; font-weight: 800; color: #94a3b8; flex-shrink: 0; }

    /* 3 DOMAIN EXAMPLES TABLE */
    .domains-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 9px;
      margin-bottom: 8px;
      border: 1.5px solid #e2e8f0;
      border-radius: 6px;
      overflow: hidden;
    }
    .domains-table th {
      background: #f1f5f9;
      color: #334155;
      text-align: left;
      padding: 5px 8px;
      font-weight: 800;
      border-bottom: 1px solid #cbd5e1;
      text-transform: uppercase;
      font-size: 8px;
    }
    .domains-table td {
      padding: 5px 8px;
      border-bottom: 1px solid #e2e8f0;
      vertical-align: top;
      line-height: 1.35;
    }
    .domains-table tr:last-child td { border-bottom: none; }
    .badge-dom {
      display: inline-block;
      font-weight: 800;
      padding: 1px 4px;
      border-radius: 3px;
      font-size: 7.5px;
      text-transform: uppercase;
    }
    .badge-it { background: #e0f2fe; color: #0284c7; }
    .badge-fin { background: #dcfce7; color: #15803d; }
    .badge-lit { background: #fef3c7; color: #b45309; }

    /* FOOTER */
    .footer {
      border-top: 1.5px solid #e2e8f0;
      padding-top: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 8.5px;
      color: #64748b;
    }
    .footer-left { display: flex; gap: 10px; align-items: center; }
    .footer-tag { font-weight: 700; color: #0284c7; }
  </style>
</head>
<body>

  <!-- HEADER -->
  <div>
    <div class="header">
      <div>
        <div class="brand-pill">📘 GroundTruth Architecture Standard</div>
        <h1>Ensuring Text-Based Invariants</h1>
        <div class="subtitle">How to guarantee that agent interpretation never deviates away from source ground truth.</div>
      </div>
      <div class="header-badge">
        <div class="label">Reliability Standard</div>
        <div class="val">Zero Hallucination</div>
      </div>
    </div>

    <!-- CORE GOLDEN AXIOM BANNER -->
    <div class="axiom-banner">
      <div class="axiom-icon">⭐</div>
      <div>
        <div class="axiom-title">The Golden Principle of Ground Truth</div>
        <div class="axiom-quote">“The principle is to capture the essentials of the text so that interpretation will never deviate away from the ground truth.”</div>
        <div class="axiom-sub">Downstream LLM interpretation naturally drifts when unconstrained. Extracting the irreducible invariant essentials creates an unbreakable tether.</div>
      </div>
    </div>

    <!-- PROMPT VS PHYSICAL FENCE ANALOGY -->
    <div class="analogy-grid">
      <div class="analogy-card bad">
        <div class="analogy-emoji">🎭</div>
        <div class="analogy-text">
          <h3>The Polite Suggestion (Prompt Only)</h3>
          <p>Telling an LLM: <em>"Please don't approve loans > $150 or forget the hardware key."</em><br/>
          <strong>Why it fails:</strong> Jailbreaks, context window drift, or persuasive users easily bypass prompt instructions. It’s a cardboard sign, not a lock.</p>
        </div>
      </div>
      <div class="analogy-card good">
        <div class="analogy-emoji">⚡</div>
        <div class="analogy-text">
          <h3>The Electric Fence (Text-Based Invariant)</h3>
          <p>Compiling the text into <strong>structural DAG forks & interceptors</strong>.<br/>
          <strong>Why it succeeds:</strong> The execution runtime physically blocks invalid state mutations before dispatch. Even if the LLM hallucinating tries, the fence refuses to open.</p>
        </div>
      </div>
    </div>

    <!-- 4-PILLAR MECHANISMS -->
    <div class="section-title"><span>🛠️</span> Four Architectural Ways to Ensure Invariants</div>
    <div class="pillars-grid">
      <div class="pillar-card p1">
        <span class="pillar-badge">1. Contract Extraction</span>
        <div class="pillar-title">5-Tier Policy Tree</div>
        <div class="pillar-desc">Parse raw text into 5 immutable layers: Root Invariants, Scoped Directives, Rules, Bounds, and Dead Ends.</div>
        <div class="pillar-code">Tier 0: Root Invariant
Tier 3: Bounds [0, $150]
Tier 4: Dead-End Abort</div>
      </div>

      <div class="pillar-card p2">
        <span class="pillar-badge">2. Code Interceptors</span>
        <div class="pillar-title">Zero-LLM Gatekeeper</div>
        <div class="pillar-desc">Place deterministic Python/JS code before every tool execution. Never let an LLM self-police its own bounds.</div>
        <div class="pillar-code">if amount > 150.00:
    abort_to_tripwire()
if ttl > 14400: revoke()</div>
      </div>

      <div class="pillar-card p3">
        <span class="pillar-badge">3. Zero Imagined Numbers</span>
        <div class="pillar-title">Respect Algebraic Limits</div>
        <div class="pillar-desc">If text states algebraic bounds without physical constants, keep them algebraic [u_min, u_max]. Never invent 42.0 kPa.</div>
        <div class="pillar-code">True Bounds: Stated Only
Unspecified: Algebraic
Invented: 0% Allowed</div>
      </div>

      <div class="pillar-card p4">
        <span class="pillar-badge">4. Circuit Breaker DAG</span>
        <div class="pillar-title">Hard Terminal Tripwires</div>
        <div class="pillar-desc">Wire invariants directly into LangGraph decision diamonds. Any breach instantly transitions to safe state reversion.</div>
        <div class="pillar-code">Diamond: Limit OK?
No -> 🛑 TRIPWIRE
Yes -> ✅ Safe Action</div>
      </div>
    </div>

    <!-- VISUAL DAG WORKFLOW -->
    <div class="dag-box">
      <div class="section-title" style="margin-bottom: 2px;"><span>🔄</span> Runtime Enforcement: The Closed-Loop Invariant Guardrail</div>
      <div class="dag-flex">
        <div class="dag-node start">
          <div class="tag">Step 1: Ingestion</div>
          <div class="txt">Raw Text / URL</div>
          <div class="sub">SOP, Statute, Novel</div>
        </div>
        <div class="dag-arrow">➔</div>
        <div class="dag-node">
          <div class="tag">Step 2: Compiler</div>
          <div class="txt">Extract Invariants</div>
          <div class="sub">Axioms & Bounds</div>
        </div>
        <div class="dag-arrow">➔</div>
        <div class="dag-node diamond">
          <div class="tag">Decision Diamond</div>
          <div class="txt">Invariant Checked?</div>
          <div class="sub">Deterministic Code</div>
        </div>
        <div class="dag-arrow">➔</div>
        <div class="dag-node tripwire">
          <div class="tag">Breach / Deviation</div>
          <div class="txt">🛑 Safe Reversion</div>
          <div class="sub">Instant Freeze & Alert</div>
        </div>
        <div class="dag-arrow" style="color: #10b981;">OR ➔</div>
        <div class="dag-node pass">
          <div class="tag">100% Satisfied</div>
          <div class="txt">✅ Action Dispatched</div>
          <div class="sub">Faithful Ground Truth</div>
        </div>
      </div>
    </div>

    <!-- 3 REAL DOMAIN EXAMPLES TABLE -->
    <div class="section-title"><span>📚</span> How It Enforces Ground Truth Across Domains</div>
    <table class="domains-table">
      <thead>
        <tr>
          <th style="width: 20%;">Domain</th>
          <th style="width: 25%;">Text Invariant</th>
          <th style="width: 25%;">Downstream Risk If Left to LLM</th>
          <th style="width: 30%;">Enforcement Circuit Breaker</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><span class="badge-dom badge-it">IT Security</span><br/><strong>SOC2 / Break-Glass</strong></td>
          <td>Physical FIDO2 key mandatory; SMS OTP strictly prohibited; Write lease capped at 4h.</td>
          <td>Agent "politely" offers SMS fallback during user login friction or leaves lease open indefinitely.</td>
          <td><strong>Hard Token Shield:</strong> Missing WebAuthn challenge or TTL &gt; 4h triggers automated SIRT audit and lease termination.</td>
        </tr>
        <tr>
          <td><span class="badge-dom badge-fin">FinTech AML</span><br/><strong>Dispute Intake</strong></td>
          <td>Federal Non-Tipping Invariant (31 U.S.C. § 5318(g)): Prohibited from disclosing SAR freezes.</td>
          <td>Chatbot answers customer: <em>"Your funds are held due to suspicious activity investigations."</em></td>
          <td><strong>Anti-Tipping Redaction Gate:</strong> Pattern interceptor catches SAR keywords; auto-routes dispute to 72h frozen queue.</td>
        </tr>
        <tr>
          <td><span class="badge-dom badge-lit">Literature</span><br/><strong>Little House / Gatsby</strong></td>
          <td>Pa's discomfort with crowded Wisconsin vs. going West to open Indian country where grass is thick.</td>
          <td>Agent inverts polarity or invents corporate IT telemetry for Laura Ingalls Wilder's frontier narrative.</td>
          <td><strong>Semantic Polarity Router:</strong> Red Stagnation maps staying in Wisconsin; Green Action maps departing West.</td>
        </tr>
      </tbody>
    </table>

  </div>

  <!-- FOOTER -->
  <div class="footer">
    <div class="footer-left">
      <span class="footer-tag">GroundTruth Architecture</span>
      <span>• Deterministic Agentic Systems</span>
      <span>• LangGraph & LangSmith Observable</span>
    </div>
    <div>Strict Fidelity • Zero Hallucination • Continuous Verification</div>
  </div>

</body>
</html>
'''

# 1. Write HTML
html_path = "scratch/ensuring_invariants_one_pager.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)
print(f"Wrote HTML to {html_path}")

# 2. Render to PDF using Playwright Chromium
pdf_path = "ensuring_invariants_one_pager.pdf"
png_path = "ensuring_invariants_one_pager.png"

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome")
    page = browser.new_page()
    page.goto(f"file:///{os.path.abspath(html_path).replace(os.sep, '/')}")
    page.wait_for_timeout(1000)

    # Generate 1-page PDF
    page.pdf(
        path=pdf_path,
        format="Letter",
        print_background=True,
        margin={"top": "0in", "bottom": "0in", "left": "0in", "right": "0in"}
    )
    print(f"Generated PDF at {pdf_path}")

    # Generate preview PNG
    page.screenshot(path=png_path)
    print(f"Captured PNG preview at {png_path}")

    browser.close()

# 3. Verify exactly 1 page
reader = pypdf.PdfReader(pdf_path)
page_count = len(reader.pages)
print(f"Verified PDF Page Count: {page_count} page(s)")
assert page_count == 1, f"Expected exactly 1 page, but got {page_count}!"

# 4. Copy to langchain-test and brain artifacts
os.system(f'copy "{pdf_path}" "scratch\\langchain-test\\{pdf_path}" /Y > nul')
os.system(f'copy "{png_path}" "scratch\\langchain-test\\{png_path}" /Y > nul')
os.system(f'copy "{pdf_path}" "C:\\Users\\richa\\.gemini\\antigravity\\brain\\3fabbe92-0913-44e6-88cd-febd17cd2f98\\{pdf_path}" /Y > nul')
os.system(f'copy "{png_path}" "C:\\Users\\richa\\.gemini\\antigravity\\brain\\3fabbe92-0913-44e6-88cd-febd17cd2f98\\{png_path}" /Y > nul')
print("Copied to all distribution destinations!")
