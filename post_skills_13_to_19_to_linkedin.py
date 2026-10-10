# -*- coding: utf-8 -*-
"""
post_skills_13_to_19_to_linkedin.py
Publishes LinkedIn posts for Skills 13 through 19:
- Skill #13: academy-guide
- Skill #14: doc-coauthoring
- Skill #15: docx
- Skill #16: pdf
- Skill #17: pptx
- Skill #18: web-artifacts-builder
- Skill #19: xlsx

Each post contains a brief summary and clean GitHub Pages live link.
"""

import sys
import time
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'
URL = "https://api.linkedin.com/v2/ugcPosts"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
}

POSTS = [
    {
        "skill": "Skill #13: academy-guide",
        "url": "https://cosmosanalytics.github.io/uat-copilot-local/academy_guide_app.html",
        "text": """Excited to share the Claude Academy Guide Studio: a standalone, HTML-only web app demonstrating Skill #13 — academy-guide (Apache 2.0)! 🎓💡

Grounding technical explanations with official learning pathways, this studio connects developer goals to verified courses from Claude Academy (academy.claude.com):

• 📚 Official Curriculum Recommender: Dynamically matches questions to verified courses across Model Context Protocol (MCP), Tool Use, Prompt Engineering, and Enterprise Team Rollouts.
• 🎯 Docs-Grounded Answers: Synthesizes high-signal technical explanations with verifiable syllabus links and module prerequisites.
• ⚡ Dual In-Browser Inference: Synthesizes custom learning syllabi via Groq LPU (500+ tok/s) with pre-provisioned free token or local WebGPU (WebLLM).
• 🛡️ Anti-Hallucination Guardrails: Restricts recommendations strictly to canonical Academy hubs with zero invented URLs.

👉 Live GitHub Pages App:
https://cosmosanalytics.github.io/uat-copilot-local/academy_guide_app.html

#ClaudeAcademy #ModelContextProtocol #PromptEngineering #DeveloperTools #AIEducation #WebGPU #Groq #OpenSource"""
    },
    {
        "skill": "Skill #14: doc-coauthoring",
        "url": "https://cosmosanalytics.github.io/uat-copilot-local/doc_coauthoring_app.html",
        "text": """Excited to share the Doc Co-Authoring Studio: a standalone, HTML-only web app demonstrating Skill #14 — doc-coauthoring (Apache 2.0)! ✍️📋

Following Anthropic's collaborative documentation runbook, this studio transforms messy brain dumps into publication-ready architectural RFCs and PRDs:

• 🔄 4-Stage Co-Authoring Stepper: Progressively guides writers through Stage 1 (Context Gathering) → Stage 2 (Structure & Outline) → Stage 3 (Section Drafting) → Stage 4 (Reader Testing & Polish).
• 🏛️ High-Assurance Architectural RFCs: Generates executive problem statements, strict invariants, failure domains, and interface contracts.
• ⚡ Dual In-Browser Inference: Runs on Groq LPU (500+ tok/s) with pre-provisioned free token or local WebGPU (WebLLM) in clean Light Mode.
• 💾 Production Export: Instant one-click copy and `.md` file download.

👉 Live GitHub Pages App:
https://cosmosanalytics.github.io/uat-copilot-local/doc_coauthoring_app.html

#TechnicalWriting #RFC #SystemDesign #SoftwareArchitecture #ProductManagement #WebGPU #Groq #OpenSource"""
    },
    {
        "skill": "Skill #15: docx",
        "url": "https://cosmosanalytics.github.io/uat-copilot-local/docx_studio_app.html",
        "text": """Excited to share the DOCX Document Studio: a standalone, HTML-only web app demonstrating Skill #15 — docx (Office Document Engine)! 📄💼

Following Anthropic's docx creation runbook, this studio synthesizes executive Word documents, docx-js scripts, and unpacked XML structures:

• 📜 Authentic Word Page Canvas: Renders letter-sized document page previews complete with margins, typography hierarchy, callout accent bars, and data tables.
• 💻 docx-js & python-docx Compiler: Generates production-ready Node.js scripts avoiding common table padding and run-splitting pitfalls.
• 📦 Unpacked XML Inspector: Direct inspection of `word/document.xml` for precise in-place edits and redlining without reformatting corruption.
• ⚡ Dual In-Browser Inference: Compiles complete docx-js scripts via Groq LPU (500+ tok/s) or local WebGPU (WebLLM).

👉 Live GitHub Pages App:
https://cosmosanalytics.github.io/uat-copilot-local/docx_studio_app.html

#WordDoc #docx #Automation #DocumentEngineering #NodeJS #Python #WebGPU #Groq #OpenSource"""
    },
    {
        "skill": "Skill #16: pdf",
        "url": "https://cosmosanalytics.github.io/uat-copilot-local/pdf_studio_app.html",
        "text": """Excited to share the PDF Processing Studio: a standalone, HTML-only web app demonstrating Skill #16 — pdf (Office Document Engine)! 📑🔍

Following Anthropic's PDF processing guide, this studio provides an end-to-end workbench for tabular extraction, coordinate geometry, and PDF synthesis:

• 📊 Financial Tabular Extraction: Generates resilient Python `pdfplumber` pipelines with explicit table strategies to extract SEC 10-K tables with zero character loss.
• 🛠️ Programmatic ReportLab Synthesizer: Compiles clean Python scripts using Flowables, TableStyles, and exact coordinate geometry.
• 👁️ PDF Sheet Visualizer: Visual layout inspection with running headers, footers, and table borders.
• ⚡ Dual In-Browser Inference: Generates custom extraction and synthesis pipelines via Groq LPU (500+ tok/s) or local WebGPU (WebLLM).

👉 Live GitHub Pages App:
https://cosmosanalytics.github.io/uat-copilot-local/pdf_studio_app.html

#PDFProcessing #Python #pdfplumber #ReportLab #DataEngineering #FinTech #WebGPU #Groq #OpenSource"""
    },
    {
        "skill": "Skill #17: pptx",
        "url": "https://cosmosanalytics.github.io/uat-copilot-local/pptx_studio_app.html",
        "text": """Excited to share the PPTX Presentation Studio: a standalone, HTML-only web app demonstrating Skill #17 — pptx (Presentation Engine)! 📊🚀

Following Anthropic's presentation design standards, this studio architects executive 16:9 widescreen slide decks and compiles clean `pptxgenjs` code:

• 🖥️ 16:9 Widescreen Deck Viewer: Interactive slide carousel displaying modern metric cards, 3-column benefit layouts, and crisp typography.
• 💻 pptxgenjs Script Compiler: Outputs production Node.js code with explicit coordinate geometry, shape styling, and text wrapping.
• 📐 Visual Hierarchy & QA: Eliminates overlapping text boxes, tiny fonts, and unreadable contrast ratios.
• ⚡ Dual In-Browser Inference: Generates custom multi-slide pitch decks via Groq LPU (500+ tok/s) or local WebGPU (WebLLM).

👉 Live GitHub Pages App:
https://cosmosanalytics.github.io/uat-copilot-local/pptx_studio_app.html

#PresentationDesign #PPTX #PitchDeck #pptxgenjs #DataVisualization #WebGPU #Groq #OpenSource"""
    },
    {
        "skill": "Skill #18: web-artifacts-builder",
        "url": "https://cosmosanalytics.github.io/uat-copilot-local/web_artifacts_builder_app.html",
        "text": """Excited to share the Web Artifacts Builder: a standalone, HTML-only web app demonstrating Skill #18 — web-artifacts-builder (Apache 2.0)! ⚡🎨

Serving as a meta-builder for elaborate Claude.ai HTML artifacts, this studio synthesizes interactive, multi-component single-file web applications:

• 🧩 Elaborate Single-File Architecture: Builds self-contained, buildless HTML widgets with responsive layouts, CSS micro-interactions, and state management.
• 📊 Live Sandboxed Widget Preview: Interactive telemetry dashboard featuring live jitter controls, SVG bar charts, and real-time metric updates.
• 💻 Code Inspector: Instant one-click copy and `.html` file export for seamless embedding.
• ⚡ Dual In-Browser Inference: Synthesizes complete bespoke web components via Groq LPU (500+ tok/s) or local WebGPU (WebLLM).

👉 Live GitHub Pages App:
https://cosmosanalytics.github.io/uat-copilot-local/web_artifacts_builder_app.html

#WebArtifacts #FrontendDesign #WebDevelopment #JavaScript #CSS #UIUX #WebGPU #Groq #OpenSource"""
    },
    {
        "skill": "Skill #19: xlsx",
        "url": "https://cosmosanalytics.github.io/uat-copilot-local/xlsx_studio_app.html",
        "text": """Excited to share the XLSX Spreadsheet Studio: a standalone, HTML-only web app demonstrating Skill #19 — xlsx (Spreadsheet Engine)! 📈💹

Completing our 19-skill journey, this studio delivers high-assurance financial model synthesis and Python `openpyxl` script generation:

• 🔢 Live Interactive Formula Grid: Dynamic spreadsheet table with active cell coordinate inspection, uppercase formulas (`SUM`, `XLOOKUP`), and currency formatting (`$#,##0`).
• 🐍 Production openpyxl Compiler: Generates robust Python scripts with column auto-fitting, gridline enforcement, and professional formatting.
• 🔄 Mandatory Recalculation Guardrails: Outlines headless LibreOffice recalculation protocols to ensure formula cache survival across third-party tools.
• ⚡ Dual In-Browser Inference: Compiles complete 3-statement financial models via Groq LPU (500+ tok/s) or local WebGPU (WebLLM).

👉 Live GitHub Pages App:
https://cosmosanalytics.github.io/uat-copilot-local/xlsx_studio_app.html

#Excel #Spreadsheets #FinancialModeling #openpyxl #Python #FinTech #WebGPU #Groq #OpenSource"""
    }
]

def publish_all_posts():
    print(f"Beginning LinkedIn publishing sequence for Skills 13 through 19 ({len(POSTS)} total posts)...\n")

    for i, p in enumerate(POSTS, start=13):
        skill_name = p['skill']
        url = p['url']
        text = p['text']

        # Verify URL is live
        try:
            r = requests.head(url, timeout=10)
            status = r.status_code
        except Exception:
            status = "ERR"
        print(f"[{skill_name}] Live URL Check: {url} -> HTTP {status}")

        payload = {
            "author": MEMBER_URN,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        try:
            res = requests.post(URL, headers=HEADERS, json=payload, timeout=15)
            if res.status_code in [200, 201]:
                data = res.json()
                post_id = data.get('id', 'N/A')
                print(f"✅ Published {skill_name} successfully! URN: {post_id}")
            else:
                print(f"❌ Failed to publish {skill_name}: HTTP {res.status_code}")
                print(res.text)
        except Exception as e:
            print(f"❌ Exception publishing {skill_name}: {e}")

        # Rate limiting pause between posts
        time.sleep(3)
        print("-" * 50)

    print("\n🎉 Sequence complete for Skills 13 through 19!")

if __name__ == "__main__":
    publish_all_posts()
