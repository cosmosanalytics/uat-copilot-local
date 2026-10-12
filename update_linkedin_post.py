# -*- coding: utf-8 -*-
"""
update_linkedin_post.py
Deletes the previous post with the repo link and publishes the clean post
with ONLY the live web app link (no github.com repo link).
"""

import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'
PREVIOUS_POST_URN = 'urn:li:share:7515232347730993152'

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
}

# 1. Delete previous post
print(f"Deleting previous post {PREVIOUS_POST_URN}...")
del_url = f"https://api.linkedin.com/v2/ugcPosts/{requests.utils.quote(PREVIOUS_POST_URN)}"
del_res = requests.delete(del_url, headers=headers)
print(f"Delete status: {del_res.status_code}")
if del_res.status_code != 204:
    # Try rest/posts endpoint as fallback
    alt_del_url = f"https://api.linkedin.com/rest/posts/{requests.utils.quote(PREVIOUS_POST_URN)}"
    alt_headers = dict(headers)
    alt_headers["LinkedIn-Version"] = "202609"
    alt_res = requests.delete(alt_del_url, headers=alt_headers)
    print(f"Fallback delete status: {alt_res.status_code}")

POST_TEXT = """Autonomous Sales & Operations Planning (S&OP) requires more than raw LLM generation—it needs a deterministic multi-agent architecture.

I built a browser-native S&OP Multi-Agent Swarm application (single-file HTML, running with Groq LPU, in-browser WebLLM / WebGPU, and an instant simulator):

🌐 11-Stage S&OP Process Across 3 Pods:
• Demand Pod (Stages 1–5): Aggregate, Forecast, Consensus, Disaggregate, Consumption
• Supply Pod (Stages 6–9): Dependent Demand, Firming, Capacity Pooling, Inventory
• Control Pod (Stages 10–11): Variance Watchdog & Executive Escalation

🛡️ Enterprise Swarm Controls:
• O(N) Shared Whiteboard with DynamoDB CAS mutex locks (stops O(N²) message storms)
• Byzantine Consensus Quorum (≥ 2/3 + 1 votes backed by S3 WORM contracts & vector proofs)
• Circuit Breakers that automatically bench misbehaving agents releasing unauthorized POs

Try the interactive app directly in your browser:
👉 Live App: https://cosmosanalytics.github.io/uat-copilot-local/sop_multi_agent_swarm_app.html

#AIEngineering #SupplyChain #MultiAgent #WebGPU #WebLLM #EnterpriseAI #AutonomousAgents"""

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

print("Publishing clean S&OP summary (NO repo link) to LinkedIn...")
url = "https://api.linkedin.com/v2/ugcPosts"
res = requests.post(url, headers=headers, json=payload)
print("Status code:", res.status_code)
print("Response:", res.text)

if res.status_code == 201:
    post_id = res.json().get('id')
    print(f"SUCCESS! Clean post published to LinkedIn. Post ID: {post_id}")
