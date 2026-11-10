import os
import sys
import json
from typing import List, Dict, Any

def analyze_failures(outputs_file: str, top_n: int = 30) -> List[Dict[str, Any]]:
    """Identifies and categorizes the top-N most confident mistakes."""
    records = []
    with open(outputs_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line.strip()))
                
    # Filter incorrect predictions
    failures = [r for r in records if r["correct"] == 0]
    
    # Sort by descending confidence (most confident errors first)
    failures = sorted(failures, key=lambda x: x["confidence"], reverse=True)
    top_failures = failures[:top_n]
    
    categorized = []
    for f in top_failures:
        n_rem = f.get("n_removed", 0)
        gold = str(f.get("gold_answer", "")).lower()
        pred = str(f.get("pred_answer", "")).lower()
        
        # Categorization logic
        if n_rem > 0:
            category = "Missing Evidence Unnoticed (Hallucination/Guess)"
            explanation = f"Supporting paragraph was removed (n_removed={n_rem}), but model hallucinated high confidence."
        elif gold in pred or pred in gold:
            category = "Entity / Format Boundary Issue"
            explanation = "Prediction contains or overlaps gold entity but exact match failed due to phrasing."
        elif f.get("dataset") == "big_math_digits":
            category = "Mathematical Derivation Error"
            explanation = "Arithmetic or algebraic step failed in reasoning chain."
        else:
            category = "Faulty Multi-Hop Reasoning"
            explanation = "Model mislinked entities across the 8 distractors despite evidence being present."
            
        categorized.append({
            "id": f["id"],
            "dataset": f.get("dataset", "unknown"),
            "confidence": f["confidence"],
            "pred_answer": f["pred_answer"],
            "gold_answer": f["gold_answer"],
            "n_removed": n_rem,
            "category": category,
            "explanation": explanation
        })
        
    return categorized

if __name__ == "__main__":
    outputs = "repo/results/e0_sample_outputs.jsonl"
    if os.path.exists(outputs):
        res = analyze_failures(outputs, 30)
        out_path = "repo/results/failure_analysis_30.json"
        with open(out_path, "w", encoding="utf-8") as out_f:
            json.dump(res, out_f, indent=2)
        print(f"Saved {len(res)} categorized failure cases to {out_path}")
