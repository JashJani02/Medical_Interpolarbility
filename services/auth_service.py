from __future__ import annotations

import streamlit as st

from services.google_auth import (
    GoogleAuthenticator,
    get_redirect_uri,
)
from services.session import SessionManager


class AuthService:

    """
    Handles:

    - Google OAuth Login (direct, in-app — no Supabase intermediary)
    - Current Session
    - Current User
    - Logout
    """

    def __init__(self):

        self.google = GoogleAuthenticator()

    # =====================================================
    # OAuth Redirect URL
    # =====================================================

    def get_redirect_url(self) -> str:
        return get_redirect_uri()

    # =====================================================
    # Google Login
    # =====================================================

    def login(self):

        auth_url = self.google.get_auth_url()

        if auth_url:

            st.markdown(
                f'<meta http-equiv="refresh" content="0; url={auth_url}">',
                unsafe_allow_html=True,
            )

            st.stop()

        raise RuntimeError(
            "Unable to generate Google OAuth URL."
        )

    # =====================================================
    # OAuth Callback (exchange the ?code= param)
    # =====================================================

    def exchange_code(self, code: str) -> dict | None:

        return self.google.exchange_code(code)

    # =====================================================
    # Current User
    # =====================================================

    def get_user(self):

        return SessionManager.get_user()

    # =====================================================
    # Admin Record (session only; allowlist is the gate)
    # =====================================================

    def get_admin(self):

        return SessionManager.get_admin()

    # =====================================================
    # Logout
    # =====================================================

    def logout(self):

        self.google.logout()

        SessionManager.logout()

        st.rerun()
