# -*- coding: utf-8 -*-
"""
Expands the Mermaid flowchart to fill and expand the available space:
- width: 100%, height: 100%
- Increases nodeSpacing and rankSpacing
- Enforces larger, crystal-clear typography
Applies to both App 08 and App 09 (root and scratch/langchain-test).
"""
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

EXPANDED_CSS = """    .mermaid-svg-container {
      flex: 1;
      min-height: 580px;
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: auto;
      padding: 16px;
    }
    #mermaidGraphEl {
      width: 100% !important;
      height: 100% !important;
      min-height: 540px !important;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    #mermaidGraphEl svg {
      width: 100% !important;
      height: 100% !important;
      max-width: 100% !important;
      min-height: 520px !important;
      max-height: 720px !important;
    }
    #mermaidGraphEl .node text,
    #mermaidGraphEl .label text,
    #mermaidGraphEl text {
      font-size: 13.5px !important;
      font-weight: 600 !important;
    }
    #mermaidGraphEl .edgeLabel text {
      font-size: 12px !important;
      font-weight: 500 !important;
    }"""

EXPANDED_RENDER_FN = """    window.renderMermaidDag = function() {
      const el = document.getElementById('mermaidGraphEl');
      if (!el) return;

      el.removeAttribute('data-processed');
      el.innerHTML = state.mermaidDag;
      try {
        mermaid.init(undefined, el);
        const svg = el.querySelector('svg');
        if (svg) {
          svg.style.width = '100%';
          svg.style.height = '100%';
          svg.style.maxWidth = '100%';
          svg.style.minHeight = '520px';
        }
      } catch (err) {
        console.warn('Mermaid render error:', err);
      }
    };"""

EXPANDED_INIT = """    mermaid.initialize({
      startOnLoad: false,
      theme: 'default',
      flowchart: {
        useMaxWidth: false,
        htmlLabels: true,
        curve: 'basis',
        nodeSpacing: 45,
        rankSpacing: 55,
        padding: 15
      }
    });"""

def expand_app(filepath):
    print(f"Expanding flowchart in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update CSS
    css_pattern = r'\.mermaid-svg-container\s*\{[\s\S]*?padding:\s*10px;\s*\}'
    if re.search(css_pattern, content):
        content = re.sub(css_pattern, EXPANDED_CSS, content)
    elif '#mermaidGraphEl svg' not in content:
        # insert before </style>
        content = content.replace('</style>', f"{EXPANDED_CSS}\n  </style>")

    # 2. Update renderMermaidDag
    render_pattern = r'window\.renderMermaidDag\s*=\s*function\(\)\s*\{[\s\S]*?console\.warn\(\'Mermaid render error:\',\s*err\);\s*\}\s*\};'
    content = re.sub(render_pattern, EXPANDED_RENDER_FN, content)

    # 3. Update mermaid.initialize
    init_pattern = r'mermaid\.initialize\(\{\s*startOnLoad:\s*false,\s*theme:\s*\'default\'\s*\}\);'
    content = re.sub(init_pattern, EXPANDED_INIT, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Done expanding {filepath}!")

for p in [
    'truth_langgraph_langsmith_studio.html',
    'scratch/langchain-test/truth_langgraph_langsmith_studio.html',
    'truth_policy_flowchart_studio.html',
    'scratch/langchain-test/truth_policy_flowchart_studio.html'
]:
    expand_app(p)
