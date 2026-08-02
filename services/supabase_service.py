from __future__ import annotations

import streamlit as st
from supabase import Client, create_client
import tomllib
from pathlib import Path

class SupabaseService:
    """
    Singleton wrapper around the Supabase client.

    NOTE (direct Google OAuth): authentication is now handled by Google OAuth
    inside the app (services/google_auth.py), not by Supabase Auth. Because
    all tables have RLS policies restricted to `authenticated` users, the app
    client uses the SERVICE ROLE key (server-side only, never exposed to the
    browser) so the dashboard can keep reading/writing data.
    """

    _client: Client | None = None

    @classmethod
    def get_client(cls) -> Client:

        if cls._client is None:

            try:
                url = st.secrets["supabase"]["SUPABASE_URL"]
                key = st.secrets["supabase"].get("SUPABASE_SERVICE_KEY")
                if not key:
                    key = st.secrets["supabase"]["SUPABASE_PUBLISHABLE_KEY"]

            except Exception:

                PROJECT_ROOT = Path(__file__).resolve().parent.parent
                SECRETS_FILE = PROJECT_ROOT / ".streamlit" / "secrets.toml"

                if not SECRETS_FILE.exists():
                    raise FileNotFoundError(
                        f"Could not find:\n{SECRETS_FILE}"
                    )

                secrets = tomllib.loads(SECRETS_FILE.read_text())

                url = secrets["supabase"]["SUPABASE_URL"]
                key = secrets["supabase"].get("SUPABASE_SERVICE_KEY")
                if not key:
                    key = secrets["supabase"]["SUPABASE_PUBLISHABLE_KEY"]

            print("CREATING CLIENT")

            cls._client = create_client(
                url,
                key
            )

        return cls._client