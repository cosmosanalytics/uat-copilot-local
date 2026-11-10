import sys
import os
import json
import torch
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from data.loaders import load_split
from src.agent.runner import AgentRunner
from src.eval.metrics import evaluate_all_metrics

def main():
    test_file = "repo_run3/data/sample/hotpot_test.jsonl"
    items = load_split(test_file)[:5]
    print(f"Loaded {len(items)} items for quick speed/memory test.")
    
    runner = AgentRunner("Qwen/Qwen2.5-1.5B-Instruct")
    test_out = "repo_run3/results/e0_speed_test.jsonl"
    if os.path.exists(test_out):
        os.remove(test_out)
        
    res = runner.run_inference(items, output_file=test_out, max_new_tokens=300)
    runner.unload()
    
    print("\nSpeed & Memory Test Results:")
    for r in res:
        print(f"ID: {r['id']} | Correct: {r['correct']} | Conf: {r['confidence']} | Latency: {r['latency_sec']:.2f}s | Pred: {r['pred_answer']} | Gold: {r['gold_answer']}")

if __name__ == "__main__":
    main()


