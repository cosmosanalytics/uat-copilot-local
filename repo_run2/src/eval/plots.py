import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Any, Optional

def plot_reliability_diagram(
    y_true: np.ndarray,
    confidences: np.ndarray,
    title: str,
    output_path: str,
    n_bins: int = 10
):
    """Generates and saves a publication-quality reliability diagram (calibration curve)."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
    bin_confs = []
    bin_accs = []
    bin_counts = []
    
    for i in range(n_bins):
        b_lo = bin_boundaries[i]
        b_hi = bin_boundaries[i + 1]
        if i == n_bins - 1:
            mask = (confidences >= b_lo) & (confidences <= b_hi)
        else:
            mask = (confidences >= b_lo) & (confidences < b_hi)
        count = np.sum(mask)
        bin_counts.append(count)
        if count > 0:
            bin_accs.append(np.mean(y_true[mask]))
            bin_confs.append(np.mean(confidences[mask]))
        else:
            bin_accs.append(0.0)
            bin_confs.append((b_lo + b_hi) / 2.0)
            
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 7), gridspec_kw={'height_ratios': [3, 1]})
    
    # Calibration plot
    ax1.plot([0, 1], [0, 1], 'k--', label='Perfect calibration')
    ax1.bar(
        [b + 0.05 for b in bin_boundaries[:-1]],
        bin_accs,
        width=0.08,
        alpha=0.6,
        color='#2563eb',
        edgecolor='#1d4ed8',
        label='Model outputs'
    )
    ax1.set_xlim([0, 1])
    ax1.set_ylim([0, 1.05])
    ax1.set_ylabel('Empirical Accuracy')
    ax1.set_title(title, fontsize=12, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper left')
    
    # Sample counts histogram
    ax2.bar([b + 0.05 for b in bin_boundaries[:-1]], bin_counts, width=0.08, color='#64748b', alpha=0.7)
    ax2.set_xlim([0, 1])
    ax2.set_xlabel('Confidence')
    ax2.set_ylabel('Count')
    ax2.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
    print(f"Saved reliability diagram to {output_path}")

def plot_risk_coverage_curve(
    y_true: np.ndarray,
    confidences: np.ndarray,
    methods_dict: Dict[str, np.ndarray],
    output_path: str,
    target_accuracy: float = 0.95
):
    """Plots comparative risk-coverage curves for multiple calibration methods."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.figure(figsize=(7, 5))
    
    colors = ['#2563eb', '#16a34a', '#dc2626', '#9333ea', '#ea580c']
    for idx, (name, confs) in enumerate(methods_dict.items()):
        N = len(y_true)
        order = np.argsort(-confs)
        sorted_y = y_true[order]
        coverages = np.arange(1, N + 1) / float(N)
        accuracies = np.cumsum(sorted_y) / np.arange(1, N + 1)
        risks = 1.0 - accuracies
        
        color = colors[idx % len(colors)]
        plt.plot(coverages * 100, risks * 100, label=name, color=color, linewidth=2)
        
    # Target error rate line (5% risk for 95% accuracy)
    target_risk = (1.0 - target_accuracy) * 100
    plt.axhline(target_risk, color='black', linestyle=':', label=f'Target Risk ({target_risk:.0f}%)')
    
    plt.xlabel('Coverage (% of cases acted upon automatically)', fontsize=11)
    plt.ylabel('Risk / Error Rate (%)', fontsize=11)
    plt.title('Selective Prediction: Risk-Coverage Curve', fontsize=12, fontweight='bold')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper left')
    plt.ylim([0, 50])
    plt.xlim([0, 100])
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
    print(f"Saved risk-coverage curve to {output_path}")

def plot_confidence_by_evidence_removed(
    methods_confs_by_nr: Dict[str, Dict[str, float]],
    output_path: str
):
    """Plots mean confidence across n_removed = 0, 1, 2 for each method."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.figure(figsize=(8, 5))
    
    x = np.arange(3)
    width = 0.18
    nr_labels = ['n=0 (Known)', 'n=1 (Partial)', 'n=2 (Unknown)']
    
    colors = ['#dc2626', '#2563eb', '#16a34a', '#9333ea', '#ea580c']
    for idx, (method_name, data) in enumerate(methods_confs_by_nr.items()):
        vals = [
            data.get('mean_conf_n_removed_0', 0.5),
            data.get('mean_conf_n_removed_1', 0.5),
            data.get('mean_conf_n_removed_2', 0.5)
        ]
        offset = (idx - len(methods_confs_by_nr) / 2.0 + 0.5) * width
        plt.bar(x + offset, vals, width, label=method_name, color=colors[idx % len(colors)], alpha=0.85)
        
    plt.xticks(x, nr_labels, fontsize=11)
    plt.ylabel('Mean Verbalized / Predicted Confidence', fontsize=11)
    plt.ylim([0, 1.05])
    plt.title('Calibrated Confidence vs Missing Evidence (HotpotQA-Modified)', fontsize=12, fontweight='bold')
    plt.grid(True, linestyle=':', alpha=0.6, axis='y')
    plt.legend(loc='lower left')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
    print(f"Saved evidence removed plot to {output_path}")
