# -*- coding: utf-8 -*-
"""
post_aws_cicd_canvas_to_linkedin.py
Publishes the AI Factory CI/CD (Worker AI -> GitHub -> AWS Production Cloud) post to LinkedIn.
"""

import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'

POST_TEXT = """From Worker AI to GitHub to AWS Production Cloud: The Autonomous AI Factory CI/CD Pipeline! ⚡☁️

How do you safely ship autonomous AI from agent cognitive minds through DevSecOps into enterprise AWS production?

We just open-sourced a full 3-tier browser-native CI/CD studio modeling the entire lifecycle with human-in-the-loop governance:

🏛️ 3 Canonical Tiers:
• 🧠 Level 1 (Worker AI Dev Mind): Society of Mind dialectical personas (Architect, Coder, Tester, Security Guard, Git of Minds) synthesizing code & unit test suites.
• 🐙 Level 2 (GitHub Actions CI/CD - S&OP Equivalent): PR ingestion, AI code reviews, 48/48 automated in-browser unit tests, CodeQL/Trivy security scans, container builds, and the Production Human Gate.
• ☁️ Level 3 (AWS Production Cloud - Company Equivalent): Unified production compute (Route 53, ALB, Amazon ECS Fargate, Aurora PostgreSQL, S3) and the full AWS AI Foundation stack (Amazon Bedrock Claude 3.5 Sonnet, AWS Step Functions multi-agent state machines, AWS Lambda tool runners, OpenSearch Serverless Vector RAG).

🛡️ 20-Page Human Intervention UI (HUI):
1. 🎛️ Run Modes: Switch seamlessly between Auto, Supervised (stops at Human Gate), and Step-by-step execution.
2. 🗂️ Approvals Inbox with Decision Cards: Plain-English why, 4-cell impact grid ($/latency/SLA/risk), Groq LPU rationale, and one-click Deploy or Reject with chips.
3. ☁️ In-Browser AWS AI Simulator: Real-time ECS Fargate tasks, Blue/Green Canary traffic slider, Bedrock temperature dial, and Step Functions visual execution tracker.
4. ⏪ Reversible Undo Ledger: Time-windowed (30s) rollback with one-click AWS target group & state reversion.

👉 Explore the live interactive app directly in your browser:
https://cosmosanalytics.github.io/AWS/
(Backup mirror: https://cosmosanalytics.github.io/uat-copilot-local/cicd_ai_factory_canvas_human_intervention.html)

📂 Open-source GitHub Repository:
https://github.com/cosmosanalytics/AWS

#AWS #AmazonBedrock #StepFunctions #Serverless #CICD #DevSecOps #AIAgents #EnterpriseAI #HumanInTheLoop #WebGPU #CloudEngineering"""

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

    print("Publishing AI Factory CI/CD post to LinkedIn...")
    res = requests.post(url, headers=headers, json=payload)
    print("Status code:", res.status_code)
    print("Response:", res.text)
    if res.status_code == 201:
        print("SUCCESS! Post published successfully to LinkedIn.")
        data = res.json()
        print("Post URN:", data.get("id"))
    else:
        print("Failed to publish to LinkedIn.")

if __name__ == "__main__":
    publish()
