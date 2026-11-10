import json
import re
from typing import Dict, List, Any, Optional
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from prompts.paper_prompts import E4_JUDGE_PROMPT

def parse_judge_json(output_text: str) -> Dict[str, Any]:
    """Extracts and parses JSON object from judge LLM output."""
    default_res = {
        "supported_claims": 1,
        "unsupported_claims": 0,
        "missing_info": [],
        "assumed_facts": 0,
        "judge_confidence": 0.5
    }
    # Match JSON block
    m = re.search(r'\{.*?\}', output_text, flags=re.DOTALL)
    if not m:
        return default_res
    try:
        data = json.loads(m.group(0))
        return {
            "supported_claims": int(data.get("supported_claims", 1)),
            "unsupported_claims": int(data.get("unsupported_claims", 0)),
            "missing_info": list(data.get("missing_info", [])),
            "assumed_facts": int(data.get("assumed_facts", 0)),
            "judge_confidence": float(data.get("judge_confidence", 0.5))
        }
    except Exception:
        return default_res

def evaluate_judge_missing_info(judge_records: List[Dict[str, Any]]) -> Dict[str, float]:
    """Validates judge recall & precision on identifying unknown cases (n_removed > 0)."""
    # Target: 1 if n_removed > 0 (unknown/missing evidence), 0 if known
    y_true_missing = []
    y_pred_missing = []
    
    for r in judge_records:
        n_rem = r.get("n_removed", 0)
        is_missing = 1 if n_rem > 0 else 0
        y_true_missing.append(is_missing)
        
        # Judge flagged missing info if len(missing_info) > 0 or unsupported_claims > 0
        findings = r.get("judge_findings", {})
        has_missing_flag = 1 if (len(findings.get("missing_info", [])) > 0 or findings.get("unsupported_claims", 0) > 0) else 0
        y_pred_missing.append(has_missing_flag)
        
    y_true_missing = np.array(y_true_missing)
    y_pred_missing = np.array(y_pred_missing)
    
    tp = np.sum((y_true_missing == 1) & (y_pred_missing == 1))
    fp = np.sum((y_true_missing == 0) & (y_pred_missing == 1))
    fn = np.sum((y_true_missing == 1) & (y_pred_missing == 0))
    tn = np.sum((y_true_missing == 0) & (y_pred_missing == 0))
    
    precision = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
    recall = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
    f1 = float(2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "true_positives": int(tp),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_negatives": int(tn)
    }

class E4HybridScorer:
    """Supports fitting E4a (judge only), E4b (code only), and E4c (hybrid)."""
    def __init__(self, mode: str = "hybrid"):
        assert mode in ["e4a_judge_only", "e4b_code_only", "e4c_hybrid"]
        self.mode = mode
        self.clf = LogisticRegression(C=1.0, penalty='l2', solver='lbfgs', max_iter=1000)

    def extract_features(self, item: Dict[str, Any], code_feats: Dict[str, float]) -> np.ndarray:
        findings = item.get("judge_findings", {})
        judge_vec = [
            float(findings.get("supported_claims", 1)),
            float(findings.get("unsupported_claims", 0)),
            float(len(findings.get("missing_info", []))),
            float(findings.get("assumed_facts", 0)),
            float(findings.get("judge_confidence", 0.5))
        ]
        code_vec = list(code_feats.values())
        
        if self.mode == "e4a_judge_only":
            return np.array(judge_vec)
        elif self.mode == "e4b_code_only":
            return np.array(code_vec)
        else: # e4c_hybrid
            return np.array(judge_vec + code_vec)

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.clf.fit(X, y)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.clf.predict_proba(X)[:, 1]
