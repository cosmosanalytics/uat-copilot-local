# -*- coding: utf-8 -*-
"""
post_ai_mpc_onepager_to_linkedin.py
Deletes previous document post (which LinkedIn mobile clips without '...see more')
and publishes as an Image Post with the high-res 1-page preview and direct PDF link,
guaranteeing the full text with '...see more' expansion on LinkedIn mobile and desktop.
"""

import os
import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'
PREVIOUS_POST_URN = 'urn:li:ugcPost:7530836688898646016'

IMAGE_PATH = r'c:\Users\richa\ai-engineering\ai_model_predictive_control_one_pager_preview.png'
PDF_URL = 'https://cosmosanalytics.github.io/workflow-builder-agent/ai_model_predictive_control_one_pager.pdf'
APP_URL = 'https://cosmosanalytics.github.io/workflow-builder-agent/'

POST_TEXT = """Most AI agents fail because they operate "open-loop" — generating 50-step plans and compounding errors when an LLM hallucinates.

To solve this, we adapted aerospace feedback control into AI Model Predictive Control (AI-MPC): a 6-layer closed-loop architecture with deterministic safety invariants:

1️⃣ State Ingestion (L1): Ingests sensor and environment telemetry into a strongly typed state schema x_t.
2️⃣ World Model (L2): Simulates candidate trajectory outcomes N steps forward before committing actions.
3️⃣ Policy Engine (L3): Generates candidate action trajectories over prediction horizon N.
4️⃣ Invariant Oracle (L4): A deterministic, non-LLM ground-truth circuit breaker enforcing hard mathematical and business invariants (PASS/FAIL).
5️⃣ Actuator (L5): Commits ONLY the immediate first action u_t of the verified policy.
6️⃣ Telemetry Feedback (L6): Re-measures true state delta at runtime and shifts the receding horizon.

📐 Receding Horizon: Search N steps ahead, commit 1 step, re-sample reality. Zero cumulative drift. Mathematical safety guarantees.

📄 1-Page Architecture PDF:
https://cosmosanalytics.github.io/workflow-builder-agent/ai_model_predictive_control_one_pager.pdf

🔗 Live Web Apps (Zero-Server In-Browser Execution):
https://cosmosanalytics.github.io/workflow-builder-agent/

#AIEngineering #ModelPredictiveControl #AIAgents #ControlTheory #SystemDesign #OpenSource"""

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'X-Restli-Protocol-Version': '2.0.0'
}

# 1. Delete previous post
print(f"1. Deleting previous post {PREVIOUS_POST_URN}...")
del_url = f"https://api.linkedin.com/rest/posts/{requests.utils.quote(PREVIOUS_POST_URN)}"
del_headers = dict(headers)
del_headers['LinkedIn-Version'] = '202609'
del_res = requests.delete(del_url, headers=del_headers, timeout=15)
print("Delete status (rest/posts):", del_res.status_code)
if del_res.status_code != 204:
    alt_del = f"https://api.linkedin.com/v2/ugcPosts/{requests.utils.quote(PREVIOUS_POST_URN)}"
    del_res2 = requests.delete(alt_del, headers=headers, timeout=15)
    print("Delete status (v2/ugcPosts):", del_res2.status_code)

# 2. Register Image Upload
print("\n2. Registering Image Upload...")
reg_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
reg_payload = {
    "registerUploadRequest": {
        "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
        "owner": MEMBER_URN,
        "serviceRelationships": [
            {
                "relationshipType": "OWNER",
                "identifier": "urn:li:userGeneratedContent"
            }
        ]
    }
}

r = requests.post(reg_url, headers=headers, json=reg_payload, timeout=20)
print("Register status:", r.status_code)
if r.status_code != 200:
    print("Error registering upload:", r.text)
    sys.exit(1)

data = r.json()["value"]
upload_url = data["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
asset_urn = data["asset"]
print("Asset URN:", asset_urn)

# 3. Upload image binary data
print("3. Uploading image binary data...")
with open(IMAGE_PATH, "rb") as f:
    img_bytes = f.read()

up_headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "image/png"
}
up_res = requests.put(upload_url, headers=up_headers, data=img_bytes, timeout=30)
print("Upload image status:", up_res.status_code)
if up_res.status_code not in (200, 201):
    print("Error uploading image:", up_res.text)
    sys.exit(1)

# 4. Publish via ugcPosts as IMAGE post
print("\n4. Publishing Image Post with full text commentary to LinkedIn...")
url = "https://api.linkedin.com/v2/ugcPosts"
share_content = {
    "shareCommentary": {"text": POST_TEXT},
    "shareMediaCategory": "IMAGE",
    "media": [
        {
            "status": "READY",
            "description": {
                "text": "AI Model Predictive Control (AI-MPC) — 6-Layer Architecture Specification (1-Page High-Res Guide)"
            },
            "media": asset_urn,
            "title": {
                "text": "AI Model Predictive Control (AI-MPC) Architecture"
            }
        }
    ]
}

payload = {
    "author": MEMBER_URN,
    "lifecycleState": "PUBLISHED",
    "specificContent": {"com.linkedin.ugc.ShareContent": share_content},
    "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
}

post_res = requests.post(url, headers=headers, json=payload, timeout=20)
print("Post status:", post_res.status_code)

if post_res.status_code == 201:
    post_id = post_res.json().get('id')
    print(f"\n[SUCCESS] Published to LinkedIn with full expandable text! Post ID: {post_id}")
else:
    print("Failed to publish post:", post_res.status_code, post_res.text)
    sys.exit(1)
