import re
import string
from typing import List, Dict, Any
from math_verify import parse, verify

def normalize_answer(s: str) -> str:
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

def exact_match_score(prediction: str, ground_truth: str) -> bool:
    return normalize_answer(prediction) == normalize_answer(ground_truth)

def format_reward_func(completions: List[str], format_pattern: str = "tabc") -> List[float]:
    """Checks completion tags and validates that confidence is a float in [0, 1]."""
    if format_pattern == "ta":
        pattern = r".*?</think>\s*<answer>.*?</answer>\s*\Z"
    elif format_pattern == "tabc":
        pattern = r".*?</think>\s*<answer>.*?</answer>\s*<analysis>.*?</analysis>\s*<confidence>.*?</confidence>\s*\Z"
    else:
        pattern = r".*?</think>\s*<answer>.*?</answer>\s*\Z"

    confidence_pattern = r"<confidence>(.*?)</confidence>"
    matches = [1.0 if re.match(pattern, content, re.DOTALL | re.MULTILINE) else 0.0 for content in completions]

    if "c" in format_pattern:
        for i, match in enumerate(matches):
            if match > 0.0:
                conf_matches = re.findall(confidence_pattern, completions[i], re.DOTALL | re.MULTILINE)
                if not conf_matches:
                    matches[i] = 0.0
                else:
                    try:
                        num = float(conf_matches[-1].strip().replace('%', ''))
                        if '%' in conf_matches[-1] or num > 1.0:
                            num = num / 100.0
                        if 0.0 <= num <= 1.0:
                            matches[i] = 1.0
                        else:
                            matches[i] = 0.0
                    except Exception:
                        matches[i] = 0.0
    return matches

def accuracy_reward_func(completions: List[str], answers: List[str], is_math: bool = False) -> List[float]:
    """Extracts text inside <answer> tags and evaluates correctness."""
    ans_pattern = r"<answer>(.*?)</answer>"
    rewards = []
    for content, gold in zip(completions, answers):
        ans_matches = re.findall(ans_pattern, content, re.DOTALL | re.MULTILINE)
        if not ans_matches:
            rewards.append(0.0)
            continue
        pred_ans = ans_matches[-1].strip()
        if not is_math:
            corr = 1.0 if exact_match_score(pred_ans, gold) else 0.0
        else:
            try:
                g_p = parse(gold, parsing_timeout=None)
                p_p = parse(pred_ans, parsing_timeout=None)
                corr = 1.0 if (g_p and p_p and verify(g_p, p_p, timeout_seconds=None)) else 0.0
            except Exception:
                corr = 0.0
        rewards.append(corr)
    return rewards

def rlcr_brier_reward_func(completions: List[str], answers: List[str], is_math: bool = False) -> List[float]:
    """Computes paper Eq. 8 reward: R = correct - (q - correct)^2."""
    acc_rewards = accuracy_reward_func(completions, answers, is_math=is_math)
    conf_pattern = r"<confidence>(.*?)</confidence>"
    rewards = []
    for content, acc in zip(completions, acc_rewards):
        conf_matches = re.findall(conf_pattern, content, re.DOTALL | re.MULTILINE)
        if not conf_matches:
            # If no confidence verbalized, default penalty
            rewards.append(acc - (0.5 - acc)**2)
            continue
        try:
            raw_c = conf_matches[-1].strip().replace('%', '')
            q = float(raw_c)
            if '%' in conf_matches[-1] or q > 1.0:
                q = q / 100.0
            q = max(0.0, min(1.0, q))
            brier_reward = acc - (q - acc)**2
            rewards.append(float(brier_reward))
        except Exception:
            rewards.append(acc - (0.5 - acc)**2)
    return rewards
