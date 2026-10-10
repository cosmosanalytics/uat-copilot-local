# -*- coding: utf-8 -*-
"""
post_aws_basics_to_linkedin.py
Publishes a brief summary of the AWS Basics Operations Studio with GitHub links to LinkedIn.
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

POST_CONTENT = """How do you ground autonomous AI agents in physical cloud infrastructure?

By establishing deterministic Level 0 AWS operation skills where the model proposes, but the kernel decides.

I built the AWS Basics Operations Studio — a browser-native interactive testbed (100% standalone HTML, Light Mode, powered by WebGPU and Groq LPU) demonstrating all 7 foundational AWS agent operations:

1. Bedrock: Foundation model inference & structured schema proposals.
2. AgentCore: Ring 0 Cedar guardrails enforcing strict syscall boundaries.
3. S3 Receipt Vault: Immutable WORM storage with SHA-256 grounding receipts.
4. DynamoDB Mutex: Distributed CAS leasing preventing multi-agent race conditions.
5. Lambda: Ephemeral tool execution in memory-capped sandboxes.
6. Step Functions: Deterministic HFSM state machines with automated rollback.
7. EventBridge & API Gateway: Inter-cluster communication and telemetry ingress.

👉 Try the live app in your browser:
https://cosmosanalytics.github.io/uat-copilot-local/aws_basics_studio_app.html

#AIEngineering #AWS #AIAgents #WebGPU #SystemsArchitecture #CloudComputing #OpenSource"""

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

print("Publishing AWS Basics Studio summary to LinkedIn...")
res = requests.post(url, headers=headers, json=payload)
print("Status code:", res.status_code)
print("Response body:", res.text)

if res.status_code == 201:
    post_id = res.json().get('id')
    print(f"\nSUCCESS! Post successfully published to LinkedIn. Post URN: {post_id}")
else:
    print("\nFAILED to publish to LinkedIn.")
    sys.exit(1)
