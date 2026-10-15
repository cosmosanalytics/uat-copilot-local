# -*- coding: utf-8 -*-
"""
post_gcp_app_to_linkedin.py
Publishes a very brief summary of the Google Cloud AI Factory app with GitHub app only link to LinkedIn.
"""

import os
import sys
import json
import requests

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = os.environ.get("LINKEDIN_ACCESS_TOKEN") or 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = os.environ.get("LINKEDIN_PERSON_URN") or 'urn:li:person:muZwZNN9P9'

POST_TEXT = """How do you design, assemble, and stress-test autonomous AI agents on Google Cloud with zero cloud bill? 🌐⚡

I built an interactive in-browser Google Cloud Simulator & AI Agent Factory running 100% client-side (WebLLM / WebGPU / Groq LPU):

• 🎨 Visual Flow Canvas: Drag & drop GCP primitives with dynamic cubic bezier routing and real-time execution pulses.
• 🧩 7-Step Assembly Protocol: Transforms natural language requirements into tiered LEGO skills with an automated Bill of Materials (BOM).
• ☁️ In-Browser GCP Engine: Tests Cloud Firestore TTL & precondition locks, Memorystore for Redis context decay, Cloud Pub/Sub ack deadlines, Cloud Workflows retries, and Apigee Circuit Breakers.
• 🧠 Dual AI Copilot: Groq LPU (~500 tok/s), local on-device WebGPU models, or deterministic offline compiler.

Try the live interactive app directly in your browser:
https://cosmosanalytics.github.io/uat-copilot-local/ai_factory_gcp_simulator.html

#AIEngineering #AIAgents #GoogleCloud #GCP #WebGPU #WebLLM #CloudArchitecture #OpenSource"""

print("Publishing Google Cloud AI Factory post to LinkedIn...")

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

res = requests.post(url, headers=headers, json=payload)
print(f"UGC API Status Code: {res.status_code}")

if res.status_code == 201:
    post_id = res.json().get('id')
    print(f"SUCCESS! Post published to LinkedIn. Post ID: {post_id}")
else:
    print(f"UGC API response: {res.text}")
    print("Attempting via REST Posts API...")
    rest_url = "https://api.linkedin.com/rest/posts"
    rest_headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0',
        'LinkedIn-Version': '202609'
    }
    rest_payload = {
        "author": MEMBER_URN,
        "commentary": POST_TEXT,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }
    res2 = requests.post(rest_url, headers=rest_headers, json=rest_payload)
    print(f"REST API Status Code: {res2.status_code}")
    if res2.status_code in [200, 201]:
        print(f"SUCCESS! Post published via REST API. Response: {res2.text}")
    else:
        print(f"REST API response: {res2.text}")
