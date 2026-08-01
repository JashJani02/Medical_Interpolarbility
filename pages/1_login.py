# this will be in place of 1_Login.py after the admin panel/ project management sub-module is functional
from __future__ import annotations

import streamlit as st

from services.auth_service import AuthService
from services.session import SessionManager
from services.supabase_service import SupabaseService

client = SupabaseService.get_client()
#print("APP SESSION")
#print(client.auth.get_session())

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Admin Login",
    page_icon="🔐",
    layout="centered"
)

auth = AuthService()

params = st.query_params
#print("Query Params:", dict(st.query_params))

if "code" in params:

    try:

        result = auth.supabase.auth.exchange_code_for_session(
            {"auth_code": params["code"]}
        )

        #print("LOGIN CLIENT:", id(auth.supabase))

        #print("===========================================================")
        #print("Exchange Result:", result)
        #print("\n\nSession after exchange:", auth.supabase.auth.get_session(),"\n\n")
        #print("User after exchange:", auth.get_user())
        #print("===========================================================")

        user = auth.get_user()

        if user:

            admin = auth.get_admin()

            if admin is None:

                auth.register_admin()

                admin = auth.get_admin()

            SessionManager.login(
                user=user,
                admin=admin
            )

            #print("AFTER SESSIONMANAGER.LOGIN")
            #print(auth.supabase.auth.get_session(),"\n\n")

            st.query_params.clear()

            #print("SESSION STATE BEFORE SWITCH PAGE")  
            #print(st.session_state)      
            st.switch_page("app.py")

        st.stop()

    except Exception as e:

        st.exception(e)
        st.stop()

SessionManager.initialize()

if SessionManager.is_logged_in():
    st.switch_page("app.py")
# ==========================================================
# Login UI
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

    if st.button(
        "🔑 Continue with Google",
        use_container_width=True,
        type="primary"
    ):

        try:
           # print("==============================")
           # print("Before login:")
           # print(auth.supabase.auth.get_session())
            #print(st.session_state)
            auth.login()
            #print("After redirect:")
            #print(st.session_state)
            #print("===============================")
        except Exception as e:

            st.error("Google Authentication is not configured yet.")

            with st.expander("Developer Details"):

                st.code(str(e))

st.divider()

st.caption(
    "Medical Interoperability Platform • Administrator Portal"
)