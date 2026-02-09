"""
lab_tools.py

High-level lab data tools for clinical reasoning.
These functions are used by the LLM inside the REPL.
"""

from mimic_memory import loaders


def get_labs_for_admission(hadm_id, hours_back=None):
    """
    Fetch lab results for a specific hospital admission.
    Optionally restrict to last N hours before discharge.
    """
    labs = loaders.get_labs_for_hadm(hadm_id, hours_back=hours_back)

    return {
        "hadm_id": hadm_id,
        "lab_count": len(labs),
        "labs": labs
    }


def summarize_lab_values(labs):
    """
    Simple summary statistics for lab values.
    """
    values = [entry["valuenum"] for entry in labs if entry["valuenum"] is not None]

    if not values:
        return {"mean": None, "min": None, "max": None}

    return {
        "mean": sum(values) / len(values),
        "min": min(values),
        "max": max(values)
    }
