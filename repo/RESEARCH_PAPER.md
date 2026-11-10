# Empirical Stability and Calibration in Language Model Uncertainty: An Exploratory Study of RLCR-Style Policies, Supervised Verifiers, and Code Scorers

**A Multi-Run Investigation of Calibration Rewards, Supervised Neural Heads, and Text-Overlap Scoring Functions**

---

### Authors
**AI Engineering Calibration Team** & **Zhao**  

---

## Abstract

Calibrating uncertainty estimates in large language models (LLMs) is essential for dependable autonomous agent deployment. Recently, Damani et al. (ICLR 2026) introduced *Reinforcement Learning with Calibration Rewards* (RLCR), proposing that optimizing language models directly against proper scoring rules (such as the Brier score) trains policies to verbalize well-calibrated confidence tags alongside generated answers. However, open empirical questions remain regarding the sample efficiency, optimization stability, and operational requirements of RL-based calibration compared to auxiliary neural verifiers and lightweight code-computed scoring functions.

In this work, we conduct an exploratory, multi-run study comparing an underpowered RLCR-style setup against supervised sequence classification heads, zero-shot judges, and deterministic text-overlap scoring functions. Evaluations are conducted across multiple seeds and train/test partitions using HotpotQA-Modified ($N=152$ test cases with controlled evidence removal, containing 21 positive matches) and an exploratory subset of Big-Math-Digits ($N=36$ cases with 2 positive matches).

Our primary empirical findings include:
1. **Performance Relative to the Constant Prior Baseline:** On the held-out test split, the empirical positive prevalence is 13.8% (21/152). A non-parametric constant prior baseline trained on the calibration split ($\bar{y}_{\text{train}}=0.224$) yields a test Brier score of **0.1264** [95% CI: 0.0974, 0.1591] and an Expected Calibration Error (ECE) of **8.6%** [2.7%, 13.8%], reflecting a train-to-test base-rate shift ($22.4\% \to 13.8\%$). By comparison, the uncalibrated base LLM (`Qwen2.5-1.5B-Instruct`) exhibits severe overconfidence (Brier 0.3910, ECE 48.5%). A simple code-computed scorer based on text overlap (E3) achieves a test Brier score of **0.1119** [0.0805, 0.1457], but its paired bootstrap Brier difference against the oracle test base rate ($0.138$) has a 95% confidence interval spanning zero ($-0.0009$ to $+0.0157$). Similarly, across 5-fold cross-validation on the same folds, E3 achieves Brier $0.1211 \pm 0.0204$ versus the constant prior's $0.1286 \pm 0.0189$.
2. **Discrimination Over Calibration:** While neither code scorers nor hybrid verifiers decisively beat the constant prior on calibration metrics under this sample size, they substantially improve **discrimination** (AUROC). Text-overlap scoring (E3) achieves an AUROC of **0.686** [95% CI: 0.572, 0.784], clearly excluding random chance ($0.500$), while a hybrid judge-code verifier (E4c) reaches an AUROC of **0.728** [0.621, 0.823].
3. **Inconclusive Underpowered RLCR-Style Training:** In contrast to the paper's full-scale implementation (7B/14B parameters, full-weight tuning, group size $G=32$, batch size 2048 tokens on multi-A100 clusters), our localized setup (1.5B, LoRA $r=16$, $G=4$, 15 steps on a single RTX 4070 GPU) showed no reliable learning. In the standard RLVR control, zero policy updates occurred: test outputs were 100% identical to the base model because all $G=4$ rollouts failed on hard multi-hop queries, causing group advantages to collapse to zero ($A_g = 0$) across steps. In RLCR, two of three independent training runs failed to learn non-trivial updates, remaining trapped at base-rate performance.
4. **Insensitivity to Evidence Removal and Scope Limitations:** On unanswerability ablations where gold evidence was removed ($n_{\text{removed}} \in \{0, 1, 2\}$), the base LLM verbalized confidence showed negligible sensitivity ($0.605$ [0.537, 0.674] at $n=0$ vs. $0.626$ [0.557, 0.698] at $n=2$, with completely overlapping confidence intervals). Text-overlap features (E3) are completely blind to missing supporting paragraphs ($\text{AUROC}_{\text{known}} = 0.477$, slightly below chance). Only semantic claim-verification judges (E2c $\text{AUROC}_{\text{known}} = 0.854$, E4c $\text{AUROC}_{\text{known}} = 0.811$) successfully identified missing evidence. E3 relies solely on surface lexical overlap and does not evaluate structured world-model features (such as Knowledge Graph state support or FSM rule margins).

