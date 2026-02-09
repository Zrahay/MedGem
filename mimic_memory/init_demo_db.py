"""
init_demo_db.py

Initializes the MIMIC demo DuckDB database with sample data for testing.
Run this script once to populate the demo database.
"""

import duckdb
import os

# Get the path to the project root
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mimic_demo.duckdb")

# Remove existing database if it exists to start fresh
if os.path.exists(db_path):
    os.remove(db_path)

conn = duckdb.connect(db_path)

# Create tables
conn.execute("""
CREATE TABLE patients (
    subject_id INTEGER PRIMARY KEY,
    gender VARCHAR,
    anchor_age INTEGER,
    anchor_year INTEGER
)
""")

conn.execute("""
CREATE TABLE admissions (
    hadm_id INTEGER PRIMARY KEY,
    subject_id INTEGER,
    admittime TIMESTAMP,
    dischtime TIMESTAMP,
    admission_type VARCHAR,
    insurance VARCHAR
)
""")

conn.execute("""
CREATE TABLE icustays (
    stay_id INTEGER PRIMARY KEY,
    hadm_id INTEGER,
    subject_id INTEGER,
    intime TIMESTAMP,
    outtime TIMESTAMP
)
""")

conn.execute("""
CREATE TABLE labevents (
    labevent_id INTEGER PRIMARY KEY,
    subject_id INTEGER,
    hadm_id INTEGER,
    charttime TIMESTAMP,
    itemid INTEGER,
    valuenum DOUBLE
)
""")

conn.execute("""
CREATE TABLE chartevents (
    stay_id INTEGER,
    subject_id INTEGER,
    hadm_id INTEGER,
    charttime TIMESTAMP,
    itemid INTEGER,
    valuenum DOUBLE
)
""")

conn.execute("""
CREATE TABLE diagnoses_icd (
    subject_id INTEGER,
    hadm_id INTEGER,
    icd_code VARCHAR,
    icd_version INTEGER
)
""")

conn.execute("""
CREATE TABLE procedures_icd (
    subject_id INTEGER,
    hadm_id INTEGER,
    icd_code VARCHAR
)
""")

conn.execute("""
CREATE TABLE prescriptions (
    subject_id INTEGER,
    hadm_id INTEGER,
    drug VARCHAR,
    starttime TIMESTAMP,
    stoptime TIMESTAMP
)
""")

# Insert sample patients (sepsis patients for A41.* ICD codes)
conn.execute("""
INSERT INTO patients VALUES
(101, 'M', 65, 2020),
(102, 'F', 72, 2020),
(103, 'M', 58, 2020),
(104, 'F', 45, 2020),
(105, 'M', 80, 2020)
""")

# Insert admissions
conn.execute("""
INSERT INTO admissions VALUES
(1001, 101, '2020-03-15 08:00:00', '2020-03-25 14:00:00', 'EMERGENCY', 'Medicare'),
(1002, 102, '2020-04-10 12:00:00', '2020-04-18 10:00:00', 'EMERGENCY', 'Medicare'),
(1003, 103, '2020-05-20 06:00:00', '2020-05-28 16:00:00', 'URGENT', 'Private'),
(1004, 104, '2020-06-05 14:00:00', '2020-06-12 11:00:00', 'EMERGENCY', 'Medicaid'),
(1005, 105, '2020-07-01 10:00:00', '2020-07-15 09:00:00', 'EMERGENCY', 'Medicare')
""")

# Insert ICU stays
conn.execute("""
INSERT INTO icustays VALUES
(2001, 1001, 101, '2020-03-15 10:00:00', '2020-03-22 08:00:00'),
(2002, 1002, 102, '2020-04-10 14:00:00', '2020-04-16 12:00:00'),
(2003, 1003, 103, '2020-05-20 08:00:00', '2020-05-26 10:00:00'),
(2004, 1004, 104, '2020-06-05 16:00:00', '2020-06-10 14:00:00'),
(2005, 1005, 105, '2020-07-01 12:00:00', '2020-07-12 10:00:00')
""")

# Insert diagnoses (A41.* = sepsis codes)
conn.execute("""
INSERT INTO diagnoses_icd VALUES
(101, 1001, 'A410', 10),
(101, 1001, 'J189', 10),
(102, 1002, 'A411', 10),
(102, 1002, 'N179', 10),
(103, 1003, 'A419', 10),
(103, 1003, 'R6520', 10),
(104, 1004, 'A4101', 10),
(105, 1005, 'A4102', 10),
(105, 1005, 'J9601', 10)
""")

# Insert lab events
# itemid 50813 = Lactate (common MIMIC itemid for lactate)
# Normal lactate: 0.5-2.0 mmol/L, elevated > 2.0, severe > 4.0

