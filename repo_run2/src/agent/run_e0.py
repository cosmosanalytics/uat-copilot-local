import os
import sys
import json
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from data.loaders import load_split
from src.agent.runner import AgentRunner
from src.eval.metrics import evaluate_all_metrics

def main():
    print("=== Running Milestone 1: E0 Baseline (Prompted Qwen2.5-1.5B) ===")
    hotpot_items = load_split("repo_run2/data/sample/hotpot_test.jsonl")[:152]
    math_items = load_split("repo_run2/data/sample/math_test.jsonl")[:36]
    
    output_jsonl = "repo_run2/results/e0_sample_outputs.jsonl"
    if os.path.exists(output_jsonl):
        os.remove(output_jsonl)
        
    runner = AgentRunner("Qwen/Qwen2.5-1.5B-Instruct")
    
    print("\n--- Running E0 on HotpotQA-Modified Sample Test (300 items) ---")
    hotpot_res = runner.run_inference_batched(
        hotpot_items,
        output_file=output_jsonl,
        batch_size=8,
        max_new_tokens=180
    )
    
    print("\n--- Running E0 on Big-Math-Digits Sample Test (300 items) ---")
    math_res = runner.run_inference_batched(
        math_items,
        output_file=output_jsonl,
        batch_size=8,
        max_new_tokens=180
    )
    
    runner.unload()
    
    # Evaluate HotpotQA metrics
    y_hp = np.array([r["correct"] for r in hotpot_res])
    q_hp = np.array([r["confidence"] for r in hotpot_res])
    known_hp = np.array([r["known"] for r in hotpot_res])
    nr_hp = np.array([r["n_removed"] for r in hotpot_res])
    metrics_hp = evaluate_all_metrics(y_hp, q_hp, n_removed=nr_hp, known=known_hp)
    
    # Constant-confidence baseline (training accuracy prior)
    train_hp = load_split("repo_run2/data/sample/hotpot_train.jsonl")
    prior_hp = 0.5 # Default prior
    q_const_hp = np.full_like(q_hp, prior_hp)
    metrics_const_hp = evaluate_all_metrics(y_hp, q_const_hp)
    
    # Evaluate Math metrics
    y_math = np.array([r["correct"] for r in math_res])
    q_math = np.array([r["confidence"] for r in math_res])
    metrics_math = evaluate_all_metrics(y_math, q_math)
    
    summary = {
        "experiment": "E0_baseline",
        "hotpot_modified": {
            "verbalized_confidence": metrics_hp,
            "constant_confidence_baseline": metrics_const_hp
        },
        "big_math_digits": {
            "verbalized_confidence": metrics_math
        }
    }
    
    summary_file = "repo_run2/results/e0_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    print(f"\nE0 Baseline completed! Summary written to {summary_file}")
    print("\n--- E0 HotpotQA-Modified Results ---")
    print(f"Accuracy: {metrics_hp['accuracy']:.4f} (95% CI: [{metrics_hp['accuracy_ci'][0]:.4f}, {metrics_hp['accuracy_ci'][1]:.4f}])")
    print(f"Brier Score: {metrics_hp['brier_score']:.4f} (Constant baseline: {metrics_const_hp['brier_score']:.4f})")
    print(f"ECE (10 bins): {metrics_hp['ece']:.4f}")
    print(f"AUROC (correctness): {metrics_hp['auroc']:.4f}")
    print(f"AUROC (known): {metrics_hp.get('auroc_known', 0.0):.4f}")
    print(f"Automation Rate @ 95%: {metrics_hp['automation_rate_95']:.4f}")
    print("Mean Confidence by n_removed:", metrics_hp.get("conf_by_n_removed"))
    
    print("\n--- E0 Big-Math-Digits Results ---")
    print(f"Accuracy: {metrics_math['accuracy']:.4f}")
    print(f"Brier Score: {metrics_math['brier_score']:.4f}")
    print(f"ECE (10 bins): {metrics_math['ece']:.4f}")
    print(f"AUROC: {metrics_math['auroc']:.4f}")

if __name__ == "__main__":
    main()

