from __future__ import annotations

import os
from datetime import datetime, timedelta
from pathlib import Path
import tomllib

import jwt
from jwt import ExpiredSignatureError
import streamlit as st
import google_auth_oauthlib.flow
import extra_streamlit_components as stx
from googleapiclient.discovery import build

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SECRET_FILE = PROJECT_ROOT / ".streamlit" / "secrets.toml"

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
]


def _load_secrets() -> dict:
    """Read st.secrets, falling back to .streamlit/secrets.toml (local dev)."""
    try:
        return dict(st.secrets)
    except Exception:
        pass
    if SECRET_FILE.exists():
        return tomllib.loads(SECRET_FILE.read_text())
    return {}


def _google_section() -> dict:
    return _load_secrets().get("google", {})


def _auth_section() -> dict:
    return _load_secrets().get("auth", {})


# =============================================================
# Redirect URI resolution
# =============================================================

def get_redirect_uri() -> str:
    """Resolve the Google OAuth redirect URI.

    Priority:
      1. Explicit GOOGLE_REDIRECT_URI override in secrets
         (set this in the Streamlit Cloud dashboard to the prod URL)
      2. GOOGLE_REDIRECT_URI_prod when running on Streamlit Cloud
         (apps are mounted under /mount/src there)
      3. GOOGLE_REDIRECT_URI (local dev default)
      4. http://localhost:8501/login
    """

    google = _google_section()

    override = google.get("GOOGLE_REDIRECT_URI")
    if override:
        return override

    if os.path.exists("/mount/src"):
        return google.get(
            "GOOGLE_REDIRECT_URI_prod",
            "https://medical-interpolarbility.streamlit.app/login",
        )

    return google.get("GOOGLE_REDIRECT_URI", "http://localhost:8501/login")


def get_google_client_config() -> dict:
    """Build the Google OAuth client config dict from secrets.

    (Equivalent to the client_secret.json downloaded from Google Cloud Console,
    but read from st.secrets so no file needs to live in the repo.)
    """

    google = _google_section()
    redirect = get_redirect_uri()

    return {
        "web": {
            "client_id": google["GOOGLE_CLIENT_ID"],
            "project_id": google.get("GOOGLE_PROJECT_ID", "gen-lang-client-0065293299"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": google["GOOGLE_CLIENT_SECRET"],
            "redirect_uris": [redirect],
        }
    }


# =============================================================
# JWT cookie persistence (survives page refreshes)
# =============================================================

class AuthTokenManager:

    def __init__(self, cookie_name: str, token_key: str, token_duration_days: int):
        self.cookie_manager = stx.CookieManager()
        self.cookie_name = cookie_name
        self.token_key = token_key
        self.token_duration_days = token_duration_days
        self.token = None

    def get_decoded_token(self) -> dict | None:
        self.token = self.cookie_manager.get(self.cookie_name)
        if not self.token:
            return None
        return self._decode_token()

    def set_token(self, email: str, oauth_id: str, name: str = ""):
        exp_date = datetime.now() + timedelta(days=self.token_duration_days)
        token = self._encode_token(email, oauth_id, name, exp_date)
        self.cookie_manager.set(
            self.cookie_name,
            token,
            expires_at=exp_date,
        )

    def delete_token(self):
        try:
            self.cookie_manager.delete(self.cookie_name)
        except KeyError:
            pass

    def _decode_token(self) -> dict | None:
        try:
            decoded = jwt.decode(self.token, self.token_key, algorithms=["HS256"])
            return decoded
        except ExpiredSignatureError:
            st.toast("Token expired, please log in again.")
            self.delete_token()
        except jwt.PyJWTError:
            self.delete_token()
        return None

    def _encode_token(self, email: str, oauth_id: str, name: str, exp_date: datetime) -> str:
        return jwt.encode(
            {
                "email": email,
                "oauth_id": oauth_id,
                "name": name,
                "exp": exp_date.timestamp(),
            },
            self.token_key,
            algorithm="HS256",
        )


# =============================================================
# Direct Google OAuth authenticator
# =============================================================

class GoogleAuthenticator:

    def __init__(self):
        auth = _auth_section()
        self.allowed_users: list[str] = [
            e.strip()
            for e in auth.get("ALLOWED_ADMINS", "").split(",")
            if e.strip()
        ]
        self.token_manager = AuthTokenManager(
            cookie_name=auth.get("COOKIE_NAME", "auth_jwt"),
            token_key=auth.get("TOKEN_KEY", "medical-interpolarbility"),
            token_duration_days=int(auth.get("TOKEN_DURATION_DAYS", 7)),
        )
        self.redirect_uri = get_redirect_uri()

    # ---------------------------------------------------------
    # Flow
    # ---------------------------------------------------------

    def _initialize_flow(self) -> google_auth_oauthlib.flow.Flow:
        return google_auth_oauthlib.flow.Flow.from_client_config(
            get_google_client_config(),
            scopes=SCOPES,
            redirect_uri=self.redirect_uri,
        )

    def get_auth_url(self) -> str:
        flow = self._initialize_flow()
        auth_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
        )
        return auth_url

    # ---------------------------------------------------------
    # Code exchange
    # ---------------------------------------------------------

    def exchange_code(self, code: str) -> dict | None:
        flow = self._initialize_flow()
        flow.fetch_token(code=code)
        creds = flow.credentials

        oauth_service = build(serviceName="oauth2", version="v2", credentials=creds)
        info = oauth_service.userinfo().get().execute()

        return {
            "oauth_id": info.get("id"),
            "email": info.get("email"),
            "name": info.get("name") or info.get("email"),
            "picture": info.get("picture"),
        }

    # ---------------------------------------------------------
    # Allowlist
    # ---------------------------------------------------------

    def is_allowed(self, email: str) -> bool:
        if not self.allowed_users:
            st.error(
                "ALLOWED_ADMINS is not configured in secrets. "
                "Add the admin email(s) to the [auth] section of .streamlit/secrets.toml "
                "(or your Streamlit Cloud dashboard secrets)."
            )
            return False
        return email in self.allowed_users

    # ---------------------------------------------------------
    # Session / cookie
    # ---------------------------------------------------------

    def get_cached_user(self) -> dict | None:
        token = self.token_manager.get_decoded_token()
        if token is None:
            return None
        return {
            "oauth_id": token.get("oauth_id"),
            "email": token.get("email"),
            "name": token.get("name") or token.get("email"),
        }

    def persist_user(self, user: dict):
        self.token_manager.set_token(
            email=user["email"],
            oauth_id=user["oauth_id"],
            name=user.get("name", ""),
        )

    def logout(self):
        self.token_manager.delete_token()
