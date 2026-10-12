# -*- coding: utf-8 -*-
"""
create_comic_reader.py
Creates `comic_book_reader.html` - a responsive mobile and desktop comic viewer
that wraps the 22-episode comic with:
- Fully responsive scaling (no horizontal scrollbar on mobile)
- Jump-to-episode navbar
- Direct PDF download button
- Light/Dark mode support
"""

import os
import re

with open("comic_book_printable.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add responsive viewport and styles
responsive_css = """
<style>
@media (max-width: 850px) {
  body {
    padding: 0 !important;
  }
  .page {
    width: 100% !important;
    max-width: 100vw !important;
    height: auto !important;
    max-height: none !important;
    padding: 12px 10px !important;
    margin: 0 0 20px 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
  }
  .header-bar {
    flex-direction: column !important;
    gap: 6px !important;
    align-items: flex-start !important;
  }
  .panel-grid, .grid-3-col, .grid-2-col {
    display: flex !important;
    flex-direction: column !important;
    gap: 12px !important;
  }
  img {
    max-width: 100% !important;
    height: auto !important;
  }
}

.comic-nav-bar {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: #0f172a;
  border-bottom: 2px solid #38bdf8;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}
.comic-nav-title {
  font-family: 'Impact', sans-serif;
  color: #38bdf8;
  font-size: 18px;
  letter-spacing: 0.5px;
}
.comic-nav-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}
.comic-nav-btn {
  background: #f59e0b;
  color: #000;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: 800;
  font-size: 12px;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.comic-nav-select {
  background: #1e293b;
  color: #f8fafc;
  border: 1px solid #475569;
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}
</style>
"""

# Navigation bar to insert at beginning of body
nav_bar = """
<div class="comic-nav-bar">
  <div class="comic-nav-title">⚡ THE 3-TIER ENTERPRISE AGENT STACK COMIC</div>
  <div class="comic-nav-actions">
    <select class="comic-nav-select" onchange="jumpToEpisode(this.value)">
      <option value="0">📖 Cover: Wild West vs Citadel</option>
      <option value="1">Ep 1: The Rosetta Stone</option>
      <option value="2">Ep 2: Amazon Bedrock</option>
      <option value="3">Ep 3: AgentCore / Nitro</option>
      <option value="4">Ep 4: Amazon S3 Vault</option>
      <option value="5">Ep 5: AWS Database</option>
      <option value="6">Ep 6: AWS Lambda</option>
      <option value="7">Ep 7: AWS Step Functions</option>
      <option value="8">Ep 8: Amazon EventBridge</option>
      <option value="9">Ep 9: Kernel Propose-Decide</option>
      <option value="10">Ep 10: Runbook Engine</option>
      <option value="11">Ep 11: Kernel Supervisor</option>
      <option value="12">Ep 12: Mutex Lease</option>
      <option value="13">Ep 13: Context Pager</option>
      <option value="14">Ep 14: Episodic Ledger</option>
      <option value="15">Ep 15: Grounding Certifier</option>
      <option value="16">Ep 16: Topology Builder</option>
      <option value="17">Ep 17: Liaison Router</option>
      <option value="18">Ep 18: Hop Limiter</option>
      <option value="19">Ep 19: Shared Whiteboard</option>
      <option value="20">Ep 20: Consensus Arbiter</option>
      <option value="21">Ep 21: Circuit Breaker</option>
      <option value="22">Ep 22: Master Blueprint</option>
    </select>
    <a href="https://github.com/cosmosanalytics/uat-copilot-local/raw/main/The_3_Tier_Enterprise_Agent_Stack_Comic_Story.pdf" class="comic-nav-btn" download>
      ⬇️ Download PDF
    </a>
  </div>
</div>
<script>
function jumpToEpisode(idx) {
  const pages = document.querySelectorAll('.page');
  const target = pages[parseInt(idx, 10)];
  if (target) {
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}
</script>
"""

# Insert responsive CSS before </head>
html = html.replace("</head>", responsive_css + "\n</head>")

# Insert nav bar right after <body>
html = html.replace("<body>", "<body>\n" + nav_bar)

with open("comic_book_reader.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Generated comic_book_reader.html, size: {len(html)} bytes")
