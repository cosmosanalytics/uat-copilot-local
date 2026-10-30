# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

for fname in ['truth_policy_flowchart_studio.html', 'truth_langgraph_langsmith_studio.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()

    # Clear anything between <textarea id="customDocTextInput"...> and </textarea>
    pattern = r'(<textarea id="customDocTextInput"[^>]*>)(.*?)(</textarea>)'
    
    def repl(m):
        # Return opening tag + empty content + closing tag
        return m.group(1) + m.group(3)

    new_html = re.sub(pattern, repl, html, flags=re.DOTALL)

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"[{fname}] Successfully emptied textarea!")
