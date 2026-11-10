import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.grader.grader import grade_exact_match, extract_tags
from data.loaders import load_split
from prompts.paper_prompts import TABC_LONG_PROMPT

def test_batched_inference():
    items = load_split("repo_run2/data/sample/hotpot_test.jsonl")[:8]
    model_id = "Qwen/Qwen2.5-1.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True, padding_side="left")
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        dtype=torch.bfloat16,
        device_map="cuda",
        trust_remote_code=True
    )
    model.eval()
    
    prompts = []
    for item in items:
        msgs = [
            {"role": "system", "content": TABC_LONG_PROMPT},
            {"role": "user", "content": item["prompt"]}
        ]
        text = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        prompts.append(text)
        
    inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=2048).to("cuda")
    
    t0 = time.time()
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=180,
            do_sample=False,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    total_time = time.time() - t0
    vram = torch.cuda.memory_allocated() / (1024**3)
    
    print(f"Batched 8 items generated in {total_time:.2f}s ({total_time/8:.2f}s/item). VRAM: {vram:.2f} GB")
    
    del model
    del tokenizer
    torch.cuda.empty_cache()

if __name__ == "__main__":
    test_batched_inference()

