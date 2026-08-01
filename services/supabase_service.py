from __future__ import annotations

import streamlit as st
from supabase import Client, create_client
import tomllib
from pathlib import Path

class SupabaseService:
    """
    Singleton wrapper around the Supabase client.
    """

    _client: Client | None = None

    @classmethod
    def get_client(cls) -> Client:

        if cls._client is None:

            try:
                url = st.secrets["supabase"]["SUPABASE_URL"]
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
                key = secrets["supabase"]["SUPABASE_PUBLISHABLE_KEY"]

            print("CREATING CLIENT")
                
            cls._client = create_client(
                url,
                key
            )

            #print("SUPABASE SERVICE MODULE")
            #print("CLIENT SESSION")
            #print(cls._client.auth.get_session())

        return cls._client