# -*- coding: utf-8 -*-
"""
post_aws_basics_to_linkedin.py
Publishes a simple, intuitive, and fun summary of the AWS Basics app to LinkedIn (single live app link only).
"""
import sys
import requests
import json

# Force stdout to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'

url = "https://api.linkedin.com/v2/ugcPosts"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
}

POST_CONTENT = """What happens when you hand an autonomous AI agent real cloud keys? 🔑🤖

Without rules: accidental chaos.
With an operating system kernel: pure clockwork!

I built an interactive browser app showing how an agent team safely runs on AWS (zero install, runs right in your browser with WebGPU & Groq LPU in crisp light mode):

🧠 Bedrock is the Dreamer — plans the ideas.
🚪 AgentCore is the Bouncer — checks IDs and blocks unauthorized moves.
🚦 DynamoDB is the Traffic Cop — stops two agents from crashing into the same job.
🔏 S3 is the Notary Public — stamps tamper-proof receipts on every fact.
🧼 Lambda is the Cleanroom — runs quick math in complete isolation.
📋 Step Functions is the Choreographer — keeps every step in exact order.
📻 EventBridge is the Walkie-Talkie — announces updates to the team.

Try the live interactive playground right in your browser:
https://cosmosanalytics.github.io/uat-copilot-local/aws_basics_studio_app.html

#AIAgents #AWS #AIArchitecture #CloudComputing #SystemsDesign #WebGPU"""

payload = {
    "author": MEMBER_URN,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {"text": POST_CONTENT},
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
}

print("Publishing fun & intuitive AWS Basics Studio summary to LinkedIn...")
res = requests.post(url, headers=headers, json=payload)
print("Status code:", res.status_code)
print("Response body:", res.text)

if res.status_code == 201:
    post_id = res.json().get('id')
    print(f"\nSUCCESS! Fun & intuitive post successfully published to LinkedIn. Post URN: {post_id}")
else:
    print("\nFAILED to publish to LinkedIn.")
    sys.exit(1)
