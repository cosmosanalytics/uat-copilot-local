# -*- coding: utf-8 -*-
"""
publish_7_ai_to_brain_posts.py
Publishes 7 concise posts to LinkedIn, one for each AI -> Neuroscience research web app:
1. Forgetting Curve (ai_to_brain_forgetting_curve.html)
2. Serial Position (ai_to_brain_serial_position.html)
3. Capacity Limit (ai_to_brain_capacity_limit.html)
4. Stroop Test (ai_to_brain_stroop_test.html)
5. Sleep Replay Test (ai_to_brain_sleep_replay_test.html)
6. Broadcast Test (ai_to_brain_broadcast_test.html)
7. Source Memory (ai_to_brain_source_memory.html)
"""

import sys
import time
import requests

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'

def escape_little_text(text: str) -> str:
    reserved = ['\\', '|', '{', '}', '@', '[', ']', '(', ')', '<', '>', '*', '_', '~']
    for ch in reserved:
        text = text.replace(ch, '\\' + ch)
    return text

POSTS = [
    {
        "name": "1. Forgetting Curve",
        "text": """AI to Neuroscience Research: The Forgetting Curve (Human Memory vs LLM Context Decay) 📉

In 1885, Hermann Ebbinghaus proved human memory decays exponentially over time without spaced reinforcement. Does an LLM agent's memory suffer the same fate across context windows?

I built an interactive web app testing Ebbinghaus decay on LLMs:
• Step 1: Takes published human forgetting baselines (58% retention at 20m, 33% at 6 days).
• Step 2: Streams intervening token distractors through attention layers.
• Step 3: Compares attention decay vs biological synaptic decay side-by-side.
• Runs 100% in-browser with WebGPU WebLLM & Groq LPU (~180ms).

👉 Interactive App:
https://cosmosanalytics.github.io/uat-copilot-local/ai_to_brain_forgetting_curve.html

#AIEngineering #Neuroscience #MemoryDecay #Ebbinghaus #LLM #WebGPU #CognitiveScience"""
    },
    {
        "name": "2. Serial Position",
        "text": """AI to Neuroscience Research: Serial Position Effect (Primacy & Recency vs Lost-in-the-Middle) 📊

Humans recall the first (primacy) and last (recency) items in a list best, while items in the middle suffer retro/proactive interference. Do LLMs exhibit the identical U-shaped curve?

I built an interactive web app running serial position probes across needle-in-a-haystack prompts:
• Step 1: Evaluates Murdock's (1962) human U-curve (85% primacy, 92% recency, 38% middle trough).
• Step 2: Dynamically shifts needles across 0% to 100% context depths.
• Step 3: Direct empirical comparison between biological working memory and transformer self-attention dispersion.
• Powered by WebGPU WebLLM & Groq LPU in a single zero-dependency HTML file.

👉 Interactive App:
https://cosmosanalytics.github.io/uat-copilot-local/ai_to_brain_serial_position.html

#AIEngineering #CognitiveScience #LostInTheMiddle #AttentionMechanisms #LLM #WebGPU"""
    },
    {
        "name": "3. Capacity Limit",
        "text": """AI to Neuroscience Research: Working Memory Capacity Limits (Cowan's 4 Chunks vs Multi-Head Attention) 🧩

Human working memory hits a biological brick wall at ~4 independent chunks (Cowan, 2001). Where does an LLM agent break down under simultaneous variable load?

I built an interactive empirical test bench:
• Step 1: Human baseline holds 3.8 items before prefrontal attentional collapse.
• Step 2: Stresses the model with 4, 8, 12, and 16 concurrent state variables.
• Step 3: Identifies where attention weight dispersion causes hallucinated dependencies (~12 items).
• Features in-browser WebGPU WebLLM, Groq LPU cloud inference, and deterministic math mode.

👉 Interactive App:
https://cosmosanalytics.github.io/uat-copilot-local/ai_to_brain_capacity_limit.html

#AIEngineering #Neuroscience #WorkingMemory #CapacityLimits #Transformer #WebGPU"""
    },
    {
        "name": "4. Stroop Test",
        "text": """AI to Neuroscience Research: The Stroop Test (Human Conflict vs LLM Attention Entropy) 🔴

In 1935, J. Ridley Stroop proved humans suffer a +142ms latency delay and error surge when reading conflicting color words ("RED" printed in green ink). Do semantic conflicts trip the model?

I built an interactive Stroop interference test bench for LLMs:
• Step 1: Human automatic ventral reading pathways cannot be inhibited (+142ms delay, +14% errors).
• Step 2: Tests congruent vs incongruent conflict pairs (color ink, HTTP 200 with error body, inverted booleans).
• Step 3: Direct scorecard measuring model token latency penalties and attention entropy spread (+68ms delay).
• Zero-backend, light mode native with WebGPU WebLLM & Groq LPU.

👉 Interactive App:
https://cosmosanalytics.github.io/uat-copilot-local/ai_to_brain_stroop_test.html

#AIEngineering #Neuroscience #StroopEffect #CognitiveConflict #Transformers #WebGPU"""
    },
    {
        "name": "5. Sleep Replay Test",
        "text": """AI to Neuroscience Research: Sleep Replay & Memory Consolidation (Hippocampus vs Agent Architecture) 💤

During slow-wave sleep, hippocampal sharp-wave ripples replay waking experiences at 10x speed, transferring memories to neocortex and boosting retention by +40%. Can sleep replay rescue agent memory?

I built an interactive test comparing naive retrieval vs offline sleep replay consolidation:
• Step 1: Human sleep consolidation findings (Diekelmann & Born, 2010).
• Step 2: Subjects agent memory to distractor interference tasks with vs without offline replay passes.
• Step 3: Replay consolidation eliminates catastrophic forgetting, lifting recall from 46% to 94%.
• Single-file HTML powered by WebGPU WebLLM & Groq LPU.

👉 Interactive App:
https://cosmosanalytics.github.io/uat-copilot-local/ai_to_brain_sleep_replay_test.html

#AIEngineering #Neuroscience #SleepReplay #MemoryConsolidation #CatastrophicForgetting #WebGPU"""
    },
    {
        "name": "6. Broadcast Test",
        "text": """AI to Neuroscience Research: The Broadcast Test (Global Workspace Theory vs Multi-Agent Teams) 📡

Specialized unconscious brain modules coordinate via a conscious Global Workspace broadcast (Baars & Dehaene), avoiding quadratic O(N²) cross-wiring. Does broadcast help agent teams?

I built an interactive multi-agent coordination laboratory:
• Step 1: Biological Global Workspace Theory (GWT) communication topology.
• Step 2: Simulates incident response across 3 to 10 agents under Pairwise Mesh vs Global Broadcast.
• Step 3: Global Workspace broadcast cuts token overhead by 66% and drops coordination deadlock from 28.5% to 0%.
• Runs in-browser with live animated topology canvas, WebGPU WebLLM & Groq LPU.

👉 Interactive App:
https://cosmosanalytics.github.io/uat-copilot-local/ai_to_brain_broadcast_test.html

#AIEngineering #MultiAgentSystems #GlobalWorkspaceTheory #CognitiveArchitecture #WebGPU"""
    },
    {
        "name": "7. Source Memory",
        "text": """AI to Neuroscience Research: Source Memory & Reality Monitoring (Human Errors vs LLM Hallucinations) 🕵️

Humans frequently confuse internally imagined thoughts with externally perceived real events (reality monitoring fails 28% of the time, Johnson et al. 1993). Does the model confuse its own thoughts?

I built an interactive reality monitoring test bench for AI agents:
• Step 1: Human source-memory confusion baseline under cognitive load.
• Step 2: Streams mixed timelines of real sensor/API telemetry vs self-generated chain-of-thought speculations.
• Step 3: Measures false external attribution where models treat internal hallucinations as verified ground truth.
• Single-file HTML with WebGPU WebLLM, Groq LPU, and deterministic reality gate.

👉 Interactive App:
https://cosmosanalytics.github.io/uat-copilot-local/ai_to_brain_source_memory.html

#AIEngineering #Neuroscience #RealityMonitoring #SourceMemory #Hallucinations #WebGPU"""
    }
]

def publish_all():
    url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202609"
    }

    print(f"=== PUBLISHING ALL 7 AI TO NEUROSCIENCE RESEARCH APPS TO LINKEDIN ===\n")
    
    for i, post_info in enumerate(POSTS, start=1):
        print(f"[{i}/7] Publishing '{post_info['name']}'...")
        escaped_commentary = escape_little_text(post_info['text'])
        
        payload = {
            "author": MEMBER_URN,
            "commentary": escaped_commentary,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False
        }

        try:
            res = requests.post(url, headers=headers, json=payload, timeout=20)
            if res.status_code == 201:
                post_id = res.headers.get("x-restli-id", "Unknown URN")
                print(f"  [SUCCESS] Published! URN: {post_id}")
            else:
                print(f"  [ERROR] Status {res.status_code}: {res.text}")
        except Exception as e:
            print(f"  [FAIL] Request failed: {e}")

        if i < len(POSTS):
            time.sleep(2.5)

    print("\n=== FINISHED PUBLISHING ALL 7 POSTS TO LINKEDIN ===")

if __name__ == "__main__":
    publish_all()
