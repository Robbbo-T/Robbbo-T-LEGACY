#!/usr/bin/env python3
import numpy as np

def compute_learning_efficiency(optimal, actual):
    """
    optimal/actual: equal-length sequences of positive KPI (higher better) or
    cost (lower better) already transformed so 'higher is better'.
    Returns [0..1], using exponentially-weighted regret (recent decisions matter more).
    """
    optimal = np.array(optimal, dtype=float)
    actual  = np.array(actual,  dtype=float)
    eps = 1e-9
    regrets = np.clip((optimal - actual) / np.maximum(optimal, eps), 0.0, 1.0)
    w = np.exp(np.linspace(-2.0, 0.0, len(regrets)))     # heavier weight for recent
    w /= (w.sum() + eps)
    weighted_regret = float((regrets * w).sum())
    return float(np.clip(1.0 - weighted_regret, 0.0, 1.0))