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

POST_TEXT = """Built an Onyx-type chatbot with side-by-side invariant grounding in a clean, crisp Light Mode UI! 💎✨

Key Highlights:
• 🎯 Direct Straight Answers: Gives succinct, direct answers in line 1 for names, amounts, and decisions without fluff or robotic quote walls.
• ⚖️ OpenJev Invariant Validation: Integrated OpenJev as a programmatic True/False evaluation judge on every answer, computing entailment confidence and citing verified source context anchors.
• 👥 Side-by-Side Invariant Grounding: Paste any document, policy, or live web URL on the left; reason with strict ground-truth guardrails on the right.
• ⚡ Dual Neural Inference: Switch seamlessly between 100% private in-browser WebGPU (Llama-3.2 via WebLLM) and sub-second cloud Groq LPU (Llama-3.3-70B).
• 🕸️ Interactive Flowchart DAGs: Synthesizes narrative dilemmas, actions, and resolutions directly into live Mermaid.js decision graphs.
• 🚀 100% Client-Side: Single standalone HTML application with responsive mobile tabs (Split / Chat / Story).

🔗 Try the Live Web App: https://cosmosanalytics.github.io/Langchain-test/onyx_truth_chatbot.html

#AI #MachineLearning #WebGPU #WebLLM #Groq #OpenJev #LLMEvaluation #GroundTruth #LangChain #SoftwareEngineering"""

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

print("Publishing post to LinkedIn...")
response = requests.post(URL, headers=HEADERS, json=payload)
print(f"Status Code: {response.status_code}")
if response.status_code in (200, 201):
    data = response.json()
    post_id = data.get("id")
    print(f"Post successfully published! Post ID: {post_id}")
    urn_id = post_id.split(":")[-1] if post_id else ""
    print(f"LinkedIn URL: https://www.linkedin.com/feed/update/{post_id}/")
else:
    print(f"Failed to publish post: {response.text}")
