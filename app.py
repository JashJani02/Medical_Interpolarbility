import streamlit as st

st.set_page_config(
    page_title="Medical Interoperability Dashboard",
    page_icon="assets/medical_interporability_full_image.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏥 Medical Interoperability Dashboard")

st.markdown(
    """
Welcome to the **Medical Interoperability Admin Panel**.

This dashboard allows administrators to monitor and analyze the complete healthcare ecosystem.

### Available Modules

- 📊 Analytics Dashboard
- 👨‍⚕️ Doctor Management *(Coming Soon)*
- 🧑‍🤝‍🧑 Patient Management *(Coming Soon)*
- 📅 Appointment Management *(Coming Soon)*
- 📑 Reports *(Coming Soon)*
- ⚙️ Settings *(Coming Soon)*

---

👈 Use the **sidebar** to open the Analytics Dashboard.
"""
)

st.info(
    "This application is currently in Phase 1 of development. "
    "Only the Analytics Dashboard is available."
)