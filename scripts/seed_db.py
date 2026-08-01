"""
===========================================================
Medical Interoperability Demo Database Seeder
Part 1 - Configuration & Helper Functions
===========================================================
"""

from __future__ import annotations
import random
from datetime import datetime, timedelta, date, time
from pathlib import Path
import tomllib
from faker import Faker
from supabase import create_client

# ----------------------------------------------------------
# Load Environment Variables
# ----------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SECRETS_FILE = PROJECT_ROOT / ".streamlit" / "secret.toml"

if not SECRETS_FILE.exists():
    raise FileNotFoundError(
        f"Could not find:\n{SECRETS_FILE}"
    )


secrets = tomllib.loads(SECRETS_FILE.read_text())

SUPABASE_URL = secrets["supabase"]["SUPABASE_URL"]
SUPABASE_KEY = secrets["supabase"]["SUPABASE_SERVICE_KEY"]

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL not found in secret.toml")

if not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_SERVICE_KEY not found in secret.toml")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ----------------------------------------------------------
# Faker
# ----------------------------------------------------------

fake = Faker("en_IN")

# ----------------------------------------------------------
# Random Seed
#
# Keeping this fixed means every run generates the same
# demo database.
# ----------------------------------------------------------

random.seed(42)

# ----------------------------------------------------------
# Configuration
# ----------------------------------------------------------

TOTAL_APPOINTMENTS_PER_PATIENT = 3

PAST_VISIT_WEIGHT = 0.40
CURRENT_VISIT_WEIGHT = 0.30
FUTURE_VISIT_WEIGHT = 0.30

# ----------------------------------------------------------
# Doctor Specialization Weights
#
# Higher number = more likely to receive appointments.
# ----------------------------------------------------------

SPECIALIZATION_WEIGHTS = {

    # Common OPD
    "General Physician": 10,
    "Dermatologist": 8,
    "Pediatrician": 7,
    "Orthopedic": 6,
    "ENT": 5,
    "Dentist": 5,
    "Gynecologist": 5,

    # Specialists
    "Cardiologist": 4,
    "Neurologist": 4,
    "Psychiatrist": 3,
    "Oncologist": 2,
    "Radiologist": 2,
    "Ophthalmologist": 2,

    # AYUSH
    "Ayurveda": 2,
    "Homeopathy": 2,
    "Siddha": 1,
    "Naturopathy": 1,
    "Integrative Medicine": 1

}

# ----------------------------------------------------------
# Possible Diagnoses
#
# Used later while generating Medical Records.
# ----------------------------------------------------------

DIAGNOSES = [

    "Common Cold",
    "Viral Fever",
    "Migraine",
    "Hypertension",
    "Diabetes Mellitus",
    "Allergic Rhinitis",
    "Back Pain",
    "Fracture",
    "Skin Infection",
    "Asthma",
    "Gastritis",
    "Sinusitis",
    "Arthritis",
    "Anxiety Disorder",
    "Depression"

]

# ----------------------------------------------------------
# Symptoms
# ----------------------------------------------------------

SYMPTOMS = [

    "Fever and body ache",
    "Persistent cough",
    "Headache",
    "Joint pain",
    "Skin irritation",
    "Shortness of breath",
    "Chest pain",
    "Nausea and vomiting",
    "Abdominal pain",
    "Runny nose",
    "Sore throat",
    "Fatigue",
    "Dizziness",
    "Back pain",
    "High blood sugar symptoms"

]


# ----------------------------------------------------------
# Treatments
# ----------------------------------------------------------

TREATMENTS = [

    "Complete bed rest and hydration.",
    "Prescribed oral antibiotics for 5 days.",
    "Pain management with NSAIDs.",
    "Lifestyle modification and diet counselling.",
    "Physiotherapy recommended.",
    "Steam inhalation and antihistamines.",
    "Blood pressure monitoring.",
    "Insulin dosage adjusted.",
    "Topical ointment prescribed.",
    "Nebulization advised.",
    "Vitamin supplementation.",
    "Follow-up consultation after one week."

]

# ----------------------------------------------------------
# Medicines
# ----------------------------------------------------------

MEDICINES = [

    "Paracetamol",
    "Ibuprofen",
    "Azithromycin",
    "Cetirizine",
    "Amoxicillin",
    "Vitamin D3",
    "Calcium Tablets",
    "Pantoprazole",
    "ORS",
    "Metformin",
    "Amlodipine",
    "Salbutamol"

]

# ----------------------------------------------------------
# Lab Reports
# ----------------------------------------------------------

LAB_REPORTS = [

    "Complete Blood Count",
    "Lipid Profile",
    "Blood Sugar",
    "MRI Scan",
    "CT Scan",
    "X-Ray",
    "ECG",
    "Liver Function Test",
    "Kidney Function Test",
    "Urine Analysis"

]

# ----------------------------------------------------------
# Medical Knowledge Dictionary
# ----------------------------------------------------------

# ----------------------------------------------------------
# Medical Knowledge Base
#
# Every specialization contains medically consistent cases.
# Future tables (Prescription, Lab Reports, Billing, etc.)
# will derive data from these cases.
# ----------------------------------------------------------

