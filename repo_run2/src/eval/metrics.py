import numpy as np
from typing import Dict, List, Optional, Tuple, Any

def compute_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Computes standard binary accuracy."""
    if len(y_true) == 0:
        return 0.0
    return float(np.mean(y_true == y_pred))

def compute_brier_score(y_true: np.ndarray, confidences: np.ndarray) -> float:
    """Computes mean squared error between confidences and binary ground truth (0 or 1).
    Brier score = (1/N) * sum((q_i - y_i)^2). Lower is better.
    """
    if len(y_true) == 0:
        return 0.0
    y_true = np.asarray(y_true, dtype=np.float64)
    confidences = np.asarray(confidences, dtype=np.float64)
    return float(np.mean((confidences - y_true) ** 2))

def compute_ece(y_true: np.ndarray, confidences: np.ndarray, n_bins: int = 10) -> float:
    """Computes Expected Calibration Error with 10 equal-width bins [0, 1].
    ECE = sum_{b=1}^B (|B_b| / N) * |acc(B_b) - conf(B_b)|
    """
    if len(y_true) == 0:
        return 0.0
    y_true = np.asarray(y_true, dtype=np.float64)
    conf = np.asarray(confidences, dtype=np.float64)
    N = len(y_true)
    
    bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    
    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]
        
        # Include upper boundary in the last bin
        if i == n_bins - 1:
            in_bin = (conf >= bin_lower) & (conf <= bin_upper)
        else:
            in_bin = (conf >= bin_lower) & (conf < bin_upper)
            
        bin_count = np.sum(in_bin)
        if bin_count > 0:
            bin_acc = np.mean(y_true[in_bin])
            bin_conf = np.mean(conf[in_bin])
            ece += (bin_count / N) * abs(bin_acc - bin_conf)
            
    return float(ece)

def compute_auroc(y_true: np.ndarray, scores: np.ndarray) -> float:
    """Computes Area Under the ROC Curve without external dependencies using trapezoidal rule / Wilcoxon-Mann-Whitney.
    Handles degenerate cases (e.g. only 1 class present) by returning 0.5.
    """
    y_true = np.asarray(y_true, dtype=np.int32)
    scores = np.asarray(scores, dtype=np.float64)
    
    n_pos = np.sum(y_true == 1)
    n_neg = np.sum(y_true == 0)
    
    if n_pos == 0 or n_neg == 0:
        return 0.5
        
    # Rank scores (average ranks for ties)
    order = np.argsort(scores)
    ranks = np.empty_like(order, dtype=np.float64)
    ranks[order] = np.arange(1, len(scores) + 1)
    
    # Handle ties in rank
    unique_scores, inverse, counts = np.unique(scores, return_inverse=True, return_counts=True)
    tie_indices = np.where(counts > 1)[0]
    for idx in tie_indices:
        mask = (inverse == idx)
        ranks[mask] = np.mean(ranks[mask])
        
    sum_ranks_pos = np.sum(ranks[y_true == 1])
    u = sum_ranks_pos - (n_pos * (n_pos + 1)) / 2.0
    auroc = u / (n_pos * n_neg)
    return float(auroc)

def compute_selective_prediction(y_true: np.ndarray, confidences: np.ndarray, target_accuracy: float = 0.95) -> Dict[str, Any]:
    """Computes risk-coverage curve and the automation rate at target accuracy (e.g. 95%).
    Sorts by descending confidence. Coverage is fraction of data acted upon.
    Risk is error rate (1 - accuracy) among selected cases.
    """
    N = len(y_true)
    if N == 0:
        return {"automation_rate": 0.0, "threshold_at_target": 1.0, "coverages": [], "risks": []}
        
    order = np.argsort(-confidences)
    sorted_y = y_true[order]
    sorted_conf = confidences[order]
    
    cum_correct = np.cumsum(sorted_y)
    coverages = np.arange(1, N + 1) / float(N)
    accuracies = cum_correct / np.arange(1, N + 1)
    risks = 1.0 - accuracies
    
    # Find maximum coverage where accuracy >= target_accuracy
    valid_indices = np.where(accuracies >= target_accuracy)[0]
    if len(valid_indices) > 0:
        max_idx = valid_indices[-1]
        automation_rate = float(coverages[max_idx])
        threshold_at_target = float(sorted_conf[max_idx])
    else:
        automation_rate = 0.0
        threshold_at_target = 1.0
        
    return {
        "automation_rate": automation_rate,
        "threshold_at_target": threshold_at_target,
        "coverages": coverages.tolist(),
        "risks": risks.tolist(),
        "accuracies": accuracies.tolist()
    }

def compute_bootstrap_ci(
    y_true: np.ndarray, 
    confidences: np.ndarray, 
    metric_fn, 
    n_resamples: int = 1000, 
    ci: float = 0.95,
    random_state: int = 42
) -> Tuple[float, float, float]:
    """Computes point estimate and 95% bootstrap confidence interval [lower, upper]."""
    rng = np.random.RandomState(random_state)
    N = len(y_true)
    if N == 0:
        return 0.0, 0.0, 0.0
        
    point_est = metric_fn(y_true, confidences)
    boot_vals = []
    for _ in range(n_resamples):
        indices = rng.randint(0, N, size=N)
        boot_vals.append(metric_fn(y_true[indices], confidences[indices]))
        
    alpha = (1.0 - ci) / 2.0
    lower = float(np.percentile(boot_vals, 100.0 * alpha))
    upper = float(np.percentile(boot_vals, 100.0 * (1.0 - alpha)))
    return float(point_est), lower, upper

def evaluate_all_metrics(
    y_true: np.ndarray,
    confidences: np.ndarray,
    n_removed: Optional[np.ndarray] = None,
    known: Optional[np.ndarray] = None,
    n_resamples: int = 1000,
    random_state: int = 42
) -> Dict[str, Any]:
    """Computes comprehensive evaluation metrics with bootstrap 95% CIs."""
    y_true = np.asarray(y_true, dtype=np.int32)
    conf = np.asarray(confidences, dtype=np.float64)
    
    # Decisions based on threshold 0.5
    y_pred = (conf >= 0.5).astype(np.int32)
    
    acc, acc_lo, acc_hi = compute_bootstrap_ci(y_true, y_pred, lambda yt, yp: compute_accuracy(yt, yp), n_resamples, random_state=random_state)
    brier, brier_lo, brier_hi = compute_bootstrap_ci(y_true, conf, compute_brier_score, n_resamples, random_state=random_state)
    ece, ece_lo, ece_hi = compute_bootstrap_ci(y_true, conf, lambda yt, cf: compute_ece(yt, cf, 10), n_resamples, random_state=random_state)
    auroc, auroc_lo, auroc_hi = compute_bootstrap_ci(y_true, conf, compute_auroc, n_resamples, random_state=random_state)
    
    sel = compute_selective_prediction(y_true, conf, target_accuracy=0.95)
    
    results = {
        "accuracy": acc, "accuracy_ci": [acc_lo, acc_hi],
        "brier_score": brier, "brier_ci": [brier_lo, brier_hi],
        "ece": ece, "ece_ci": [ece_lo, ece_hi],
        "auroc": auroc, "auroc_ci": [auroc_lo, auroc_hi],
        "automation_rate_95": sel["automation_rate"],
        "threshold_95": sel["threshold_at_target"]
    }
    
    # Analysis metrics if known/n_removed are provided
    if known is not None:
        known = np.asarray(known, dtype=np.int32)
        auroc_known = compute_auroc(known, conf)
        results["auroc_known"] = auroc_known
        
    if n_removed is not None:
        n_removed = np.asarray(n_removed, dtype=np.int32)
        conf_by_n = {}
        for nr in [0, 1, 2]:
            mask = (n_removed == nr)
            if np.sum(mask) > 0:
                conf_by_n[f"mean_conf_n_removed_{nr}"] = float(np.mean(conf[mask]))
        results["conf_by_n_removed"] = conf_by_n
        
    return results
