from __future__ import annotations

import pandas as pd
import streamlit as st

from services.supabase_service import SupabaseService


class AnalyticsService:
    """
    Provides all analytics used throughout the Admin Dashboard.

    Every graph, KPI and insight should obtain its data from this
    service instead of querying Supabase directly inside Streamlit.
    """

    def __init__(self):

        self.supabase = SupabaseService.get_client()

    # ==========================================================
    # Base Table Loaders
    # ==========================================================

    @st.cache_data(ttl=300)
    def get_patients(_self) -> pd.DataFrame:

        data = (
            _self.supabase
            .table("patients")
            .select("*")
            .execute()
            .data
        )

        df = pd.DataFrame(data)

        if not df.empty and "dob" in df.columns:
            df["dob"] = pd.to_datetime(df["dob"])

        return df

    @st.cache_data(ttl=300)
    def get_doctors(_self) -> pd.DataFrame:

        data = (
            _self.supabase
            .table("doctors")
            .select("*")
            .execute()
            .data
        )
        #print("getdoctor")
        #print("=" * 60)
        #print(data)
        #print("=" * 60)

        df = pd.DataFrame(data)
        #print(df.columns.tolist())
        #print(df.head())

        return df

    @st.cache_data(ttl=300)
    def get_appointments(_self) -> pd.DataFrame:
        #print("GETAPPOINTMENTANALYTICSSERVICE")
        session = _self.supabase.auth.get_session()
        client = SupabaseService.get_client()
        #print("CLIENT SESSION:", client.auth.get_session())
        #print("=" * 60)
        #print("SESSION:", session)
        #print("USER:", _self.supabase.auth.get_user())
        #print("=" * 60)
        response = (
            _self.supabase
            .table("appointments")
            .select("*")
            .execute()
        )

        #print("\n========== RAW RESPONSE ==========")
        #print(response)
        #print("==================================")

        data = response.data

        df = pd.DataFrame(data)

        #print("\n========== DATAFRAME ==========")
        #print(df.columns.tolist())
        #print(df.head())
        #print(df.shape)
        #print("================================")

        #print("\n========== SESSION ==========")
        #print(_self.supabase.auth.get_session())
        #print("================================")

        #print("\n========== CLIENT ID ==========")
        #print("ANALYTICS CLIENT:", id(_self.supabase))
        #print("================================")

        if df.empty:
            return df

        df["appointment_date"] = pd.to_datetime(df["appointment_date"])

        return df
    

    @st.cache_data(ttl=300)
    def get_doctor_availability(_self) -> pd.DataFrame:

        data = (
            _self.supabase
            .table("doctor_availability")
            .select("*")
            .execute()
            .data
        )

        return pd.DataFrame(data)

    def get_summary_text(self) -> str:

        kpi = self.get_dashboard_kpis()

        status = self.get_status_distribution()

        top_status = status.sort_values(
            "Count",
            ascending=False
        ).iloc[0]["Status"]

        return (
            f"The system currently contains "
            f"{kpi['patients']} patients, "
            f"{kpi['doctors']} doctors and "
            f"{kpi['appointments']} appointments.\n\n"

            f"Most appointments are **{top_status}**.\n\n"

            f"Completed appointments: **{kpi['completed']}**\n"
            f"Pending appointments: **{kpi['pending']}**\n"
            f"Confirmed appointments: **{kpi['confirmed']}**\n"
            f"Cancelled appointments: **{kpi['cancelled']}**."
        )

    def get_highlight_text(self) -> str:

        appointments = self.get_appointments()
        #print("=====================")        
        #print(appointments)
        #print(appointments.columns)
        #print("=====================")

        if appointments.empty:
            return "No appointment data available."

        doctors = self.get_doctors()

        merged = appointments.merge(
            doctors[
                [
                    "id",
                    "specialization"
                ]
            ],
            left_on="doctor_id",
            right_on="id",
            how="left"
        )

        workload = (
            merged["specialization"]
            .value_counts()
        )

        top_specialization = workload.idxmax()
        total = workload.max()

        completion = (
            appointments["status"] == "Completed"
        ).sum()

        completion_rate = round(
            completion * 100 / len(appointments),
            1
        )

        return (
            f"🏆 **{top_specialization}** currently has the highest workload "
            f"with **{total} appointments**.\n\n"
            f"Overall appointment completion rate is **{completion_rate}%**."
        )

    # ==========================================================
    # Dashboard KPIs
    # ==========================================================

    def get_dashboard_kpis(self):

        patients = self.get_patients()
        doctors = self.get_doctors()
        appointments = self.get_appointments()

        completed = (
            appointments["status"] == "Completed"
        ).sum()

        pending = (
            appointments["status"] == "Pending"
        ).sum()

        confirmed = (
            appointments["status"] == "Confirmed"
        ).sum()

        cancelled = (
            appointments["status"] == "Cancelled"
        ).sum()

        completion_rate = 0

        if len(appointments) > 0:

            completion_rate = round(
                completed * 100 / len(appointments),
                1
            )

        return {

            "patients": len(patients),

            "doctors": len(doctors),

            "appointments": len(appointments),

            "completed": completed,

            "pending": pending,

            "confirmed": confirmed,

            "cancelled": cancelled,

            "completion_rate": completion_rate

        }

    # ==========================================================
    # Patient Analytics
    # ==========================================================

    def get_age_distribution(self):

        patients = self.get_patients()

        if patients.empty:
            return pd.DataFrame()

        today = pd.Timestamp.today()

        patients["Age"] = (
            (
                today - patients["dob"]
            ).dt.days // 365
        )

        return patients

    def get_blood_group_distribution(self):

        patients = self.get_patients()

        return (

            patients["blood_group"]

            .value_counts()

            .rename_axis("Blood Group")

            .reset_index(name="Patients")

        )

    def get_average_height(self):

        patients = self.get_patients()

        return round(
            patients["height_cm"].mean(),
            2
        )

    def get_average_weight(self):

        patients = self.get_patients()

        return round(
            patients["weight_kg"].mean(),
            2
        )

    # ==========================================================
    # Appointment Analytics
    # ==========================================================

    def get_status_distribution(self):

        appointments = self.get_appointments()

        return (

            appointments["status"]

            .value_counts()

            .rename_axis("Status")

            .reset_index(name="Count")

        )

    def get_daily_appointments(self):

        appointments = self.get_appointments()

        return (

            appointments

            .groupby("appointment_date")

            .size()

            .reset_index(name="Appointments")

        )

    def get_weekday_distribution(self):

        appointments = self.get_appointments()

        appointments["Weekday"] = (

            appointments["appointment_date"]

            .dt.day_name()

        )

        order = [

            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"

        ]

        return (

            appointments

            .groupby("Weekday")

            .size()

            .reindex(order, fill_value=0)

            .reset_index(name="Appointments")

        )

    # ==========================================================
    # Dashboard Charts
    # ==========================================================

    def get_status_distribution(self) -> pd.DataFrame:

        appointments = self.get_appointments()

        return (
            appointments["status"]
            .value_counts()
            .rename_axis("Status")
            .reset_index(name="Count")
        )


    def get_daily_appointments(self) -> pd.DataFrame:

        appointments = self.get_appointments()

        appointments["appointment_date"] = pd.to_datetime(
            appointments["appointment_date"]
        )

        return (
            appointments
            .groupby("appointment_date")
            .size()
            .reset_index(name="Appointments")
        )


    def get_specialization_distribution(self) -> pd.DataFrame:

        appointments = self.get_appointments()
        doctors = self.get_doctors()

        merged = appointments.merge(
            doctors[["id", "specialization"]],
            left_on="doctor_id",
            right_on="id"
        )

        return (
            merged
            .groupby("specialization")
            .size()
            .reset_index(name="Appointments")
            .rename(columns={"specialization":"Specialization"})
            .sort_values(
                "Appointments",
                ascending=False
            )
        )


    def get_doctor_workload(self) -> pd.DataFrame:

        appointments = self.get_appointments()
        doctors = self.get_doctors()

        merged = appointments.merge(
            doctors[
                [
                    "id",
                    "doctor_name",
                    "specialization"
                ]
            ],
            left_on="doctor_id",
            right_on="id",
            how="left"
        )

        return (
            merged
            .groupby(
                [
                    "doctor_name",
                    "specialization"
                ]
            )
            .size()
            .reset_index(name="Appointments")
            .rename(columns={
                "doctor_name": "Doctor",
                "specialization": "Specialization"
            })
            .sort_values(
                "Appointments",
                ascending=False
            )
        )


    def get_weekday_distribution(self) -> pd.DataFrame:

        appointments = self.get_appointments()

        appointments["appointment_date"] = pd.to_datetime(
            appointments["appointment_date"]
        )

        appointments["Weekday"] = (
            appointments["appointment_date"]
            .dt.day_name()
        )

        order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        result = (
            appointments["Weekday"]
            .value_counts()
            .reindex(order, fill_value=0)
            .rename_axis("Weekday")
            .reset_index(name="Appointments")
        )

        return result


    def get_status_by_specialization(self) -> pd.DataFrame:

        appointments = self.get_appointments()
        doctors = self.get_doctors()

        df = appointments.merge(
            doctors[["id", "specialization"]],
            left_on="doctor_id",
            right_on="id"
        )

        return (
            df.groupby(
                ["specialization", "status"]
            )
            .size()
            .reset_index(name="Count")
        )


    def get_top_doctors(self, limit: int = 10) -> pd.DataFrame:

        workload = self.get_doctor_workload()

        return workload.head(limit)


    def get_top_patients(self, limit=10):

        appointments = self.get_appointments()
        patients = self.get_patients()

        merged = appointments.merge(
            patients[
                [
                    "id",
                    "patient_name"
                ]
            ],
            left_on="patient_id",
            right_on="id",
            how="left"
        )

        return (
            merged
            .groupby("patient_name")
            .size()
            .reset_index(name="Appointments")
            .rename(columns={
                "patient_name": "Patient"
            })
            .sort_values(
                "Appointments",
                ascending=False
            )
            .head(limit)
        )


    # ==========================================================
    # Insight Cards
    # ==========================================================

    def get_insights(self) -> dict:

        appointments = self.get_appointments()

        appointments["appointment_date"] = pd.to_datetime(
            appointments["appointment_date"]
        )

        today = pd.Timestamp.today().normalize()

        upcoming = len(
            appointments[
                appointments["appointment_date"] >= today
            ]
        )

        completed = (
            appointments["status"] == "Completed"
        ).sum()

        cancelled = (
            appointments["status"] == "Cancelled"
        ).sum()

        completion_rate = (
            completed / len(appointments) * 100
            if len(appointments)
            else 0
        )

        busiest_day = (
            appointments["appointment_date"]
            .value_counts()
            .idxmax()
        )

        busiest_count = (
            appointments["appointment_date"]
            .value_counts()
            .max()
        )

        return {

            "upcoming": upcoming,

            "completion_rate": round(
                completion_rate,
                2
            ),

            "cancelled": cancelled,

            "busiest_day": busiest_day,

            "busiest_count": busiest_count

        }


    def get_specialization_workload(self) -> pd.DataFrame:
        """
        Appointment count grouped by doctor specialization.
        """

        appointments = self.get_appointments()
        doctors = self.get_doctors()

        merged = appointments.merge(
            doctors[
                [
                    "id",
                    "specialization"
                ]
            ],
            left_on="doctor_id",
            right_on="id",
            how="left"
        )

        return (
            merged
            .groupby("specialization")
            .size()
            .reset_index(name="Appointments")
            .sort_values(
                "Appointments",
                ascending=False
            )
        )


    def get_top_doctors(self, limit=10):

        appointments = self.get_appointments()
        doctors = self.get_doctors()

        merged = appointments.merge(
            doctors[
                [
                    "id",
                    "doctor_name"
                ]
            ],
            left_on="doctor_id",
            right_on="id",
            how="left"
        )

        return (
            merged
            .groupby("doctor_name")
            .size()
            .reset_index(name="Patients")
            .rename(columns={
                "doctor_name": "Doctor"
            })
            .sort_values(
                "Patients",
                ascending=False
            )
            .head(limit)
        )


    def get_weekday_distribution(self) -> pd.DataFrame:
        """
        Appointments grouped by weekday.
        """

        appointments = self.get_appointments().copy()

        appointments["appointment_date"] = pd.to_datetime(
            appointments["appointment_date"]
        )

        appointments["Weekday"] = appointments[
            "appointment_date"
        ].dt.day_name()

        order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        result = (
            appointments
            .groupby("Weekday")
            .size()
            .reindex(order, fill_value=0)
            .reset_index(name="Appointments")
        )

        return result


    def get_insights(self) -> list[str]:
        """
        Generate quick insights for the dashboard.
        """

        appointments = self.get_appointments()
        doctors = self.get_doctors()

        insights = []

        status_counts = appointments["status"].value_counts()

        completed = int(status_counts.get("Completed", 0))
        pending = int(status_counts.get("Pending", 0))
        confirmed = int(status_counts.get("Confirmed", 0))
        cancelled = int(status_counts.get("Cancelled", 0))

        insights.append(
            f"Completed appointments account for **{completed}** visits."
        )

        insights.append(
            f"There are **{pending + confirmed}** upcoming appointments requiring attention."
        )

        merged = appointments.merge(
            doctors[
                [
                    "id",
                    "specialization"
                ]
            ],
            left_on="doctor_id",
            right_on="id"
        )

        top_specialization = (
            merged["specialization"]
            .value_counts()
            .idxmax()
        )

        top_count = (
            merged["specialization"]
            .value_counts()
            .max()
        )

        insights.append(
            f"**{top_specialization}** currently has the highest workload with **{top_count} appointments**."
        )

        return insights

    def get_doctors_per_specialization(self):

        doctors = self.get_doctors()

        return (
            doctors["specialization"]
            .value_counts()
            .rename_axis("Specialization")
            .reset_index(name="Doctors")
        )


    def get_medical_record_kpis(self) -> dict:
        """
        Dashboard KPIs for Medical Records.
        """

        client = self.supabase

        total_records = (
            client.table("medical_records")
            .select("id", count="exact")
            .execute()
            .count
        )

        followups = (
            client.table("medical_records")
            .select("id", count="exact")
            .eq("follow_up_required", True)
            .execute()
            .count
        )

        diagnoses = (
            client.table("medical_records")
            .select("diagnosis")
            .execute()
        )

        unique_diagnoses = len(
            {
                row["diagnosis"]
                for row in diagnoses.data
            }
        )

        doctors = (
            client.table("medical_records")
            .select("doctor_id")
            .execute()
        )

        unique_doctors = len(
            {
                row["doctor_id"]
                for row in doctors.data
            }
        )

        return {

            "records": total_records,

            "followups": followups,

            "diagnoses": unique_diagnoses,

            "doctors": unique_doctors

        }

    def get_diagnosis_distribution(self):
        """
        Diagnosis frequency distribution.
        """

        query = (
            self.supabase
            .table("medical_records")
            .select("diagnosis")
            .execute()
        )

        import pandas as pd

        df = pd.DataFrame(query.data)

        if df.empty:
            return df

        return (
            df["diagnosis"]
            .value_counts()
            .rename_axis("Diagnosis")
            .reset_index(name="Cases")
        )

    def get_records_per_specialization(self) -> pd.DataFrame:
        """
        Medical records grouped by doctor's specialization.
        """

        records = (
            self.supabase
            .table("medical_records")
            .select("doctor_id")
            .execute()
            .data
        )

        doctors = self.get_doctors()

        df = pd.DataFrame(records)

        if df.empty:
            return df

        merged = df.merge(
            doctors[["id", "specialization"]],
            left_on="doctor_id",
            right_on="id",
            how="left"
        )

        return (
            merged
            .groupby("specialization")
            .size()
            .reset_index(name="Records")
            .rename(columns={
                "specialization": "Specialization"
            })
            .sort_values(
                "Records",
                ascending=False
            )
        )

    def get_records_per_doctor(self) -> pd.DataFrame:
        """
        Medical records created by each doctor.
        """

        records = (
            self.supabase
            .table("medical_records")
            .select("doctor_id")
            .execute()
            .data
        )

        doctors = self.get_doctors()

        df = pd.DataFrame(records)

        if df.empty:
            return df

        merged = df.merge(
            doctors[
                [
                    "id",
                    "doctor_name"
                ]
            ],
            left_on="doctor_id",
            right_on="id",
            how="left"
        )

        return (
            merged
            .groupby("doctor_name")
            .size()
            .reset_index(name="Records")
            .rename(columns={
                "doctor_name": "Doctor"
            })
            .sort_values(
                "Records",
                ascending=False
            )
        )

    def get_followup_distribution(self) -> pd.DataFrame:
        """
        Distribution of records requiring follow-up.
        """

        records = (
            self.supabase
            .table("medical_records")
            .select("follow_up_required")
            .execute()
            .data
        )

        df = pd.DataFrame(records)

        if df.empty:
            return df

        df["Status"] = df["follow_up_required"].map({
            True: "Follow-up Required",
            False: "No Follow-up"
        })

        return (
            df["Status"]
            .value_counts()
            .rename_axis("Status")
            .reset_index(name="Records")
        )

    def get_doctor_followup_stats(self) -> pd.DataFrame:
        """
        Total records vs follow-ups per doctor.
        """

        records = (
            self.supabase
            .table("medical_records")
            .select(
                "doctor_id,"
                "follow_up_required"
            )
            .execute()
            .data
        )

        doctors = self.get_doctors()

        df = pd.DataFrame(records)

        if df.empty:
            return df

        merged = df.merge(
            doctors[
                [
                    "id",
                    "doctor_name"
                ]
            ],
            left_on="doctor_id",
            right_on="id",
            how="left"
        )

        result = (
            merged
            .groupby("doctor_name")
            .agg(
                Total_Records=("doctor_id", "count"),
                Followups=("follow_up_required", "sum")
            )
            .reset_index()
            .rename(columns={
                "doctor_name": "Doctor"
            })
            .sort_values(
                "Followups",
                ascending=False
            )
        )

        return result

    def get_records_per_patient(self) -> pd.DataFrame:
        """
        Medical records grouped by patient.
        """

        records = (
            self.supabase
            .table("medical_records")
            .select("patient_id")
            .execute()
            .data
        )

        patients = self.get_patients()

        df = pd.DataFrame(records)

        if df.empty:
            return df

        merged = df.merge(
            patients[
                [
                    "id",
                    "patient_name"
                ]
            ],
            left_on="patient_id",
            right_on="id",
            how="left"
        )

        return (
            merged
            .groupby("patient_name")
            .size()
            .reset_index(name="Records")
            .rename(columns={
                "patient_name": "Patient"
            })
            .sort_values(
                "Records",
                ascending=False
            )
        )

    def get_upcoming_followups(self) -> pd.DataFrame:
        """
        Patients requiring follow-up.
        """

        records = (
            self.supabase
            .table("medical_records")
            .select("*")
            .eq("follow_up_required", True)
            .execute()
            .data
        )

        df = pd.DataFrame(records)

        if df.empty:
            return df

        patients = self.get_patients()

        doctors = self.get_doctors()

        df = (
            df.merge(
                patients[
                    [
                        "id",
                        "patient_name"
                    ]
                ],
                left_on="patient_id",
                right_on="id",
                how="left"
            )
            .merge(
                doctors[
                    [
                        "id",
                        "doctor_name"
                    ]
                ],
                left_on="doctor_id",
                right_on="id",
                how="left",
                suffixes=("_patient", "_doctor")
            )
        )

        return (
            df[
                [
                    "patient_name",
                    "doctor_name",
                    "diagnosis",
                    "follow_up_date"
                ]
            ]
            .rename(columns={
                "patient_name": "Patient",
                "doctor_name": "Doctor",
                "diagnosis": "Diagnosis",
                "follow_up_date": "Follow-up Date"
            })
            .sort_values("Follow-up Date")
        )

    @st.cache_data(ttl=300)
    def get_medical_records(_self) -> pd.DataFrame:

        data = (
            _self.supabase
            .table("medical_records")
            .select("*")
            .execute()
            .data
        )

        return pd.DataFrame(data)

    # ==========================================================
