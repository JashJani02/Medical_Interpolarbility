from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.analytics_service import AnalyticsService

# ==========================================================
# Page Configuration
# ==========================================================
st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

analytics = AnalyticsService()

st.title("📊 Analytics Dashboard")
st.caption("Complete system-wide analytics for the Medical Interoperability Platform.")
with st.expander("Dashboard Overview", expanded=False):

    st.markdown("""
This dashboard provides administrators with a centralized overview of the Medical
Interoperability Platform.

### What you'll find here

- **Appointment Analytics**
  - Scheduling trends, appointment lifecycle, completion rates and booking patterns.

- **Doctor & Specialization Analytics**
  - Doctor workload, department demand and specialization distribution.

- **Patient Analytics**
  - Patient demographics, blood group distribution and healthcare utilization.

- **Doctor Availability**
  - Current doctor schedules and staffing availability.

- **Medical Records Analytics**
  - Diagnosis trends, follow-up workload and clinical documentation statistics.

- **Database Explorer**
  - Direct access to every major table used throughout the system.

Every visualization is accompanied by automatically generated insights to help administrators identify trends quickly and make informed operational decisions.
""")
st.divider()


# ==========================================================
# Reusable pattern: title -> graph -> insight (st.info)
# Every chart section below follows this exact shape.
# ==========================================================
def render_graph(title: str, df: pd.DataFrame, empty_msg: str, chart_fn, insight_fn):
    st.markdown(f"##### {title}")
    if df is None or df.empty:
        st.info(empty_msg)
        return
    st.plotly_chart(chart_fn(df), use_container_width=True)
    try:
        st.info(insight_fn(df))
    except Exception:
        st.info("Insight unavailable for the current data.")


# ==========================================================
# KPI CARDS
# ==========================================================
kpi = analytics.get_dashboard_kpis()

r1 = st.columns(5)
r1[0].metric("👥 Patients", kpi["patients"])
r1[1].metric("🩺 Doctors", kpi["doctors"])
r1[2].metric("📅 Appointments", kpi["appointments"])
r1[3].metric("✅ Completed", kpi["completed"])
r1[4].metric("📈 Completion rate", f"{kpi['completion_rate']}%")

r2 = st.columns(3)
r2[0].metric("🟡 Pending", kpi["pending"])
r2[1].metric("🔵 Confirmed", kpi["confirmed"])
r2[2].metric("🔴 Cancelled", kpi["cancelled"])

st.divider()

# ==========================================================
# APPOINTMENT ANALYTICS
# ==========================================================
st.header("📅 Appointment Analytics")
st.caption(
    "Monitor appointment activity across the platform, including scheduling trends, "
    "appointment completion, weekday booking patterns, and specialization demand."
)

status_df = analytics.get_status_distribution()
render_graph(
    "Appointment Status Distribution", status_df,
    "No appointment status data available.",
    chart_fn=lambda df: px.pie(df, names="Status", values="Count", hole=0.45),
    insight_fn=lambda df: (
        lambda top, total: f"**{top['Status']}** is the most common status — "
                            f"{top['Count']} of {total} appointments "
                            f"({round(top['Count'] * 100 / total, 1)}%)."
    )(df.sort_values("Count", ascending=False).iloc[0], df["Count"].sum())
)

daily_df = analytics.get_daily_appointments()
render_graph(
    "Daily Appointment Trend", daily_df,
    "No appointment date data available.",
    chart_fn=lambda df: px.line(df, x="appointment_date", y="Appointments", markers=True),
    insight_fn=lambda df: (
        lambda top: f"The busiest day so far was "
                    f"**{pd.Timestamp(top['appointment_date']).strftime('%b %d, %Y')}** "
                    f"with {top['Appointments']} appointments."
    )(df.sort_values("Appointments", ascending=False).iloc[0])
)

