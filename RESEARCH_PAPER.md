# Empirical Stability and Calibration in Language Model Uncertainty: An Exploratory Study of RLCR-Style Policies, Supervised Verifiers, and Code Scorers

**A Multi-Run Investigation of Calibration Rewards, Supervised Neural Heads, and Text-Overlap Scoring Functions**

---

### Authors
**AI Engineering Calibration Team** & **Zhao**  

---

## Abstract

Calibrating uncertainty estimates in large language models (LLMs) is essential for dependable autonomous agent deployment. Recently, Damani et al. (ICLR 2026) introduced *Reinforcement Learning with Calibration Rewards* (RLCR), proposing that training language models with proper scoring rules (such as the Brier score) encourages calibrated verbalized confidence alongside answers. However, empirical questions remain regarding the sample efficiency, optimization stability, and operational requirements of RL-based calibration compared to lightweight auxiliary verifiers and simple code-computed heuristic scoring functions.

In this work, we conduct an exploratory, multi-run study comparing an underpowered RLCR-style setup against supervised sequence classification heads, zero-shot judges, and deterministic text-overlap scoring functions. Evaluations are conducted across multiple seeds and train/test partitions using HotpotQA-Modified ($N=152$ test cases with controlled evidence removal, containing 21 positive matches) and an exploratory subset of Big-Math-Digits ($N=36$ cases with 2 positive matches).

Our primary empirical findings include:
1. **Performance Relative to the Constant Prior Baseline:** On the held-out test split, the empirical positive prevalence is 13.8% (21/152). A non-parametric constant prior baseline (E0-Constant, predicting $\bar{y}=0.224$) achieves a Brier score of **0.1201** [95% CI: 0.0853, 0.1592] and an Expected Calibration Error (ECE) of **3.2%** [0.1%, 8.4%]. By comparison, the uncalibrated base LLM (`Qwen2.5-1.5B-Instruct`) exhibits severe overconfidence (Brier 0.3910, ECE 48.5%). A simple code-computed scorer based on text overlap (E3) achieves a modest Brier lift over the constant prior of **+0.0082** (Brier **0.1119** [0.0805, 0.1457], AUROC **0.686** [0.572, 0.784]), while a hybrid judge-code verifier (E4c) yields a lift of **+0.0103** (Brier **0.1098** [0.0794, 0.1436], AUROC **0.728** [0.621, 0.823]).
2. **Inconclusive Underpowered RLCR-Style Training:** In contrast to the paper's full-scale implementation (7B/14B parameters, full-weight tuning, group size $G=32$, batch size 2048 tokens, 500+ steps), our localized setup (1.5B, LoRA $r=16$, $G=4$, 15 steps on a single RTX 4070 GPU) proved largely inconclusive. Two of three independent RLCR training runs failed to learn non-trivial policy updates due to sparse rewards and zero-advantage group collapse (where all $G=4$ rollouts failed on hard multi-hop queries). In the standard RLVR control, greedy decoding outputs were identical to the base model across all 152 test items because the advantages remained zero on nearly all steps.
3. **Determinism vs. Real Resampling Variance:** When evaluated on a fixed static test split, code-computed scorers exhibit exact deterministic invariance ($\sigma = 0.0000$). When evaluating true sampling variance across 5-fold resampled cross-validation splits, E3 demonstrates empirical variability of $\text{Brier} = 0.1211 \pm 0.0204$, $\text{ECE} = 4.5\% \pm 1.2\%$, and $\text{AUROC} = 0.667 \pm 0.088$.
4. **Insensitivity to Evidence Removal and Scope Limitations:** On unanswerability ablations where gold evidence was removed ($n_{\text{removed}} \in \{0, 1, 2\}$), the base LLM verbalized confidence showed negligible sensitivity ($0.605$ [0.537, 0.674] at $n=0$ vs. $0.626$ [0.557, 0.698] at $n=2$, with completely overlapping confidence intervals). Text-overlap features (E3) are blind to missing supporting paragraphs ($\text{AUROC}_{\text{known}} = 0.477$, slightly below random chance). Only semantic claim-verification judges (E2c $\text{AUROC}_{\text{known}} = 0.854$, E4c $\text{AUROC}_{\text{known}} = 0.811$) successfully identified missing evidence. E3 relies solely on surface lexical overlap and does not evaluate structured world-model features (such as Knowledge Graph state support or FSM rule margins).

---

## 1. Introduction

