# -*- coding: utf-8 -*-
"""
post_ai_factory_app_to_linkedin.py
Publishes a brief summary of the AI Agent Factory & In-Browser AWS Simulator to LinkedIn with GitHub app link only.
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

text = """Introducing the AI Agent Factory & In-Browser AWS Simulator! ⚡🛠️

Design, assemble, and stress-test autonomous AI agent systems entirely inside your browser:

• 🎨 Interactive Visual Flow Canvas: Drag & drop agent primitives with dynamic cubic bezier cables, port-to-port routing, and real-time pulse animations.
• 🧩 7-Step Assembly Protocol: From natural language requirements to tiered LEGO skills (Tier 0 Primitives, Tier 1 Single Agent, Tier 2 Multi-Agent Teams) with automated Bill of Materials (BOM).
• ☁️ In-Browser AWS Simulator: 8 client-side primitives powered by PyScript & Pyodide—testing DynamoDB TTL, ElastiCache context decay, SQS priority queues, WAF rate limits, and Circuit Breakers with zero AWS bill.
• 🧠 Dual AI Copilot: Instant Groq LPU (~500 tok/s) and local WebGPU / WebLLM models on device.

👉 Run the live interactive app directly in your browser:
https://cosmosanalytics.github.io/uat-copilot-local/ai_factory_aws_simulator.html

#AIAgents #AgenticAI #WebAssembly #PyScript #SystemArchitecture #AWS #WebGPU #OpenSource"""

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

    print("Publishing AI Agent Factory post to LinkedIn...")
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
