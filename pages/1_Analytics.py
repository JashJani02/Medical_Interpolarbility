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
# PATIENT DEMOGRAPHICS
# ==========================================================
st.header("🧑‍🤝‍🧑 Patient Demographics")

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

st.divider()

# ==========================================================
# PATIENT ACTIVITY
# ==========================================================
st.header("👥 Patient Activity")

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
# DATABASE TABLES
# ==========================================================
st.subheader("🗄 Database Explorer")

patients_tab, doctors_tab, appointments_tab, availability_tab = st.tabs(
    ["Patients", "Doctors", "Appointments", "Doctor Availability"]
)

with patients_tab:
    st.dataframe(analytics.get_patients(), use_container_width=True, hide_index=True)
with doctors_tab:
    st.dataframe(analytics.get_doctors(), use_container_width=True, hide_index=True)
with appointments_tab:
    st.dataframe(analytics.get_appointments(), use_container_width=True, hide_index=True)
with availability_tab:
    st.dataframe(analytics.get_doctor_availability(), use_container_width=True, hide_index=True)

st.divider()

# ==========================================================
# FOOTER
# ==========================================================
st.caption("Medical Interoperability Dashboard • Analytics Module • Phase 1")