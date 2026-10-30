with open('scratch/patch_smart_synthesis.py', 'r', encoding='utf-8') as f:
    code = f.read()

exec(code)

import re

def patch_app(filepath):
    print(f"Patching {filepath} with adaptive genre synthesis...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'window\.synthesizeFromCustomInputs\s*=\s*function\(\)\s*\{[\s\S]*?showToast\([^\)]+\);\s*\};'
    content = re.sub(pattern, lambda m: SMART_SYNTHESIS_JS.strip(), content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}!")

for p in [
    'truth_policy_flowchart_studio.html',
    'scratch/langchain-test/truth_policy_flowchart_studio.html',
    'truth_langgraph_langsmith_studio.html',
    'scratch/langchain-test/truth_langgraph_langsmith_studio.html'
]:
    patch_app(p)
