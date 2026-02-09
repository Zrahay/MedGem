"""
vitals_tools.py

High-level vitals data tools for ICU trend analysis.
Used by the LLM inside the REPL environment.
"""

from mimic_memory.db_connection import MIMICDatabase

db = MIMICDatabase()


def get_vitals_for_stay(stay_id, hours_back=None):
    """
    Fetch vitals for an ICU stay.
    Optionally restrict to last N hours before ICU discharge.
    """
    if hours_back:
        sql = """
        SELECT charttime, itemid, valuenum
        FROM chartevents
        WHERE stay_id = %s
        AND charttime >= (
            SELECT outtime FROM icustays WHERE stay_id = %s
        ) - interval '%s hour'
        """
        vitals = db.query(sql, (stay_id, stay_id, hours_back))
    else:
        sql = """
        SELECT charttime, itemid, valuenum
        FROM chartevents
        WHERE stay_id = %s
        """
        vitals = db.query(sql, (stay_id,))

    return {
        "stay_id": stay_id,
        "vital_count": len(vitals),
        "vitals": vitals
    }


def summarize_vitals(vitals):
    """
    Basic statistics on vitals data.
    """
    values = [entry["valuenum"] for entry in vitals if entry["valuenum"] is not None]

    if not values:
        return {"mean": None, "min": None, "max": None}

    return {
        "mean": sum(values) / len(values),
        "min": min(values),
        "max": max(values)
    }
