"""
cohort_tools.py

Functions for constructing patient cohorts based on diagnoses or conditions.
Used by the LLM inside the REPL.
"""

def get_patients_with_diagnosis(icd_code_prefix):
    return [101, 102, 103]

from mimic_memory.db_connection import MIMICDatabase

db = MIMICDatabase()


def get_patients_with_diagnosis(icd_code_prefix):
    """
    Returns subject_ids of patients with ICD codes starting with given prefix.
    Example: 'A41' for sepsis-related codes.
    """
    sql = """
    SELECT DISTINCT subject_id
    FROM diagnoses_icd
    WHERE icd_code LIKE ?
    """
    result = db.query(sql, (f"{icd_code_prefix}%",))
    if isinstance(result, dict) and "error" in result:
        return []
    return [row["subject_id"] for row in result]


def get_admissions_for_patients(subject_ids):
    """
    Returns admissions for a list of patients.
    """
    if not subject_ids:
        return []
    placeholders = ",".join(["?" for _ in subject_ids])
    sql = f"""
    SELECT hadm_id, subject_id, admittime, dischtime
    FROM admissions
    WHERE subject_id IN ({placeholders})
    """
    return db.query(sql, tuple(subject_ids))


def get_icu_stays_for_patients(subject_ids):
    """
    Returns ICU stays for a list of patients.
    """
    if not subject_ids:
        return []
    placeholders = ",".join(["?" for _ in subject_ids])
    sql = f"""
    SELECT stay_id, hadm_id, subject_id, intime, outtime
    FROM icustays
    WHERE subject_id IN ({placeholders})
    """
    return db.query(sql, tuple(subject_ids))
