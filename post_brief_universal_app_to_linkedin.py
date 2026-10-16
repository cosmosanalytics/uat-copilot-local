# -*- coding: utf-8 -*-
"""
post_brief_universal_app_to_linkedin.py
Publishes a very brief summary of the Universal AI Agent Factory app to LinkedIn with GitHub app link only.
"""

import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'

text = """The Universal AI Agent Factory: Maximize the Core, Minimize the Cloud ⚡⬡

Across AWS, Azure, GCP, Cloudflare, Kubernetes, Databricks, and Oracle OCI, we implemented the Hexagonal Architecture for autonomous AI agents:

• 88% Invariant Core: Cognitive tiering, invariant contract verification, quorum consensus, and 7-step assembly protocol—written once, runs identically anywhere.
• 12% Isolated Periphery: Thin pluggable drivers for KV, queues, caches, and circuit breakers hot-swapped across all 7 cloud platforms with 0 core code changes.
• Dual AI Copilot: Instant Groq LPU (~500 tok/s) and local WebGPU / WebLLM with client-side Python Wasm execution at $0 cloud cost.

👉 Run the live interactive app directly in your browser:
https://cosmosanalytics.github.io/uat-copilot-local/ai_factory_universal_core.html

#SoftwareArchitecture #AIAgents #AgenticAI #CloudArchitecture #WebAssembly #OpenSource"""

def publish():
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
    print("Publishing brief Universal AI Factory summary to LinkedIn...")
    res = requests.post(url_ugc, headers=headers_ugc, json=payload_ugc)
    print("Status code:", res.status_code)
    print("Response:", res.text)
    if res.status_code == 201:
        post_id = res.json().get('id')
        print(f"\n[SUCCESS] Successfully published to LinkedIn! ID: {post_id}")
        return post_id
    return None

if __name__ == "__main__":
    publish()