weekday_df = analytics.get_weekday_distribution()
render_graph(
    "Appointments by Weekday", weekday_df,
    "No weekday data available.",
    chart_fn=lambda df: px.bar(df, x="Weekday", y="Appointments"),
    insight_fn=lambda df: (
        lambda top: f"Most appointments were booked on **{top['Weekday']}** "
                    f"({top['Appointments']} total)."
    )(df.sort_values("Appointments", ascending=False).iloc[0])
)

status_spec_df = analytics.get_status_by_specialization()
render_graph(
    "Appointment Status by Specialization", status_spec_df,
    "No status-by-specialization data available.",
    chart_fn=lambda df: px.bar(
        df, x="specialization", y="Count", color="status", barmode="stack",
        labels={"specialization": "Specialization", "status": "Status"}
    ),
    insight_fn=lambda df: (
        lambda top: f"**{top['specialization']}** has the most **{top['status']}** "
                    f"appointments, with {top['Count']} recorded."
    )(df.sort_values("Count", ascending=False).iloc[0])
)

st.divider()

# ==========================================================
# DOCTOR & SPECIALIZATION ANALYTICS
# ==========================================================
st.header("🩺 Doctor & Specialization Analytics")
st.caption(
    "Understand doctor workload, specialization demand, and department utilization "
    "to support staffing and operational planning."
)

spec_dist_df = analytics.get_specialization_distribution()
render_graph(
    "Appointments by Specialization", spec_dist_df,
    "No specialization data available.",
    chart_fn=lambda df: px.bar(df, x="Specialization", y="Appointments", color="Appointments"),
    insight_fn=lambda df: (
        lambda top: f"**{top['Specialization']}** receives the most appointments "
                    f"({top['Appointments']})."
    )(df.sort_values("Appointments", ascending=False).iloc[0])
)

workload_df = analytics.get_doctor_workload()
render_graph(
    "Doctor Workload", workload_df,
    "No doctor workload data available.",
    chart_fn=lambda df: px.bar(df, x="Doctor", y="Appointments", color="Specialization"),
    insight_fn=lambda df: (
        lambda top: f"**{top['Doctor']}** ({top['Specialization']}) carries the "
                    f"heaviest caseload — {top['Appointments']} appointments."
    )(df.sort_values("Appointments", ascending=False).iloc[0])
)

doctors_per_spec_df = analytics.get_doctors_per_specialization()
render_graph(
    "Doctors per Specialization", doctors_per_spec_df,
    "No specialization roster data available.",
    chart_fn=lambda df: px.bar(df, x="Specialization", y="Doctors", color="Doctors"),
    insight_fn=lambda df: (
        lambda top: f"**{top['Specialization']}** has the most doctors on staff "
                    f"({top['Doctors']})."
    )(df.sort_values("Doctors", ascending=False).iloc[0])
)

top_doctors_df = analytics.get_top_doctors()
render_graph(
    "Most Active Doctors", top_doctors_df,
    "No doctor ranking data available.",
    chart_fn=lambda df: px.bar(df, x="Doctor", y=df.columns[-1], color=df.columns[-1]),
    insight_fn=lambda df: (
        lambda top, col: f"**{top['Doctor']}** ranks highest with {top[col]} {col.lower()}."
    )(df.sort_values(df.columns[-1], ascending=False).iloc[0], df.columns[-1])
)

st.divider()

# ==========================================================
# PATIENT ACTIVITY
# ==========================================================
st.header("👥 Patient Analytics")

st.caption(
    "Explore patient demographics, blood groups, age distribution, "
    "and healthcare utilization across the platform."
)

patients = analytics.get_patients()
if not patients.empty:
    avg_height = analytics.get_average_height()
    avg_weight = analytics.get_average_weight()
    m1, m2 = st.columns(2)
    m1.metric("📏 Average height", f"{avg_height} cm" if pd.notna(avg_height) else "—")
    m2.metric("⚖️ Average weight", f"{avg_weight} kg" if pd.notna(avg_weight) else "—")

