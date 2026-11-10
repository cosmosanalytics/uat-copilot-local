import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import json
import time
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from peft import LoraConfig, get_peft_model, TaskType
from src.eval.metrics import evaluate_all_metrics

# Set random seed
torch.manual_seed(42)

class CalibrationDataset(Dataset):
    def __init__(self, records, raw_dict, tokenizer, max_length=1024):
        self.samples = []
        for r in records:
            r_id = r["id"]
            raw = raw_dict.get(r_id, {})
            prompt = raw.get("prompt", "")
            ans = r.get("pred_answer", "")
            sol = r.get("think", "") or ""
            
            # E2b Context-aware input
            text = f"{prompt}\n\nProposed Solution: {sol}\nProposed Answer: {ans}"
            enc = tokenizer(text, truncation=True, max_length=max_length, padding="max_length", return_tensors="pt")
            
            self.samples.append({
                "input_ids": enc["input_ids"].squeeze(0),
                "attention_mask": enc["attention_mask"].squeeze(0),
                "label": torch.tensor(float(r["correct"]), dtype=torch.float32)
            })

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]

def train_e2_classifier():
    print("==================================================================")
    print("  STARTING REAL TRAINING: E2 0.5B Sequence Classifier with LoRA   ")
    print("==================================================================")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_id = "Qwen/Qwen2.5-0.5B"
    
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    print(f"Loading {model_id} for Sequence Classification on {device}...")
    base_model = AutoModelForSequenceClassification.from_pretrained(
        model_id,
        num_labels=1,
        torch_dtype=torch.bfloat16,
        device_map=device,
        trust_remote_code=True
    )
    base_model.config.pad_token_id = tokenizer.pad_token_id
    
    peft_config = LoraConfig(
        task_type=TaskType.SEQ_CLS,
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "v_proj"],
        modules_to_save=["score"]
    )
    model = get_peft_model(base_model, peft_config)
    model.print_trainable_parameters()
    
    # Load training data (from calibration split)
    cal_records = [json.loads(l) for l in open("repo/results/cal_outputs.jsonl", encoding="utf-8")]
    cal_raw = {json.loads(l)["id"]: json.loads(l) for l in open("repo/data/sample/hotpot_cal.jsonl", encoding="utf-8")}
    
    train_dataset = CalibrationDataset(cal_records, cal_raw, tokenizer)
    train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-4, weight_decay=0.01)
    criterion = nn.BCEWithLogitsLoss()
    
    num_epochs = 3
    model.train()
    print(f"\nTraining for {num_epochs} epochs on {len(train_dataset)} examples...")
    t0 = time.time()
    
    for epoch in range(num_epochs):
        epoch_loss = 0.0
        for step, batch in enumerate(train_loader):
            optimizer.zero_grad()
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits.squeeze(-1)
            loss = criterion(logits, labels)
            
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            
        avg_loss = epoch_loss / len(train_loader)
        print(f"Epoch {epoch+1}/{num_epochs} Complete | Avg Loss: {avg_loss:.4f} | Time: {time.time()-t0:.1f}s")
        
    # Save checkpoint
    save_dir = "repo/results/checkpoints/e2_classifier_0.5b"
    os.makedirs(save_dir, exist_ok=True)
    model.save_pretrained(save_dir)
    tokenizer.save_pretrained(save_dir)
    print(f"\nTrained LoRA checkpoint saved to {save_dir}")
    
    # Evaluate on held-out test split (152 items)
    print("\n--- Evaluating Trained 0.5B Classifier on Held-Out Test Set ---")
    test_records = [json.loads(l) for l in open("repo/results/e0_sample_outputs.jsonl", encoding="utf-8")]
    test_raw = {json.loads(l)["id"]: json.loads(l) for l in open("repo/data/sample/hotpot_test.jsonl", encoding="utf-8")}
    
    model.eval()
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
    
    # Save predictions
    out_preds = "repo/results/e2_trained_predictions.json"
    with open(out_preds, "w", encoding="utf-8") as f:
        json.dump({"metrics": metrics, "predictions": all_probs}, f, indent=2)
        
    print(f"Results of Trained 0.5B Classifier saved to {out_preds}:")
    print(f"Accuracy: {metrics['accuracy']*100:.1f}%")
    print(f"Brier Score: {metrics['brier_score']:.4f}")
    print(f"ECE: {metrics['ece']*100:.1f}%")
    print(f"AUROC (correctness): {metrics['auroc']:.3f}")
    print(f"AUROC (known): {metrics.get('auroc_known', 0.5):.3f}")
    
    del model
    del base_model
    del tokenizer
    torch.cuda.empty_cache()
    print("GPU memory cleared.")

if __name__ == "__main__":
    train_e2_classifier()
