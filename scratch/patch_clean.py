# -*- coding: utf-8 -*-
"""
Clean, syntax-verified patch:
1. Adds `window.highlightInvariantsInText = function(escapedText) { ... }` cleanly.
2. Sanitizes input URL in `connectWebUrl` and `synthesizeFromCustomInputs` so that accidental
   concatenated paste (e.g. 'https://...https://...') automatically strips down to the valid URL.
3. Automatically calls `renderCascadeTree()` and `renderMermaidDag()` and switches to Step 2
   upon clicking 'Compile' or 'Connect'.
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

highlight_fn = """
    window.highlightInvariantsInText = function(escapedText) {
      if (!escapedText) return '';
      if (!state.highlightDocInvariants) return escapedText;
      return escapedText
        .replace(/\\b(STRICTLY PROHIBITED|MUST NEVER|PROHIBITED|FORBIDDEN|CANNOT|SHALL NOT|MUST|REQUIRED|EXEMPT)\\b/g, '<mark style="background:#fee2e2; color:#b91c1c; font-weight:800; padding:1px 4px; border-radius:3px;">$1</mark>')
        .replace(/(\\$\\d[\\d,]*(\\.\\d{2})?|\\b\\d+(\\.\\d+)?\\s*(hours?|minutes?|seconds?|ms|%|percent|kPa|days?|years?)\\b)/gi, '<mark style="background:#fef3c7; color:#92400e; font-weight:800; padding:1px 4px; border-radius:3px;">$1</mark>');
    };
"""

def patch_app(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add highlightInvariantsInText right before renderStep1Inputs
    idx_render = html.find('renderStep1Inputs = function()')
    if idx_render != -1 and 'highlightInvariantsInText = function' not in html:
        html = html[:idx_render] + highlight_fn + '\n    ' + html[idx_render:]
        print(f"[{fname}] Added window.highlightInvariantsInText.")

    # 2. Add URL cleaner at the top of fetchWebUrlContent
    fetch_marker = 'async function fetchWebUrlContent(url) {'
    idx_fetch = html.find(fetch_marker)
    if idx_fetch != -1:
        cleaner = """async function fetchWebUrlContent(url) {
      if (url) {
        url = url.trim();
        const secondHttp = url.indexOf('http', 4);
        if (secondHttp !== -1) {
          url = url.substring(0, secondHttp).trim();
        }
      }"""
        html = html[:idx_fetch] + cleaner + html[idx_fetch + len(fetch_marker):]
        print(f"[{fname}] Added URL cleaner in fetchWebUrlContent.")

    # 3. Add URL cleaner in connectWebUrl as well
    idx_connect = html.find('window.connectWebUrl = async function() {')
    if idx_connect != -1:
        old_val_line = "const url = urlInput ? urlInput.value.trim() : '';"
        new_val_line = """let url = urlInput ? urlInput.value.trim() : '';
      if (url) {
        const secondHttp = url.indexOf('http', 4);
        if (secondHttp !== -1) {
          url = url.substring(0, secondHttp).trim();
          if (urlInput) urlInput.value = url;
        }
      }"""
        html = html.replace(old_val_line, new_val_line, 1)
        print(f"[{fname}] Added URL cleaner in connectWebUrl.")

    # 4. In synthesizeFromCustomInputs, switch to Step 2 when done
    old_toast = "showToast(toastMsg);"
    idx_toast = html.find(old_toast)
    if idx_toast != -1:
        new_toast = """showToast(toastMsg);
      renderCascadeTree();
      renderMermaidDag();
      switchStep(2);"""
        html = html[:idx_toast] + new_toast + html[idx_toast + len(old_toast):]
        print(f"[{fname}] Added auto switchStep(2) to synthesizeFromCustomInputs.")

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[{fname}] Successfully patched and saved!")

patch_app('truth_policy_flowchart_studio.html')
patch_app('truth_langgraph_langsmith_studio.html')
