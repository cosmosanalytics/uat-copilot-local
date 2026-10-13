"""
build_brain_to_ai_apps.py
Master builder for all 4 Brain-to-AI translation apps:
1. brain_to_ai_homeostasis.html  (Hypothalamic Homeostasis -> Autonomic Agent Regulation)
2. brain_to_ai_somatic_marker.html (Somatic Marker Hypothesis -> Dynamic Goal Weighting & Prioritization)
3. brain_to_ai_theory_of_mind.html (Theory of Mind -> Multi-Agent Negotiation & Intent Reading)
4. brain_to_ai_consolidation.html (Hippocampal Consolidation -> Episodic Plasticity & Long-Term Heuristic Recall)

All apps feature:
- Deterministic simulation mode
- Groq LPU (~200ms) with pre-provisioned key & model selection (openai/gpt-oss-20b, qwen/qwen3.8-27b)
- In-browser WebGPU WebLLM (Qwen2.5-1.5B, Llama-3.2-1B) with client-side model downloader
"""

import subprocess
import sys

def main():
    print("Building all 4 Brain-to-AI apps with full WebLLM + Groq LPU + Deterministic engines...")
    subprocess.check_call([sys.executable, "write_somatic_marker_app.py"])
    subprocess.check_call([sys.executable, "build_all_4_brain_apps.py"])
    print("All 4 apps successfully generated and verified!")

if __name__ == "__main__":
    main()
