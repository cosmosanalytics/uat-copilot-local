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

POST_TEXT = """Excited to release Onyx Truth Studio (App 10) 💎✨ — a side-by-side, invariant-grounded reasoning chatbot powered by in-browser WebGPU and Groq LPU!

Key Highlights:
• 👥 Side-by-Side Invariant Grounding: Paste any document excerpt, policy, or live web URL on the left; reason with strict ground-truth zero-hallucination guardrails on the right.
• ⚡ Dual Neural Inference: Switch seamlessly between 100% private in-browser WebGPU (Llama-3.2 via WebLLM) and ultra-fast cloud Groq LPU (Llama-3.3-70B at 500+ tok/s).
• 🕸️ LLM Flowchart DAG Compiler: Prompts the LLM to analyze the source narrative or SOP and renders interactive Mermaid.js decision graphs live in chat.
• 🚀 100% Client-Side: Single standalone HTML file with zero server dependencies.

🔗 Live Web App: https://cosmosanalytics.github.io/Langchain-test/onyx_truth_chatbot.html
📁 GitHub Repo: https://github.com/cosmosanalytics/Langchain-test

#AI #MachineLearning #WebGPU #WebLLM #Groq #OpenSource #LangChain #ArtificialIntelligence #SoftwareEngineering"""

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
    # Form post URL
    urn_id = post_id.split(":")[-1] if post_id else ""
    print(f"LinkedIn URL: https://www.linkedin.com/feed/update/{post_id}/")
else:
    print(f"Failed to publish post: {response.text}")
