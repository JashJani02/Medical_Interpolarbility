from __future__ import annotations

import streamlit as st
from supabase_auth import (
    SignInWithOAuthCredentials,
    SignInWithOAuthCredentialsOptions,
    Provider
)
from services.supabase_service import SupabaseService

from pathlib import Path
import tomllib

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SECRET_FILE = PROJECT_ROOT / ".streamlit" / "secrets.toml"

secrets = tomllib.loads(SECRET_FILE.read_text())

redirect = secrets["supabase"]["SUPABASE_REDIRECT_URL_prod"]

class AuthService:

    """
    Handles:

    - Google OAuth Login
    - Current Session
    - Current User
    - Admin Registration
    - Logout
    """

    def __init__(self):

        self.supabase = SupabaseService.get_client()

    # =====================================================
    # Google Login
    # =====================================================

    def login(self):

        credentials = SignInWithOAuthCredentials(
            provider="google",
            options=SignInWithOAuthCredentialsOptions(
                redirect_to=st.secrets["supabase"]["SUPABASE_REDIRECT_URL_prod"]
            )
        )

        response = self.supabase.auth.sign_in_with_oauth(credentials)

        #print("====================================")
        #print("RSPONSE URL",response.url)
        #print(st.secrets["supabase"]["SUPABASE_REDIRECT_URL_prod"])
        #print("=============================")
        if response.url:

            st.markdown(
                f'<meta http-equiv="refresh" content="0; url={response.url}">',
                unsafe_allow_html=True,
            )

            st.stop()

        raise RuntimeError(
            "Unable to generate Google OAuth URL."
        )

    # =====================================================
    # Current Session
    # =====================================================

    def get_session(self):

        return self.supabase.auth.get_session()

    # =====================================================
    # Current User
    # =====================================================

    def get_user(self):

        result = self.supabase.auth.get_user()

        if result is None or result.user is None:

            return None

        return result.user

    # =====================================================
    # Admin Exists?
    # =====================================================

    def admin_exists(self, user_id: str) -> bool:

        response = (

            self.supabase

            .table("admins")

            .select("id")

            .eq("id", user_id)

            .limit(1)

            .execute()

        )

        return len(response.data) > 0

    # =====================================================
    # Register Admin
    # =====================================================

    def register_admin(self):

        user = self.get_user()

        if user is None:

            return

        if self.admin_exists(user.id):

            return

        full_name = ""

        metadata = user.user_metadata or {}

        if "full_name" in metadata:

            full_name = metadata["full_name"]

        elif "name" in metadata:

            full_name = metadata["name"]

        else:

            full_name = user.email

        response = (
    self.supabase
    .table("admins")
    .insert(
        {
            "id": user.id,
            "full_name": full_name,
            "email": user.email,
        }
    )
    .execute()
)

        #print("Admin Insert Response:")
        #print(response.data)

    # =====================================================
    # Logout
    # =====================================================

    def logout(self):

        self.supabase.auth.sign_out()

        for key in list(st.session_state.keys()):

            del st.session_state[key]

        st.rerun()

    # =====================================================
    # Get Admin Record
    # =====================================================

    def get_admin(self):

        user = self.get_user()

        if user is None:
            return None

        response = (
            self.supabase
            .table("admins")
            .select("*")
            .eq("id", user.id)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]