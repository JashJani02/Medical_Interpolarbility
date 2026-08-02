# Direct Google OAuth login (no Supabase Auth intermediary)
from __future__ import annotations

import streamlit as st

from services.auth_service import AuthService
from services.session import SessionManager

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Admin Login",
    page_icon="🔐",
    layout="centered"
)

auth = AuthService()

SessionManager.initialize()

# ==========================================================
# 1) Already logged in (session state or JWT cookie)
# ==========================================================

if SessionManager.is_logged_in():
    st.switch_page("app.py")

cached = auth.google.get_cached_user()
if cached and auth.google.is_allowed(cached["email"]):
    SessionManager.login(user=cached)
    st.query_params.clear()
    st.rerun()

# ==========================================================
# 2) OAuth callback: Google redirected back with ?code=...
# ==========================================================

params = st.query_params

code = params.get("code")
if code:

    if isinstance(code, list):
        code = code[0]

    try:

        user = auth.exchange_code(code)

        st.query_params.clear()

        if user and auth.google.is_allowed(user["email"]):

            # persist in a JWT cookie so login survives page refreshes
            auth.google.persist_user(user)

            SessionManager.login(user=user)

            # give the cookie component a moment to write before rerun
            import time
            time.sleep(1)

            st.rerun()

        else:

            st.error(
                "Access denied: your Google account is not an authorized "
                "administrator."
            )

        st.stop()

    except Exception as e:

        st.exception(e)
        st.stop()

# ==========================================================
# 3) Login UI
# ==========================================================

st.markdown("# 🔐 Admin Login")

st.markdown(
    """
Welcome to the **Medical Interoperability Admin Dashboard**.

Please sign in using your Google account.

Only authorized administrators will be allowed to access the dashboard.
    """
)

st.divider()

col1, col2, col3 = st.columns([1, 3, 1])

with col2:

    try:

        auth_url = auth.google.get_auth_url()

        st.link_button(
            "🔑 Continue with Google",
            auth_url,
            use_container_width=True,
            type="primary"
        )

    except Exception as e:

        st.error("Google Authentication is not configured yet.")

        with st.expander("Developer Details"):

            st.code(str(e))

st.divider()

st.caption(
    "Medical Interoperability Platform • Administrator Portal"
)
