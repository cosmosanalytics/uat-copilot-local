# -*- coding: utf-8 -*-
import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'
URL = "https://api.linkedin.com/v2/ugcPosts"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
}

POST_TEXT = """Excited to share the Frontend Design Agent Studio: a standalone, HTML-only web app demonstrating the safest open-source agent skill — frontend-design (Apache 2.0)! 🎨⚡

Starting from the Open-Source Skills Map, this app isolates the #1 safest browser-ready skill and runs it directly on client hardware:

• 🛡️ Safest Open-Source Skill: 100% text-only runbook under Apache 2.0. Zero host execution, zero Python dependencies, zero security risks.
• ⚡ Dual In-Browser Inference: Runs fully locally on WebGPU via WebLLM (@mlc-ai/web-llm) or through Groq LPU (500+ tok/s), with instant showcase presets.
• 📐 Anti-Generic UI Synthesis: Mounts Anthropic's frontend-design runbook to avoid generic AI SaaS templates, enforcing deliberate palettes, intentional typography, and single bold focal points.
• 👁️ Real-Time Sandbox: Renders live responsive prototypes (Desktop / Tablet / Mobile) with instant code inspection and export.

🔗 Live Web App:
https://cosmosanalytics.github.io/uat-copilot-local/frontend_design_app.html

💻 GitHub Repo:
https://github.com/cosmosanalytics/uat-copilot-local

#AIAgents #WebGPU #WebLLM #Groq #OpenSource #Frontend #WebDevelopment #UIDesign"""

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

print("Publishing Frontend Design Agent summary to LinkedIn...")
res = requests.post(URL, headers=HEADERS, json=payload)
print(f"Status code: {res.status_code}")
print(f"Response: {res.text}")

if res.status_code == 201:
    post_id = res.json().get('id')
    print(f"\nSUCCESS! Post published. ID: {post_id}")
else:
    print("\nFAILED to publish post.")
