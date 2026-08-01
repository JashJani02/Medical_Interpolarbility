import streamlit as st
from services.session import SessionManager
from services.supabase_service import SupabaseService

client = SupabaseService.get_client()

#st.write(client.auth.get_session())

st.set_page_config(
    page_title="Medical Interoperability Dashboard",
    page_icon="assets/medical_interporability_full_image.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

SessionManager.initialize()

SessionManager.require_login()

st.title("🏥 Medical Interoperability Dashboard")

st.markdown(
    """
Welcome to the **Medical Interoperability Admin Panel**.

This dashboard allows administrators to monitor and analyze the complete healthcare ecosystem.

### Available Modules

- 📊 Analytics Dashboard
- 🛡️ Admin Panel (Project Management + Analytics Modules)
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