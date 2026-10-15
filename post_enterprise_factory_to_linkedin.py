# -*- coding: utf-8 -*-
import os
import sys
import json
import requests

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = os.environ.get("LINKEDIN_ACCESS_TOKEN") or 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = os.environ.get("LINKEDIN_PERSON_URN") or 'urn:li:person:muZwZNN9P9'

POST_TEXT = """How do you orchestrate autonomous AI from multi-enterprise supply chains down to intra-agent cognition?

I built an interactive 4-tier fractal AI factory canvas that runs 100% in your browser (WebLLM / WebGPU / Groq LPU):

🌐 Level 4 (Value Chain): 6 Interconnected Enterprises (Foundry, Substrates, OEM, EMS, 3PL, Hyperscaler)
🏢 Level 3 (Company): 6 Enterprise Organizations (CRM, S&OP, ERP, MES, WMS, Finance)
🏭 Level 2 (Organization): 38 Specialized Workers executing end-to-end business workflows
🧠 Level 1 (Mind): Society of Mind with Dialectical Debate personas, deterministic harness, and memory guards

Interactive browser app:
https://cosmosanalytics.github.io/uat-copilot-local/enterprise_ai_factory_canvas.html

#AIEngineering #AIAgents #EnterpriseAI #SupplyChain #WebGPU #WebLLM #SystemArchitecture"""

print("Attempting to publish to LinkedIn...")

# Try UGC Posts API
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
print(f"UGC API Status: {res.status_code}")

if res.status_code == 201:
    post_id = res.json().get('id')
    print(f"SUCCESS! Post published via UGC API. Post ID: {post_id}")
else:
    print(f"UGC API response: {res.text}")
    print("Trying Rest Posts API...")
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
    print(f"Rest API Status: {res2.status_code}")
    if res2.status_code in [200, 201]:
        print(f"SUCCESS! Post published via REST API. Response: {res2.text}")
    else:
        print(f"Rest API response: {res2.text}")