---

## 1. Introduction

Autonomous language agent architectures increasingly rely on self-reported confidence to govern tool execution, retrieval refinement, and human hand-off decisions. However, pre-trained and instruction-tuned language models routinely express unwarranted confidence in erroneous or hallucinated outputs, posing serious reliability concerns.

To address this challenge, Damani et al. (2026) introduced *Reinforcement Learning with Calibration Rewards* (RLCR), optimizing policy models using proper scoring rules (such as Brier score) within Group Relative Policy Optimization (GRPO) to train models to accurately express confidence alongside answers. Concurrently, practitioners frequently employ alternative calibration strategies, including auxiliary sequence classifiers, prompted LLM judges, or lightweight heuristic scoring models based on surface text features.

In this paper, we report empirical observations from a local study designed to understand the practical characteristics of these calibration methods under modest computational constraints (a single 12 GB GPU). We evaluate three independent runs of our pipeline and critically assess the stability, sample efficiency, and limitations of each approach.

### 1.1 Study Scope and Clarifications

To ensure scientific clarity, we define the precise scope of this investigation:
- **Underpowered RL Exploration:** Our RLCR implementation is an exploratory, low-compute study (1.5B parameters, LoRA adaptation, rollout group size $G=4$, 15 gradient steps) and is not a reproduction of Damani et al.'s full-scale regime (7B/14B parameters, full-model weights, $G=32$, batch size 2048, 1–3 epochs on multi-A100 clusters). Our RL results highlight optimization pitfalls under constrained sample sizes rather than evaluating the asymptotic limits of the RLCR objective.
- **Appropriate Baseline Anchor:** Because the test set accuracy prevalence is low (13.8%), all methods must be benchmarked against the constant prior anchor, taking into account the base-rate shift between training ($\bar{y}=0.224$) and testing splits ($\bar{y}=0.138$).
- **Primary Metrics:** With only 21 positive matches on the test set, binned Expected Calibration Error (ECE) is statistically biased and sensitive to binning parameters. We treat Brier score and AUROC as primary metrics, reporting ECE purely as a descriptive statistic.
- **Scope of E3 Features:** The code-computed scorer evaluated here (E3) uses simple lexical overlap, length ratios, format compliance, and token-level containment. It does not incorporate structured world-model or knowledge graph invariants.

---

## 2. Background and Theoretical Formulation

### 2.1 Calibration and Proper Scoring Rules

Let $x \in \mathcal{X}$ denote an input query with retrieved context, $y \in \mathcal{Y}$ the ground truth answer, and $\hat{y} \in \mathcal{Y}$ the model-generated output. Let $c \in [0, 1]$ represent the model's reported probability that $\hat{y} = y$, and let $z = \mathbb{I}(\hat{y} = y) \in \{0, 1\}$ denote binary correctness.

Calibration is measured via the **Brier Score**:
$$\text{Brier} = \frac{1}{N} \sum_{i=1}^N (c_i - z_i)^2$$

For an uninformative baseline predicting a constant probability equal to the dataset prior $\bar{y} = \frac{1}{N}\sum z_i$, the expected in-sample Brier score is $\bar{y}(1 - \bar{y})$. When an out-of-sample predictor applies a training base rate $p_{\text{train}}$ to a test set with base rate $p_{\text{test}}$, the expected Brier score decomposes as:
$$\mathbb{E}[\text{Brier}] = p_{\text{test}}(1 - p_{\text{test}}) + (p_{\text{train}} - p_{\text{test}})^2$$
The second term reflects the base-rate shift penalty. When positive prevalence is low, the constant prior sets a competitive numerical threshold that any meaningful calibration model must surpass.

The **Expected Calibration Error (ECE)** groups predictions into $M$ equal-width bins $B_m \subset [0, 1]$:
$$\text{ECE} = \sum_{m=1}^M \frac{|B_m|}{N} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|$$

Discrimination is assessed using the **Area Under the Receiver Operating Characteristic Curve (AUROC)** for correctness classification, and $\text{AUROC}_{\text{known}}$ for unanswerability detection (classifying whether gold evidence was withheld).

