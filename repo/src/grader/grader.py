import re
import string
from typing import Optional, Tuple, Dict, Any
from math_verify import parse, verify

def normalize_text(s: str) -> str:
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text: str) -> str:
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text: str) -> str:
        return ' '.join(text.split())

    def remove_punc(text: str) -> str:
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text: str) -> str:
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))

def grade_exact_match(prediction: str, ground_truth: str) -> bool:
    """Exact Match grading for QA tasks (e.g. HotpotQA)."""
    norm_pred = normalize_text(prediction)
    norm_gold = normalize_text(ground_truth)
    if not norm_pred or not norm_gold:
        return False
    return norm_pred == norm_gold

def grade_math(prediction: str, ground_truth: str) -> bool:
    """Math verification grading for math tasks (e.g. Big-Math, GSM8K, MATH-500)."""
    norm_pred = prediction.strip()
    norm_gold = ground_truth.strip()
    
    # Quick exact string check
    if norm_pred.lower() == norm_gold.lower():
        return True
        
    try:
        gold_parsed = parse(norm_gold, parsing_timeout=None)
        pred_parsed = parse(norm_pred, parsing_timeout=None)
        if gold_parsed and pred_parsed:
            match = verify(gold_parsed, pred_parsed, timeout_seconds=None)
            if match:
                return True
    except Exception:
        pass
        
    # Numerical fallback
    try:
        def clean_num(x):
            return float(re.sub(r'[^\d.-]', '', x))
        return abs(clean_num(norm_pred) - clean_num(norm_gold)) < 1e-5
    except Exception:
        return False

def extract_tags(text: str) -> Dict[str, Optional[str]]:
    """Extracts <think>, <answer>, <analysis>, and <confidence> tags from model output."""
    res = {
        "think": None,
        "answer": None,
        "analysis": None,
        "confidence": None,
        "raw_confidence": None,
        "confidence_float": None
    }
    
    think_m = re.search(r'<think>(.*?)</think>', text, flags=re.DOTALL | re.IGNORECASE)
    if think_m:
        res["think"] = think_m.group(1).strip()
        
    ans_m = re.search(r'<answer>(.*?)</answer>', text, flags=re.DOTALL | re.IGNORECASE)
    if ans_m:
        res["answer"] = ans_m.group(1).strip()
    else:
        # Fallback: if no tag, take last line or whole text if short
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        res["answer"] = lines[-1] if lines else ""
        
    anal_m = re.search(r'<analysis>(.*?)</analysis>', text, flags=re.DOTALL | re.IGNORECASE)
    if anal_m:
        res["analysis"] = anal_m.group(1).strip()
        
    conf_m = re.search(r'<confidence>(.*?)</confidence>', text, flags=re.DOTALL | re.IGNORECASE)
    if conf_m:
        raw_conf = conf_m.group(1).strip()
        res["confidence"] = raw_conf
        res["raw_confidence"] = raw_conf
        
        # Parse float value
        # Look for numbers like 0.85 or 85% or 85
        num_m = re.search(r'([0-9]+(?:\.[0-9]+)?)\s*(%)?', raw_conf)
        if num_m:
            val = float(num_m.group(1))
            is_pct = num_m.group(2) == '%' or val > 1.0
            if is_pct:
                val = val / 100.0
            val = max(0.0, min(1.0, val))
            res["confidence_float"] = val
            
    return res
