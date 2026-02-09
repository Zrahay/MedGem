"""
schema.py

Defines a safe, high-level schema description of MIMIC-IV tables.
This is shown to the root model so it knows what data exists,
without exposing raw database access.
"""

SCHEMA_DESCRIPTION = """
MIMIC-IV Clinical Database Schema (Simplified)

patients:
- subject_id (int): Unique patient identifier
- gender (str)
- anchor_age (int)
- anchor_year (int)

admissions:
- hadm_id (int): Hospital admission ID
- subject_id (int)
- admittime (datetime)
- dischtime (datetime)
- admission_type (str)
- insurance (str)

icustays:
- stay_id (int): ICU stay identifier
- hadm_id (int)
- subject_id (int)
- intime (datetime)
- outtime (datetime)

labevents:
- subject_id (int)
- hadm_id (int)
- charttime (datetime)
- itemid (int): Lab test ID
- valuenum (float)

chartevents (vitals):
- subject_id (int)
- hadm_id (int)
- stay_id (int)
- charttime (datetime)
- itemid (int)
- valuenum (float)

diagnoses_icd:
- subject_id (int)
- hadm_id (int)
- icd_code (str)

procedures_icd:
- subject_id (int)
- hadm_id (int)
- icd_code (str)

prescriptions:
- subject_id (int)
- hadm_id (int)
- drug (str)
- starttime (datetime)
- stoptime (datetime)
"""

def get_schema_description():
    return SCHEMA_DESCRIPTION
