import os
import json
import time
import torch
from typing import List, Dict, Any, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.grader.grader import grade_exact_match, grade_math, extract_tags
from src.eval.metrics import evaluate_all_metrics
from prompts.paper_prompts import TABC_LONG_PROMPT, GEN_PROMPT

class AgentRunner:
    def __init__(self, model_id: str = "Qwen/Qwen2.5-1.5B-Instruct", device: str = "cuda"):
        self.model_id = model_id
        self.device = device
        print(f"Loading {model_id} onto {device}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True, padding_side="left")
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            dtype=torch.bfloat16,
            device_map=device,
            trust_remote_code=True
        )
        self.model.eval()
        vram_gb = torch.cuda.memory_allocated() / (1024**3) if torch.cuda.is_available() else 0
        print(f"Model loaded. VRAM allocated: {vram_gb:.2f} GB")

    def run_inference_batched(
        self,
        items: List[Dict[str, Any]],
        system_prompt: str = TABC_LONG_PROMPT,
        output_file: Optional[str] = None,
        batch_size: int = 8,
        max_new_tokens: int = 180,
        temperature: float = 0.7,
        do_sample: bool = False
    ) -> List[Dict[str, Any]]:
        results = []
        start_time = time.time()
        n_items = len(items)
        
        for b_start in range(0, n_items, batch_size):
            b_end = min(b_start + batch_size, n_items)
            batch = items[b_start:b_end]
            t0 = time.time()
            
            prompts = []
            for item in batch:
                msgs = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": item["prompt"]}
                ]
                formatted = self.tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
                prompts.append(formatted)
                
            inputs = self.tokenizer(
                prompts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=2048
            ).to(self.device)
            
            with torch.no_grad():
                gen_kwargs = {
                    "max_new_tokens": max_new_tokens,
                    "pad_token_id": self.tokenizer.pad_token_id,
                    "eos_token_id": self.tokenizer.eos_token_id,
                }
                if do_sample and temperature > 0:
                    gen_kwargs["do_sample"] = True
                    gen_kwargs["temperature"] = temperature
                else:
                    gen_kwargs["do_sample"] = False
                    
                outputs = self.model.generate(**inputs, **gen_kwargs)
                input_len = inputs["input_ids"].shape[1]
                gen_texts = [
                    self.tokenizer.decode(outputs[i][input_len:], skip_special_tokens=True)
                    for i in range(len(batch))
                ]

            batch_latency = (time.time() - t0) / len(batch)
            
            for item, gen_text in zip(batch, gen_texts):
                tags = extract_tags(gen_text)
                is_math = (item.get("dataset") == "big_math_digits")
                gold_ans = str(item["answer"])
                pred_ans = tags["answer"] or ""
                
                if is_math:
                    correct = int(grade_math(pred_ans, gold_ans))
                else:
                    correct = int(grade_exact_match(pred_ans, gold_ans))
                    
                conf = tags["confidence_float"]
                if conf is None:
                    conf = 0.5
                    
                record = {
                    "id": item["id"],
                    "dataset": item.get("dataset", "unknown"),
                    "pred_answer": pred_ans,
                    "gold_answer": gold_ans,
                    "correct": correct,
                    "confidence": conf,
                    "raw_confidence": tags["raw_confidence"],
                    "known": item.get("known", 1),
                    "n_removed": item.get("n_removed", 0),
                    "think": tags["think"],
                    "analysis": tags["analysis"],
                    "latency_sec": batch_latency,
                    "full_output": gen_text
                }
                results.append(record)
                
                if output_file:
                    os.makedirs(os.path.dirname(output_file), exist_ok=True)
                    with open(output_file, "a", encoding="utf-8") as f:
                        f.write(json.dumps(record) + "\n")
                        
            elapsed = time.time() - start_time
            print(f"[{b_end}/{n_items}] Items processed | Avg: {elapsed/b_end:.2f}s/item | Last batch: {time.time()-t0:.2f}s")

        return results

    def unload(self):
        del self.model
        del self.tokenizer
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        print("Model unloaded and CUDA cache emptied.")