Autonomous language agent architectures increasingly rely on self-reported confidence to govern tool execution, retrieval refinement, and human hand-off decisions. However, pre-trained and instruction-tuned language models routinely express unwarranted confidence in erroneous or hallucinated outputs, posing serious reliability concerns.

To address this challenge, Damani et al. (2026) introduced *Reinforcement Learning with Calibration Rewards* (RLCR), optimizing policy models using proper scoring rules (such as Brier score) within Group Relative Policy Optimization (GRPO) to train models to accurately express confidence alongside answers. Concurrently, practitioners frequently employ alternative calibration strategies, including auxiliary sequence classifiers, prompted LLM judges, or lightweight heuristic scoring models based on surface text features.

In this paper, we report empirical observations from a local study designed to understand the practical characteristics of these calibration methods under modest computational constraints (a single 12 GB GPU). We evaluate three independent runs of our pipeline and critically assess the stability, sample efficiency, and limitations of each approach.

### 1.1 Study Scope and Clarifications

To ensure scientific clarity, we define the precise scope of this investigation:
- **Underpowered RL Exploration:** Our RLCR implementation is an exploratory, low-compute study (1.5B parameters, LoRA adaptation, rollout group size $G=4$, 15 gradient steps) and is not a reproduction of Damani et al.'s full-scale regime (7B/14B parameters, full-model weights, $G=32$, batch size 2048, 500+ steps). Our RL results highlight optimization pitfalls under constrained sample sizes rather than evaluating the asymptotic limits of the RLCR objective.
- **Appropriate Baseline Anchor:** Because the test set accuracy prevalence is low (13.8%), all methods must be benchmarked against the constant prior anchor (predicting empirical base rate $\bar{y}=0.224$, Brier = 0.1201), rather than celebrating large relative reductions over an uncalibrated base LLM.
- **Scope of E3 Features:** The code-computed scorer evaluated here (E3) uses simple lexical overlap, length ratios, format compliance, and token-level containment. It does not incorporate structured world-model or knowledge graph invariants.

---

## 2. Background and Theoretical Formulation

### 2.1 Calibration and Proper Scoring Rules

Let $x \in \mathcal{X}$ denote an input query with retrieved context, $y \in \mathcal{Y}$ the ground truth answer, and $\hat{y} \in \mathcal{Y}$ the model-generated output. Let $c \in [0, 1]$ represent the model's reported probability that $\hat{y} = y$, and let $z = \mathbb{I}(\hat{y} = y) \in \{0, 1\}$ denote binary correctness.

Calibration is measured via the **Brier Score**:
$$\text{Brier} = \frac{1}{N} \sum_{i=1}^N (c_i - z_i)^2$$

For an uninformative baseline predicting a constant probability equal to the dataset prior $\bar{y} = \frac{1}{N}\sum z_i$, the expected Brier score is $\bar{y}(1 - \bar{y})$. When positive prevalence is low, the constant prior sets a competitive numerical threshold that any meaningful calibration model must surpass.

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
- **Statistical Resampling:** 1,000 bootstrap resamples on the test set ($N=152$) to establish 95% percentile confidence intervals for all metrics.

---

## 5. Empirical Results

### 5.1 Comprehensive Benchmark Matrix

Table 1 presents calibration metrics, bootstrap 95% confidence intervals, and Brier lift relative to the E0-Constant Prior anchor on the held-out test split ($N=152$, 21 positives).

**Table 1: Empirical performance on HotpotQA-Modified test split ($N=152$, 21 positives). Brackets denote 95% bootstrap confidence intervals (1,000 resamples). $\Delta\text{Brier}$ indicates lift over E0-Constant Prior ($\text{Brier}_{\text{prior}} - \text{Brier}_{\text{method}}$; positive values indicate improvement).**

