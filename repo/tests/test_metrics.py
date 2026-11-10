import pytest
import numpy as np
import sys
import os

# Add repo root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.eval.metrics import (
    compute_accuracy,
    compute_brier_score,
    compute_ece,
    compute_auroc,
    compute_selective_prediction,
    compute_bootstrap_ci,
    evaluate_all_metrics
)

def test_perfect_calibration():
    y = np.array([1, 1, 0, 0])
    conf = np.array([1.0, 1.0, 0.0, 0.0])
    
    assert compute_accuracy(y, (conf >= 0.5).astype(int)) == 1.0
    assert compute_brier_score(y, conf) == 0.0
    assert compute_ece(y, conf, n_bins=10) == 0.0
    assert compute_auroc(y, conf) == 1.0

def test_complete_miscalibration():
    y = np.array([0, 0])
    conf = np.array([1.0, 1.0])
    
    assert compute_accuracy(y, (conf >= 0.5).astype(int)) == 0.0
    assert compute_brier_score(y, conf) == 1.0
    assert compute_ece(y, conf, n_bins=10) == 1.0

def test_inverted_ranking_auroc():
    y = np.array([1, 1, 0, 0])
    conf = np.array([0.1, 0.2, 0.8, 0.9])
    
    assert compute_auroc(y, conf) == 0.0

def test_ties_in_auroc():
    y = np.array([1, 0, 1, 0])
    conf = np.array([0.5, 0.5, 0.5, 0.5])
    
    assert compute_auroc(y, conf) == 0.5

def test_ece_known_bin_distribution():
    # 10 cases in bin [0.8, 0.9): 8 correct, 2 incorrect -> empirical acc = 0.8, mean conf = 0.85 -> gap = 0.05
    y = np.array([1]*8 + [0]*2)
    conf = np.array([0.85]*10)
    
    ece = compute_ece(y, conf, n_bins=10)
    assert np.isclose(ece, 0.05, atol=1e-5)

def test_selective_prediction():
    # 10 cases: 9 correct with high confidence, 1 wrong with low confidence
    y = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 0])
    conf = np.array([0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.20])
    
    res = compute_selective_prediction(y, conf, target_accuracy=0.95)
    # The top 9 cases have 100% accuracy (>= 95%), all 10 have 90% (<95%)
    assert np.isclose(res["automation_rate"], 0.9)
    assert np.isclose(res["threshold_at_target"], 0.91)

def test_bootstrap_ci():
    y = np.array([1, 1, 1, 1, 0, 0, 0, 0])
    conf = np.array([0.8, 0.7, 0.9, 0.6, 0.2, 0.3, 0.1, 0.4])
    
    pt, lo, hi = compute_bootstrap_ci(y, conf, compute_brier_score, n_resamples=500, random_state=42)
    assert lo <= pt <= hi

def test_evaluate_all_metrics_structure():
    y = np.array([1, 1, 0, 0, 1])
    conf = np.array([0.9, 0.8, 0.3, 0.2, 0.6])
    n_removed = np.array([0, 1, 2, 2, 0])
    known = np.array([1, 0, 0, 0, 1])
    
    res = evaluate_all_metrics(y, conf, n_removed=n_removed, known=known, n_resamples=200)
    assert "accuracy" in res
    assert "brier_score" in res
    assert "ece" in res
    assert "auroc" in res
    assert "auroc_known" in res
    assert "conf_by_n_removed" in res
    assert "mean_conf_n_removed_0" in res["conf_by_n_removed"]
