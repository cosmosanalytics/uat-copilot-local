import os
import json
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from src.eval.metrics import evaluate_all_metrics

class E3Scorer:
    def __init__(self, feature_names: List[str]):
        self.feature_names = feature_names
        self.model_correct = None
        self.model_known = None
        self.single_feature_model = None
        self.best_c = 1.0

    def fit(self, X: np.ndarray, y_correct: np.ndarray, y_known: Optional[np.ndarray] = None):
        """Fits L2 regularized Logistic Regression with cross-validation for C."""
        if len(np.unique(y_correct)) < 2:
            self.constant_prob = max(0.01, float(np.mean(y_correct)))
            self.model_correct = None
            self.single_feature_model = None
            return

        C_candidates = [0.01, 0.1, 1.0, 10.0, 100.0]
        best_score = -1.0
        best_c = 1.0
        
        # 5-fold CV
        n_pos = int(np.sum(y_correct == 1))
        n_neg = int(np.sum(y_correct == 0))
        n_splits = min(5, min(n_pos, n_neg))
        if n_splits >= 2:
            skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
            for c in C_candidates:
                scores = []
                for train_idx, val_idx in skf.split(X, y_correct):
                    if len(np.unique(y_correct[train_idx])) < 2:
                        continue
                    clf = LogisticRegression(C=c, penalty='l2', solver='lbfgs', max_iter=1000)
                    clf.fit(X[train_idx], y_correct[train_idx])
                    # Evaluate negative Brier (higher is better)
                    probs = clf.predict_proba(X[val_idx])[:, 1]
                    brier = -np.mean((probs - y_correct[val_idx]) ** 2)
                    scores.append(brier)
                if scores:
                    mean_sc = np.mean(scores)
                    if mean_sc > best_score:
                        best_score = mean_sc
                        best_c = c
        else:
            best_c = 1.0
            
        self.best_c = best_c
        self.model_correct = LogisticRegression(C=best_c, penalty='l2', solver='lbfgs', max_iter=1000)
        self.model_correct.fit(X, y_correct)
        
        # Single-feature Platt scaling on first feature (e.g. answer_in_context or self_consistency)
        self.single_feature_model = LogisticRegression(C=1.0, max_iter=1000)
        self.single_feature_model.fit(X[:, :1], y_correct)
        
        # Head for known/unknown if provided
        if y_known is not None and len(np.unique(y_known)) > 1:
            self.model_known = LogisticRegression(C=best_c, penalty='l2', solver='lbfgs', max_iter=1000)
            self.model_known.fit(X, y_known)

    def predict_proba_correct(self, X: np.ndarray) -> np.ndarray:
        if self.model_correct is None:
            return np.full(len(X), getattr(self, "constant_prob", 0.05))
        return self.model_correct.predict_proba(X)[:, 1]

    def predict_proba_known(self, X: np.ndarray) -> Optional[np.ndarray]:
        if self.model_known is not None:
            return self.model_known.predict_proba(X)[:, 1]
        return None

    def predict_single_feature(self, X: np.ndarray) -> np.ndarray:
        if self.single_feature_model is None:
            return np.full(len(X), getattr(self, "constant_prob", 0.05))
        return self.single_feature_model.predict_proba(X[:, :1])[:, 1]

    def get_coefficients(self) -> Dict[str, float]:
        coefs = {}
        if self.model_correct is not None:
            for name, w in zip(self.feature_names, self.model_correct.coef_[0]):
                coefs[name] = float(w)
            coefs["intercept"] = float(self.model_correct.intercept_[0])
        return coefs
