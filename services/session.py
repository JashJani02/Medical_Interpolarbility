from __future__ import annotations

import streamlit as st


class SessionManager:
    """
    Centralized Streamlit session management.

    Stores UI/application state only.
    Authentication itself is handled by Supabase Auth.
    """

    # =====================================================
    # Initialize Session
    # =====================================================

    @staticmethod
    def initialize():

        defaults = {

            "logged_in": False,

            "user": None,

            "admin": None,

            "initialized": False

        }

        for key, value in defaults.items():

            if key not in st.session_state:

                st.session_state[key] = value

    # =====================================================
    # Login
    # =====================================================

    @staticmethod
    def login(user, admin=None):

        st.session_state.logged_in = True

        st.session_state.user = user

        st.session_state.admin = admin

        st.session_state.initialized = True

    # =====================================================
    # Logout
    # =====================================================

    @staticmethod
    def logout():

        for key in list(st.session_state.keys()):

            del st.session_state[key]

    # =====================================================
    # Getters
    # =====================================================

    @staticmethod
    def is_logged_in():

        return st.session_state.get(
            "logged_in",
            False
        )

    @staticmethod
    def get_user():

        return st.session_state.get(
            "user"
        )

    @staticmethod
    def get_admin():

        return st.session_state.get(
            "admin"
        )

    # =====================================================
    # Require Login
    # =====================================================

    @staticmethod
    def require_login():

        if not SessionManager.is_logged_in():

            st.warning(
                "Please login first."
            )

            st.switch_page(
                "pages/1_login.py"
            )

            st.stop()

    @staticmethod
    def get_user_id():

        user = SessionManager.get_user()

        if user is None:

            return None

        return user.id

    @staticmethod
    def get_email():

        user = SessionManager.get_user()

        if user is None:

            return None

        return user.email

    @staticmethod
    def get_name():

        user = SessionManager.get_user()

        if user is None:

            return None

        metadata = user.user_metadata or {}

        return (

            metadata.get("full_name")

            or metadata.get("name")

            or user.email

        )

#print("SUPABASE SERVICE MODULE")
#print(__name__)
#print(__file__)