MEDICAL_CASES = {

    "General Physician": [

        {
            "diagnosis": "Common Cold",
            "symptoms": [
                "Runny nose",
                "Sneezing",
                "Sore throat",
                "Low-grade fever"
            ],
            "treatment": "Adequate hydration, rest, steam inhalation and symptomatic treatment.",
            "medicines": [
                "Paracetamol",
                "Cetirizine"
            ],
            "labs": [
                "Complete Blood Count"
            ],
            "notes": [
                "Patient presented with mild upper respiratory tract symptoms. Conservative management advised.",
                "No signs of secondary bacterial infection. Symptomatic treatment initiated."
            ]
        },

        {
            "diagnosis": "Viral Fever",
            "symptoms": [
                "High fever",
                "Body ache",
                "Fatigue",
                "Headache"
            ],
            "treatment": "Hydration, antipyretics and observation.",
            "medicines": [
                "Paracetamol",
                "ORS"
            ],
            "labs": [
                "Complete Blood Count"
            ],
            "notes": [
                "Vitals stable. Fever likely viral in origin.",
                "Patient advised adequate fluid intake and rest."
            ]
        },

        {
            "diagnosis": "Hypertension",
            "symptoms": [
                "Headache",
                "Dizziness",
                "Blurred vision"
            ],
            "treatment": "Lifestyle modification and antihypertensive therapy.",
            "medicines": [
                "Amlodipine"
            ],
            "labs": [
                "Lipid Profile"
            ],
            "notes": [
                "Elevated blood pressure recorded during examination.",
                "Dietary salt restriction and exercise advised."
            ]
        }

    ],

    "Dermatologist": [

        {
            "diagnosis": "Skin Infection",
            "symptoms": [
                "Redness",
                "Skin rash",
                "Itching",
                "Localized swelling"
            ],
            "treatment": "Topical medication with hygiene instructions.",
            "medicines": [
                "Amoxicillin"
            ],
            "labs": [],
            "notes": [
                "Localized bacterial skin infection noted.",
                "Patient advised to keep affected area clean and dry."
            ]
        }

    ],

    "Orthopedic": [

        {
            "diagnosis": "Fracture",
            "symptoms": [
                "Severe limb pain",
                "Swelling",
                "Restricted movement"
            ],
            "treatment": "Immobilization followed by orthopedic casting.",
            "medicines": [
                "Ibuprofen"
            ],
            "labs": [
                "X-Ray"
            ],
            "notes": [
                "Localized tenderness with restricted range of motion.",
                "Radiographic evaluation recommended."
            ]
        },

        {
            "diagnosis": "Arthritis",
            "symptoms": [
                "Joint pain",
                "Morning stiffness",
                "Joint swelling"
            ],
            "treatment": "NSAIDs, physiotherapy and lifestyle modification.",
            "medicines": [
                "Ibuprofen"
            ],
            "labs": [],
            "notes": [
                "Degenerative joint changes suspected.",
                "Physiotherapy exercises explained."
            ]
        }

    ],

    "Cardiologist": [

        {
            "diagnosis": "Hypertension",
            "symptoms": [
                "Chest discomfort",
                "Headache",
                "Dizziness"
            ],
            "treatment": "Blood pressure management and cardiac risk reduction.",
            "medicines": [
                "Amlodipine"
            ],
            "labs": [
                "ECG",
                "Lipid Profile"
            ],
            "notes": [
                "Cardiovascular examination performed.",
                "Regular BP monitoring advised."
            ]
        }

    ],

    "Pediatrician": [

        {
            "diagnosis": "Viral Fever",
            "symptoms": [
                "Fever",
                "Cough",
                "Loss of appetite"
            ],
            "treatment": "Hydration and supportive care.",
            "medicines": [
                "Paracetamol"
            ],
            "labs": [
                "Complete Blood Count"
            ],
            "notes": [
                "Child active and clinically stable.",
                "Parents educated regarding warning signs."
            ]
        }

    ],

    "ENT": [

        {
            "diagnosis": "Sinusitis",
            "symptoms": [
                "Facial pain",
                "Nasal congestion",
                "Headache"
            ],
            "treatment": "Steam inhalation, antibiotics when indicated.",
            "medicines": [
                "Azithromycin",
                "Cetirizine"
            ],
            "labs": [],
            "notes": [
                "Maxillary sinus tenderness present.",
                "Steam inhalation advised."
            ]
        }

    ],

    "Psychiatrist": [

        {
            "diagnosis": "Anxiety Disorder",
            "symptoms": [
                "Excessive worrying",
                "Restlessness",
                "Difficulty sleeping"
            ],
            "treatment": "Counselling with behavioural therapy.",
            "medicines": [],
            "labs": [],
            "notes": [
                "Mental status examination completed.",
                "Stress management techniques discussed."
            ]
        },

        {
            "diagnosis": "Depression",
            "symptoms": [
                "Persistent sadness",
                "Fatigue",
                "Loss of interest"
            ],
            "treatment": "Psychotherapy with regular follow-up.",
            "medicines": [],
            "labs": [],
            "notes": [
                "Patient cooperative throughout consultation.",
                "Follow-up scheduled to monitor progress."
            ]
        }

    ],

    "Dentist": [

        {
            "diagnosis": "Dental Caries",
            "symptoms": [
                "Tooth pain",
                "Sensitivity",
                "Difficulty chewing"
            ],
            "treatment": "Dental restoration and oral hygiene counselling.",
            "medicines": [
                "Ibuprofen"
            ],
            "labs": [],
            "notes": [
                "Dental examination revealed carious lesion.",
                "Oral hygiene instructions provided."
            ]
        }

    ]
}

