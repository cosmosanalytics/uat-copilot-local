# -*- coding: utf-8 -*-
"""
Injects the Universal Live Web Fetcher and Semantic Ground Truth Synthesizer
into truth_policy_flowchart_studio.html and truth_langgraph_langsmith_studio.html
"""
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/universal_distill.js', 'r', encoding='utf-8') as f:
    universal_code = f.read()

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update the Connect button to have an ID so we can toggle spinner
    html = html.replace('onclick="applyCustomWebUrl()">Connect</button>', 'id="connectWebBtn" onclick="applyCustomWebUrl()">Connect</button>')

    # 2. Find the start of distillUrlToKnowledge
    start_idx = html.find('function distillUrlToKnowledge(url)')
    if start_idx == -1:
        start_idx = html.find('distillUrlToKnowledge =')

    # Find the end of synthesizeFromCustomInputs block
    end_marker = 'showToast(isLiterary'
    end_idx = html.find(end_marker, start_idx)
    if end_idx != -1:
        # Find the closing brace of synthesizeFromCustomInputs
        close_brace_idx = html.find('};', end_idx) + 2
    else:
        print(f"Could not find end marker in {filename}")
        return False

    print(f"[{filename}] Replacing from {start_idx} to {close_brace_idx} (len {close_brace_idx - start_idx})")

    # Construct the updated code block including applyCustomWebUrl
    replacement_block = universal_code + """
    applyCustomWebUrl = async function() {
      await connectWebUrl();
    };
"""

    new_html = html[:start_idx] + replacement_block + html[close_brace_idx:]

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"Successfully updated {filename}!")
    return True

update_file('truth_policy_flowchart_studio.html')
update_file('truth_langgraph_langsmith_studio.html')