age_df = analytics.get_age_distribution()
render_graph(
    "Patient Age Distribution", age_df,
    "No age data available.",
    chart_fn=lambda df: px.histogram(df, x="Age", nbins=20),
    insight_fn=lambda df: (
        f"The average patient age is **{df['Age'].mean():.0f} years**, "
        f"ranging from {int(df['Age'].min())} to {int(df['Age'].max())}."
    )
)

bg_df = analytics.get_blood_group_distribution()
render_graph(
    "Blood Group Distribution", bg_df,
    "No blood group data available.",
    chart_fn=lambda df: px.pie(df, names="Blood Group", values="Patients", hole=0.45),
    insight_fn=lambda df: (
        lambda top, total: f"**{top['Blood Group']}** is the most common blood group — "
                            f"{round(top['Patients'] * 100 / total, 1)}% of patients."
    )(df.sort_values("Patients", ascending=False).iloc[0], df["Patients"].sum())
)

top_patients_df = analytics.get_top_patients()
render_graph(
    "Most Frequent Patients", top_patients_df,
    "No patient activity data available.",
    chart_fn=lambda df: px.bar(df, x="Patient", y="Appointments", color="Appointments"),
    insight_fn=lambda df: (
        lambda top: f"**{top['Patient']}** has booked the most appointments "
                    f"({top['Appointments']})."
    )(df.sort_values("Appointments", ascending=False).iloc[0])
)

st.divider()

# ==========================================================
# DOCTOR AVAILABILITY
# ==========================================================
st.header("🗓️ Doctor Availability")
st.caption(
    "Review doctor schedules and availability to understand staffing capacity "
    "and appointment coverage."
)

availability_df = analytics.get_doctor_availability()
st.markdown("##### Scheduled Availability Slots")
if availability_df.empty:
    st.info("No availability schedules recorded yet.")
else:
    st.dataframe(availability_df, use_container_width=True, hide_index=True)
    try:
        slot_counts = availability_df["doctor_id"].value_counts()
        st.info(
            f"There are **{len(availability_df)}** availability slots defined across "
            f"**{availability_df['doctor_id'].nunique()}** doctors — the busiest doctor "
            f"has **{slot_counts.max()}** slots."
        )
    except Exception:
        st.info(f"There are **{len(availability_df)}** availability slots recorded.")

st.divider()

# ==========================================================
# MEDICAL RECORDS ANALYTICS
# ==========================================================
st.header("🩺 Medical Records Analytics")
st.caption(
    "Analyze diagnosis trends, clinical documentation, follow-up requirements, "
    "and patient medical history to monitor healthcare delivery."
)

medical_kpi = analytics.get_medical_record_kpis()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "📄 Medical Records",
    medical_kpi["records"]
)

c2.metric(
    "🧾 Diagnoses",
    medical_kpi["diagnoses"]
)

c3.metric(
    "🔔 Follow-ups",
    medical_kpi["followups"]
)

c4.metric(
    "👨‍⚕️ Doctors",
    medical_kpi["doctors"]
)

diagnosis_df = analytics.get_diagnosis_distribution()

render_graph(
    "Diagnosis Distribution",

    diagnosis_df,

    "No diagnosis data available.",

    chart_fn=lambda df: px.bar(
        df,
        x="Diagnosis",
        y="Cases",
        color="Cases"
    ),

    insight_fn=lambda df: (
        lambda top, total:
        f"**{top['Diagnosis']}** is the most common diagnosis with "
        f"{top['Cases']} medical records "
        f"({round(top['Cases'] * 100 / total,1)}%)."
    )(
        df.sort_values("Cases", ascending=False).iloc[0],
        df["Cases"].sum()
    )
)

spec_df = analytics.get_records_per_specialization()

render_graph(
    "Medical Records by Specialization",

    spec_df,

    "No specialization data available.",

    chart_fn=lambda df: px.bar(
        df,
        x="Specialization",
        y="Records",
        color="Records"
    ),

    insight_fn=lambda df: (
        lambda top:
        f"**{top['Specialization']}** has created the highest number "
        f"of medical records ({top['Records']})."
    )(
        df.sort_values(
            "Records",
            ascending=False
        ).iloc[0]
    )
)

