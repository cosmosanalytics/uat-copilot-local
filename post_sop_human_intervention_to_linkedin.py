import requests
import json

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'

POST_TEXT = """How should humans supervise autonomous AI factories without getting buried in operational weeds? 

The answer is: "Ambient by default, human by exception."

In high-stakes enterprise workflows like S&OP (Sales & Operations Planning), multi-agent systems coordinate multi-million dollar forecasts, plant capacities, and purchase orders. But a human cannot approve 50 micro-steps an hour.

I built a live, browser-native S&OP AI Factory Canvas with a complete Human Intervention UI:
1. 🛡️ 4 Autonomy Levels: Ambient (A), Notify (N), Confirm (C), and Human-Only (H).
2. 🗂️ One Decision Per Card: Plain-English headline, why, 4-cell impact grid ($/units/SLA), risk score, and undo window.
3. 👤 Canvas Human Gate: Draggable approval checkpoints with dynamic waiting pulses.
4. ↩️ Undo Ledger: Every executed action is reversible or flagged, with 1-tap state rollbacks.
5. 📈 Trust Ramp: Automatically promotes C ➔ N after 3 clean approvals; demotes on rejection.
6. 🚦 Global Spend Guards: Actions exceeding $500,000 automatically force human confirmation.

Zero-install, browser-native in high-contrast Light Mode.

👉 Try the live interactive canvas in your browser:
https://cosmosanalytics.github.io/uat-copilot-local/sop_ai_factory_canvas_human_intervention.html

#SupplyChain #AIAgents #AmbientAI #EnterpriseAI #HumanInTheLoop #ProductDesign #SystemsArchitecture #SoftwareEngineering"""

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

print("Publishing S&OP Human Intervention Canvas post to LinkedIn...")
res = requests.post(url, headers=headers, json=payload)
print("Status code:", res.status_code)
print("Response:", res.text)

if res.status_code == 201:
    post_id = res.json().get('id')
    print("SUCCESS! Post published. ID:", post_id)
else:
    print("Failed to post:", res.text)
