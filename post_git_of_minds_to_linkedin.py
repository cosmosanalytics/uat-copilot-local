# -*- coding: utf-8 -*-
"""
post_git_of_minds_to_linkedin.py
Publishes a brief summary of Git of Minds (DAG of Agent Thought) to LinkedIn with GitHub app link only.
"""

import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'

text = """Git of Minds: Visual Git for Agentic Thought & Speculative Branching ⚡🌿

What if complex agent reasoning wasn't a linear chat thread, but a Git repository?

When an autonomous agent faces an ambiguous decision, it shouldn't just guess—it branches into 3 competing timelines:

• 🌿 Interactive Git Graph Canvas: Visual DAG of Minds with commit inspection, branch switching (feat/aggressive, feat/cautious, feat/lateral), and animated DAG edges.
• 🍒 Cherry-Pick & Merge Protocol: Resolve cognitive merge conflicts by cherry-picking isolated insights and executing consensus merges into production HEAD.
• 🔍 Speculative Branch Comparator: Side-by-side trade-off evaluations comparing execution velocity, risk indices, and simulated failure rates.
• ⚡ Dual AI Inference: Instant Groq LPU (~500 tok/s) and local WebLLM / WebGPU with Python WebAssembly execution at $0 cloud spend.

👉 Run the live interactive app directly in your browser:
https://cosmosanalytics.github.io/uat-copilot-local/git_of_minds_simulator.html

#AIAgents #AgenticAI #GitOfMinds #TreeOfThought #SoftwareArchitecture #WebAssembly #WebGPU #OpenSource"""

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
    print("Publishing Git of Minds post to LinkedIn...")
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