# ----------------------------------------------------------
# Weekday Mapping
# ----------------------------------------------------------

WEEKDAY_INDEX = {

    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6

}

# ----------------------------------------------------------
# Utility Functions
# ----------------------------------------------------------

def weighted_choice(doctors: list[dict]) -> dict:
    """
    Returns a doctor using specialization weights.
    """

    weights = []

    for doctor in doctors:

        weights.append(
            SPECIALIZATION_WEIGHTS.get(
                doctor["specialization"],
                1
            )
        )

    return random.choices(
        doctors,
        weights=weights,
        k=1
    )[0]


def random_status(appointment_date: date) -> str:
    """
    Decide appointment status based on date.
    """

    today = date.today()

    if appointment_date < today:

        return random.choices(

            ["Completed", "Cancelled"],
            weights=[90, 10]

        )[0]

    elif appointment_date <= today + timedelta(days=5):

        return "Confirmed"

    return "Pending"


def random_datetime(days: int = 30) -> date:
    """
    Random date within ±days.
    """

    return date.today() + timedelta(

        days=random.randint(
            -days,
            days
        )

    )


def print_header(title: str):

    print()

    print("=" * 60)

    print(title)

    print("=" * 60)


# ----------------------------------------------------------
# Load Database Tables
# ----------------------------------------------------------

print_header("Loading Database")

patients = (
    supabase
    .table("patients")
    .select("*")
    .execute()
    .data
)

doctors = (
    supabase
    .table("doctors")
    .select("*")
    .execute()
    .data
)

doctor_lookup = {
    doctor["id"]: doctor
    for doctor in doctors
}

doctor_availability = (
    supabase
    .table("doctor_availability")
    .select("*")
    .execute()
    .data
)

# ----------------------------------------------------------
# Load Existing Appointments
# ----------------------------------------------------------

appointments = (
    supabase
    .table("appointments")
    .select("*")
    .execute()
    .data
)

print(f"Appointments Loaded       : {len(appointments)}")


# ----------------------------------------------------------
# Load Existing Medical Records
# ----------------------------------------------------------

existing_medical_records = (
    supabase
    .table("medical_records")
    .select("appointment_id")
    .execute()
    .data
)

existing_appointment_ids = {

    row["appointment_id"]

    for row in existing_medical_records

}

print(
    f"Existing Medical Records  : {len(existing_appointment_ids)}"
)

print("\nFirst availability record:")
print(doctor_availability[0])

print("\n===== SAMPLE AVAILABILITY =====")

for row in doctor_availability[:3]:
    print(row)

print("===============================\n")

print(f"Patients Loaded           : {len(patients)}")
print(f"Doctors Loaded            : {len(doctors)}")
print(f"Availability Records      : {len(doctor_availability)}")

# ----------------------------------------------------------
# Build Availability Lookup
# ----------------------------------------------------------

availability_lookup = {}

for slot in doctor_availability:

    doctor_id = slot["doctor_id"]

    availability_lookup.setdefault(
        doctor_id,
        []
    ).append(slot)

print(
    f"Doctors with schedules    : {len(availability_lookup)}"
)

# ----------------------------------------------------------
# Part 1 Complete
# ----------------------------------------------------------

print_header("Part 1 Complete")
print("Configuration Loaded Successfully.")

# ==========================================================
# PART 2
# Appointment Generation
# ==========================================================

# print_header("Generating Appointments")

# appointments = []

# # Prevent doctor double-bookings
# #
# # Key:
# # (doctor_id, appointment_date, appointment_time)
# #
# occupied_slots = set()


# # ----------------------------------------------------------
# # Utility
# # ----------------------------------------------------------

# def random_time_between(start_time, end_time):

#     if isinstance(start_time, str):
#         start_time = datetime.strptime(
#             start_time,
#             "%H:%M:%S"
#         ).time()

#     if isinstance(end_time, str):
#         end_time = datetime.strptime(
#             end_time,
#             "%H:%M:%S"
#         ).time()

#     start_minutes = (
#         start_time.hour * 60
#         + start_time.minute
#     )

#     end_minutes = (
#         end_time.hour * 60
#         + end_time.minute
#     )

#     possible = list(
#         range(
#             start_minutes,
#             end_minutes,
#             30
#         )
#     )

#     chosen = random.choice(possible)

#     return time(
#         chosen // 60,
#         chosen % 60
#     )


# def next_matching_weekday(target_weekday):
#     """
#     Returns a date having the requested weekday.

#     Example:
#     Monday -> nearest Monday
#     """

#     today = date.today()

#     offset = (target_weekday - today.weekday()) % 7

#     return today + timedelta(days=offset)


# # ----------------------------------------------------------
# # Main Generator
# # ----------------------------------------------------------

# for patient in patients:

#     used_doctors = set()

#     patient_visits = 0

#     while patient_visits < TOTAL_APPOINTMENTS_PER_PATIENT:

#         # ------------------------------------------
#         # Choose doctor
#         # ------------------------------------------

#         doctor = weighted_choice(doctors)

#         if doctor["id"] in used_doctors:
#             continue

#         used_doctors.add(
#             doctor["id"]
#         )

#         # ------------------------------------------
#         # Availability
#         # ------------------------------------------

#         slots = availability_lookup.get(
#             doctor["id"],
#             []
#         )

