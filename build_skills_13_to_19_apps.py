"""
build_skills_13_to_19_apps.py
Builds standalone, HTML-only web applications for Skills 13 through 19:
- Skill #13: academy-guide        -> academy_guide_app.html
- Skill #14: doc-coauthoring      -> doc_coauthoring_app.html
- Skill #15: docx                 -> docx_studio_app.html
- Skill #16: pdf                  -> pdf_studio_app.html
- Skill #17: pptx                 -> pptx_studio_app.html
- Skill #18: web-artifacts-builder-> web_artifacts_builder_app.html
- Skill #19: xlsx                 -> xlsx_studio_app.html

Key Architectural Standards:
1. Pure Light Mode by default with instant Dark Mode toggle and localStorage persistence.
2. Dual Inference: Groq LPU (500+ tok/s with pre-provisioned XOR key) + Local WebGPU (WebLLM) + Instant Offline Showcase.
3. User Input enabled: Input textarea pre-filled on load with prompt chips (zero empty-input blocking alerts).
4. Authentic Anthropic runbook guidelines and interactive render stages for each skill domain.
5. Export suite: Copy to clipboard and download output files.
"""

import json
import os
import sys

# Shared Groq XOR cipher key
XOR_KEY_SNIPPET = """const _XK = [77, 89, 65, 117, 102, 71, 88, 71, 115, 18, 66, 108, 99, 125, 69, 67, 125, 123, 97, 78, 88, 88, 30, 123, 125, 109, 78, 83, 72, 25, 108, 115, 102, 69, 96, 71, 115, 24, 95, 30, 127, 73, 93, 77, 92, 99, 69, 29, 123, 64, 80, 104, 71, 31, 114, 29];
const PROVISIONED_GROQ_KEY = _XK.map(c => String.fromCharCode(c ^ 42)).join("");"""

SHARED_CSS_ROOT = """
  :root {
    --bg-canvas: #f8fafc;
    --bg-panel: #ffffff;
    --bg-panel-subtle: #f1f5f9;
    --border-subtle: #e2e8f0;
    --border-focus: #2563eb;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-muted: #64748b;
    --accent-blue: #2563eb;
    --accent-indigo: #4f46e5;
    --accent-emerald: #059669;
    --accent-amber: #d97706;
    --accent-rose: #e11d48;
    --accent-purple: #7c3aed;
    --card-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
    --font-ui: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-display: 'Bricolage Grotesque', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
  }

  html[data-theme="dark"] {
    --bg-canvas: #090d16;
    --bg-panel: #0f172a;
    --bg-panel-subtle: #1e293b;
    --border-subtle: #334155;
    --border-focus: #60a5fa;
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --text-muted: #94a3b8;
    --accent-blue: #60a5fa;
    --accent-indigo: #818cf8;
    --accent-emerald: #34d399;
    --card-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg-canvas);
    color: var(--text-primary);
    font-family: var(--font-ui);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    transition: background 0.2s ease, color 0.2s ease;
  }
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
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-size: 1.25rem;
    font-weight: 800;
  }
  .brand-text h1 {
    font-family: var(--font-display);
    font-size: 1.2rem;
    font-weight: 800;
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
  .header-actions {
    display: flex;
    align-items: center;
    gap: 12px;
  }
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
    background: #2563eb;
    color: #ffffff;
    box-shadow: 0 1px 4px rgba(37, 99, 235, 0.3);
  }
  .engine-btn.active.webgpu {
    background: #4f46e5;
    color: #ffffff;
    box-shadow: 0 1px 4px rgba(79, 70, 229, 0.3);
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
  .workspace-layout {
    display: grid;
    grid-template-columns: 410px 1fr;
    flex: 1;
    min-height: 0;
  }
  @media (max-width: 1024px) {
    .workspace-layout { grid-template-columns: 1fr; }
  }
  .control-pane {
    background: var(--bg-panel);
    border-right: 1px solid var(--border-subtle);
    padding: 1.25rem 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.15rem;
    overflow-y: auto;
  }
  .section-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 800;
    color: var(--text-muted);
    margin-bottom: 0.45rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .chips-container {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 0.5rem;
  }
  .chip-btn {
    background: var(--bg-panel-subtle);
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 0.74rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .chip-btn:hover {
    border-color: var(--border-focus);
    color: var(--text-primary);
  }
  .chip-btn.active {
    background: #eff6ff;
    border-color: #3b82f6;
    color: #1d4ed8;
  }
  .user-textarea {
    width: 100%;
    min-height: 120px;
    background: var(--bg-panel-subtle);
    border: 1px solid var(--border-subtle);
    color: var(--text-primary);
    padding: 10px 12px;
    border-radius: 8px;
    font-size: 0.82rem;
    font-family: var(--font-ui);
    line-height: 1.5;
    resize: vertical;
  }
  .user-textarea:focus {
    outline: none;
    border-color: var(--border-focus);
    background: var(--bg-panel);
  }
  .btn-primary {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    color: #ffffff;
    border: none;
    padding: 11px 16px;
    border-radius: 8px;
    font-size: 0.84rem;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: all 0.2s ease;
    box-shadow: 0 2px 6px rgba(37, 99, 235, 0.25);
  }
  .btn-primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35);
  }
  .btn-secondary {
    background: var(--bg-panel-subtle);
    border: 1px solid var(--border-subtle);
    color: var(--text-primary);
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 0.76rem;
    font-weight: 600;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }
  .stage-pane {
    background: var(--bg-canvas);
    display: flex;
    flex-direction: column;
    min-height: 0;
    overflow-y: auto;
  }
  .stage-tabs {
    background: var(--bg-panel);
    border-bottom: 1px solid var(--border-subtle);
    display: flex;
    padding: 0 1.5rem;
    gap: 4px;
  }
  .tab-btn {
    padding: 12px 18px;
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text-muted);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.15s ease;
  }
  .tab-btn:hover { color: var(--text-primary); }
  .tab-btn.active {
    color: var(--accent-blue);
    border-bottom-color: var(--accent-blue);
  }
  .tab-content {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    flex: 1;
  }
  .stage-footer {
    background: var(--bg-panel);
    border-top: 1px solid var(--border-subtle);
    padding: 0.75rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: auto;
  }
  .footer-meta {
    font-size: 0.74rem;
    color: var(--text-muted);
    font-family: var(--font-mono);
  }
  .code-block {
    background: var(--bg-panel);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 1rem;
    font-family: var(--font-mono);
    font-size: 0.76rem;
    line-height: 1.55;
    white-space: pre-wrap;
    word-break: break-all;
    overflow-x: auto;
    max-height: 600px;
  }
  .card {
    background: var(--bg-panel);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 1.25rem;
    box-shadow: var(--card-shadow);
  }
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border-subtle);
  }
  .toast-box {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: #0f172a;
    color: #ffffff;
    padding: 10px 18px;
    border-radius: 8px;
    font-size: 0.8rem;
    font-weight: 600;
    box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    display: none;
    z-index: 100;
  }
"""

print("Starting generation of Skills 13 to 19 applications...")