# Patient 101 - improving lactate trend
conn.execute("""
INSERT INTO labevents VALUES
(1, 101, 1001, '2020-03-15 10:30:00', 50813, 5.2),
(2, 101, 1001, '2020-03-15 16:00:00', 50813, 4.8),
(3, 101, 1001, '2020-03-16 04:00:00', 50813, 3.5),
(4, 101, 1001, '2020-03-16 16:00:00', 50813, 2.8),
(5, 101, 1001, '2020-03-17 08:00:00', 50813, 2.1),
(6, 101, 1001, '2020-03-18 08:00:00', 50813, 1.5)
""")

# Patient 102 - worsening lactate trend
conn.execute("""
INSERT INTO labevents VALUES
(7, 102, 1002, '2020-04-10 14:30:00', 50813, 2.1),
(8, 102, 1002, '2020-04-10 20:00:00', 50813, 3.2),
(9, 102, 1002, '2020-04-11 04:00:00', 50813, 4.5),
(10, 102, 1002, '2020-04-11 12:00:00', 50813, 5.8),
(11, 102, 1002, '2020-04-12 08:00:00', 50813, 4.2),
(12, 102, 1002, '2020-04-13 08:00:00', 50813, 2.5)
""")

# Patient 103 - stable elevated lactate
conn.execute("""
INSERT INTO labevents VALUES
(13, 103, 1003, '2020-05-20 08:30:00', 50813, 3.2),
(14, 103, 1003, '2020-05-20 16:00:00', 50813, 3.4),
(15, 103, 1003, '2020-05-21 04:00:00', 50813, 3.1),
(16, 103, 1003, '2020-05-21 16:00:00', 50813, 3.3),
(17, 103, 1003, '2020-05-22 08:00:00', 50813, 2.9)
""")

# Patient 104 - rapidly improving
conn.execute("""
INSERT INTO labevents VALUES
(18, 104, 1004, '2020-06-05 16:30:00', 50813, 6.5),
(19, 104, 1004, '2020-06-05 22:00:00', 50813, 4.2),
(20, 104, 1004, '2020-06-06 06:00:00', 50813, 2.8),
(21, 104, 1004, '2020-06-06 14:00:00', 50813, 1.9),
(22, 104, 1004, '2020-06-07 08:00:00', 50813, 1.4)
""")

# Patient 105 - persistently high
conn.execute("""
INSERT INTO labevents VALUES
(23, 105, 1005, '2020-07-01 12:30:00', 50813, 4.8),
(24, 105, 1005, '2020-07-02 00:00:00', 50813, 5.2),
(25, 105, 1005, '2020-07-02 12:00:00', 50813, 5.5),
(26, 105, 1005, '2020-07-03 00:00:00', 50813, 5.1),
(27, 105, 1005, '2020-07-03 12:00:00', 50813, 4.9),
(28, 105, 1005, '2020-07-04 12:00:00', 50813, 4.5)
""")

# Add some other lab values to make it realistic
# itemid 50912 = Creatinine, 51265 = Platelets, 51301 = WBC
conn.execute("""
INSERT INTO labevents VALUES
(29, 101, 1001, '2020-03-15 10:30:00', 50912, 2.1),
(30, 101, 1001, '2020-03-16 08:00:00', 50912, 1.8),
(31, 102, 1002, '2020-04-10 14:30:00', 50912, 1.5),
(32, 103, 1003, '2020-05-20 08:30:00', 51265, 85),
(33, 104, 1004, '2020-06-05 16:30:00', 51301, 18.5)
""")

# Insert vitals (chartevents)
# itemid 220045 = Heart Rate, 220050 = ABP Systolic, 220210 = Respiratory Rate
conn.execute("""
INSERT INTO chartevents VALUES
(2001, 101, 1001, '2020-03-15 10:00:00', 220045, 110),
(2001, 101, 1001, '2020-03-15 12:00:00', 220045, 105),
(2001, 101, 1001, '2020-03-15 14:00:00', 220045, 98),
(2002, 102, 1002, '2020-04-10 14:00:00', 220045, 95),
(2002, 102, 1002, '2020-04-10 16:00:00', 220045, 102),
(2003, 103, 1003, '2020-05-20 08:00:00', 220050, 85),
(2004, 104, 1004, '2020-06-05 16:00:00', 220210, 24),
(2005, 105, 1005, '2020-07-01 12:00:00', 220045, 115)
""")

conn.close()

print("✅ Demo database initialized successfully!")
print(f"   Database path: {db_path}")
print("   Tables created: patients, admissions, icustays, labevents, chartevents, diagnoses_icd, procedures_icd, prescriptions")
print("   Sample sepsis patients: 5 patients with A41.* ICD codes")
print("   Sample lactate trends: Various patterns (improving, worsening, stable, etc.)")
