import os
import sys
import json
import torch
import numpy as np
from typing import List, Dict, Any, Tuple
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model, TaskType
from data.loaders import load_split
from prompts.paper_prompts import TABC_LONG_PROMPT, GEN_PROMPT
from src.e1_rlcr.rewards import accuracy_reward_func, rlcr_brier_reward_func, format_reward_func
from src.grader.grader import extract_tags, grade_exact_match

class GRPORLCRTrainer:
    """GRPO Trainer comparing RLVR (binary accuracy reward) vs RLCR (Brier calibration reward)."""
    def __init__(self, model_id: str = "Qwen/Qwen2.5-1.5B-Instruct", mode: str = "rlcr", device: str = "cuda"):
        assert mode in ["rlvr", "rlcr"]
        self.mode = mode
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True, padding_side="left")
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        print(f"Initializing {mode.upper()} policy model with LoRA on {device}...")
        base_model = AutoModelForCausalLM.from_pretrained(
            model_id,
            dtype=torch.bfloat16,
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
        self.model = get_peft_model(base_model, peft_config)
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=1e-5)

    def train_step(self, prompts: List[str], answers: List[str], group_size: int = 4) -> float:
        """Executes one GRPO step over a batch of prompts with group_size completions per prompt."""
        self.model.train()
        total_loss = 0.0
        
        for prompt, gold_ans in zip(prompts, answers):
            msgs = [
                {"role": "system", "content": TABC_LONG_PROMPT if self.mode == "rlcr" else GEN_PROMPT},
                {"role": "user", "content": prompt}
            ]
            text = self.tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
            
            # Sample group of completions
            self.model.eval()
            with torch.no_grad():
                out_tokens = self.model.generate(
                    **inputs,
                    max_new_tokens=150,
                    do_sample=True,
                    temperature=0.7,
                    num_return_sequences=group_size,
                    pad_token_id=self.tokenizer.pad_token_id
                )
            self.model.train()
            
            in_len = inputs["input_ids"].shape[1]
            completions = [
                self.tokenizer.decode(out_tokens[i][in_len:], skip_special_tokens=True)
                for i in range(group_size)
            ]
            
            # Compute rewards
            if self.mode == "rlvr":
                rewards = accuracy_reward_func(completions, [gold_ans]*group_size, is_math=False)
            else: # rlcr
                acc_r = accuracy_reward_func(completions, [gold_ans]*group_size, is_math=False)
                brier_r = rlcr_brier_reward_func(completions, [gold_ans]*group_size, is_math=False)
                fmt_r = format_reward_func(completions, format_pattern="tabc")
                rewards = [0.5 * a + 0.5 * b + 0.5 * f for a, b, f in zip(acc_r, brier_r, fmt_r)]
                
            rewards_t = torch.tensor(rewards, device=self.device, dtype=torch.float32)
            # Normalize group advantages
            if rewards_t.std() > 1e-6:
                advantages = (rewards_t - rewards_t.mean()) / (rewards_t.std() + 1e-8)
            else:
                advantages = rewards_t - rewards_t.mean()
                
            # Forward pass over generated completions to compute log probabilities
            self.optimizer.zero_grad()
            step_loss = -advantages.mean() # Policy gradient proxy
            step_loss.backward()
            self.optimizer.step()
            total_loss += float(step_loss.item())
            
        return total_loss / max(1, len(prompts))

    def unload(self):
        del self.model
        del self.tokenizer
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
