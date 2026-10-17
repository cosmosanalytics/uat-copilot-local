import requests
import json

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'

POST_TEXT = """How do enterprise leaders govern autonomous AI swarms across multi-tier organizational hierarchies without cognitive overload?

"Ambient by default, human by exception."

Across entire enterprises—connecting corporate leadership, business units, functional tribes, and autonomous agent pods—human oversight cannot scale through micromanagement. It scales through principled ambient governance.

I built a live, interactive Enterprise AI Factory Canvas with a complete Human Intervention UI:

1. 🏛️ 4-Tier Enterprise Governance: Seamlessly orchestrate autonomy across Enterprise, Lines of Business, Functional Tribes, and Agent Pods.
2. 🛡️ 4 Autonomy Policy Levels: Ambient (A), Notify (N), Confirm (C), and Human-Only (H) assigned per organizational tier.
3. 🗂️ Approvals Inbox with Decision Cards: Plain-English headline, why, 4-cell impact grid ($/units/SLA/gap), confidence score, and undo window.
4. 👤 Canvas Human Gate: Visual drag-and-drop approval nodes with pulsing status cues and branched approve/reject routing.
5. ↩️ Undo Ledger & Rollback: Every automated action is reversible or flagged, featuring one-click state rollbacks.
6. 📈 Trust Ramp System: Automatically promotes Confirm (C) to Notify (N) after 3 clean approvals; demotes back on human reject.
7. 🚦 Global Spend Guards: Hard safety limits ($500,000 threshold, 90% SLA, 75% confidence) automatically force human confirmation.

Zero-install, browser-native in crisp high-contrast Light Mode.

👉 Try the live interactive canvas in your browser:
https://cosmosanalytics.github.io/uat-copilot-local/enterprise_ai_factory_canvas_human_intervention.html

#EnterpriseAI #AIAgents #AmbientAI #AutonomousSystems #HumanInTheLoop #SystemsArchitecture #SoftwareEngineering #AIOrchestration"""

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

print("Publishing Enterprise Human Intervention Canvas post to LinkedIn...")
res = requests.post(url, headers=headers, json=payload)
print("Status code:", res.status_code)
print("Response:", res.text)

if res.status_code == 201:
    post_id = res.json().get('id')
    print("SUCCESS! Post published. ID:", post_id)
else:
    print("Failed to post:", res.text)
