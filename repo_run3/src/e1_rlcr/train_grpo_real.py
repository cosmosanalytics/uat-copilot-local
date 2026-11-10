import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import json
import time
import torch
import torch.nn.functional as F
import numpy as np
from typing import List, Dict, Any
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model, TaskType, PeftModel
from prompts.paper_prompts import TABC_LONG_PROMPT
from src.e1_rlcr.rewards import accuracy_reward_func, rlcr_brier_reward_func, format_reward_func
from src.grader.grader import extract_tags, grade_exact_match
from src.eval.metrics import evaluate_all_metrics

def format_prompt(context_str: str, question: str) -> str:
    return f"Context:\n{context_str}\n\nQuestion: {question}"

def run_grpo_training(
    mode: str = "rlcr", # "rlvr" or "rlcr"
    num_steps: int = 25,
    group_size: int = 4,
    learning_rate: float = 1e-5,
    save_dir: str = "repo_run3/results/checkpoints/rlcr_lora"
):
    print(f"\n{'='*70}")
    print(f"  STARTING REAL GRPO TRAINING: {mode.upper()} ({num_steps} Steps, G={group_size})")
    print(f"{'='*70}")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    base_model_id = "Qwen/Qwen2.5-1.5B-Instruct"
    
    tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True, padding_side="left")
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    print(f"Loading {base_model_id} base model...")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.bfloat16,
        device_map=device,
        trust_remote_code=True
    )
    
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "v_proj"]
    )
    model = get_peft_model(base_model, peft_config)
    model.gradient_checkpointing_enable()
    model.print_trainable_parameters()
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    
    # Load training dataset
    train_path = "repo_run3/data/sample/hotpot_train.jsonl"
    with open(train_path, "r", encoding="utf-8") as f:
        train_data = [json.loads(line) for line in f]
        
    print(f"Loaded {len(train_data)} training items. Beginning GRPO iterations...")
    
    t0 = time.time()
    for step in range(1, num_steps + 1):
        # Pick item
        item = train_data[(step - 1) % len(train_data)]
        user_prompt = item.get("prompt", "")
        gold_ans = item.get("answer", "")
        
        messages = [
            {"role": "system", "content": TABC_LONG_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        input_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True).to(device)
        prompt_len = inputs["input_ids"].shape[1]
        
        # 1. Rollout completions with sampling
        model.eval()
        with torch.no_grad():
            gen_out = model.generate(
                **inputs,
                max_new_tokens=150,
                do_sample=True,
                temperature=0.8,
                top_p=0.9,
                num_return_sequences=group_size,
                pad_token_id=tokenizer.pad_token_id
            )
        model.train()
        
        completions = [
            tokenizer.decode(gen_out[i][prompt_len:], skip_special_tokens=True)
            for i in range(group_size)
        ]
        
        # 2. Compute rewards
        fmt_rewards = format_reward_func(completions, format_pattern="tabc")
        acc_rewards = accuracy_reward_func(completions, [gold_ans] * group_size, is_math=False)
        
        if mode == "rlvr":
            # RLVR: Pure binary accuracy reward + format reward
            raw_rewards = [0.5 * f + 1.0 * a for f, a in zip(fmt_rewards, acc_rewards)]
        else:
            # RLCR: Brier calibration reward + format reward
            brier_rewards = rlcr_brier_reward_func(completions, [gold_ans] * group_size, is_math=False)
            raw_rewards = [0.5 * f + 1.0 * b for f, b in zip(fmt_rewards, brier_rewards)]
            
        rewards_t = torch.tensor(raw_rewards, device=device, dtype=torch.float32)
        mean_r = rewards_t.mean()
        std_r = rewards_t.std()
        
        # Advantage normalization
        if std_r > 1e-5:
            advantages = (rewards_t - mean_r) / (std_r + 1e-8)
        else:
            advantages = rewards_t - mean_r
        # Clamp advantages for policy stability
        advantages = torch.clamp(advantages, -2.0, 2.0)
        
        # 3. Policy gradient step with micro-batching per completion
        optimizer.zero_grad()
        step_loss = 0.0
        
        for i in range(group_size):
            seq_in = gen_out[i:i+1] # [1, L]
            lbl = seq_in.clone()
            lbl[:, :prompt_len] = -100
            
            outputs = model(input_ids=seq_in)
            logits_i = outputs.logits[:, :-1, :].contiguous()
            shift_lbl_i = lbl[:, 1:].contiguous()
            
            mask_i = (shift_lbl_i != -100).float()
            loss_toks = F.cross_entropy(logits_i.view(-1, logits_i.size(-1)), shift_lbl_i.view(-1), reduction="none").view(1, -1)
            seq_loss = (loss_toks * mask_i).sum() / (mask_i.sum() + 1e-8)
            
            loss_i = (advantages[i].detach() * seq_loss) / group_size
            loss_i.backward()
            step_loss += loss_i.item()
            
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        torch.cuda.empty_cache()
        
        if step % 5 == 0 or step == 1:
            print(f"Step {step:2d}/{num_steps:2d} | Mean Reward: {mean_r.item():.3f} | Loss: {step_loss:.4f} | Acc: {sum(acc_rewards)/group_size:.2f}")
            
    elapsed = time.time() - t0
    print(f"\nTraining completed in {elapsed:.1f}s. Saving checkpoint to {save_dir}...")
    os.makedirs(save_dir, exist_ok=True)
    model.save_pretrained(save_dir)
    tokenizer.save_pretrained(save_dir)
    print(f"Successfully saved {mode.upper()} adapter weights.")
    
    # Clean up GPU
    del model
    del base_model
    del tokenizer
    torch.cuda.empty_cache()

def evaluate_checkpoint(
    ckpt_dir: str,
    out_file: str,
    max_eval_items: int = 152
):
    print(f"\nEvaluating checkpoint from {ckpt_dir} on test set...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    base_model_id = "Qwen/Qwen2.5-1.5B-Instruct"
    
    tokenizer = AutoTokenizer.from_pretrained(ckpt_dir, trust_remote_code=True, padding_side="left")
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.bfloat16,
        device_map=device,
        trust_remote_code=True
    )
    model = PeftModel.from_pretrained(base_model, ckpt_dir)
    model.eval()
    
    test_path = "repo_run3/data/sample/hotpot_test.jsonl"
    with open(test_path, "r", encoding="utf-8") as f:
        test_items = [json.loads(line) for line in f][:max_eval_items]
        
    results = []
    print(f"Running inference on {len(test_items)} test cases...")
    
    for i, item in enumerate(test_items):
        user_prompt = item.get("prompt", "")
        gold_ans = item.get("answer", "")
        messages = [
            {"role": "system", "content": TABC_LONG_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        input_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True).to(device)
        prompt_len = inputs["input_ids"].shape[1]
        
        with torch.no_grad():
            gen_out = model.generate(
                **inputs,
                max_new_tokens=150,
                do_sample=False, # greedy for deterministic eval
                pad_token_id=tokenizer.pad_token_id
            )
        completion = tokenizer.decode(gen_out[0][prompt_len:], skip_special_tokens=True)
        
        parsed = extract_tags(completion)
        pred_ans = parsed.get("answer", "")
        conf = parsed.get("confidence")
        if conf is None or np.isnan(conf):
            conf = 0.5
            
        correct = grade_exact_match(pred_ans, gold_ans)
        
        results.append({
            "id": item["id"],
            "prompt": user_prompt,
            "gold_answer": gold_ans,
            "pred_answer": pred_ans,
            "pred_confidence": float(conf),
            "correct": bool(correct),
            "n_removed": item.get("n_removed", 0),
            "known": item.get("known", 1),
            "raw_completion": completion
        })
        if (i + 1) % 50 == 0 or (i + 1) == len(test_items):
            print(f"Evaluated {i+1}/{len(test_items)} items...")
            
    with open(out_file, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
            
    # Compute metrics
    y_true = np.array([r["correct"] for r in results])
    q_pred = np.array([r["pred_confidence"] for r in results])
    kn_true = np.array([r["known"] for r in results])
    nr_true = np.array([r["n_removed"] for r in results])
    
    metrics = evaluate_all_metrics(y_true, q_pred, n_removed=nr_true, known=kn_true)
    print(f"\n--- Checkpoint Evaluation Results ({ckpt_dir}) ---")
    print(f"Accuracy: {metrics['accuracy']*100:.1f}%")
    print(f"Brier Score: {metrics['brier_score']:.4f}")
    print(f"ECE (10 bins): {metrics['ece']*100:.1f}%")
    print(f"AUROC (correctness): {metrics['auroc']:.3f}")
    print(f"AUROC (known): {metrics.get('auroc_known', 0.5):.3f}")
    print("Mean Confidence by n_removed:", metrics.get("conf_by_n_removed"))
    
    del model
    del base_model
    del tokenizer
    torch.cuda.empty_cache()
    return metrics

if __name__ == "__main__":
    # 1. Train RLVR
    run_grpo_training(
        mode="rlvr",
        num_steps=15,
        group_size=4,
        learning_rate=1e-5,
        save_dir="repo_run3/results/checkpoints/rlvr_lora"
    )
    
    # 2. Train RLCR
    run_grpo_training(
        mode="rlcr",
        num_steps=15,
        group_size=4,
        learning_rate=1e-5,
        save_dir="repo_run3/results/checkpoints/rlcr_lora"
    )
    print("\nGRPO RL training completed successfully for both RLVR and RLCR!")