### 2.2 Reinforcement Learning with Calibration Rewards (RLCR)

In standard Reinforcement Learning with Verifiable Rewards (RLVR), the policy receives binary rewards based strictly on correctness:
$$R_{\text{RLVR}}(x, \hat{y}) = z \in \{0, 1\}$$

RLVR penalizes incorrect answers equally regardless of expressed uncertainty, incentivizing verbalized overconfidence. Damani et al. (2026) introduce RLCR, modifying the reward function to penalize miscalibration using the proper Brier scoring rule:
$$R_{\text{RLCR}}(x, \hat{y}, c) = z - (c - z)^2$$

When $z = 1$, $R_{\text{RLCR}} = 1 - (1 - c)^2 = 2c - c^2$, which strictly increases with $c$ and reaches maximum reward $+1.0$ at $c=1.0$. When $z = 0$, $R_{\text{RLCR}} = 0 - c^2 = -c^2$, which penalizes overconfidence and is maximized at $0.0$ when $c=0.0$.

In Damani et al.'s formulation of RLCR:
1. Advantage estimation uses unnormalized group differences: $A_g = R_g - \text{mean}(\{R_j\})$, omitting division by group standard deviation.
2. The policy objective omits the KL divergence penalty term ($\beta = 0$) to allow unconstrained exploration of confidence tokens.

---

## 3. Evaluated Architectures

We examine five distinct calibration architectures:

```
Evaluated Calibration Paradigms:
┌─────────────────────────────────────────────────────────────────────────────┐
│ E0: Prompted Base Agent (Qwen2.5-1.5B-Instruct)                             │
│ Zero-shot prompt requesting reasoning, answer, and confidence tag.          │
└─────────────────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────────────────┐
│ E1: RL Policy Optimization (RLVR vs. RLCR-Style)                            │
│ Qwen2.5-1.5B LoRA policy trained via GRPO on correctness / Brier rewards.   │
└─────────────────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────────────────┐
│ E2: Supervised Neural Sequence Classifier                                   │
│ Qwen2.5-0.5B with a trained linear sequence classification head on [Q,C,A]. │
└─────────────────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────────────────┐
│ E3: Text-Overlap Code Scorer (Convex Logistic Regression)                   │
│ Lexical overlap, length ratio, formatting, containment -> L2 Logistic Reg.  │
└─────────────────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────────────────┐
│ E4: Hybrid Verifier                                                         │
│ Concatenation of prompted judge findings and E3 text-overlap features.     │
└─────────────────────────────────────────────────────────────────────────────┘
```

1. **E0: Constant Prior Anchor:** Non-parametric baseline predicting constant $c = \bar{y} \approx 0.224$ (the empirical training set accuracy).
2. **E0: Prompted Base Agent:** Single LLM (`Qwen2.5-1.5B-Instruct`) prompted zero-shot to output reasoning, an answer inside `<answer>` tags, and confidence inside `<confidence>` tags.
3. **E1: RLVR Policy:** LoRA fine-tuning ($r=16, \alpha=32$) trained on binary accuracy reward ($R \in \{0, 1\}$).
4. **E1: RLCR-Style Policy:** Identical GRPO LoRA configuration trained on Brier calibration reward ($R = z - (c - z)^2$).
5. **E2b: Two-Model Sequence Classifier:** Dedicated `Qwen2.5-0.5B` equipped with a LoRA-adapted linear sequence classification head (`modules_to_save=["score"]`), trained with binary cross-entropy loss over question-context-answer triples.
6. **E2c: Prompted Judge:** Structured LLM prompting simulating claim verification and reporting uncalibrated confidence.
7. **E3: Text-Overlap Code Scorer:** Frozen generator evaluated on deterministic text features (token Jaccard overlap, length ratio, formatting compliance, lexical containment proxy) mapped to probabilities via cross-validated $L_2$ Logistic Regression ($C=1.0$).
8. **E4c: Hybrid Verifier:** Combines prompted judge claim findings with E3 text-overlap features into regularized logistic regression.

---

## 4. Experimental Setup

### 4.1 Datasets and Sample Counts

