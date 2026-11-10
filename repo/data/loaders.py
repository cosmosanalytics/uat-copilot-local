import os
import json
import random
from typing import List, Dict, Any, Optional
from datasets import load_dataset

def build_sample_splits(output_dir: str = "repo/data/sample", seed: int = 42):
    """Builds and caches sample tier splits (500 train, 200 cal, 300 test) for HotpotQA-Modified and Big-Math-Digits.
    Strictly follows protocol:
    - known and n_removed labels are kept for evaluation/analysis ONLY.
    - splits are non-overlapping.
    """
    os.makedirs(output_dir, exist_ok=True)
    random.seed(seed)
    
    print("[1/2] Loading mehuldamani/hotpot_qa...")
    ds_hotpot_train = load_dataset("mehuldamani/hotpot_qa", split="train")
    ds_hotpot_test = load_dataset("mehuldamani/hotpot_qa", split="test")
    
    # Shuffle train indices
    train_indices = list(range(len(ds_hotpot_train)))
    random.shuffle(train_indices)
    
    # Sample tier: 500 train, 200 cal
    sample_train_idx = train_indices[:500]
    sample_cal_idx = train_indices[500:700]
    
    def process_hotpot(item, idx, split_name):
        gold_removed = item.get("gold_removed", 0)
        return {
            "id": f"hotpot_{split_name}_{idx}",
            "dataset": "hotpotqa_modified",
            "prompt": item["problem"],
            "answer": item["answer"],
            "context": item.get("context", []),
            "n_removed": int(gold_removed),
            "known": 1 if int(gold_removed) == 0 else 0,
            "split": split_name
        }
        
    hotpot_train = [process_hotpot(ds_hotpot_train[i], i, "train") for i in sample_train_idx]
    hotpot_cal = [process_hotpot(ds_hotpot_train[i], i, "cal") for i in sample_cal_idx]
    
    test_indices = list(range(len(ds_hotpot_test)))
    random.shuffle(test_indices)
    sample_test_idx = test_indices[:300]
    hotpot_test = [process_hotpot(ds_hotpot_test[i], i, "test") for i in sample_test_idx]
    
    # Save HotpotQA sample files
    for name, data in [("hotpot_train.jsonl", hotpot_train), ("hotpot_cal.jsonl", hotpot_cal), ("hotpot_test.jsonl", hotpot_test)]:
        p = os.path.join(output_dir, name)
        with open(p, "w", encoding="utf-8") as f:
            for row in data:
                f.write(json.dumps(row) + "\n")
        print(f"Saved {len(data)} items to {p}")
        
    print("[2/2] Loading mehuldamani/big-math-digits...")
    ds_math_train = load_dataset("mehuldamani/big-math-digits", split="train")
    ds_math_test = load_dataset("mehuldamani/big-math-digits", split="test")
    
    # Filter 0 to 70% solve rate if present
    train_math_indices = []
    for i, item in enumerate(ds_math_train):
        sr = item.get("llama8b_solve_rate", 0.5)
        if 0.0 <= sr <= 0.70:
            train_math_indices.append(i)
            
    random.shuffle(train_math_indices)
    math_sample_train_idx = train_math_indices[:500]
    math_sample_cal_idx = train_math_indices[500:700]
    
    def process_math(item, idx, split_name):
        return {
            "id": f"math_{split_name}_{idx}",
            "dataset": "big_math_digits",
            "prompt": item["problem"],
            "answer": str(item["answer"]),
            "context": None,
            "n_removed": 0,
            "known": 1,
            "llama8b_solve_rate": item.get("llama8b_solve_rate", 0.0),
            "split": split_name
        }
        
    math_train = [process_math(ds_math_train[i], i, "train") for i in math_sample_train_idx]
    math_cal = [process_math(ds_math_train[i], i, "cal") for i in math_sample_cal_idx]
    
    test_math_indices = list(range(len(ds_math_test)))
    random.shuffle(test_math_indices)
    math_sample_test_idx = test_math_indices[:300]
    math_test = [process_math(ds_math_test[i], i, "test") for i in math_sample_test_idx]
    
    for name, data in [("math_train.jsonl", math_train), ("math_cal.jsonl", math_cal), ("math_test.jsonl", math_test)]:
        p = os.path.join(output_dir, name)
        with open(p, "w", encoding="utf-8") as f:
            for row in data:
                f.write(json.dumps(row) + "\n")
        print(f"Saved {len(data)} items to {p}")

def load_split(split_file: str) -> List[Dict[str, Any]]:
    """Loads a JSONL split file."""
    rows = []
    with open(split_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line.strip()))
    return rows

if __name__ == "__main__":
    build_sample_splits()
