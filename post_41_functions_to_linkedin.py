# -*- coding: utf-8 -*-
"""
post_41_functions_to_linkedin.py
Publishes the Brain ⇄ AI Function Map (All 41 Cognitive & Researched Functions) to LinkedIn.
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

text = """The Brain ⇄ AI Function Map: All 41 Cognitive & Researched Functions Studio 🧠⚡

What does human cognition possess that modern AI architectures have, add, lack, or are currently researching?

I built an interactive web application mapping all 41 brain functions across 6 cognitive pillars:
• 21 REACTIVE (Responds after stimulus): Selective attention, working memory, decision-making, planning, motor execution, global workspace, synaptic signaling...
• 7 PROACTIVE (+ Acts before): +Perception, +Prioritizing, +Flexibility, +Learning, +Self-regulation, +Reads intent, +Stays aware
• 1 PARTLY: Metacognition (self-calibration, confidence bounds & knowing what you don't know)
• 7 NOT YET: Multisensory, spatial navigation, time perception, forgetting, reward learning, emotion, interoception
• 5 RESEARCH (? Science studying): ?Predictive coding, ?Reconsolidation, ?Insight (aha), ?Sleep & memory, ?Consciousness

Key Features:
1. Filter by category or search across all 41 functions with deep biological mechanisms, AI equivalents, and capability gaps.
2. Live benchmarking on Groq LPU (~180ms), in-browser WebGPU WebLLM, or deterministic neural simulation.
3. Light mode native with zero backend dependencies.

👉 Interactive App:
https://cosmosanalytics.github.io/uat-copilot-local/brain_ai_all_41_functions.html

#AIEngineering #Neuroscience #CognitiveArchitecture #AutonomousAgents #WebGPU #Groq #ArtificialIntelligence #MachineLearning"""

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