- **HotpotQA-Modified:** Multi-hop reasoning dataset with distractor paragraphs and controlled evidence removal ($n_{\text{removed}} \in \{0, 1, 2\}$).
  - Training split: $N = 36$ cases (8 positive matches, 28 negative matches; positive prevalence = 22.2%).
  - Calibration split: $N = 100$ cases (17 positive matches, 83 negative matches; positive prevalence = 17.0%).
  - Held-out test split: $N = 152$ cases (21 positive matches, 131 negative matches; positive prevalence = 13.8%).
- **Big-Math-Digits:** Out-of-domain evaluation set of multi-digit arithmetic and modular operations.
  - Test split: $N = 36$ cases (only 2 positive matches, 34 negative matches; positive prevalence = 5.6%).

### 4.2 Training Hyperparameters

- **Hardware:** Single NVIDIA GeForce RTX 4070 (11.99 GB VRAM), Windows 11, PyTorch 2.6.0+cu124.
- **GRPO Configuration:** 15 optimization steps, group rollout size $G=4$, sequence length 512, micro-batch size $N=1$, gradient accumulation steps $= 4$, learning rate $1 \times 10^{-5}$.
- **Sequence Classifier:** 3 epochs, batch size 2, gradient accumulation 2, AdamW, learning rate $5 \times 10^{-5}$.
- **Statistical Resampling:** 1,000 bootstrap resamples on the test set ($N=152$) to establish 95% percentile confidence intervals for all metrics, and 10,000 bootstrap resamples for paired difference tests.

---

## 5. Empirical Results

### 5.1 Comprehensive Benchmark Matrix

Table 1 presents calibration metrics, bootstrap 95% confidence intervals, and Brier lift relative to the E0-Constant Prior anchor on the held-out test split ($N=152$, 21 positives).

**Table 1: Empirical performance on HotpotQA-Modified test split ($N=152$, 21 positives). Brackets denote 95% bootstrap confidence intervals (1,000 resamples). $\Delta\text{Brier}$ indicates lift over the training constant prior ($\text{Brier}_{\text{prior}} - \text{Brier}_{\text{method}}$). ECE is descriptive.**

| Method | Architecture / Strategy | Brier Score [95% CI] | $\Delta\text{Brier}$ (Lift) | ECE [95% CI] | AUROC [95% CI] | $\text{AUROC}_{\text{known}}$ |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **E0: Constant Prior (Train Rate)** | Prior Anchor ($\bar{y}_{\text{train}}=0.224$) | 0.1264 [0.0974, 0.1591] | +0.0000 (Anchor) | 8.6% [2.7%, 13.8%] | 0.500 [0.500, 0.500] | 0.500 |
| *E0: Constant Prior (Test Oracle)* | Oracle Base Rate ($\bar{y}_{\text{test}}=0.138$) | 0.1191 [0.0898, 0.1502] | +0.0073 | 0.0% [0.0%, 0.0%] | 0.500 [0.500, 0.500] | 0.500 |
| **E0: Prompted Base LLM** | 1 LLM (`Qwen2.5-1.5B`) | 0.3910 [0.3499, 0.4389] | -0.2646 | 48.5% [42.5%, 54.6%] | 0.505 [0.383, 0.624] | 0.513 |
| **E1: RLVR (Underpowered)** | 1 LLM (RL-Trained) | *No policy update* | *Zero gradient* | *Identical to base* | 0.505 [0.383, 0.624] | 0.513 |
| **E1: RLCR-Style (Run 1)** | 1 LLM (Brier Reward) | 0.3586 [0.3154, 0.4008] | -0.2322 | 46.7% [40.8%, 52.1%] | 0.635 [0.513, 0.744] | 0.511 |
| **E2b: 0.5B Sequence Classifier**| 2 LLMs (Trained 0.5B Head) | 0.1775 [0.1264, 0.2346] | -0.0511 | 16.6% [11.9%, 23.8%] | 0.524 [0.383, 0.656] | 0.470 |
| **E2c: Prompted Judge (Raw)** | 2 LLMs (Zero-Shot) | 0.2082 [0.1679, 0.2520] | -0.0818 | 24.6% [18.4%, 30.3%] | 0.619 [0.514, 0.724] | **0.854** |
| **E3: Text-Overlap Scorer** | 1 LLM + Overlap LR | 0.1119 [0.0805, 0.1457] | +0.0145 | 3.0% [1.9%, 8.7%] | **0.686 [0.572, 0.784]** | 0.477 |
| **E4c: Hybrid (Judge + Overlap)**| 2 LLMs + Hybrid LR | 0.1098 [0.0794, 0.1436] | +0.0166 | 2.6% [2.1%, 8.7%] | **0.728 [0.621, 0.823]** | **0.811** |

