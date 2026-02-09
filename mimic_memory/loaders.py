"""
loaders.py

Safe data access functions for MIMIC-IV.
These are used by higher-level tools and never expose raw SQL to the LLM.
"""

from mimic_memory.db_connection import MIMICDatabase

db = MIMICDatabase()


def get_patient_demographics(subject_id):
    sql = """
    SELECT subject_id, gender, anchor_age, anchor_year
    FROM patients
    WHERE subject_id = %s
    """
    return db.query(sql, (subject_id,))


def get_admissions(subject_id):
    sql = """
    SELECT hadm_id, admittime, dischtime, admission_type
    FROM admissions
    WHERE subject_id = %s
    """
    return db.query(sql, (subject_id,))


def get_icu_stays(subject_id):
    sql = """
    SELECT stay_id, hadm_id, intime, outtime
    FROM icustays
    WHERE subject_id = %s
    """
    return db.query(sql, (subject_id,))


def get_labs_for_hadm(hadm_id, hours_back=None):
    if hours_back:
        sql = """
        SELECT charttime, itemid, valuenum
        FROM labevents
        WHERE hadm_id = %s
        AND charttime >= (SELECT dischtime FROM admissions WHERE hadm_id = %s) - interval '%s hour'
        """
        return db.query(sql, (hadm_id, hadm_id, hours_back))
    else:
        sql = """
        SELECT charttime, itemid, valuenum
        FROM labevents
        WHERE hadm_id = %s
        """
        return db.query(sql, (hadm_id,))


def get_diagnoses(subject_id):
    sql = """
    SELECT icd_code
    FROM diagnoses_icd
    WHERE subject_id = %s
    """
    return db.query(sql, (subject_id,))