#         if len(slots) == 0:
#             continue

#         slot = random.choice(slots)

#         weekday_name = slot["weekday"]

#         weekday_index = WEEKDAY_INDEX[
#             weekday_name
#         ]

#         # ------------------------------------------
#         # Appointment Date
#         # ------------------------------------------

#         visit_type = random.choices(

#             ["past", "current", "future"],

#             weights=[
#                 PAST_VISIT_WEIGHT,
#                 CURRENT_VISIT_WEIGHT,
#                 FUTURE_VISIT_WEIGHT
#             ]

#         )[0]

#         base_date = next_matching_weekday(
#             weekday_index
#         )

#         if visit_type == "past":

#             appointment_date = (

#                 base_date
#                 - timedelta(
#                     days=random.randint(7, 60)
#                 )

#             )

#         elif visit_type == "current":

#             appointment_date = (

#                 base_date
#                 + timedelta(
#                     days=random.randint(0, 5)
#                 )

#             )

#         else:

#             appointment_date = (

#                 base_date
#                 + timedelta(
#                     days=random.randint(7, 35)
#                 )

#             )

#         # ------------------------------------------
#         # Appointment Time
#         # ------------------------------------------

#         appointment_time = random_time_between(

#             slot["start_time"],
#             slot["end_time"]

#         )

#         # ------------------------------------------
#         # Prevent doctor double booking
#         # ------------------------------------------

#         key = (

#             doctor["id"],
#             appointment_date,
#             appointment_time

#         )

#         if key in occupied_slots:
#             continue

#         occupied_slots.add(key)

#         # ------------------------------------------
#         # Status
#         # ------------------------------------------

#         status = random_status(
#             appointment_date
#         )

#         # ------------------------------------------
#         # Store
#         # ------------------------------------------

#         appointments.append(

#             {

#                 "patient_id": patient["id"],

#                 "doctor_id": doctor["id"],

#                 "appointment_date": appointment_date.isoformat(),

#                 "appointment_time": appointment_time.strftime(
#                     "%H:%M:%S"
#                 ),

#                 "status": status

#             }

#         )

#         patient_visits += 1


# print()

# print(f"Appointments Generated : {len(appointments)}")

# print(f"Doctor Slots Occupied  : {len(occupied_slots)}")

# print_header("Uploading Appointments")

# response = (
#     supabase
#     .table("appointments")
#     .insert(appointments)
#     .execute()
# )

# appointments = response.data
# print(f"Inserted {len(appointments)} appointments.")

# print_header("Part 2 Complete")

# ==========================================================
# PART 3
# Medical Record Generation
# ==========================================================

# print_header("Generating Medical Records")

# medical_records = []

# generated = 0
# skipped = 0

# HIGH_FOLLOW_UP = {

#     "Hypertension",
#     "Diabetes Mellitus",
#     "Fracture",
#     "Arthritis",
#     "Depression",
#     "Anxiety Disorder"

# }

# for appointment in appointments:

#     # ------------------------------------------------------
#     # Only completed appointments generate records
#     # ------------------------------------------------------

#     if appointment["status"] != "Completed":
#         continue

#     # ------------------------------------------------------
#     # Skip existing records
#     # ------------------------------------------------------

#     if appointment["id"] in existing_appointment_ids:
#         skipped += 1
#         continue

#     # ------------------------------------------------------
#     # Fetch doctor
#     # ------------------------------------------------------

#     doctor = doctor_lookup.get(
#         appointment["doctor_id"]
#     )

#     if doctor is None:
#         continue

#     specialization = doctor["specialization"]

#     # ------------------------------------------------------
#     # Skip unsupported specializations
#     # ------------------------------------------------------

#     if specialization not in MEDICAL_CASES:
#         print(
#         f"Skipping doctor '{doctor['doctor_name']}' "
#         f"({specialization}) - no medical cases defined."
#     )

#         continue

#     # ------------------------------------------------------
#     # Pick one realistic case
#     # ------------------------------------------------------

#     case = random.choice(
#         MEDICAL_CASES[specialization]
#     )

#     print(
#     f"Generating record -> "
#     f"{doctor['doctor_name']} | "
#     f"{specialization} | "
#     f"{case['diagnosis']}"
# )

#     diagnosis = case["diagnosis"]

#     symptom_count = random.randint(
#     min(2, len(case["symptoms"])),
#     len(case["symptoms"])
# )

#     symptoms = ", ".join(
#         random.sample(
#             case["symptoms"],
#             k=symptom_count
#         )
#     )

#     treatment = case["treatment"]

#     notes = random.choice(
#         case["notes"]
#     )

#     if diagnosis in HIGH_FOLLOW_UP:
#         follow_up_required = random.random() < 0.80
#     else:
#         follow_up_required = random.random() < 0.25

#     follow_up_date = None

#     if follow_up_required:

#         appointment_date = appointment["appointment_date"]

#         if isinstance(appointment_date, str):
#             appointment_date = date.fromisoformat(
#                 appointment_date
#             )

#         if diagnosis == "Fracture":

#             days = random.randint(14, 45)

#         elif diagnosis in {
#             "Hypertension",
#             "Diabetes Mellitus"
#         }:

#             days = random.randint(30, 90)

#         else:

#             days = random.randint(7, 30)

#         follow_up_date = (
#             appointment_date + timedelta(days=days)
#         ).isoformat()

