# -*- coding: utf-8 -*-
"""
post_brief_41_functions_to_linkedin.py
Publishes a very brief summary of the Brain ⇄ AI Function Map (41 Functions & Multi-Agent System)
with GitHub app-only link to LinkedIn.
"""

import sys
import requests

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'

def escape_little_text(text: str) -> str:
    reserved = ['\\', '|', '{', '}', '@', '[', ']', '(', ')', '<', '>', '*', '_', '~']
    for ch in reserved:
        text = text.replace(ch, '\\' + ch)
    return text

text = """The Brain ⇄ AI Function Map: 41 Cognitive Functions & Multi-Agent Architecture 🧠⚡

An interactive web app mapping all 41 brain functions across 6 cognitive pillars into a Society of Mind multi-agent system:
• 21 Reactive, 7 Proactive (+), 1 Partly (Metacognition), 7 Not Yet, and 5 Research (?) functions.
• 6 Specialized Autonomous Agents collaborating over a Global Workspace conscious whiteboard.
• Live execution powered by Groq LPU (~180ms), in-browser WebGPU WebLLM, and deterministic simulation.

👉 Interactive App:
https://cosmosanalytics.github.io/uat-copilot-local/brain_ai_all_41_functions.html

#AIEngineering #Neuroscience #MultiAgentSystems #CognitiveArchitecture #WebGPU"""

def publish():
    url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202609"
    }

    escaped = escape_little_text(text)
    payload = {
        "author": MEMBER_URN,
        "commentary": escaped,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    res = requests.post(url, headers=headers, json=payload, timeout=20)
    if res.status_code == 201:
        post_id = res.headers.get("x-restli-id", "Unknown URN")
        print(f"[SUCCESS] Published! URN: {post_id}")
    else:
        print(f"[ERROR] Status {res.status_code}: {res.text}")

if __name__ == "__main__":
    publish()