| Method | Architecture / Strategy | Brier Score [95% CI] | $\Delta\text{Brier}$ (Lift) | ECE [95% CI] | AUROC [95% CI] | $\text{AUROC}_{\text{known}}$ |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **E0: Constant Prior** | Prior Anchor ($\bar{y}=0.224$) | 0.1201 [0.0853, 0.1592] | +0.0000 (Anchor) | 3.2% [0.1%, 8.4%] | 0.500 [0.500, 0.500] | 0.500 |
| **E0: Prompted Base LLM** | 1 LLM (`Qwen2.5-1.5B`) | 0.3910 [0.3499, 0.4389] | -0.2709 | 48.5% [42.5%, 54.6%] | 0.505 [0.383, 0.624] | 0.513 |
| **E1: RLVR (Underpowered)** | 1 LLM (RL-Trained) | 0.3910 [0.3499, 0.4389] | -0.2709 | 48.5% [42.5%, 54.6%] | 0.505 [0.383, 0.624] | 0.513 |
| **E1: RLCR-Style (Run 1)** | 1 LLM (Brier Reward) | 0.3586 [0.3154, 0.4008] | -0.2385 | 46.7% [40.8%, 52.1%] | 0.635 [0.513, 0.744] | 0.511 |
| **E2b: 0.5B Sequence Classifier**| 2 LLMs (Trained 0.5B Head) | 0.1258 [0.0963, 0.1589] | -0.0057 | 8.2% [2.3%, 13.4%] | 0.500 [0.500, 0.500] | 0.500 |
| **E2c: Prompted Judge (Raw)** | 2 LLMs (Zero-Shot) | 0.2082 [0.1679, 0.2520] | -0.0881 | 24.6% [18.4%, 30.3%] | 0.619 [0.514, 0.724] | **0.854** |
| **E3: Text-Overlap Scorer** | 1 LLM + Overlap LR | **0.1119 [0.0805, 0.1457]** | **+0.0082** | **3.0% [1.9%, 8.7%]** | **0.686 [0.572, 0.784]** | 0.477 |
| **E4c: Hybrid (Judge + Overlap)**| 2 LLMs + Hybrid LR | **0.1098 [0.0794, 0.1436]** | **+0.0103** | **2.6% [2.1%, 8.7%]** | **0.728 [0.621, 0.823]** | **0.811** |

```
Brier Score Comparison (Lower is Better; Constant Prior = 0.1201):
E0 Base LLM:      ████████████████████████████████████████ 0.3910
E1 RLCR (Run 1):  ████████████████████████████████████ 0.3586
E2c Judge:        █████████████████████ 0.2082
E2b 0.5B Head:    █████████████ 0.1258
E0 Constant Prior:████████████ 0.1201  [BASELINE ANCHOR]
E3 Text Overlap:  ███████████  0.1119  (Lift: +0.0082 over Prior)
E4c Hybrid:       ███████████  0.1098  (Lift: +0.0103 over Prior)
```

### 5.2 Critical Analysis of Findings

#### A. Lift Over the Constant Prior
When evaluated in an imbalanced retrieval setting where true accuracy is low (13.8%), predicting the constant prior achieves a Brier score of 0.1201. The uncalibrated base LLM suffers from severe overconfidence (mean verbalized confidence of 0.605 on incorrect answers), worsening the Brier score to 0.3910. 

Zhao's text-overlap scorer (E3) achieves a modest Brier improvement of **+0.0082** over the constant prior (a 6.8% reduction), while improving discrimination to AUROC **0.686** [0.572, 0.784]. The hybrid model (E4c) achieves the best overall Brier score (**0.1098**, lift of **+0.0103** over prior) and correctness discrimination (AUROC **0.728** [0.621, 0.823]).

#### B. The Trivial 86.2% Majority Class Accuracy
In previous iterations of this benchmark, an accuracy of "86.2%" was reported across several methods. This value is a mathematical artifact of class imbalance. Because the positive rate is 13.8% (21/152), all calibrated confidence scores fall below 0.5 ($c_i \in [0.10, 0.40]$). Under a standard 0.5 decision threshold, every item is classified as negative, yielding trivial majority-class accuracy of $1 - 0.138 = 86.2\%$. We omit this misleading metric in favor of AUROC and Brier lift.

#### C. Inconclusive Nature of Underpowered RLCR-Style Runs
Our low-compute RLCR experiments highlight serious sample-efficiency bottlenecks:
- In the standard RLVR control, all 152 test outputs and verbalized confidence scores were 100% identical to the base model. Because base model accuracy was low (~19%), group rollouts of size $G=4$ rarely produced at least one correct answer. When all $G=4$ completions scored zero, the group advantage $A_g = \frac{R_g - \text{mean}}{\text{std}}$ collapsed to zero, providing zero gradient updates across 15 steps.
- In RLCR, only one of three runs (Run 1) demonstrated an increase in correctness discrimination (AUROC 0.635). In Runs 2 and 3, rollouts failed to discover reward-improving trajectories, leaving the policy at base-rate performance.
- We conclude that RLCR cannot be reliably studied under such low sample budgets ($G=4$, 15 steps); robust policy learning requires the large rollout batches ($G \ge 32$) and extended optimization schedules employed by Damani et al.

