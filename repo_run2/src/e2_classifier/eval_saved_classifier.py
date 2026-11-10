import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import json
import torch
import numpy as np
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from peft import PeftModel
from src.e2_classifier.train_classifier_real import CalibrationDataset
from src.eval.metrics import evaluate_all_metrics

def main():
    print("=== Evaluating Trained E2 0.5B LoRA Classifier from Saved Checkpoint ===")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    base_id = "Qwen/Qwen2.5-0.5B"
    ckpt_dir = "repo_run2/results/checkpoints/e2_classifier_0.5b"
    
    tokenizer = AutoTokenizer.from_pretrained(ckpt_dir, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    base_model = AutoModelForSequenceClassification.from_pretrained(
        base_id,
        num_labels=1,
        torch_dtype=torch.bfloat16,
        device_map=device,
        trust_remote_code=True
    )
    base_model.config.pad_token_id = tokenizer.pad_token_id
    model = PeftModel.from_pretrained(base_model, ckpt_dir)
    model.eval()
    
    test_records = [json.loads(l) for l in open("repo_run2/results/e0_sample_outputs.jsonl", encoding="utf-8")]
    test_raw = {json.loads(l)["id"]: json.loads(l) for l in open("repo_run2/data/sample/hotpot_test.jsonl", encoding="utf-8")}
    
    test_dataset = CalibrationDataset(test_records, test_raw, tokenizer)
    test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)
    
    all_probs = []
    with torch.no_grad():
        for batch in test_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            logits = model(input_ids=input_ids, attention_mask=attention_mask).logits.squeeze(-1)
            probs = torch.sigmoid(logits).cpu().tolist()
            if isinstance(probs, float):
                probs = [probs]
            all_probs.extend(probs)
            
    q_pred = np.array(all_probs)
    y_true = np.array([r["correct"] for r in test_records])
    kn_true = np.array([r["known"] for r in test_records])
    nr_true = np.array([r["n_removed"] for r in test_records])
    
    metrics = evaluate_all_metrics(y_true, q_pred, n_removed=nr_true, known=kn_true)
    
    out_preds = "repo_run2/results/e2_trained_predictions.json"
    with open(out_preds, "w", encoding="utf-8") as f:
        json.dump({"metrics": metrics, "predictions": all_probs}, f, indent=2)
        
    print(f"\n--- Trained 0.5B Classifier Evaluation Metrics ---")
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

if __name__ == "__main__":
    main()

