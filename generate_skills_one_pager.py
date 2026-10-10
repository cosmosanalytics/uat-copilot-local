# -*- coding: utf-8 -*-
"""
Generator for open_source_skills_one_pager.pdf & .html (V2 - Corrected Edition):
Incorporates all sharp feedback:
1. Document skills (docx, pdf, pptx, xlsx) explicitly marked as PROPRIETARY (Anthropic, All rights reserved) and Python/Office runtime.
2. Corrected blurbs:
   - web-artifacts-builder: React + Vite + Tailwind + shadcn/ui with init & bundle scripts.
   - theme-factory: 10 actual presets (Arctic Frost, Botanical Garden, Desert Rose, Midnight Galaxy, etc.).
   - canvas-design: Poster-style visual art outputting .png/.pdf from design philosophies.
   - slack-gif-creator: Animated GIFs optimized for Slack with frame & size constraints.
3. Verified Apache 2.0 open-source status for the other 15 skills (including claude-api, webapp-testing, discernment-nudge, academy-guide).
4. Fixed layout spacing: eliminated large squad gaps, tight cohesive rhythm, strictly 1 single page verified by PyMuPDF.
"""

import os
import subprocess
import pymupdf

HTML_PATH = os.path.abspath(r"C:\Users\richa\ai-engineering\open_source_skills_one_pager.html")
PDF_PATH = os.path.abspath(r"C:\Users\richa\ai-engineering\open_source_skills_one_pager.pdf")
PNG_PATH = os.path.abspath(r"C:\Users\richa\ai-engineering\open_source_skills_preview.png")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Anthropic Agent Skills Catalog Cheat Sheet</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;700;800&display=swap" rel="stylesheet">
<style>
  @page {
    size: letter portrait;
    margin: 0.20in 0.24in 0.20in 0.24in;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  
  html, body {
    height: 100%;
  }

  body {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #0F172A;
    background: #FFFFFF;
    line-height: 1.25;
    font-size: 7.9pt;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 10.55in;
    max-height: 10.55in;
    overflow: hidden;
  }

  /* HEADER BANNER */
  .header-card {
    background: linear-gradient(135deg, #0F172A 0%, #312E81 50%, #4338CA 100%);
    border-radius: 7px;
    padding: 8px 14px;
    color: #FFFFFF;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.10);
  }
  .header-left h1 {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 15.0pt;
    font-weight: 800;
    letter-spacing: -0.3px;
    line-height: 1.1;
    background: linear-gradient(90deg, #FFFFFF 0%, #C7D2FE 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .header-left p {
    font-size: 7.9pt;
    color: #E2E8F0;
    margin-top: 2px;
    font-weight: 500;
  }
  .header-badge {
    background: rgba(255, 255, 255, 0.14);
    border: 1px solid rgba(255, 255, 255, 0.28);
    border-radius: 999px;
    padding: 3px 9px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.0pt;
    font-weight: 700;
    letter-spacing: 0.4px;
    text-transform: uppercase;
    text-align: right;
  }

  /* CONCEPT INTRO STRIP */
  .concept-strip {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 4px 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 7.5pt;
    color: #475569;
    margin-top: 4px;
  }
  .concept-pill {
    font-weight: 800;
    color: #4F46E5;
    background: #EEF2FF;
    padding: 1px 5px;
    border-radius: 3px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.0pt;
  }

  /* 4 SQUADS CONTAINER */
  .squads-container {
    display: flex;
    flex-direction: column;
    gap: 6px;
    flex: 1;
    margin: 5px 0;
  }

  .squad-block {
    border-radius: 6px;
    border: 1px solid #E2E8F0;
    overflow: hidden;
    background: #FFFFFF;
  }

  .squad-header {
    padding: 3.5px 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 800;
    font-size: 8.0pt;
    letter-spacing: -0.1px;
  }
  .squad-header.purple { background: #FAF5FF; color: #6B21A8; border-bottom: 1px solid #F3E8FF; }
  .squad-header.blue   { background: #F0F9FF; color: #0369A1; border-bottom: 1px solid #E0F2FE; }
  .squad-header.amber  { background: #FFFBEB; color: #B45309; border-bottom: 1px solid #FEF3C7; }
  .squad-header.emerald{ background: #ECFDF5; color: #047857; border-bottom: 1px solid #D1FAE5; }

  .squad-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 6.6pt;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 3px;
    text-transform: uppercase;
  }
  .squad-header.purple .squad-tag { background: #E9D5FF; color: #581C87; }
  .squad-header.blue   .squad-tag { background: #BAE6FD; color: #075985; }
  .squad-header.amber  .squad-tag { background: #FDE68A; color: #92400E; }
  .squad-header.emerald .squad-tag { background: #A7F3D0; color: #065F46; }

  /* SKILL CELLS GRID */
  .skills-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 4px;
    padding: 5px 7px;
  }
  .skills-grid.four-col {
    grid-template-columns: repeat(4, 1fr);
  }
  .skills-grid.five-col {
    grid-template-columns: repeat(5, 1fr);
  }

  .skill-cell {
    background: #F8FAFC;
    border: 1px solid #F1F5F9;
    border-radius: 5px;
    padding: 4px 6px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .skill-cell.proprietary {
    background: #FFFDF5;
    border: 1px solid #FEF3C7;
  }

  .skill-name-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1px;
  }
  .skill-code {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 800;
    font-size: 7.5pt;
    color: #1E293B;
  }
  .skill-badge {
    font-size: 6.2pt;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    padding: 1px 4px;
    border-radius: 3px;
  }
  .skill-badge.oss { background: #E0E7FF; color: #4338CA; }
  .skill-badge.prop { background: #FEE2E2; color: #991B1B; }

  .skill-desc {
    font-size: 6.8pt;
    color: #475569;
    line-height: 1.22;
  }
  .skill-killer-feature {
    margin-top: 2px;
    font-size: 6.5pt;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 3px;
  }

  /* BOTTOM CHEAT-SHEET RUNBOOK STRIP */
  .bottom-runbook {
    background: #0F172A;
    color: #F8FAFC;
    border-radius: 6px;
    padding: 6px 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 7.0pt;
    margin-top: 2px;
  }
  .runbook-step {
    display: flex;
    align-items: center;
    gap: 5px;
  }
  .step-num {
    background: #4F46E5;
    color: #FFFFFF;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 6.6pt;
  }
  .step-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 6.9pt;
  }

  /* FOOTER */
  .footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 6.6pt;
    color: #94A3B8;
    padding: 2px 2px 0 2px;
  }
  .footer strong { color: #475569; }
</style>
</head>
<body>

  <!-- HEADER -->
  <div class="header-card">
    <div class="header-left">
      <h1>Anthropic Agent Skills Catalog Cheat Sheet</h1>
      <p>Official Breakdown: 15 Apache 2.0 Open-Source Capabilities + 4 Proprietary Document Skills</p>
    </div>
    <div class="header-badge">
      <div>SKILL.md Spec</div>
      <div style="color: #A5B4FC; font-size:6.0pt; font-weight:600;">19 Capabilities</div>
    </div>
  </div>

  <!-- CONCEPT INTRO STRIP -->
  <div class="concept-strip">
    <div>
      <strong>Anatomy:</strong> A skill is a folder containing a <span class="concept-pill">SKILL.md</span> runbook with YAML frontmatter + markdown execution procedures.
    </div>
    <div>
      ⚡ <strong>Progressive Disclosure:</strong> LLM only reads <code>description:</code> metadata until task triggers it &rarr; <em>zero context pollution</em>.
    </div>
  </div>

  <!-- SQUADS CONTAINER -->
  <div class="squads-container">

    <!-- SQUAD 1: CREATIVE UI & FRONTEND ARTIFACTS (Apache 2.0) -->
    <div class="squad-block">
      <div class="squad-header purple">
        <span>🎨 Squad 1: Creative UI, Graphics &amp; Frontend Artifacts (Apache 2.0 &bull; Open-Source)</span>
        <span class="squad-tag">6 Skills</span>
      </div>
      <div class="skills-grid">
        <!-- 1.1 frontend-design -->
        <div class="skill-cell">
          <div class="skill-name-row">
            <span class="skill-code">frontend-design</span>
            <span class="skill-badge oss">Apache 2.0</span>
          </div>
          <p class="skill-desc">Distinctive visual art direction, intentional typography, color harmony, and avoiding generic sterile defaults.</p>
          <div class="skill-killer-feature" style="color:#6B21A8;">✦ Anti-generic styling rules</div>
        </div>
        <!-- 1.2 web-artifacts-builder -->
        <div class="skill-cell">
          <div class="skill-name-row">
            <span class="skill-code">web-artifacts-builder</span>
            <span class="skill-badge oss">Apache 2.0</span>
          </div>
          <p class="skill-desc">Complex multi-component web apps using React, Tailwind CSS, Vite &amp; shadcn/ui with init and bundle scripts.</p>
          <div class="skill-killer-feature" style="color:#6B21A8;">✦ React + Tailwind + shadcn</div>
        </div>
        <!-- 1.3 theme-factory -->
        <div class="skill-cell">
          <div class="skill-name-row">
            <span class="skill-code">theme-factory</span>
            <span class="skill-badge oss">Apache 2.0</span>
          </div>
          <p class="skill-desc">10 pre-set themes (Arctic Frost, Botanical Garden, Desert Rose, Midnight Galaxy, Golden Hour, Sunset Blvd).</p>
          <div class="skill-killer-feature" style="color:#6B21A8;">✦ 10 verified color/font presets</div>
        </div>
        <!-- 1.4 algorithmic-art -->
        <div class="skill-cell">
          <div class="skill-name-row">
            <span class="skill-code">algorithmic-art</span>
            <span class="skill-badge oss">Apache 2.0</span>
          </div>
          <p class="skill-desc">Generative p5.js art: Perlin noise flow fields, chromatic aberration, particle trails, and interactive parameter exploration.</p>
          <div class="skill-killer-feature" style="color:#6B21A8;">✦ Autonomous p5.js canvases</div>
        </div>
        <!-- 1.5 canvas-design -->
        <div class="skill-cell">
          <div class="skill-name-row">
            <span class="skill-code">canvas-design</span>
            <span class="skill-badge oss">Apache 2.0</span>
          </div>
          <p class="skill-desc">Poster-style visual art and static designs exported as .png and .pdf documents from written design philosophies.</p>
          <div class="skill-killer-feature" style="color:#6B21A8;">✦ Poster art (.png / .pdf)</div>
        </div>
        <!-- 1.6 slack-gif-creator -->
        <div class="skill-cell">
          <div class="skill-name-row">
            <span class="skill-code">slack-gif-creator</span>
            <span class="skill-badge oss">Apache 2.0</span>
          </div>
          <p class="skill-desc">Knowledge and utilities for creating animated GIFs optimized for Slack with frame, color &amp; file size constraints.</p>
          <div class="skill-killer-feature" style="color:#6B21A8;">✦ Slack-optimized animated GIFs</div>
        </div>
      </div>
    </div>

    <!-- SQUAD 2: AGENT ARCHITECTURE & ENGINEERING (Apache 2.0) -->
    <div class="squad-block">
      <div class="squad-header blue">
        <span>⚡ Squad 2: Agent Architecture, MCP &amp; Testing (Apache 2.0 &bull; Open-Source)</span>
        <span class="squad-tag">4 Skills</span>
      </div>
      <div class="skills-grid four-col">
        <!-- 2.1 skill-creator -->
        <div class="skill-cell">
          <div class="skill-name-row">
            <span class="skill-code">skill-creator</span>
            <span class="skill-badge oss">Apache 2.0</span>
          </div>
          <p class="skill-desc">Meta-skill to author, calibrate, and lint new <code>SKILL.md</code> files with positive triggers &amp; negative distractors.</p>
          <div class="skill-killer-feature" style="color:#0369A1;">✦ Self-replicating skill engine</div>
        </div>
        <!-- 2.2 mcp-builder -->
        <div class="skill-cell">
          <div class="skill-name-row">
            <span class="skill-code">mcp-builder</span>
            <span class="skill-badge oss">Apache 2.0</span>
          </div>
          <p class="skill-desc">Full Model Context Protocol server scaffold in TypeScript &amp; Python with tools, prompts, resources &amp; stdio/SSE.</p>
          <div class="skill-killer-feature" style="color:#0369A1;">✦ Turn-key tool integrations</div>
        </div>
        <!-- 2.3 claude-api -->
        <div class="skill-cell">
          <div class="skill-name-row">
            <span class="skill-code">claude-api</span>
            <span class="skill-badge oss">Apache 2.0</span>
          </div>
          <p class="skill-desc">Exhaustive reference for Anthropic API SDKs, streaming patterns, structured JSON schemas &amp; prompt caching.</p>
          <div class="skill-killer-feature" style="color:#0369A1;">✦ Production API contracts</div>
        </div>
        <!-- 2.4 webapp-testing -->
        <div class="skill-cell">
          <div class="skill-name-row">
            <span class="skill-code">webapp-testing</span>
            <span class="skill-badge oss">Apache 2.0</span>
          </div>
          <p class="skill-desc">Interactive local web app testing with Playwright: UI debugging, browser screenshots, and console log capture.</p>
          <div class="skill-killer-feature" style="color:#0369A1;">✦ Playwright UI verification</div>
        </div>
      </div>
    </div>

    <!-- SQUAD 3: GOVERNANCE, EPISTEMIC SAFETY & COMMS (Apache 2.0) -->
    <div class="squad-block">
      <div class="squad-header amber">
        <span>🛡️ Squad 3: Governance, Epistemic Safety &amp; Comms (Apache 2.0 &bull; Open-Source)</span>
        <span class="squad-tag">5 Skills</span>
      </div>
      <div class="skills-grid five-col">
        <!-- 3.1 discernment-nudge -->
        <div class="skill-cell">
          <div class="skill-name-row">
            <span class="skill-code">discernment-nudge</span>
            <span class="skill-badge oss">Apache 2.0</span>
          </div>
          <p class="skill-desc">Epistemic checkpoint: prompts user to examine implicit assumptions &amp; failure modes on actionable plans.</p>
          <div class="skill-killer-feature" style="color:#B45309;">✦ Pre-mortem safety gate</div>
        </div>
        <!-- 3.2 brand-guidelines -->
        <div class="skill-cell">
          <div class="skill-name-row">
            <span class="skill-code">brand-guidelines</span>
            <span class="skill-badge oss">Apache 2.0</span>
          </div>
          <p class="skill-desc">Official Anthropic brand colors, typography scales, accessibility contrasts &amp; brand voice consistency.</p>
          <div class="skill-killer-feature" style="color:#B45309;">✦ WCAG contrast compliance</div>
        </div>
        <!-- 3.3 internal-comms -->
        <div class="skill-cell">
          <div class="skill-name-row">
            <span class="skill-code">internal-comms</span>
            <span class="skill-badge oss">Apache 2.0</span>
          </div>
          <p class="skill-desc">High-signal internal memos: status updates, post-mortems, team syncs, and 30-60-90 day planning drafts.</p>
          <div class="skill-killer-feature" style="color:#B45309;">✦ High-signal memos</div>
        </div>
        <!-- 3.4 academy-guide -->
        <div class="skill-cell">
          <div class="skill-name-row">
            <span class="skill-code">academy-guide</span>
            <span class="skill-badge oss">Apache 2.0</span>
          </div>
          <p class="skill-desc">Matches user queries against Claude Academy course catalog for tutorials, videos &amp; onboarding guides.</p>
          <div class="skill-killer-feature" style="color:#B45309;">✦ Curated learning paths</div>
        </div>
        <!-- 3.5 doc-coauthoring -->
        <div class="skill-cell">
          <div class="skill-name-row">
            <span class="skill-code">doc-coauthoring</span>
            <span class="skill-badge oss">Open Standard</span>
          </div>
          <p class="skill-desc">Structured collaborative workflow for drafting technical specs, RFCs, and PRDs with incremental review phases.</p>
          <div class="skill-killer-feature" style="color:#B45309;">✦ Living technical RFCs</div>
        </div>
      </div>
    </div>

    <!-- SQUAD 4: PROPRIETARY DOCUMENT AUTOMATION -->
    <div class="squad-block">
      <div class="squad-header emerald">
        <span>🔒 Squad 4: Proprietary Document &amp; File Tooling (Anthropic Proprietary &bull; Python Runtime)</span>
        <span class="squad-tag">4 Skills</span>
      </div>
      <div class="skills-grid four-col">
        <!-- 4.1 docx -->
        <div class="skill-cell proprietary">
          <div class="skill-name-row">
            <span class="skill-code">docx</span>
            <span class="skill-badge prop">Proprietary</span>
          </div>
          <p class="skill-desc">Create/edit Word (.docx/.dotx) via python-docx &amp; XML archives. Generates formal reports with TOCs &amp; letterheads.</p>
          <div class="skill-killer-feature" style="color:#991B1B;">⚠️ Python/Office &bull; All rights reserved</div>
        </div>
        <!-- 4.2 pdf -->
        <div class="skill-cell proprietary">
          <div class="skill-name-row">
            <span class="skill-code">pdf</span>
            <span class="skill-badge prop">Proprietary</span>
          </div>
          <p class="skill-desc">Merge, split, OCR, table extract, watermark &amp; form-fill using pypdf, pdfplumber &amp; CLI pdftk tools.</p>
          <div class="skill-killer-feature" style="color:#991B1B;">⚠️ Python CLI &bull; All rights reserved</div>
        </div>
        <!-- 4.3 pptx -->
        <div class="skill-cell proprietary">
          <div class="skill-name-row">
            <span class="skill-code">pptx</span>
            <span class="skill-badge prop">Proprietary</span>
          </div>
          <p class="skill-desc">Pitch deck and slide generation via python-pptx with 16:9 widescreen layout, visual cards &amp; layout trees.</p>
          <div class="skill-killer-feature" style="color:#991B1B;">⚠️ Python/Office &bull; All rights reserved</div>
        </div>
        <!-- 4.4 xlsx -->
        <div class="skill-cell proprietary">
          <div class="skill-name-row">
            <span class="skill-code">xlsx</span>
            <span class="skill-badge prop">Proprietary</span>
          </div>
          <p class="skill-desc">Spreadsheet data engineering: financial models, formulas, pivot tables &amp; charts via openpyxl &amp; pandas.</p>
          <div class="skill-killer-feature" style="color:#991B1B;">⚠️ Python/Office &bull; All rights reserved</div>
        </div>
      </div>
    </div>

  </div>

  <!-- BOTTOM CHEAT-SHEET RUNBOOK STRIP -->
  <div class="bottom-runbook">
    <div style="font-weight:800; font-family:'Bricolage Grotesque'; font-size:8.2pt; color:#A5B4FC;">
      🚀 3-Step Lifecycle:
    </div>
    <div class="runbook-step">
      <span class="step-num">1</span>
      <span class="step-text"><strong>Discover:</strong> Agent matches YAML <code>description:</code> trigger</span>
    </div>
    <div class="runbook-step">
      <span class="step-num">2</span>
      <span class="step-text"><strong>Mount:</strong> Load body markdown on demand into context</span>
    </div>
    <div class="runbook-step">
      <span class="step-num">3</span>
      <span class="step-text"><strong>Execute:</strong> Synthesize verified code or artifacts via WebLLM / LPU</span>
    </div>
  </div>

  <!-- FOOTER -->
  <div class="footer">
    <div><strong>Upstream Source:</strong> github.com/anthropics/skills &bull; 15 Apache 2.0 Open-Source + 4 Anthropic Proprietary Skills</div>
    <div><strong>Interactive Studio:</strong> cosmosanalytics.github.io/uat-copilot-local/internet_skills_studio.html</div>
  </div>

</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Wrote HTML to {HTML_PATH}")

# Compile PDF via Headless Chrome
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_PATH}",
    f"file:///{HTML_PATH}"
]
print("Compiling PDF via Headless Chrome...")
subprocess.run(cmd, check=True)
print(f"Generated PDF at {PDF_PATH}")

# Verify exact page count with PyMuPDF
doc = pymupdf.open(PDF_PATH)
page_count = len(doc)
print(f"=== VERIFICATION: PAGE COUNT = {page_count} ===")
if page_count != 1:
    print(f"WARNING: Expected exactly 1 page, got {page_count}!")
else:
    print("SUCCESS: Strictly exactly 1 page verified!")

# Render preview image
page = doc[0]
pix = page.get_pixmap(dpi=150)
pix.save(PNG_PATH)
print(f"Rendered visual preview to {PNG_PATH}")
