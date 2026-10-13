# -*- coding: utf-8 -*-
"""
post_gif_summary_to_linkedin.py
Uploads the proactive system advantages GIF recording and publishes
a brief summary post to LinkedIn.
"""

import os
import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'
GIF_PATH = 'proactive_system_advantages_recording.gif'

POST_TEXT = """Reactive Core vs. Proactive Cognitive Stack: 4 Live Duels 🎬

What happens when you augment deterministic AI agents with proactive capabilities from human cognition?

Watch the side-by-side benchmark comparing the Reactive Core Alone against the Proactive Cognitive Stack across 4 disruptions:

1. 🛑 The Dead-End Trap: Reactive loops 3x into fatal crash; Proactive prunes the dead route & detours in 1.4s (100% recovery).
2. 🌊 Context Window Storm: Reactive hits HTTP 429 throttle; Proactive regulates burn rate & saves 78% tokens.
3. 🤝 Swarm Deadlock: Reactive dumps 14 rounds of JSON bloat; Proactive reads intent to agree in 2 rounds (-85% chatter).
4. 🧠 Repeat Disturbance: Reactive re-evaluates 28 steps from scratch; Proactive recalls episodic heuristic in 180ms.

📊 The Net Delta:
• +300% Reliability on Out-of-Distribution Shocks
• -78% Total Token Burn Costs
• 8.8× Faster Convergence Speed

👉 Interactive App (WebGPU WebLLM + Groq LPU):
https://cosmosanalytics.github.io/uat-copilot-local/agent_extended_cognitive_pyramid.html

#AIEngineering #EnterpriseAI #CognitiveArchitecture #MultiAgent #WebGPU #Neuroscience"""

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'LinkedIn-Version': '202609'
}

print("1. Initializing Image Upload on LinkedIn...")
init_url = 'https://api.linkedin.com/rest/images?action=initializeUpload'
init_payload = {
    'initializeUploadRequest': {
        'owner': MEMBER_URN
    }
}
init_res = requests.post(init_url, headers=headers, json=init_payload)
print("Init status:", init_res.status_code)

if init_res.status_code != 200:
    print("Init error:", init_res.text)
    sys.exit(1)

init_data = init_res.json()
upload_url = init_data['value']['uploadUrl']
image_urn = init_data['value']['image']
print("Image URN:", image_urn)

print("2. Uploading GIF binary to LinkedIn...")
with open(GIF_PATH, 'rb') as f:
    gif_bytes = f.read()

up_headers = {
    'Authorization': f'Bearer {TOKEN}'
}
up_res = requests.put(upload_url, data=gif_bytes, headers=up_headers)
print("Upload status:", up_res.status_code)

if up_res.status_code not in (200, 201):
    print("Upload failed:", up_res.text)
    sys.exit(1)

print("3. Publishing Post with Attached GIF Animation...")
post_url = 'https://api.linkedin.com/rest/posts'
post_payload = {
    'author': MEMBER_URN,
    'commentary': POST_TEXT,
    'visibility': 'PUBLIC',
    'distribution': {
        'feedDistribution': 'MAIN_FEED',
        'targetEntities': [],
        'thirdPartyDistributionChannels': []
    },
    'content': {
        'media': {
            'id': image_urn,
            'title': 'Reactive Core vs Proactive Cognitive Stack: 4 Live Duels'
        }
    },
    'lifecycleState': 'PUBLISHED',
    'isReshareDisabledByAuthor': False
}

post_res = requests.post(post_url, headers=headers, json=post_payload)
print("Publish status code:", post_res.status_code)
print("Response text:", post_res.text)

if post_res.status_code == 201:
    post_urn = post_res.headers.get('x-restli-id')
    print(f"SUCCESS! Post published with GIF attached. Post URN: {post_urn}")
else:
    print("Publishing failed.")
