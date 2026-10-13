# -*- coding: utf-8 -*-
"""
post_multi_agent_society_of_mind_to_linkedin.py
Publishes the Multi-Agent Society of Mind (41 Brain Functions) to LinkedIn.
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

text = """The Brain as a Multi-Agent System: Society of Mind Architecture for 41 Cognitive Functions 🧠🤖

Marvin Minsky once famously proposed: "The mind is not a single entity, but a society of specialized agents."

I upgraded the Brain ⇄ AI Function Map into an interactive Multi-Agent Society of Mind Studio, dividing all 41 brain functions across 6 specialized autonomous pillar agents:

1. 👁️ Perceptor Agent (Thalamic Gater): Controls proactive intake (+Perception), selective attention, inhibition of return, and predictive coding.
2. 💾 Memory Agent (Hippocampal Librarian): Manages working memory, autoassociative episodic retrieval, consolidation, and Ebbinghaus forgetting decay.
3. 🧮 Executive Judge (Prefrontal Arbiter): Enforces planning, metacognitive epistemic calibration, decision-making, and response inhibition circuit breakers.
4. 📚 Affective Agent (Amygdala/VTA): Computes somatic threat markers, emotional urgency scores, and reward prediction errors.
5. ⚡ Motor Governor (Cerebellum & Insula): Executes verified tool actions, lateral inhibition, and homeostatic interoception.
6. 📡 Workspace Hub (Conscious Blackboard): Implements Bernard Baars' Global Workspace Theory—broadcasting state updates across all agents simultaneously in O(N) time.

Key Features:
• Interactive Multi-Agent Scenarios: Watch the 6 agents collaborate in real-time across zero-day security breaches, database deadlock failovers, and lateral insight paradoxes.
• Dual Execution Substrate: Powered by Groq LPU (~180ms), local client-side WebGPU WebLLM, and deterministic simulation in a single zero-dependency HTML file.
• Live Cognitive Pulsing: Corresponding brain functions highlight on the 41-function map as each agent speaks.

👉 Interactive Multi-Agent Web App:
https://cosmosanalytics.github.io/uat-copilot-local/brain_ai_all_41_functions.html

#MultiAgentSystems #CognitiveArchitecture #Neuroscience #SocietyOfMind #GlobalWorkspaceTheory #WebGPU #AIEngineering"""

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
