import re
import string
import numpy as np
from typing import List, Dict, Any, Optional, Tuple

def normalize_text_simple(s: str) -> str:
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)
    def white_space_fix(text):
        return ' '.join(text.split())
    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)
    def lower(text):
        return text.lower()
    return white_space_fix(remove_articles(remove_punc(lower(s))))

def check_answer_in_context(answer: str, context_paragraphs: List[str]) -> float:
    """Feature 1: Returns 1.0 if normalized answer appears in any context paragraph, else 0.0."""
    if not answer or not context_paragraphs:
        return 0.0
    norm_ans = normalize_text_simple(answer)
    if not norm_ans or len(norm_ans) < 2:
        return 0.0
        
    for p in context_paragraphs:
        norm_p = normalize_text_simple(p)
        if norm_ans in norm_p:
            return 1.0
    return 0.0

def compute_lexical_similarity(question: str, context_paragraphs: List[str]) -> Tuple[float, float]:
    """Computes max similarity and top-2 mean similarity between question and paragraphs using word-level jaccard/overlap."""
    if not question or not context_paragraphs:
        return 0.0, 0.0
    q_words = set(normalize_text_simple(question).split())
    if not q_words:
        return 0.0, 0.0
        
    sims = []
    for p in context_paragraphs:
        p_words = set(normalize_text_simple(p).split())
        if not p_words:
            sims.append(0.0)
            continue
        overlap = len(q_words & p_words) / float(len(q_words | p_words))
        sims.append(overlap)
        
    sims = sorted(sims, reverse=True)
    max_sim = sims[0] if sims else 0.0
    top2_mean = float(np.mean(sims[:2])) if len(sims) >= 2 else max_sim
    return float(max_sim), float(top2_mean)

def compute_nli_entailment_proxy(question: str, answer: str, context_paragraphs: List[str]) -> float:
    """Feature 3: NLI entailment proxy score: token overlap of (question + answer) against context."""
    if not context_paragraphs or not answer:
        return 0.0
    hypothesis_words = set(normalize_text_simple(f"{question} {answer}").split())
    if not hypothesis_words:
        return 0.0
        
    max_score = 0.0
    for p in context_paragraphs:
        p_words = set(normalize_text_simple(p).split())
        if not p_words:
            continue
        precision = len(hypothesis_words & p_words) / float(len(hypothesis_words))
        if precision > max_score:
            max_score = precision
    return float(max_score)

def compute_format_validity(answer: str, is_math: bool = False) -> float:
    """Feature 5: Non-empty, no unclosed tags, valid characters."""
    if not answer or not answer.strip():
        return 0.0
    ans = answer.strip()
    if "<" in ans or ">" in ans or len(ans) > 200:
        return 0.0
    if is_math:
        # Check if contains numeric digits or math symbols
        if re.search(r'[\d]', ans):
            return 1.0
        return 0.0
    return 1.0

def compute_reasoning_length_bucket(think_text: Optional[str]) -> float:
    """Reasoning length bucket: normalized length between 0 and 1."""
    if not think_text:
        return 0.0
    words = len(think_text.split())
    if words < 30:
        return 0.1
    elif words < 75:
        return 0.3
    elif words < 150:
        return 0.6
    elif words < 250:
        return 0.8
    else:
        return 1.0

class Tuple_Sim:
    pass

def extract_features_for_case(
    question: str,
    answer: str,
    think: Optional[str],
    context_paragraphs: Optional[List[str]],
    is_math: bool = False,
    self_consistency: float = 1.0
) -> Dict[str, float]:
    """Extracts features for E3 based on dataset type."""
    feat = {}
    feat["self_consistency"] = float(self_consistency)
    feat["format_validity"] = compute_format_validity(answer, is_math=is_math)
    
    if not is_math and context_paragraphs is not None:
        feat["answer_in_context"] = check_answer_in_context(answer, context_paragraphs)
        max_sim, top2_sim = compute_lexical_similarity(question, context_paragraphs)
        feat["max_emb_sim"] = max_sim
        feat["top2_emb_sim"] = top2_sim
        feat["nli_entailment"] = compute_nli_entailment_proxy(question, answer, context_paragraphs)
    else:
        feat["reasoning_len_bucket"] = compute_reasoning_length_bucket(think)
        
    return feat