```
Brier Score Comparison (Lower is Better; Training Prior = 0.1264, Test Oracle = 0.1191):
E0 Base LLM:      ████████████████████████████████████████ 0.3910
E1 RLCR (Run 1):  ████████████████████████████████████ 0.3586
E2c Judge:        █████████████████████ 0.2082
E2b 0.5B Head:    █████████████████ 0.1775
E0 Train Prior:   █████████████ 0.1264  [TRAINING BASE-RATE ANCHOR]
E0 Test Oracle:   ████████████  0.1191  [ORACLE IN-SAMPLE ANCHOR]
E3 Text Overlap:  ███████████   0.1119  (AUROC: 0.686)
E4c Hybrid:       ███████████   0.1098  (AUROC: 0.728)
```

### 5.2 Critical Analysis of Findings

#### A. Does E3 Decisively Beat the Constant Prior?
When evaluated against the out-of-sample training prior ($c=0.224$), E3 achieves a paired Brier difference of $+0.0146$ [95% CI: $+0.0096, +0.0188$]. However, this apparent advantage largely stems from the **train-to-test base-rate shift** ($22.4\% \to 13.8\%$), which penalizes the training prior by $(0.224 - 0.138)^2 \approx 0.0074$. 

When compared against the oracle test-set base rate ($0.138$), E3's paired Brier difference is $+0.0072$, and its 95% bootstrap confidence interval spans **$-0.0009$ to $+0.0157$**, crossing zero. Similarly, across 5-fold cross-validation on the same folds (Section 6), E3 achieves a mean Brier of $0.1211 \pm 0.0204$ versus the constant prior's $0.1286 \pm 0.0189$, with a mean paired difference of $+0.0076 \pm 0.0053$ (and on Fold 4, E3 was slightly worse than the constant prior, $0.1373$ vs. $0.1345$). 

Therefore, **we do not claim that E3 decisively improves calibration over a well-calibrated constant prior**. What the data robustly supports is that E3 provides meaningful **discrimination** (AUROC 0.686 [0.572, 0.784], clearly excluding random chance 0.500).

#### B. Clarification of Supervised Classifier (E2b) Performance
In an earlier draft summary of these experiments, E2b was temporarily reported as having Brier 0.1258 and AUROC 0.500 with zero CI width. That anomaly occurred because a dictionary lookup fallback defaulted all test predictions to a constant 0.22 when test IDs were mismatched. Restoring the genuine saved predictions from disk (`results/e2_trained_predictions.json`) confirms that the trained 0.5B classifier achieved Brier **0.1775** [0.1264, 0.2346] and AUROC **0.524** [0.383, 0.656]. Because the sequence classifier was fine-tuned on a tiny training set ($N=36$), it struggled to generalize, performing substantially worse than the constant prior.

#### C. Inconclusive Nature of Underpowered RLCR-Style Runs
Our low-compute RL experiments highlight serious sample-efficiency bottlenecks:
- In the standard RLVR control, all 152 test outputs and verbalized confidence scores were 100% identical to the base model. Because base model accuracy was low (~19%), group rollouts of size $G=4$ rarely produced at least one correct answer. When all $G=4$ completions scored zero, the group advantage $A_g = \frac{R_g - \text{mean}}{\text{std}}$ collapsed to zero, providing zero gradient updates across 15 steps. We mark RLVR in Table 1 as *No policy update* rather than a substantive empirical result.
- In RLCR, only one of three runs (Run 1) demonstrated an increase in correctness discrimination (AUROC 0.635). In Runs 2 and 3, rollouts failed to discover reward-improving trajectories, leaving the policy at base-rate performance.
- We conclude that RLCR cannot be reliably studied under such low sample budgets ($G=4$, 15 steps); robust policy learning requires the large rollout batches ($G \ge 32$) and extended optimization schedules employed by Damani et al.

---

## 6. Resampled Cross-Validation Variance

To measure actual empirical variance across data partitions, we performed 5-fold cross-validation across all 252 available HotpotQA items, comparing E3 and the constant prior on the exact same folds.