doctor_df = analytics.get_records_per_doctor()

render_graph(
    "Medical Records by Doctor",

    doctor_df,

    "No doctor data available.",

    chart_fn=lambda df: px.bar(
        df,
        x="Doctor",
        y="Records",
        color="Records"
    ),

    insight_fn=lambda df: (
        lambda top:
        f"**{top['Doctor']}** has created the most medical records "
        f"({top['Records']})."
    )(
        df.sort_values(
            "Records",
            ascending=False
        ).iloc[0]
    )
)

followup_df = analytics.get_followup_distribution()

render_graph(
    "Follow-up Distribution",

    followup_df,

    "No follow-up data available.",

    chart_fn=lambda df: px.pie(
        df,
        names="Status",
        values="Records",
        hole=0.45
    ),

    insight_fn=lambda df: (
        lambda top, total:
        f"**{top['Status']}** accounts for "
        f"{top['Records']} of {total} medical records "
        f"({round(top['Records']*100/total,1)}%)."
    )(
        df.sort_values(
            "Records",
            ascending=False
        ).iloc[0],
        df["Records"].sum()
    )
)

doctor_followup_df = analytics.get_doctor_followup_stats()

render_graph(
    "Doctor Follow-up Workload",

    doctor_followup_df,

    "No doctor follow-up data available.",

    chart_fn=lambda df: px.bar(
        df,
        x="Doctor",
        y=[
            "Total_Records",
            "Followups"
        ],
        barmode="group"
    ),

    insight_fn=lambda df: (
        lambda top:
        f"**{top['Doctor']}** currently has the highest follow-up workload "
        f"with **{top['Followups']}** scheduled follow-ups."
    )(
        df.sort_values(
            "Followups",
            ascending=False
        ).iloc[0]
    )
)

patient_records_df = analytics.get_records_per_patient()

render_graph(
    "Medical Records per Patient",

    patient_records_df,

    "No patient medical records available.",

    chart_fn=lambda df: px.bar(
        df,
        x="Patient",
        y="Records",
        color="Records"
    ),

    insight_fn=lambda df: (
        lambda top:
        f"**{top['Patient']}** has the highest number of recorded medical visits ({top['Records']})."
    )(
        df.sort_values(
            "Records",
            ascending=False
        ).iloc[0]
    )
)

st.markdown("##### Upcoming Follow-ups")

followup_table = analytics.get_upcoming_followups()

if followup_table.empty:

    st.info("No follow-up appointments scheduled.")

else:

    st.dataframe(
        followup_table,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        f"There are **{len(followup_table)}** patients requiring follow-up care."
    )
st.divider()
# ==========================================================
# DATABASE TABLES
# ==========================================================
st.subheader("🗄 Database Explorer")
st.caption(
    "Browse the underlying database tables that power the analytics dashboard "
    "for auditing, verification, and manual inspection."
)

patients_tab, doctors_tab, availability_tab, appointments_tab, medical_tab = st.tabs(
    ["Patients","Doctors","Doctor Availability","Appointments","Medical Records",]
)

with patients_tab:
    st.dataframe(analytics.get_patients(), use_container_width=True, hide_index=True)
with doctors_tab:
    st.dataframe(analytics.get_doctors(), use_container_width=True, hide_index=True)
with availability_tab:
    st.dataframe(analytics.get_doctor_availability(), use_container_width=True, hide_index=True)
with appointments_tab:
    st.dataframe(analytics.get_appointments(), use_container_width=True, hide_index=True)
with medical_tab:
    st.dataframe(analytics.get_medical_records(),use_container_width=True,hide_index=True)

st.divider()

# ==========================================================
# FOOTER
# ==========================================================
st.caption("Medical Interoperability Dashboard • Analytics Module • Phase 1")