#     # ------------------------------------------------------
#     # Store Record
#     # ------------------------------------------------------

#     medical_records.append(

#             {

#                 "appointment_id": appointment["id"],

#                 "patient_id": appointment["patient_id"],

#                 "doctor_id": appointment["doctor_id"],

#                 "diagnosis": diagnosis,

#                 "symptoms": symptoms,

#                 "treatment": treatment,

#                 "notes": notes,

#                 "follow_up_required": follow_up_required,

#                 "follow_up_date": follow_up_date

#             }

#         )

#     generated += 1


# # ----------------------------------------------------------
# # Upload
# # ----------------------------------------------------------

# print()
# print("=" * 60)
# print("Medical Record Summary")
# print("=" * 60)

# print(f"Medical Records Generated : {generated}")
# print(f"Skipped Existing Records  : {skipped}")
# print(f"Uploading : {len(medical_records)}")
# if medical_records:

#     response = (

#         supabase
#         .table("medical_records")
#         .insert(medical_records)
#         .execute()

#     )

#     print(
#         f"Inserted {len(response.data)} medical records."
#     )

# else:

#     print(
#         "No new medical records to insert."
#     )

# print_header("Part 3 Complete")

# ==========================================================
# PART 4
# Medicine Master Generation
# ==========================================================

# print_header("Generating Medicine Master")

# MEDICINE_MASTER = [

#     {
#         "name": "Paracetamol",
#         "generic_name": "Acetaminophen",
#         "strength": "500 mg",
#         "dosage_form": "Tablet",
#         "manufacturer": "Sun Pharma",
#         "description": "Analgesic and antipyretic."
#     },

#     {
#         "name": "Ibuprofen",
#         "generic_name": "Ibuprofen",
#         "strength": "400 mg",
#         "dosage_form": "Tablet",
#         "manufacturer": "Cipla",
#         "description": "NSAID used for pain and inflammation."
#     },

#     {
#         "name": "Azithromycin",
#         "generic_name": "Azithromycin",
#         "strength": "500 mg",
#         "dosage_form": "Tablet",
#         "manufacturer": "Alembic",
#         "description": "Macrolide antibiotic."
#     },

#     {
#         "name": "Cetirizine",
#         "generic_name": "Cetirizine",
#         "strength": "10 mg",
#         "dosage_form": "Tablet",
#         "manufacturer": "Dr. Reddy's",
#         "description": "Antihistamine for allergy relief."
#     },

#     {
#         "name": "Amoxicillin",
#         "generic_name": "Amoxicillin",
#         "strength": "500 mg",
#         "dosage_form": "Capsule",
#         "manufacturer": "Mankind",
#         "description": "Broad-spectrum penicillin antibiotic."
#     },

#     {
#         "name": "Vitamin D3",
#         "generic_name": "Cholecalciferol",
#         "strength": "60000 IU",
#         "dosage_form": "Capsule",
#         "manufacturer": "Cipla",
#         "description": "Vitamin D supplement."
#     },

#     {
#         "name": "Calcium Tablets",
#         "generic_name": "Calcium Carbonate",
#         "strength": "500 mg",
#         "dosage_form": "Tablet",
#         "manufacturer": "Abbott",
#         "description": "Calcium supplementation."
#     },

#     {
#         "name": "Pantoprazole",
#         "generic_name": "Pantoprazole",
#         "strength": "40 mg",
#         "dosage_form": "Tablet",
#         "manufacturer": "Sun Pharma",
#         "description": "Proton pump inhibitor."
#     },

#     {
#         "name": "ORS",
#         "generic_name": "Oral Rehydration Salts",
#         "strength": "WHO Formula",
#         "dosage_form": "Powder",
#         "manufacturer": "WHO",
#         "description": "Oral rehydration therapy."
#     },

#     {
#         "name": "Metformin",
#         "generic_name": "Metformin Hydrochloride",
#         "strength": "500 mg",
#         "dosage_form": "Tablet",
#         "manufacturer": "USV",
#         "description": "Antidiabetic medication."
#     },

#     {
#         "name": "Amlodipine",
#         "generic_name": "Amlodipine",
#         "strength": "5 mg",
#         "dosage_form": "Tablet",
#         "manufacturer": "Torrent Pharma",
#         "description": "Calcium channel blocker."
#     },

#     {
#         "name": "Salbutamol",
#         "generic_name": "Salbutamol",
#         "strength": "100 mcg",
#         "dosage_form": "Inhaler",
#         "manufacturer": "GSK",
#         "description": "Bronchodilator."
#     }

# ]

# # ----------------------------------------------------------
# # Existing Medicines
# # ----------------------------------------------------------

# existing_medicines = (

#     supabase
#     .table("medicines")
#     .select(
#         "name,generic_name,strength,dosage_form"
#     )
#     .execute()
#     .data

# )

# existing_keys = {

#     (
#         row["name"],
#         row["generic_name"],
#         row["strength"],
#         row["dosage_form"]
#     )

#     for row in existing_medicines

# }

# # ----------------------------------------------------------
# # Filter Already Existing
# # ----------------------------------------------------------

# new_medicines = []

# for medicine in MEDICINE_MASTER:

#     key = (

#         medicine["name"],
#         medicine["generic_name"],
#         medicine["strength"],
#         medicine["dosage_form"]

#     )

#     if key not in existing_keys:

#         new_medicines.append(medicine)

