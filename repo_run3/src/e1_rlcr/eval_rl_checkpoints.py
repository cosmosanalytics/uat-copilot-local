import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import json
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from data.loaders import load_split
from prompts.paper_prompts import TABC_LONG_PROMPT
from src.grader.grader import extract_tags, grade_exact_match
from src.eval.metrics import evaluate_all_metrics

def eval_policy(ckpt_dir, out_file, batch_size=8, max_new_tokens=180):
    print(f"\nEvaluating Policy from {ckpt_dir} -> {out_file}...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    base_id = "Qwen/Qwen2.5-1.5B-Instruct"
    
    tokenizer = AutoTokenizer.from_pretrained(ckpt_dir, trust_remote_code=True, padding_side="left")
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    base_model = AutoModelForCausalLM.from_pretrained(
        base_id,
        dtype=torch.bfloat16,
        device_map=device,
        trust_remote_code=True
    )
    model = PeftModel.from_pretrained(base_model, ckpt_dir)
    model.eval()
    
    test_items = load_split("repo_run3/data/sample/hotpot_test.jsonl")[:152]
    results = []
    
    for b_start in range(0, len(test_items), batch_size):
        b_end = min(b_start + batch_size, len(test_items))
        batch = test_items[b_start:b_end]
        
        prompts = []
        for item in batch:
            msgs = [
                {"role": "system", "content": TABC_LONG_PROMPT},
                {"role": "user", "content": item["prompt"]}
            ]
            formatted = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            prompts.append(formatted)
            
        inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=2048).to(device)
        input_len = inputs["input_ids"].shape[1]
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id
            )
            
        for i, item in enumerate(batch):
            gen_text = tokenizer.decode(outputs[i][input_len:], skip_special_tokens=True)
            parsed = extract_tags(gen_text)
            pred_ans = parsed.get("answer", "")
            conf = parsed.get("confidence_float")
            if conf is None or not isinstance(conf, (int, float)):
                conf = 0.5
            correct = grade_exact_match(pred_ans, item["answer"])
            results.append({
                "id": item["id"],
                "prompt": item["prompt"],
                "gold_answer": item["answer"],
                "pred_answer": pred_ans,
                "confidence": float(conf),
                "correct": bool(correct),
                "n_removed": item.get("n_removed", 0),
                "known": item.get("known", 1),
                "raw_completion": gen_text
            })
            
    with open(out_file, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
            
    y_true = np.array([r["correct"] for r in results])
    q_pred = np.array([r["confidence"] for r in results])
    kn_true = np.array([r["known"] for r in results])
    nr_true = np.array([r["n_removed"] for r in results])
    
    metrics = evaluate_all_metrics(y_true, q_pred, n_removed=nr_true, known=kn_true)
    print(f"Metrics for {ckpt_dir}:")
    print(f"Accuracy: {metrics['accuracy']*100:.1f}%")
    print(f"Brier: {metrics['brier_score']:.4f}")
    print(f"ECE: {metrics['ece']*100:.1f}%")
    print(f"AUROC: {metrics['auroc']:.3f}")
    print(f"Mean Confidence by n_removed:", metrics.get("conf_by_n_removed"))
    
    del model
    del base_model
    del tokenizer
    torch.cuda.empty_cache()
    return metrics

if __name__ == "__main__":
    print("Evaluating trained RLVR and RLCR checkpoints with full 2048-length batched inference...")
    rlvr_metrics = eval_policy("repo_run3/results/checkpoints/rlvr_lora", "repo_run3/results/rlvr_test_outputs.jsonl")
    rlcr_metrics = eval_policy("repo_run3/results/checkpoints/rlcr_lora", "repo_run3/results/rlcr_test_outputs.jsonl")
    
    with open("repo_run3/results/e1_real_grpo_summary.json", "w", encoding="utf-8") as f:
        json.dump({"rlvr": rlvr_metrics, "rlcr": rlcr_metrics}, f, indent=2)
    print("\nSaved updated results to repo_run3/results/e1_real_grpo_summary.json")


