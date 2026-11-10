import os
import json
import torch
import torch.nn as nn
from typing import List, Dict, Any, Optional
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType
from prompts.paper_prompts import DEEPSEEK_VERIFIER_PROMPT
from src.grader.grader import extract_tags

class PromptedJudgeE2c:
    """Zero-shot prompted verifier (E2c) that predicts confidence given question, context, and answer."""
    def __init__(self, tokenizer, model, device: str = "cuda"):
        self.tokenizer = tokenizer
        self.model = model
        self.device = device

    def predict_confidence(self, question: str, solution: str, answer: str, context: Optional[str] = None) -> float:
        content = f"Question: {question}\n"
        if context:
            content += f"Context: {context}\n"
        content += f"Proposed Solution: {solution}\nProposed Answer: {answer}\n"
        
        msgs = [
            {"role": "system", "content": DEEPSEEK_VERIFIER_PROMPT},
            {"role": "user", "content": content}
        ]
        text = self.tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=1536).to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=150,
                do_sample=False,
                pad_token_id=self.tokenizer.pad_token_id
            )
            input_len = inputs["input_ids"].shape[1]
            gen_text = self.tokenizer.decode(outputs[0][input_len:], skip_special_tokens=True)
            
        tags = extract_tags(gen_text)
        conf = tags["confidence_float"]
        return conf if conf is not None else 0.5

class BrierLoss(nn.Module):
    """Brier/MSE Loss for binary classification calibration (Paper Eq. 10)."""
    def __init__(self):
        super().__init__()
        self.mse = nn.MSELoss()

    def forward(self, logits, targets):
        probs = torch.sigmoid(logits.squeeze(-1))
        return self.mse(probs, targets.float())

class TwoModelClassifier:
    """Trained sequence classification model (0.5B or 1.5B) for E2a and E2b."""
    def __init__(self, model_id: str = "Qwen/Qwen2.5-0.5B", loss_type: str = "bce", device: str = "cuda"):
        self.model_id = model_id
        self.loss_type = loss_type
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_id,
            num_labels=1,
            trust_remote_code=True
        )
        
        # Apply LoRA for 12GB VRAM efficiency
        peft_config = LoraConfig(
            task_type=TaskType.SEQ_CLS,
            r=16,
            lora_alpha=32,
            lora_dropout=0.05,
            target_modules=["q_proj", "v_proj"]
        )
        self.model = get_peft_model(self.model, peft_config)
        self.model.to(device)

    def predict_probabilities(self, texts: List[str]) -> List[float]:
        self.model.eval()
        inputs = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=1536).to(self.device)
        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.sigmoid(logits.squeeze(-1)).cpu().tolist()
        if isinstance(probs, float):
            probs = [probs]
        return probs