# # ----------------------------------------------------------
# # Upload
# # ----------------------------------------------------------

# if new_medicines:

#     response = (

#         supabase
#         .table("medicines")
#         .insert(new_medicines)
#         .execute()

#     )

#     print(
#         f"Inserted {len(response.data)} medicines."
#     )

# else:

#     print(
#         "Medicine master already populated."
#     )

# print_header("Part 4 Complete")

# ==========================================================
# PART 5
# Medicine Inventory Generation
# ==========================================================

# print_header("Generating Medicine Inventory")

# # ----------------------------------------------------------
# # Load Medicine Master
# # ----------------------------------------------------------

# medicines = (
#     supabase
#     .table("medicines")
#     .select("*")
#     .execute()
#     .data
# )

# # ----------------------------------------------------------
# # Existing Inventory
# # ----------------------------------------------------------

# existing_inventory = (
#     supabase
#     .table("medicine_inventory")
#     .select("batch_number")
#     .execute()
#     .data
# )

# existing_batches = {

#     row["batch_number"]

#     for row in existing_inventory

# }

# inventory_records = []

# # ----------------------------------------------------------
# # Generate Inventory
# # ----------------------------------------------------------

# for medicine in medicines:

#     # each medicine gets between 2–4 batches
#     batches = random.randint(2, 4)

#     for batch_no in range(1, batches + 1):

#         batch_number = (
#             f"{medicine['name'][:3].upper()}"
#             f"-{fake.random_number(digits=5, fix_len=True)}"
#             f"-{batch_no}"
#         )

#         if batch_number in existing_batches:
#             continue

#         expiry_date = (
#             date.today()
#             + timedelta(days=random.randint(180, 900))
#         )

#         quantity = random.randint(
#             100,
#             1000
#         )

#         price = round(
#             random.uniform(5, 500),
#             2
#         )

#         inventory_records.append(

#             {

#                 "medicine_id": medicine["id"],

#                 "batch_number": batch_number,

#                 "expiry_date": expiry_date.isoformat(),

#                 "quantity_in_stock": quantity,

#                 "unit_price": price

#             }

#         )

# # ----------------------------------------------------------
# # Upload
# # ----------------------------------------------------------

# if inventory_records:

#     response = (

#         supabase
#         .table("medicine_inventory")
#         .insert(inventory_records)
#         .execute()

#     )

#     print(
#         f"Inserted {len(response.data)} inventory batches."
#     )

# else:

#     print(
#         "Medicine inventory already populated."
#     )

# print_header("Part 5 Complete")


