"""
patient_tools.py

High-level patient data access functions.
These are exposed to the LLM inside the REPL environment.
"""

from mimic_memory import loaders

def get_patient_overview(subject_id):
    return {"demographics": {"age": 65}, "admissions": [1]}


def get_patient_overview(subject_id):
    """
    Returns a structured summary of a patient's demographics and admissions.
    """
    demographics = loaders.get_patient_demographics(subject_id)
    admissions = loaders.get_admissions(subject_id)

    return {
        "demographics": demographics,
        "admissions": admissions
    }


def get_icu_history(subject_id):
    """
    Returns all ICU stays for a patient.
    """
    return loaders.get_icu_stays(subject_id)


def get_patient_diagnoses(subject_id):
    """
    Returns ICD diagnoses for a patient.
    """
    return loaders.get_diagnoses(subject_id)