# Medicine
# ==========================================================

    @st.cache_data(ttl=300)
    def get_medicines(_self) -> pd.DataFrame:

        data = (
            _self.supabase
            .table("medicines")
            .select("*")
            .execute()
            .data
        )

        return pd.DataFrame(data)


    # ==========================================================
    # Medicine Inventory
    # ==========================================================

    @st.cache_data(ttl=300)
    def get_medicine_inventory(_self) -> pd.DataFrame:

        data = (
            _self.supabase
            .table("medicine_inventory")
            .select("*")
            .execute()
            .data
        )

        return pd.DataFrame(data)


    # ==========================================================
    # Prescriptions
    # ==========================================================

    @st.cache_data(ttl=300)
    def get_prescriptions(_self) -> pd.DataFrame:

        data = (
            _self.supabase
            .table("prescriptions")
            .select("*")
            .execute()
            .data
        )

        return pd.DataFrame(data)


    # ==========================================================
    # Lab Reports
    # ==========================================================

    @st.cache_data(ttl=300)
    def get_lab_reports(_self) -> pd.DataFrame:

        data = (
            _self.supabase
            .table("lab_reports")
            .select("*")
            .execute()
            .data
        )

        return pd.DataFrame(data)

    def get_inventory_with_medicine(self):

        inventory = self.get_medicine_inventory()
        medicines = self.get_medicines()

        if inventory.empty:
            return inventory

        return inventory.merge(

            medicines[
                [
                    "id",
                    "name"
                ]
            ].rename(
    columns={
        "name": "Medicine"
    }
),

            left_on="medicine_id",
            right_on="id",
            how="left",

            suffixes=(
                "",
                "_medicine"
            )

        )

    def get_prescriptions_with_names(self):

        prescriptions = self.get_prescriptions()

        if prescriptions.empty:
            return prescriptions

        medicines = self.get_medicines()

        medical_records = self.get_medical_records()

        return (

            prescriptions

            .merge(

                medicines[
                    [
                        "id",
                        "name"
                    ]
                ].rename(columns={"name":"Medicine"}),

                left_on="medicine_id",
                right_on="id",
                how="left"

            )

            .merge(

                medical_records[
                    [
                        "id",
                        "diagnosis"
                    ]
                ].rename(columns={"diagnosis": "Diagnosis"}),

                left_on="medical_record_uuid",
                right_on="id",
                how="left",

                suffixes=(
                    "",
                    "_record"
                )

            )

        )

    def get_lab_reports_with_diagnosis(self):

        reports = self.get_lab_reports()

        if reports.empty:
            return reports

        medical_records = self.get_medical_records()

        return reports.merge(

            medical_records[
                [
                    "id",
                    "diagnosis"
                ]
            ].rename(
    columns={
        "diagnosis": "Diagnosis"
    }
),

            left_on="medical_record_uuid",
            right_on="id",
            how="left"

        )
