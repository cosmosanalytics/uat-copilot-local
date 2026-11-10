import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.loaders import load_split
from src.agent.runner import AgentRunner

def main():
    print("=== Generating Agent Outputs for Calibration and Math Splits ===")
    runner = AgentRunner("Qwen/Qwen2.5-1.5B-Instruct")
    
    # 1. HotpotQA Calibration Split (100 items for fitting logistic regressions)
    cal_items = load_split("repo_run3/data/sample/hotpot_cal.jsonl")[:100]
    cal_file = "repo_run3/results/cal_outputs.jsonl"
    if os.path.exists(cal_file):
        os.remove(cal_file)
    print(f"\n--- Generating {len(cal_items)} HotpotQA Calibration Outputs ---")
    runner.run_inference_batched(cal_items, output_file=cal_file, batch_size=8, max_new_tokens=180)
    
    # 2. Big-Math-Digits Test Split (36 items for Out-of-Domain Math evaluation)
    math_items = load_split("repo_run3/data/sample/math_test.jsonl")[:36]
    math_file = "repo_run3/results/math_outputs.jsonl"
    if os.path.exists(math_file):
        os.remove(math_file)
    print(f"\n--- Generating {len(math_items)} Big-Math Test Outputs ---")
    runner.run_inference_batched(math_items, output_file=math_file, batch_size=8, max_new_tokens=180)
    
    # 3. Big-Math Calibration Split (20 items for per-task math calibration)
    math_cal_items = load_split("repo_run3/data/sample/math_cal.jsonl")[:20]
    math_cal_file = "repo_run3/results/math_cal_outputs.jsonl"
    if os.path.exists(math_cal_file):
        os.remove(math_cal_file)
    print(f"\n--- Generating {len(math_cal_items)} Big-Math Calibration Outputs ---")
    runner.run_inference_batched(math_cal_items, output_file=math_cal_file, batch_size=8, max_new_tokens=180)
    
    runner.unload()
    print("\nAll required agent outputs generated and cached successfully!")

if __name__ == "__main__":
    main()


