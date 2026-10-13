# -*- coding: utf-8 -*-
"""
post_cognitive_pyramid_to_linkedin.py
Publishes a very brief summary of the 3-Tier Extended Cognitive Pyramid app with only the GitHub app link to LinkedIn.
"""

import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'

POST_TEXT = """What happens when you augment enterprise AI agents with capabilities from human neuroscience?

I built an interactive web app modeling The Agent Brain in Three Tiers: combining 12 original cloud primitives with 8 extended cognitive capabilities:

🔺 Tier 0 (Foundations): + Perceives (sensory intake) & + Regulates (autonomic token/memory budget)
🧠 Tier 1 (Executive Mind): + Prioritizes (goal weighting), + Adapts (dynamic DAG pivoting) & + Learns (episodic plasticity)
🌐 Tier 2 (Networked Brain): + Reads intent (Theory of Mind), + Speaks (calibrated language) & + Stays aware (collective swarm consciousness)

⚡ Includes a live Side-by-Side Advantage Benchmark proving how cognitive extensions achieve 100% recovery vs. brittle pipeline crashes, while cutting token burn by 78%. Runs in-browser via WebGPU/WebLLM, Groq LPU (~200ms), or instant simulator.

👉 Interactive App: https://cosmosanalytics.github.io/uat-copilot-local/agent_extended_cognitive_pyramid.html

#AIEngineering #EnterpriseAI #CognitiveArchitecture #MultiAgent #WebGPU #WebLLM #Neuroscience"""

url = "https://api.linkedin.com/v2/ugcPosts"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
}

payload = {
    "author": MEMBER_URN,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": POST_TEXT
            },
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

print("Publishing Extended Cognitive Pyramid summary to LinkedIn...")
res = requests.post(url, headers=headers, json=payload)
print("Status code:", res.status_code)
print("Response:", res.text)

if res.status_code == 201:
    post_id = res.json().get('id')
    print(f"SUCCESS! Post published to LinkedIn. Post ID: {post_id}")
else:
    print(f"Failed with status code: {res.status_code}")