**Table 2: 5-Fold cross-validation comparison on identical data folds ($N=252$).**

| Fold | Constant Prior Brier | Text-Overlap (E3) Brier | Paired Difference ($\text{Brier}_{\text{prior}} - \text{Brier}_{\text{E3}}$) | E3 AUROC |
|:---:|:---:|:---:|:---:|:---:|
| **Fold 1** | 0.1323 | 0.1211 | +0.0112 | 0.724 |
| **Fold 2** | 0.0928 | 0.0824 | +0.0104 | 0.758 |
| **Fold 3** | 0.1345 | 0.1264 | +0.0081 | 0.612 |
| **Fold 4** | 0.1345 | 0.1373 | -0.0028 | 0.589 |
| **Fold 5** | 0.1489 | 0.1381 | +0.0108 | 0.651 |
| **Mean $\pm \sigma$** | **0.1286 $\pm$ 0.0189** | **0.1211 $\pm$ 0.0204** | **+0.0076 $\pm$ 0.0053** | **0.667 $\pm$ 0.088** |

Across data splits, E3 exhibits standard deviation of $\sigma_{\text{Brier}} = 0.0204$ and $\sigma_{\text{AUROC}} = 0.088$, illustrating normal empirical variability. On Fold 4, E3 was slightly worse than the constant prior.

---

## 7. Evidence Removal and Insensitivity to Information Withholding

To evaluate whether models recognize when required supporting evidence has been omitted, we analyzed verbalized confidence as gold paragraphs were ablated ($n_{\text{removed}} \in \{0, 1, 2\}$).

**Table 3: Verbalized confidence under controlled evidence ablation.**

| Evidence Condition | Sample Count | Base LLM (E0) Mean [95% CI] | Text-Overlap (E3) Mean [95% CI] | Hybrid Verifier (E4c) Mean [95% CI] |
|:---|:---:|:---:|:---:|:---:|
| $n_{\text{removed}} = 0$ (Supported) | $N = 48$ | 0.605 [0.537, 0.674] | 0.176 [0.155, 0.198] | 0.227 [0.185, 0.272] |
| $n_{\text{removed}} = 1$ (Partial) | $N = 61$ | 0.587 [0.534, 0.639] | 0.167 [0.152, 0.182] | 0.137 [0.118, 0.158] |
| $n_{\text{removed}} = 2$ (Unanswerable) | $N = 43$ | 0.626 [0.557, 0.698] | 0.161 [0.147, 0.175] | **0.134 [0.115, 0.154]** |
| $\text{AUROC}_{\text{known}}$ | — | 0.513 | 0.477 (Below Chance) | **0.811** |

### 7.1 Insensitivity, Not Significant Inversion
The apparent shift in base LLM confidence from $0.605$ ($n=0$) to $0.626$ ($n=2$) represents an absolute difference of only $0.021$. Because the 95% bootstrap confidence intervals overlap completely ([0.537, 0.674] vs. [0.557, 0.698]), this difference is statistically indistinguishable from zero. Rather than exhibiting an active "confidence inversion", the base LLM is simply **insensitive to evidence omission**: it expresses high confidence (~60%) regardless of whether the retrieved context contains the necessary facts.

### 7.2 Blindness of Text-Overlap Features to Missing Evidence
Crucially, the text-overlap scorer (E3) yields an $\text{AUROC}_{\text{known}}$ of **0.477**, which is slightly below random chance (0.500). Because E3 measures whether the candidate answer string appears anywhere in the prompt text, it cannot detect that a required second-hop supporting premise is absent. Only judge-based architectures (E2c $\text{AUROC}_{\text{known}} = 0.854$, E4c $\text{AUROC}_{\text{known}} = 0.811$) successfully identify missing supporting premises through semantic verification.

---

## 8. Out-of-Domain Evaluation: Big-Math-Digits Limitations

We evaluated out-of-domain transfer on an exploratory subset of Big-Math-Digits ($N=36$ arithmetic cases).

**Table 4: Evaluation on Big-Math-Digits ($N=36$, 2 positives).**

