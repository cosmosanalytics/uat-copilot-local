# -*- coding: utf-8 -*-
"""
post_ai_mpc_onepager_to_linkedin.py
Deletes previous post and publishes the AI Model Predictive Control (AI-MPC) summary
and 1-page PDF document with a tightened lead-in for clean mobile feed display.
"""

import os
import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'
PREVIOUS_POST_URN = 'urn:li:ugcPost:7530833944238411776'

PDF_PATH = r'c:\Users\richa\ai-engineering\ai_model_predictive_control_one_pager.pdf'
TITLE = "AI Model Predictive Control (AI-MPC) — 6-Layer Architecture Specification"

# Tightened opening without early blank line breaks to prevent feed clipping
POST_TEXT = """Most AI agents fail because they operate "open-loop" — generating 50-step plans and compounding errors when an LLM hallucinates. To solve this, we adapted aerospace feedback control into AI Model Predictive Control (AI-MPC): a 6-layer closed-loop architecture with deterministic safety invariants.

1️⃣ State Ingestion (L1): Ingests sensor and environment telemetry into a strongly typed state schema x_t.
2️⃣ World Model (L2): Simulates candidate trajectory outcomes N steps forward before committing actions.
3️⃣ Policy Engine (L3): Generates candidate action trajectories over prediction horizon N.
4️⃣ Invariant Oracle (L4): A deterministic, non-LLM ground-truth circuit breaker enforcing hard mathematical and business invariants (PASS/FAIL).
5️⃣ Actuator (L5): Commits ONLY the immediate first action u_t of the verified policy.
6️⃣ Telemetry Feedback (L6): Re-measures true state delta at runtime and shifts the receding horizon.

📐 Receding Horizon: Search N steps ahead, commit 1 step, re-sample reality. Zero cumulative drift. Mathematical safety guarantees.

Attached is our 1-page formal architecture specification.

🔗 Live Apps & Architecture:
https://cosmosanalytics.github.io/workflow-builder-agent/

#AIEngineering #ModelPredictiveControl #AIAgents #ControlTheory #SystemDesign #OpenSource"""

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'X-Restli-Protocol-Version': '2.0.0',
    'LinkedIn-Version': '202609'
}

# 1. Delete previous post
print(f"1. Deleting previous post {PREVIOUS_POST_URN}...")
del_url = f"https://api.linkedin.com/rest/posts/{requests.utils.quote(PREVIOUS_POST_URN)}"
del_res = requests.delete(del_url, headers=headers, timeout=15)
print("Delete status (rest/posts):", del_res.status_code)
if del_res.status_code != 204:
    alt_del = f"https://api.linkedin.com/v2/ugcPosts/{requests.utils.quote(PREVIOUS_POST_URN)}"
    del_res2 = requests.delete(alt_del, headers={'Authorization': f'Bearer {TOKEN}', 'X-Restli-Protocol-Version': '2.0.0'}, timeout=15)
    print("Delete status (v2/ugcPosts):", del_res2.status_code)

# 2. Initialize and upload document
print(f"\n2. Initializing Document Upload for '{TITLE}'...")
init_url = "https://api.linkedin.com/rest/documents?action=initializeUpload"
init_payload = {
    "initializeUploadRequest": {
        "owner": MEMBER_URN
    }
}

res = requests.post(init_url, headers=headers, json=init_payload, timeout=20)
print("Initialize status:", res.status_code)
if res.status_code != 200:
    print("Error initializing:", res.text)
    sys.exit(1)

data = res.json()
upload_url = data['value']['uploadUrl']
doc_urn = data['value']['document']
print("Document URN:", doc_urn)

print("3. Uploading PDF binary data...")
with open(PDF_PATH, 'rb') as f:
    pdf_bytes = f.read()

up_headers = {'Authorization': f'Bearer {TOKEN}'}
up_res = requests.put(upload_url, data=pdf_bytes, headers=up_headers, timeout=30)
print("Upload status:", up_res.status_code)
if up_res.status_code not in (200, 201):
    print("Upload error:", up_res.text)
    sys.exit(1)

# 3. Publish updated post
print("4. Publishing updated post with clean continuous lead-in...")
post_url = "https://api.linkedin.com/rest/posts"
post_payload = {
    "author": MEMBER_URN,
    "commentary": POST_TEXT,
    "visibility": "PUBLIC",
    "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
    },
    "content": {
        "media": {
            "title": TITLE,
            "id": doc_urn
        }
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": False
}

post_res = requests.post(post_url, headers=headers, json=post_payload, timeout=20)
print("Post status:", post_res.status_code)

if post_res.status_code == 201:
    post_urn = post_res.headers.get('x-restli-id')
    print("SUCCESS_POST_URN:", post_urn)
    print("\nSuccessfully updated post on LinkedIn with clean mobile lead-in!")
else:
    print("Failed to publish post:", post_res.status_code, post_res.text)
    sys.exit(1)
