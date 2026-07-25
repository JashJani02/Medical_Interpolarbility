"""
===========================================================
Medical Interoperability Demo Database Seeder
Part 1 - Configuration & Helper Functions

Tech Stack
----------
- Python 3.11+
- Supabase
- Faker

Author:
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
    "Chest X-Ray",
    "ECG",
    "Liver Function Test",
    "Kidney Function Test",
    "Urine Analysis"

]

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

doctor_availability = (
    supabase
    .table("doctor_availability")
    .select("*")
    .execute()
    .data
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

print_header("Generating Appointments")

appointments = []

# Prevent doctor double-bookings
#
# Key:
# (doctor_id, appointment_date, appointment_time)
#
occupied_slots = set()


# ----------------------------------------------------------
# Utility
# ----------------------------------------------------------

def random_time_between(start_time, end_time):

    if isinstance(start_time, str):
        start_time = datetime.strptime(
            start_time,
            "%H:%M:%S"
        ).time()

    if isinstance(end_time, str):
        end_time = datetime.strptime(
            end_time,
            "%H:%M:%S"
        ).time()

    start_minutes = (
        start_time.hour * 60
        + start_time.minute
    )

    end_minutes = (
        end_time.hour * 60
        + end_time.minute
    )

    possible = list(
        range(
            start_minutes,
            end_minutes,
            30
        )
    )

    chosen = random.choice(possible)

    return time(
        chosen // 60,
        chosen % 60
    )


def next_matching_weekday(target_weekday):
    """
    Returns a date having the requested weekday.

    Example:
    Monday -> nearest Monday
    """

    today = date.today()

    offset = (target_weekday - today.weekday()) % 7

    return today + timedelta(days=offset)


# ----------------------------------------------------------
# Main Generator
# ----------------------------------------------------------

for patient in patients:

    used_doctors = set()

    patient_visits = 0

    while patient_visits < TOTAL_APPOINTMENTS_PER_PATIENT:

        # ------------------------------------------
        # Choose doctor
        # ------------------------------------------

        doctor = weighted_choice(doctors)

        if doctor["id"] in used_doctors:
            continue

        used_doctors.add(
            doctor["id"]
        )

        # ------------------------------------------
        # Availability
        # ------------------------------------------

        slots = availability_lookup.get(
            doctor["id"],
            []
        )

        if len(slots) == 0:
            continue

        slot = random.choice(slots)

        weekday_name = slot["weekday"]

        weekday_index = WEEKDAY_INDEX[
            weekday_name
        ]

        # ------------------------------------------
        # Appointment Date
        # ------------------------------------------

        visit_type = random.choices(

            ["past", "current", "future"],

            weights=[
                PAST_VISIT_WEIGHT,
                CURRENT_VISIT_WEIGHT,
                FUTURE_VISIT_WEIGHT
            ]

        )[0]

        base_date = next_matching_weekday(
            weekday_index
        )

        if visit_type == "past":

            appointment_date = (

                base_date
                - timedelta(
                    days=random.randint(7, 60)
                )

            )

        elif visit_type == "current":

            appointment_date = (

                base_date
                + timedelta(
                    days=random.randint(0, 5)
                )

            )

        else:

            appointment_date = (

                base_date
                + timedelta(
                    days=random.randint(7, 35)
                )

            )

        # ------------------------------------------
        # Appointment Time
        # ------------------------------------------

        appointment_time = random_time_between(

            slot["start_time"],
            slot["end_time"]

        )

        # ------------------------------------------
        # Prevent doctor double booking
        # ------------------------------------------

        key = (

            doctor["id"],
            appointment_date,
            appointment_time

        )

        if key in occupied_slots:
            continue

        occupied_slots.add(key)

        # ------------------------------------------
        # Status
        # ------------------------------------------

        status = random_status(
            appointment_date
        )

        # ------------------------------------------
        # Store
        # ------------------------------------------

        appointments.append(

            {

                "patient_id": patient["id"],

                "doctor_id": doctor["id"],

                "appointment_date": appointment_date.isoformat(),

                "appointment_time": appointment_time.strftime(
                    "%H:%M:%S"
                ),

                "status": status

            }

        )

        patient_visits += 1


print()

print(f"Appointments Generated : {len(appointments)}")

print(f"Doctor Slots Occupied  : {len(occupied_slots)}")

print_header("Uploading Appointments")

response = (
    supabase
    .table("appointments")
    .insert(appointments)
    .execute()
)

appointments = response.data
print(f"Inserted {len(appointments)} appointments.")

print_header("Part 2 Complete")

# ==========================================================
# PART 3
# Medical Record Generation
# ==========================================================

# print_header("Generating Medical Records")

# medical_records = []

# for appointment in appointments:

#     # Only completed appointments produce records
#     if appointment["status"] != "Completed":
#         continue

#     diagnosis = random.choice(DIAGNOSES)

#     complaint = fake.sentence(nb_words=8)

#     observations = fake.paragraph(nb_sentences=3)

#     follow_up = random.random() < 0.45

#     follow_up_date = None

#     if follow_up:

#         visit_date = date.fromisoformat(
#             appointment["appointment_date"]
#         )

#         follow_up_date = (
#             visit_date +
#             timedelta(
#                 days=random.randint(7, 30)
#             )
#         ).isoformat()

#     medical_records.append(

#         {

#             "appointment": appointment["id"],

#             "patient_id": appointment["patient_id"],

#             "doctor_id": appointment["doctor_id"],

#             "diagnosis": diagnosis,

#             "chief_complaint": complaint,

#             "observations": observations,

#             "follow_up_required": follow_up,

#             "follow_up_date": follow_up_date

#         }

#     )

# print()

# print(f"Medical Records Generated : {len(medical_records)}")

# response = (
#     supabase
#     .table("medical_records")
#     .insert(medical_records)
#     .execute()
# )

# medical_records = response.data
# print(f"Inserted {len(medical_records)} medical records.")
# print_header("Part 3 Complete")