#! This will now be the single source of truth for all future parts
#! Updates to this part is to be revised
#! older parts are to be considered......READ-ONLY
MEDICAL_KNOWLEDGE = {

    "Common Cold": {

        "symptoms": [
            "Runny nose",
            "Sneezing",
            "Sore throat",
            "Low-grade fever"
        ],

        "treatment":
            "Adequate hydration, steam inhalation, rest and symptomatic treatment.",

        "labs": [
            "Complete Blood Count"
        ],

        "follow_up_days": 7,

        "medicines": [

            {
                "name": "Paracetamol",
                "dosage": "500 mg",
                "frequency": "Every 6 hours",
                "duration": "5 Days",
                "instructions": "After food"
            },

            {
                "name": "Cetirizine",
                "dosage": "10 mg",
                "frequency": "Once Daily",
                "duration": "5 Days",
                "instructions": "Take at bedtime"
            }

        ]

    },

    "Viral Fever": {

        "symptoms": [
            "High fever",
            "Body ache",
            "Fatigue",
            "Headache"
        ],

        "treatment":
            "Hydration, bed rest and antipyretics.",

        "labs": [
            "Complete Blood Count"
        ],

        "follow_up_days": 5,

        "medicines": [

            {
                "name": "Paracetamol",
                "dosage": "650 mg",
                "frequency": "Every 6 hours",
                "duration": "5 Days",
                "instructions": "After food"
            },

            {
                "name": "ORS",
                "dosage": "200 ml",
                "frequency": "After every loose stool",
                "duration": "3 Days",
                "instructions": None
            }

        ]

    },

    "Migraine": {

        "symptoms": [
            "Severe headache",
            "Photophobia",
            "Nausea",
            "Vomiting"
        ],

        "treatment":
            "Pain management and adequate hydration.",

        "labs": [],

        "follow_up_days": 14,

        "medicines": [

            {
                "name": "Ibuprofen",
                "dosage": "400 mg",
                "frequency": "Twice Daily",
                "duration": "5 Days",
                "instructions": "Take after meals"
            }

        ]

    },

    "Hypertension": {

        "symptoms": [
            "Headache",
            "Dizziness",
            "Blurred vision"
        ],

        "treatment":
            "Lifestyle modification with antihypertensive therapy.",

        "labs": [
            "ECG",
            "Lipid Profile"
        ],

        "follow_up_days": 30,

        "medicines": [

            {
                "name": "Amlodipine",
                "dosage": "5 mg",
                "frequency": "Once Daily",
                "duration": "30 Days",
                "instructions": "Take every morning"
            }

        ]

    },

    "Diabetes Mellitus": {

        "symptoms": [
            "High blood sugar symptoms",
            "Fatigue",
            "Frequent urination",
            "Increased thirst"
        ],

        "treatment":
            "Blood sugar control with lifestyle modification.",

        "labs": [
            "Blood Sugar"
        ],

        "follow_up_days": 30,

        "medicines": [

            {
                "name": "Metformin",
                "dosage": "500 mg",
                "frequency": "Twice Daily",
                "duration": "30 Days",
                "instructions": "After meals"
            }

        ]

    },

    "Allergic Rhinitis": {

        "symptoms": [
            "Runny nose",
            "Sneezing",
            "Watery eyes",
            "Nasal congestion"
        ],

        "treatment":
            "Avoid allergens and antihistamines.",

        "labs": [],

        "follow_up_days": 14,

        "medicines": [

            {
                "name": "Cetirizine",
                "dosage": "10 mg",
                "frequency": "Once Daily",
                "duration": "7 Days",
                "instructions": "Take at bedtime"
            }

        ]

    },

    "Back Pain": {

        "symptoms": [
            "Back pain",
            "Muscle stiffness",
            "Restricted movement"
        ],

        "treatment":
            "NSAIDs and physiotherapy.",

        "labs": [],

        "follow_up_days": 14,

        "medicines": [

            {
                "name": "Ibuprofen",
                "dosage": "400 mg",
                "frequency": "Twice Daily",
                "duration": "7 Days",
                "instructions": "After food"
            }

        ]

    },

    "Fracture": {

        "symptoms": [
            "Severe limb pain",
            "Swelling",
            "Restricted movement"
        ],

        "treatment":
            "Immobilization and orthopedic management.",

        "labs": [
            "X-Ray"
        ],

        "follow_up_days": 30,

        "medicines": [

            {
                "name": "Ibuprofen",
                "dosage": "400 mg",
                "frequency": "Three Times Daily",
                "duration": "10 Days",
                "instructions": "After meals"
            },

            {
                "name": "Calcium Tablets",
                "dosage": "500 mg",
                "frequency": "Once Daily",
                "duration": "60 Days",
                "instructions": "After breakfast"
            },

            {
                "name": "Vitamin D3",
                "dosage": "60000 IU",
                "frequency": "Once Weekly",
                "duration": "8 Weeks",
                "instructions": "After lunch"
            }

        ]

    },

    "Skin Infection": {

        "symptoms": [
            "Skin rash",
            "Redness",
            "Localized swelling",
            "Itching"
        ],

        "treatment":
            "Antibiotics and local hygiene.",

        "labs": [],

        "follow_up_days": 10,

        "medicines": [

            {
                "name": "Amoxicillin",
                "dosage": "500 mg",
                "frequency": "Three Times Daily",
                "duration": "7 Days",
                "instructions": "After meals"
            }

        ]

    },

    "Asthma": {

        "symptoms": [
            "Shortness of breath",
            "Chest tightness",
            "Persistent cough",
            "Wheezing"
        ],

        "treatment":
            "Bronchodilator therapy.",

        "labs": [],

        "follow_up_days": 14,

        "medicines": [

            {
                "name": "Salbutamol",
                "dosage": "2 Puffs",
                "frequency": "As Needed",
                "duration": "30 Days",
                "instructions": "Shake inhaler before use"
            }

        ]

    },

    "Gastritis": {

        "symptoms": [
            "Abdominal pain",
            "Nausea and vomiting",
            "Heartburn"
        ],

        "treatment":
            "Acid suppression and dietary modification.",

        "labs": [],

        "follow_up_days": 14,

        "medicines": [

            {
                "name": "Pantoprazole",
                "dosage": "40 mg",
                "frequency": "Once Daily",
                "duration": "14 Days",
                "instructions": "Take before breakfast"
            }

        ]

    },

    "Sinusitis": {

        "symptoms": [
            "Facial pain",
            "Headache",
            "Nasal congestion"
        ],

        "treatment":
            "Steam inhalation and antibiotics if indicated.",

        "labs": [],

        "follow_up_days": 10,

        "medicines": [

            {
                "name": "Azithromycin",
                "dosage": "500 mg",
                "frequency": "Once Daily",
                "duration": "3 Days",
                "instructions": "After meals"
            },

            {
                "name": "Cetirizine",
                "dosage": "10 mg",
                "frequency": "Once Daily",
                "duration": "5 Days",
                "instructions": "At bedtime"
            }

        ]

    },

    "Arthritis": {

        "symptoms": [
            "Joint pain",
            "Morning stiffness",
            "Joint swelling"
        ],

        "treatment":
            "NSAIDs with physiotherapy.",

        "labs": [],

        "follow_up_days": 30,

        "medicines": [

            {
                "name": "Ibuprofen",
                "dosage": "400 mg",
                "frequency": "Twice Daily",
                "duration": "14 Days",
                "instructions": "After food"
            },

            {
                "name": "Calcium Tablets",
                "dosage": "500 mg",
                "frequency": "Once Daily",
                "duration": "60 Days",
                "instructions": None
            }

        ]

    },

    "Anxiety Disorder": {

        "symptoms": [
            "Restlessness",
            "Difficulty sleeping",
            "Excessive worrying"
        ],

        "treatment":
            "Counselling and behavioural therapy.",

        "labs": [],

        "follow_up_days": 14,

        "medicines": []

    },

    "Depression": {

        "symptoms": [
            "Persistent sadness",
            "Fatigue",
            "Loss of interest"
        ],

        "treatment":
            "Psychotherapy and regular follow-up.",

        "labs": [],

        "follow_up_days": 21,

        "medicines": []

    }

}

