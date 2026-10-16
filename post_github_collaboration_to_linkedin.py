# -*- coding: utf-8 -*-
"""
post_github_collaboration_to_linkedin.py
Publishes a brief summary of GitHub Multi-Agent Collaboration Simulator to LinkedIn with GitHub app link only.
"""

import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'

text = """GitHub Agent Collaboration Simulator: Multi-Agent PRs & CI/CD Pipelines ⚡🐙

What does software development look like when autonomous AI agents collaborate as a team on GitHub?

We built an in-browser GitHub PR & CI/CD workflow simulator powered by specialized multi-agent roles:

• 👩‍💻 Alice (Feature Dev Agent): Implements features, generates clean diffs, and opens PR #42 for distributed 2/3 quorum consensus.
• 🔍 Bob (Security & Invariant Auditor): Audits code diffs for secret leaks and blocks merges with "Changes Requested" if invariant bounds are breached.
• 🤖 Charlie (GitHub Actions CI/CD Bot): Runs unit test suites, linter checks, and secret scanners, streaming live workflow logs.
• 👑 Diana (Lead Maintainer Agent): Reviews architecture, approves consensus, and triggers Squash & Merge into production main.
• ⚡ Dual AI Inference: Groq LPU (~500 tok/s) and local WebLLM / WebGPU with Python Wasm execution at $0 cloud spend.

👉 Run the live interactive app directly in your browser:
https://cosmosanalytics.github.io/uat-copilot-local/github_agent_collaboration_simulator.html

#GitHub #CICD #AIAgents #AgenticAI #DevOps #SoftwareEngineering #WebAssembly #OpenSource"""

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
    print("Publishing GitHub Agent Collaboration post to LinkedIn...")
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
