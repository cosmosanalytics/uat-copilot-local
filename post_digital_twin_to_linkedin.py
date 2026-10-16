# -*- coding: utf-8 -*-
"""
post_digital_twin_to_linkedin.py
Publishes a brief summary of The Local-First Personal Digital Twin web app to LinkedIn with GitHub app link only.
"""

import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'

text = """The Local-First Personal Digital Twin: 100% Private, On-Device AI ⚡👤

Your private career memory vault, executive rehearsal coach, and knowledge engine running entirely inside your browser:

• 🛡️ Zero-Cloud Durability: Protected from browser cache eviction via navigator.storage.persist() with native hard disk mounting and encrypted .twin backups.
• 📉 Ebbinghaus Memory Retention: Mathematical forgetting curve modeling with spaced repetition reinforcement to lock career anchors permanently.
• 🎙️ Live Rehearsal Studio: Practice salary negotiations, staff+ architecture defenses, and board pitches with real-time critique from your digital twin.
• ⚡ Dual AI Inference: Instant Groq LPU (~500 tok/s) and local WebLLM / WebGPU with Python Wasm execution at $0 cloud spend.

👉 Run the live interactive app directly in your browser:
https://cosmosanalytics.github.io/uat-copilot-local/personal_digital_twin_local.html

#DigitalTwin #LocalFirst #WebGPU #WebAssembly #PrivacyFirst #AIAgents #OpenSource"""

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
    print("Publishing Personal Digital Twin post to LinkedIn...")
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