# ==========================================================
# PART 6
# Prescription Generation
# ==========================================================

# print_header("Generating Prescriptions")

# # ----------------------------------------------------------
# # Load Medical Records
# # ----------------------------------------------------------

# medical_records = (
#     supabase
#     .table("medical_records")
#     .select("*")
#     .execute()
#     .data
# )

# # ----------------------------------------------------------
# # Load Medicines
# # ----------------------------------------------------------

# medicines = (
#     supabase
#     .table("medicines")
#     .select("id,name")
#     .execute()
#     .data
# )

# medicine_lookup = {
#     medicine["name"]: medicine["id"]
#     for medicine in medicines
# }

# # ----------------------------------------------------------
# # Existing Prescriptions
# # ----------------------------------------------------------

# existing = (
#     supabase
#     .table("prescriptions")
#     .select("medical_record_uuid")
#     .execute()
#     .data
# )

# already_done = {
#     row["medical_record_uuid"]
#     for row in existing
# }

# # ----------------------------------------------------------
# # Generate
# # ----------------------------------------------------------

# prescriptions = []

# generated = 0
# skipped = 0

# for record in medical_records:

#     if record["id"] in already_done:
#         skipped += 1
#         continue

#     diagnosis = record["diagnosis"]

#     if diagnosis not in MEDICAL_KNOWLEDGE:
#         continue

#     knowledge = MEDICAL_KNOWLEDGE[diagnosis]

#     prescribed_date = (
#         record["created_at"][:10]
#         if record.get("created_at")
#         else date.today().isoformat()
#     )

#     for med in knowledge["medicines"]:

#         medicine_id = medicine_lookup.get(
#             med["name"]
#         )

#         if medicine_id is None:
#             print(
#                 f"Medicine not found -> {med['name']}"
#             )
#             continue

#         prescriptions.append(

#             {

#                 "medical_record_uuid": record["id"],

#                 "medicine_id": medicine_id,

#                 "dosage": med["dosage"],

#                 "frequency": med["frequency"],

#                 "duration": med["duration"],

#                 "instructions": med.get(
#                     "instructions"
#                 ),

#                 "prescribed_date": prescribed_date

#             }

#         )

#         generated += 1

# # ----------------------------------------------------------
# # Upload
# # ----------------------------------------------------------

# print()
# print("=" * 60)
# print("Prescription Summary")
# print("=" * 60)

# print(f"Generated : {generated}")
# print(f"Skipped   : {skipped}")

# if prescriptions:

#     response = (
#         supabase
#         .table("prescriptions")
#         .insert(prescriptions)
#         .execute()
#     )

#     print(
#         f"Inserted {len(response.data)} prescriptions."
#     )

# else:

#     print("No new prescriptions to insert.")

# print_header("Part 6 Complete")

# ==========================================================
# PART 7
# Lab Report Generation
# ==========================================================

# print_header("Generating Lab Reports")

# # ----------------------------------------------------------
# # Load Medical Records
# # ----------------------------------------------------------

# medical_records = (

#     supabase
#     .table("medical_records")
#     .select("*")
#     .execute()
#     .data

# )

# # ----------------------------------------------------------
# # Existing Reports
# # ----------------------------------------------------------

# existing_reports = (

#     supabase
#     .table("lab_reports")
#     .select("medical_record_uuid, report_name")
#     .execute()
#     .data

# )

# existing_keys = {

#     (
#         row["medical_record_uuid"],
#         row["report_name"]
#     )

#     for row in existing_reports

# }

# # ----------------------------------------------------------
# # Generate Reports
# # ----------------------------------------------------------

# lab_reports = []

# generated = 0
# skipped = 0

# for record in medical_records:

#     diagnosis = record["diagnosis"]

#     if diagnosis not in MEDICAL_KNOWLEDGE:
#         continue

#     knowledge = MEDICAL_KNOWLEDGE[diagnosis]

#     labs = knowledge.get("labs", [])

#     if len(labs) == 0:
#         continue

#     created_at = (

#         record["created_at"]

#         if record.get("created_at")

#         else datetime.now().isoformat()

#     )

#     for report_name in labs:

#         key = (
#             record["id"],
#             report_name
#         )

#         if key in existing_keys:
#             skipped += 1
#             continue

#         # ------------------------------------------
#         # Fake report location
#         # ------------------------------------------

#         safe_name = (

#             report_name
#             .replace(" ", "_")
#             .replace("/", "_")

#         )

#         report_url = (
#             f"reports/{safe_name}/{record['id']}.pdf"
#         )

#         lab_reports.append(

#             {

#                 "medical_record_uuid": record["id"],

#                 "report_name": report_name,

#                 "report_url": report_url,

#                 "created_at": created_at

#             }

#         )

#         generated += 1

# # ----------------------------------------------------------
# # Upload
# # ----------------------------------------------------------

# print()

# print("=" * 60)
# print("Lab Report Summary")
# print("=" * 60)

# print(f"Generated : {generated}")
# print(f"Skipped   : {skipped}")

# if lab_reports:

#     response = (

#         supabase
#         .table("lab_reports")
#         .insert(lab_reports)
#         .execute()

#     )

#     print(
#         f"Inserted {len(response.data)} lab reports."
#     )

# else:

#     print(
#         "No new lab reports to insert."
#     )

# print_header("Part 7 Complete")