| Method | Brier Score [95% CI] | ECE [95% CI] | AUROC [95% CI] | Statistical Validity |
|:---|:---:|:---:|:---:|:---|
| **E0: Prompted Base Agent** | 0.0577 [0.0078, 0.1250] | 3.5% [1.0%, 8.5%] | 0.500 [0.500, 0.500] | Insufficient Positives ($N_{\text{pos}}=2$) |
| **E3: Text-Overlap Scorer** | 0.0511 [0.0068, 0.1127] | 2.1% [1.7%, 10.0%] | 0.779 [0.500, 0.864] | Wide CI; Inconclusive |
| **E4c: Hybrid Verifier** | 0.0504 [0.0055, 0.1112] | 0.7% [0.5%, 8.2%] | 0.853 [0.500, 0.941] | Wide CI; Inconclusive |

With only **2 positive correct answers** among 36 test cases, the 95% confidence intervals for AUROC span from random chance (0.500) to 0.941. Consequently, **we explicitly retract previous claims of "exceptional 0.853 AUROC transfer"**. Reliable evaluation of out-of-domain transfer requires larger evaluation sets with at least 30 to 50 positive instances.

---

## 9. Failure Case Taxonomy (Extreme Overconfident Tail)

To characterize model miscalibration, we examined the **top 30 most confident incorrect predictions under the E0 baseline** (the tail cases with the largest individual Brier loss $(c_i - 0)^2$). These 30 cases describe the failure modes of the extreme overconfident tail, not the overall distribution across all errors:

1. **Insensitivity to Missing Supporting Facts (14/30 tail cases):** In multi-hop questions where gold paragraphs were ablated ($n_{\text{removed}} > 0$), the model fabricated plausible reasoning paths connecting unrelated entities and assigned confidence exceeding 85%.
2. **Surface Lexical Overlap Traps (10/30 tail cases):** The candidate answer contained exact lexical substrings from distractor paragraphs (e.g., matching a location or date mentioned in an unrelated context), leading both the base LLM and E3 to assign falsely elevated confidence.
3. **Paraphrase Penalties (6/30 tail cases):** The model produced semantically valid answers using synonyms not present in the text (e.g., "physician" for "doctor"), leading text-overlap features to predict near-zero probability.

---

## 10. Scope and Limitations of Text-Overlap Features

It is important to emphasize that E3 is strictly a **lexical text-overlap baseline**:
- It evaluates word-level Jaccard overlap, length ratios, formatting tags, and token containment.
- It **does not test world-model verification**, such as Knowledge Graph (KG) path support, Finite State Machine (FSM) state validity, or missing fact share from structured schemas.
- Future work should evaluate whether incorporating formal world-model constraints can resolve E3's failure on unanswerable multi-hop questions ($\text{AUROC}_{\text{known}} = 0.477$).

---

## 11. Conclusion

This exploratory study provides an empirical comparison of uncertainty calibration methods under modest computational resources:
1. When positive prevalence is low (13.8%), the non-parametric constant prior provides a formidable baseline (Brier 0.1264 considering base-rate shift, 0.1191 test oracle). Text-overlap scorers do not decisively beat the constant prior on Brier score (paired difference 95% CI spans zero), but they provide genuine **discrimination** (E3 AUROC 0.686 [0.572, 0.784], E4c AUROC 0.728 [0.621, 0.823]).
2. Under low compute ($G=4$, 15 steps), RLCR-style training suffers from zero-advantage collapse, resulting in no policy updates for RLVR and inconclusive outcomes for RLCR.
3. Zero-shot LLMs exhibit insensitivity to evidence omission rather than statistically significant inversion, and pure text-overlap features are blind to missing supporting premises ($\text{AUROC}_{\text{known}} = 0.477$). Only semantic claim judges successfully detect withheld evidence.

We recommend that practical calibration pipelines combine lightweight semantic claim verification with formal paired confidence intervals and explicit baseline lift reporting.

---

## References

- Mehul Damani, et al. *Beyond Binary Rewards: Training Language Models to Reason About Their Uncertainty with Calibration Rewards*. ICLR 2026.
- Glenn W. Brier. *Verification of forecasts expressed in terms of probability*. Monthly Weather Review, 78(1):1–3, 1950.
- Saurav Kadavath, et al. *Language Models (Mostly) Know What They Know*. arXiv:2207.05221, 2022.
- Zhilin Yang, et al. *HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering*. EMNLP 2018.
- Jacob Devlin, et al. *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL 2019.
- Lianmin Zheng, et al. *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. NeurIPS 2023.
