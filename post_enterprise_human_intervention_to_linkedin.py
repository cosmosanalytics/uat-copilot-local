import requests
import json

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'

POST_TEXT = """How should humans supervise autonomous AI factories across an enterprise without getting buried in operational noise?

"Ambient by default, human by exception."

We designed the Enterprise AI Factory across 3 canonical organizational tiers—Company, Organization, and Worker Mind—now equipped with a complete Human Intervention UI:

🏛️ 3 Canonical Tiers (Internal Enterprise Architecture):
• 🏢 Level 3 (Company Value Stream): Connects 6 core organizations—CRM Commercial, S&OP Planning, ERP Core, MES Shop Floor, WMS Logistics, and Finance/Treasury—into a unified operating loop.
• 🏭 Level 2 (Organization Workflows): 38 specialized workers across all 6 departments (MRP II explosions, SMT line dispatch, wave picking, 3-way invoice matching).
• 🧠 Level 1 (Worker Cognitive Mind): Internal "Society of Mind" with dialectical debate personas and deterministic cognitive harnesses.

🛡️ Human Intervention & Autonomous Control System:
1. 🎚️ 4 Autonomy Policy Levels: Ambient (A), Notify (N), Confirm (C), and Human-Only (H) assigned across Company, Organizations, and Workers.
2. 🗂️ Approvals Inbox with Decision Cards: Plain-English headline, why, 4-cell impact grid ($/units/SLA/gap), confidence score, and countdown undo window.
3. 👤 Canvas Human Gate: Visual approval checkpoints on canvas with pulsing waiting states.
4. ↩️ Undo Ledger & Rollback: Every automated action is reversible or flagged, featuring one-click state rollbacks.
5. 📈 Trust Ramp System: Automatically promotes Confirm (C) to Notify (N) after 3 clean approvals; demotes back on human reject.
6. 🚦 Global Spend Guards: Hard safety limits ($500,000 threshold, 90% SLA, 75% confidence) automatically force human confirmation.

Zero-install, browser-native in crisp high-contrast Light Mode.

👉 Explore the live interactive Enterprise AI Factory Canvas:
https://cosmosanalytics.github.io/uat-copilot-local/enterprise_ai_factory_canvas_human_intervention.html

#EnterpriseAI #AIAgents #AmbientAI #AutonomousSystems #HumanInTheLoop #SystemsArchitecture #SoftwareEngineering #SupplyChain"""

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

print("Publishing corrected 3-Tier Enterprise AI Factory post to LinkedIn...")
res = requests.post(url, headers=headers, json=payload)
print("Status code:", res.status_code)
print("Response:", res.text)

if res.status_code == 201:
    post_id = res.json().get('id')
    print("SUCCESS! Post published. ID:", post_id)
else:
    print("Failed to post:", res.text)
