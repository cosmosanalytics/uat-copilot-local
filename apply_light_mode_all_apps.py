import os
import re

LIGHT_MODE_CSS = r'''
  /* LIGHT MODE THEME */
  body.light-mode {
    --bg-page: #F8FAFC;
    --bg-surface: #FFFFFF;
    --bg-card: #FFFFFF;
    --bg-subtle: #F1F5F9;
    --border: #CBD5E1;
    --text-main: #0F172A;
    --text-muted: #64748B;
  }
  body.light-mode header {
    background: #FFFFFF !important;
    border-bottom-color: #E2E8F0 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  body.light-mode .status-strip {
    background: #FFFFFF !important;
    border-color: #E2E8F0 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  }
  body.light-mode .status-tag {
    background: #F1F5F9 !important;
    border-color: #CBD5E1 !important;
    color: #334155 !important;
  }
  body.light-mode .engine-pill {
    background: #F1F5F9 !important;
    border-color: #CBD5E1 !important;
    color: #64748B !important;
  }
  body.light-mode .engine-pill.active {
    background: #FFFFFF !important;
    color: #0F172A !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
  }
  body.light-mode .model-picker-wrap {
    background: #F8FAFC !important;
  }
  body.light-mode .model-select {
    color: #0F172A !important;
  }
  body.light-mode .model-select option {
    background: #FFFFFF !important;
    color: #0F172A !important;
  }
  body.light-mode .card,
  body.light-mode .vitals-panel,
  body.light-mode .simulation-view,
  body.light-mode .agent-box,
  body.light-mode .trial-card,
  body.light-mode .scenario-card,
  body.light-mode .weights-card,
  body.light-mode .tree-card {
    background: #FFFFFF !important;
    border-color: #E2E8F0 !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.04) !important;
  }
  body.light-mode .slider-item,
  body.light-mode .vital-gauge,
  body.light-mode .scenario-box {
    background: #F8FAFC !important;
    border-color: #E2E8F0 !important;
  }
  body.light-mode .gauge-bar-wrap {
    background: #E2E8F0 !important;
  }
  body.light-mode .scenario-box input,
  body.light-mode .input-field {
    background: #FFFFFF !important;
    border-color: #CBD5E1 !important;
    color: #0F172A !important;
  }
  body.light-mode .modal-card {
    background: #FFFFFF !important;
    color: #0F172A !important;
  }
  body.light-mode .btn-preset {
    background: #F1F5F9 !important;
    border-color: #CBD5E1 !important;
    color: #64748B !important;
  }
  body.light-mode .btn-preset.active {
    background: #EFF6FF !important;
    color: #1D4ED8 !important;
    border-color: #3B82F6 !important;
  }
  body.light-mode .btn-secondary {
    background: #F8FAFC !important;
    border-color: #CBD5E1 !important;
    color: #1E293B !important;
  }
  body.light-mode .log-box,
  body.light-mode .reasoning-box,
  body.light-mode .ripple-visualizer,
  body.light-mode #ai-rationale-box,
  body.light-mode #consolidation-rationale {
    background: #F8FAFC !important;
    border-color: #E2E8F0 !important;
    color: #334155 !important;
  }
  body.light-mode .bubble {
    background: #F8FAFC !important;
    color: #1E293B !important;
    border-color: #E2E8F0 !important;
  }
  body.light-mode .bubble.intent {
    background: #FAF5FF !important;
    color: #581C87 !important;
  }
  body.light-mode .bubble.deadlock {
    background: #FEF2F2 !important;
    color: #991B1B !important;
  }
  body.light-mode .bubble.success {
    background: #F0FDF4 !important;
    color: #166534 !important;
  }
  body.light-mode .event-card {
    background: #F8FAFC !important;
    border-color: #E2E8F0 !important;
    color: #1E293B !important;
  }
  body.light-mode .event-card.crash {
    background: #FEF2F2 !important;
    color: #991B1B !important;
  }
  body.light-mode .tree-node {
    background: #FFFFFF !important;
    border-color: #E2E8F0 !important;
  }
  body.light-mode .tree-node.promoted {
    background: #F0FDF4 !important;
  }
  body.light-mode .tree-node.pruned {
    background: #FEF2F2 !important;
  }
  body.light-mode .node-metrics {
    color: #475569 !important;
    border-top-color: #E2E8F0 !important;
  }
  body.light-mode .summary-banner,
  body.light-mode .telemetry-summary {
    background: #F0FDF4 !important;
    color: #065F46 !important;
    border-color: #10B981 !important;
  }
  body.light-mode .heuristic-card {
    background: #F0FDF4 !important;
    color: #065F46 !important;
    border-color: #10B981 !important;
  }
  body.light-mode .similarity-bar-wrap {
    background: #E2E8F0 !important;
  }
'''

THEME_TOGGLE_HTML = r'''<button class="theme-toggle-btn" id="theme-btn" onclick="toggleTheme()" title="Toggle Light/Dark Theme" style="background:transparent; border:1px solid var(--border); border-radius:8px; font-size:14px; padding:6px 10px; cursor:pointer;">☀️</button>'''

THEME_TOGGLE_JS = r'''
    function toggleTheme() {
      document.body.classList.toggle('light-mode');
      const isLight = document.body.classList.contains('light-mode');
      localStorage.setItem('theme_mode', isLight ? 'light' : 'dark');
      const btn = document.getElementById('theme-btn');
      if (btn) btn.innerText = isLight ? '🌙' : '☀️';
    }

    // Default to light mode (user preference)
    (function initTheme() {
      const saved = localStorage.getItem('theme_mode');
      if (saved === 'dark') {
        document.body.classList.remove('light-mode');
        window.addEventListener('DOMContentLoaded', () => {
          const btn = document.getElementById('theme-btn');
          if (btn) btn.innerText = '☀️';
        });
      } else {
        document.body.classList.add('light-mode');
        window.addEventListener('DOMContentLoaded', () => {
          const btn = document.getElementById('theme-btn');
          if (btn) btn.innerText = '🌙';
        });
      }
    })();
'''

apps = [
    "brain_to_ai_somatic_marker.html",
    "brain_to_ai_theory_of_mind.html",
    "brain_to_ai_consolidation.html",
    "brain_to_ai_homeostasis.html"
]

for app in apps:
    with open(app, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add CSS
    if "/* LIGHT MODE THEME */" not in content:
        content = content.replace("</style>", LIGHT_MODE_CSS + "\n</style>", 1)

    # 2. Add Theme button in header
    if 'id="theme-btn"' not in content:
        # insert before </header>
        content = re.sub(r'(<button class="btn-config"[^>]*>.*?</button>)', r'\1\n      ' + THEME_TOGGLE_HTML, content)

    # 3. Add JS
    if "function toggleTheme()" not in content:
        content = content.replace("<script>", "<script>\n" + THEME_TOGGLE_JS, 1)

    with open(app, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Upgraded {app} with light mode theme support!")

print("All apps successfully upgraded with light mode!")