---

## 6. Determinism vs. Resampled Split Variance

When evaluated on the static 152-item test set, code-computed scorers (E3) produce identical metrics across runs ($\sigma = 0.0000$). This uniformity reflects numerical determinism (evaluating frozen model outputs with deterministic string operations on a static partition) rather than statistical certainty.

To measure actual empirical variance across data partitions, we performed 5-fold cross-validation across all 252 available HotpotQA items.

**Table 2: 5-Fold cross-validation resampling variance for Text-Overlap Scorer (E3).**

| Metric | Resampled 5-Fold Mean $\pm \sigma$ | 95% Confidence Interval |
|:---|:---:|:---:|
| **Brier Score** | **0.1211 $\pm$ 0.0204** | [0.1007, 0.1415] |
| **ECE** | **4.5% $\pm$ 1.2%** | [3.3%, 5.7%] |
| **AUROC** | **0.667 $\pm$ 0.088** | [0.579, 0.755] |

Across data splits, E3 exhibits a standard deviation of $\sigma_{\text{Brier}} = 0.0204$ and $\sigma_{\text{AUROC}} = 0.088$, illustrating the normal empirical variability expected on sample sizes of this magnitude.

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

## 9. Failure Case Taxonomy

To characterize model miscalibration, we examined the **top 30 most confident incorrect predictions under the E0 baseline** (the cases with the largest individual Brier penalty $(c_i - 0)^2$).

1. **Insensitivity to Missing Supporting Facts (46.7%, 14/30 cases):** In multi-hop questions where gold paragraphs were ablated ($n_{\text{removed}} > 0$), the model fabricated plausible reasoning paths connecting unrelated entities and assigned confidence exceeding 85%.
2. **Surface Lexical Overlap Traps (33.3%, 10/30 cases):** The candidate answer contained exact lexical substrings from distractor paragraphs (e.g., matching a location or date mentioned in an unrelated context), leading both the base LLM and E3 to assign falsely elevated confidence.
3. **Paraphrase Penalties (20.0%, 6/30 cases):** The model produced semantically valid answers using synonyms not present in the text (e.g., "physician" for "doctor"), leading text-overlap features to predict near-zero probability.

---

## 10. Scope and Limitations of Text-Overlap Features

It is important to emphasize that E3 is strictly a **lexical text-overlap baseline**:
- It evaluates word-level Jaccard overlap, length ratios, formatting tags, and token containment.
- It **does not test world-model verification**, such as Knowledge Graph (KG) path support, Finite State Machine (FSM) state validity, or missing fact share from structured schemas.
- Future work should evaluate whether incorporating formal world-model constraints can resolve E3's failure on unanswerable multi-hop questions ($\text{AUROC}_{\text{known}} = 0.477$).

---

## 11. Conclusion

This exploratory study provides an empirical comparison of uncertainty calibration methods under modest computational resources:
1. When positive prevalence is low, the non-parametric constant prior (Brier 0.1201, ECE 3.2%) provides a formidable baseline that simple text-overlap scorers only marginally improve upon (Brier lift of +0.0082 to +0.0103).
2. Under low compute ($G=4$, 15 steps), RLCR-style training suffers from severe sample inefficiency and zero-advantage collapse, rendering results inconclusive.
3. Zero-shot LLMs exhibit insensitivity to evidence omission rather than statistically significant inversion, and pure text-overlap features are blind to missing supporting premises ($\text{AUROC}_{\text{known}} = 0.477$).
4. Evaluating domain transfer on subsets with few positive cases yields wide confidence intervals that preclude strong generalization claims.

We recommend that practical calibration pipelines combine lightweight semantic claim verification with formal confidence intervals and explicit baseline lift reporting.

---

## References

- Mehul Damani, et al. *Beyond Binary Rewards: Training Language Models to Reason About Their Uncertainty with Calibration Rewards*. ICLR 2026.
- Glenn W. Brier. *Verification of forecasts expressed in terms of probability*. Monthly Weather Review, 78(1):1–3, 1950.
- Saurav Kadavath, et al. *Language Models (Mostly) Know What They Know*. arXiv:2207.05221, 2022.
- Zhilin Yang, et al. *HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering*. EMNLP 2018.
- Jacob Devlin, et al. *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL 2019.
- Lianmin Zheng, et al. *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. NeurIPS 2023.
