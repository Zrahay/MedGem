"""
stats_tools.py

Basic statistical utilities for cohort-level analysis.
Used by the LLM inside the REPL.
"""

def mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


def median(values):
    values = sorted([v for v in values if v is not None])
    n = len(values)
    if n == 0:
        return None
    if n % 2 == 1:
        return values[n // 2]
    return (values[n // 2 - 1] + values[n // 2]) / 2


def proportion(condition_list):
    """
    Takes a list of booleans and returns proportion of True values.
    """
    if not condition_list:
        return None
    return sum(condition_list) / len(condition_list)


def summarize_numeric_list(values):
    """
    Returns basic summary stats for a numeric list.
    """
    values = [v for v in values if v is not None]
    if not values:
        return {"mean": None, "min": None, "max": None}

    return {
        "mean": mean(values),
        "min": min(values),
        "max": max(values)
    }
