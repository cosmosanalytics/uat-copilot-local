import requests
import json

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'

POST_TEXT = """Human working memory has only ~4 cognitive slots (Miller's Law), yet modern software bombards us with hundreds of micro-decisions every hour. 

Ambient AI flips this interface: the machine absorbs 95% of operational cognitive load in the background, surfacing only high-leverage executive choices.

I built a zero-install, single-file browser app demonstrating Ambient AI across 6 everyday domains:
1. 📧 Inbox Triage: 87 unread emails condensed into 1 actionable card.
2. 📊 Spreadsheet Discrepancies: Pinpointing $42.15 invoice mismatches instantly.
3. 📅 Calendar Harmonizer: Seamless cross-timezone consensus (Tokyo/London/NYC).
4. 📑 Contract HUD: Surfacing hidden uncapped liability in 20-page agreements.
5. 🐙 Git Merge Conflicts: AST auto-resolution without manual diff terror.
6. 🛒 Choice Paralysis: Filtering 40 options down to 2 clear trade-offs.

Powered by Groq LPU (~500 tok/s) and local WebLLM / WebGPU with real-time cognitive metrics.

👉 Try the live interactive web app in your browser:
https://cosmosanalytics.github.io/uat-copilot-local/ambient_ai_everyday_cognitive_ergonomics.html

#AmbientAI #CognitiveErgonomics #ArtificialIntelligence #WebLLM #Groq #UXDesign #ProductDesign #HumanComputerInteraction"""

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

print("Publishing Ambient AI Everyday Cognitive Ergonomics post to LinkedIn...")
res = requests.post(url, headers=headers, json=payload)
print("Status code:", res.status_code)
print("Response:", res.text)

if res.status_code == 201:
    post_id = res.json().get('id')
    print("SUCCESS! Post published. ID:", post_id)
else:
    print("Failed to post:", res.text)
