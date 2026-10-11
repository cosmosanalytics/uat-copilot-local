# -*- coding: utf-8 -*-
import json
import re

with open('multi_agent_system_studio_app.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'const SWARM_SKILLS_LIBRARY = (\[[\s\S]*?\]);', content)
if m:
    skills = json.loads(m.group(1))
    print(f"Total skills: {len(skills)}")
    for i, s in enumerate(skills):
        print(f"{i+1:2d}. [{s['tierCode']}] {s['name']} -> {s['title']}")
else:
    print("Could not find SWARM_SKILLS_LIBRARY")
