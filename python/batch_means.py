"""Batch means method for statistical analysis."""

from __future__ import annotations

import math
from typing import List, Tuple


def calculate_batch_statistics(
    response_times: List[float], num_batches: int, batch_size: int
) -> Tuple[List[float], List[float]]:
    """
    Calculate batch means and batch 95th percentiles.
    
    Args:
        response_times: List of response times
        num_batches: Number of batches (m)
        batch_size: Size of each batch (b)
    
    Returns:
        Tuple of (batch_means, batch_percentiles)
    """
    batch_means: List[float] = []
    batch_percentiles: List[float] = []
    
    total_needed = num_batches * batch_size
    if len(response_times) < total_needed:
        raise ValueError(
            f"Not enough data: need {total_needed}, have {len(response_times)}"
        )
    
    data = response_times[:total_needed]
    
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = start_idx + batch_size
        batch = data[start_idx:end_idx]
        
        batch_mean = sum(batch) / len(batch)
        batch_means.append(batch_mean)
        
        sorted_batch = sorted(batch)
        n = len(sorted_batch)
        percentile_pos = int(math.ceil(n * 0.95))
        percentile_idx = min(percentile_pos - 1, n - 1)
        batch_percentile = sorted_batch[percentile_idx]
        batch_percentiles.append(batch_percentile)
    
    return batch_means, batch_percentiles


def calculate_statistics_with_ci(
    response_times: List[float],
    num_batches: int,
    batch_size: int,
    confidence_level: float = 0.95,
) -> dict:
    """
    Calculate mean, 95th percentile, and their confidence intervals using batch means.
    
    Args:
        response_times: List of response times
        num_batches: Total number of batches (m)
        batch_size: Size of each batch (b)
        confidence_level: Confidence level (default 0.95)
    
    Returns:
        Dictionary with statistics and confidence intervals
    """
    if num_batches < 2:
        raise ValueError("Need at least 2 batches (one to ignore, one to use)")
    
    batch_means, batch_percentiles = calculate_batch_statistics(
        response_times, num_batches, batch_size
    )
    
    used_means = batch_means[1:]
    used_percentiles = batch_percentiles[1:]
    
    n = len(used_means)
    
    mean_of_means = sum(used_means) / n
    mean_of_percentiles = sum(used_percentiles) / n
    
    var_of_means = sum((x - mean_of_means) ** 2 for x in used_means) / (n - 1)
    var_of_percentiles = sum(
        (x - mean_of_percentiles) ** 2 for x in used_percentiles
    ) / (n - 1)
    
    se_mean = math.sqrt(var_of_means / n)
    se_percentile = math.sqrt(var_of_percentiles / n)
    
    try:
        from scipy import stats
        
        alpha = 1 - confidence_level
        t_value = stats.t.ppf(1 - alpha / 2, n - 1)
    except ImportError:
        t_value = 2.0
    
    ci_mean_lower = mean_of_means - t_value * se_mean
    ci_mean_upper = mean_of_means + t_value * se_mean
    
    ci_percentile_lower = mean_of_percentiles - t_value * se_percentile
    ci_percentile_upper = mean_of_percentiles + t_value * se_percentile
    
    return {
        "mean": mean_of_means,
        "mean_ci_lower": ci_mean_lower,
        "mean_ci_upper": ci_mean_upper,
        "percentile_95": mean_of_percentiles,
        "percentile_95_ci_lower": ci_percentile_lower,
        "percentile_95_ci_upper": ci_percentile_upper,
        "num_batches_used": n,
    }

