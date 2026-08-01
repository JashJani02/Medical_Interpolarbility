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


def _get_redirect_url() -> str:
    """Resolve the OAuth redirect URL.

    Priority: SUPABASE_REDIRECT_URL (local dev) -> SUPABASE_REDIRECT_URL_prod.
    Read from st.secrets, falling back to .streamlit/secrets.toml.
    """

    for key in ("SUPABASE_REDIRECT_URL", "SUPABASE_REDIRECT_URL_prod"):
        try:
            url = st.secrets["supabase"].get(key)
        except Exception:
            url = None
        if url:
            return url

    if not SECRET_FILE.exists():
        raise RuntimeError(
            "Missing .streamlit/secrets.toml. Create it with [supabase] "
            "SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY and SUPABASE_REDIRECT_URL(_prod). "
            "See the setup steps in the README."
        )

    secrets = tomllib.loads(SECRET_FILE.read_text())

    for key in ("SUPABASE_REDIRECT_URL", "SUPABASE_REDIRECT_URL_prod"):
        url = secrets["supabase"].get(key)
        if url:
            return url

    raise RuntimeError(
        "No SUPABASE_REDIRECT_URL set in .streamlit/secrets.toml."
    )

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
    # OAuth Redirect URL
    # =====================================================

    def get_redirect_url(self) -> str:
        return _get_redirect_url()

    # =====================================================
    # Google Login
    # =====================================================

    def login(self):

        credentials = SignInWithOAuthCredentials(
            provider="google",
            options=SignInWithOAuthCredentialsOptions(
                redirect_to=_get_redirect_url()
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