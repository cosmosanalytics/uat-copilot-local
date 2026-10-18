# -*- coding: utf-8 -*-
"""
publish_ambient_ai_brief_to_linkedin.py
Publishes a brief summary of the app to LinkedIn with the GitHub app link only,
highlighting Ambient AI resolving human cognitive limitations.
"""

import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'

POST_TEXT = """Humans have finite cognitive bandwidth. We cannot continuously track thousands of cloud telemetry streams, code diffs, and security alerts without decision fatigue.

The AI Factory CI/CD canvas operationalizes Ambient AI to solve this exact limitation: "Ambient by default, human by exception."

Instead of demanding constant vigilance, ambient agents autonomously run the heavy continuous delivery loop—from Worker AI code generation through GitHub DevSecOps verification into AWS Production Cloud (ECS, Bedrock, Step Functions, Lambda).

Ambient AI interrupts human awareness only at critical inflection gates using high-signal Decision Cards:
• 4-cell impact metrics ($ / latency / SLA / risk)
• Clear dialectical rationales
• 30-second reversible rollback windows

Human judgment is preserved for strategy, while ambient AI absorbs the operational cognitive load.

👉 Experience the live app in your browser:
https://cosmosanalytics.github.io/AWS/

#AmbientAI #CognitiveErgonomics #AIAgents #EnterpriseAI #AWS #SystemsArchitecture #HumanInTheLoop"""

def publish():
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

    print("Publishing brief Ambient AI summary post to LinkedIn...")
    res = requests.post(url, headers=headers, json=payload)
    print("Status code:", res.status_code)
    print("Response:", res.text)
    if res.status_code == 201:
        data = res.json()
        print("SUCCESS! Post published with URN:", data.get("id"))
    else:
        print("Publishing failed with status:", res.status_code)

if __name__ == "__main__":
    publish()
