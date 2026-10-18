# -*- coding: utf-8 -*-
"""
post_enterprise_ai_factory_to_linkedin.py
Publishes a brief summary of the Enterprise AI Factory (Company -> All 6 Organizations -> Worker Mind)
to LinkedIn with the GitHub app link only.
"""

import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'

def escape_little_text(text: str) -> str:
    reserved = ['\\', '|', '{', '}', '@', '[', ']', '(', ')', '<', '>', '*', '_', '~']
    for ch in reserved:
        text = text.replace(ch, '\\' + ch)
    return text

text = """The Complete Enterprise AI Factory: From Corporate Ecosystem to Worker Mind! 🌐🏢

We just launched a 3-tier fractal studio modeling an entire autonomous enterprise inside your browser:

• 🏢 Level 3 (Company Value Stream): Connects 6 core organizations—CRM Commercial, S&OP Planning, ERP Core, MES Shop Floor, WMS Logistics, and Finance/Treasury—into a unified operating loop.
• 🏭 Level 2 (Organization Workflows): 38 specialized workers across all 6 departments, from MRP II component explosion to SMT line dispatch, wave picking, and 3-way invoice matching.
• 🧠 Level 1 (Worker Cognitive Mind): Every worker is modeled as an internal "Society of Mind" with dialectical debate personas and cognitive skills (ElastiCache, DynamoDB, Cedar policy gates).
• 📱 Mobile-First Interactive Canvas: Full-width canvas, touch gestures, sliding drawers, and animated bezier cables running 100% client-side with Groq LPU (~500 tok/s) and local WebGPU.

👉 Explore the live Enterprise AI Factory directly in your browser:
https://cosmosanalytics.github.io/uat-copilot-local/company_ai_factory_canvas.html

#EnterpriseAI #AgenticAI #SupplyChain #ERP #SOP #DigitalTransformation #WebGPU #Groq #OpenSource"""

def publish():
    url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202609"
    }

    escaped = escape_little_text(text)
    payload = {
        "author": MEMBER_URN,
        "commentary": escaped,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    print("Publishing Enterprise AI Factory post to LinkedIn...")
    res = requests.post(url, headers=headers, json=payload)
    print("Status code:", res.status_code)
    print("Response headers:", dict(res.headers))
    print("Response text:", res.text)

    if res.status_code == 201:
        post_urn = res.headers.get("x-restli-id") or res.headers.get("x-linkedin-id")
        print(f"\n[SUCCESS] Successfully published to LinkedIn! Post URN: {post_urn}")
        return post_urn
    else:
        print("\n[FALLBACK] Trying /v2/ugcPosts endpoint...")
        url_ugc = "https://api.linkedin.com/v2/ugcPosts"
        headers_ugc = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        payload_ugc = {
            "author": MEMBER_URN,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        res2 = requests.post(url_ugc, headers=headers_ugc, json=payload_ugc)
        print("Fallback Status code:", res2.status_code)
        print("Fallback Response:", res2.text)
        if res2.status_code == 201:
            post_id = res2.json().get('id')
            print(f"\n[SUCCESS] Successfully published via UGC! ID: {post_id}")
            return post_id
        return None

if __name__ == "__main__":
    publish()
