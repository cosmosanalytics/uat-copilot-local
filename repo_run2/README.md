# Calibrated Confidence for LLM Agents: RLCR Reproduction and Evaluation

This repository reproduces and extends the experimental framework from Damani et al., *"Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty"* (RLCR, arXiv:2507.16806, ICLR 2026), comparing four confidence calibration methods on the paper's original datasets under consumer GPU constraints (12 GB VRAM).

## Methods Compared

| ID | Method | Models | Calibration Mechanism | Compute Cost |
|---|---|---|---|---|
| **E0** | Base Model (Control) | 1 LLM | Verbalized confidence in `<confidence>` tag | Lowest (Inference only) |
| **E1** | RLCR (Paper's Method) | 1 LLM (RL-Trained) | Proper scoring rule (Brier reward Eq. 8) via GRPO | High (RL training) |
| **E2** | Two-Model Classifier | 2 LLMs | Trained sequence classifier (0.5B/1.5B) on solution & context | High (2 models in training & inference) |
| **E3** | Code-Computed Scorer (Zhao's Method) | 1 LLM + Logistic Reg. | L2 regularized logistic regression on 5 code features | Cheap, inspectable, zero RL |
| **E4** | Hybrid Scorer | 2 LLMs + Logistic Reg. | Prompted judge findings + code features into LR | Moderate (Prompted judge + LR) |

## Repository Structure

```
repo_run2/
├── README.md                  # This file
├── configs/base.yaml          # Pinned hyperparameters and seeds
├── data/
│   ├── loaders.py             # HotpotQA-Modified & Big-Math Digits loaders
│   └── sample/                # Sample tier splits (500 train, 200 cal, 300 test)
├── prompts/
│   └── paper_prompts.py       # Paper-faithful system prompts (<think>, <answer>, <analysis>, <confidence>)
├── src/
│   ├── agent/runner.py        # Batched inference with KV cache
│   ├── eval/metrics.py        # Accuracy, Brier, 10-bin ECE, AUROC, 95% Bootstrap CIs
│   ├── eval/plots.py          # Reliability diagrams and risk-coverage curves
│   ├── grader/grader.py       # Exact match, math-verify, tag parser
│   ├── e1_rlcr/               # GRPO trainer & reward functions
│   ├── e2_classifier/         # Two-model sequence classifiers & prompted judge
│   ├── e3_scorer/             # Code feature extraction & per-task L2 logistic regression
│   ├── e4_hybrid/             # Judge JSON parser & hybrid logistic model
│   └── orchestrator.py        # End-to-end multi-milestone evaluation
├── results/                   # Per-case JSONL, metrics CSV, figures
└── report.md                  # Full scientific research report
```

## Quickstart & Reproduction

### 1. Setup Environment
```bash
pip install -r requirements.txt
```

### 2. Run Metrics Unit Tests
```bash
pytest repo_run2/tests/test_metrics.py repo_run2/tests/test_grader.py -v
```

### 3. Run Experiments (E0 - E4)
```bash
python repo_run2/src/orchestrator.py
```

### 4. Inspect Results
- Summary metrics: `repo_run2/results/main_results_table.csv`
- Figures: `repo_run2/results/figures/`
- Full report: `repo_run2/report.md`

