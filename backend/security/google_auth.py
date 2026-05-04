import os
from typing import Dict, List, Optional

from fastapi import HTTPException
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token

from ..models.auth_models import AuthenticatedUser

SESSION_COOKIE_NAME = "scoutferno_session"
SESSION_USER_KEY = "user"


def _csv_env(name: str) -> List[str]:
    raw = os.getenv(name, "")
    return [value.strip() for value in raw.split(",") if value.strip()]


def normalize_origin(origin: str) -> str:
    if origin.startswith(("http://", "https://")):
        return origin
    return f"https://{origin}"


def get_cors_origins() -> Dict[str, Optional[str]]:
    default_origins = [
        "https://scouting.ramferno.com",
        "https://api.ramferno.com",
        "http://localhost:5173",
        "476905af-6beb-4714-b1c7-6fda8308185d.cfargotunnel.com",
        "bab0278a-7e0b-43fd-810e-3158fae509f6.cfargotunnel.com",
        "7e6fdead-4433-4b0b-ac31-45524d5ba102.cfargotunnel.com",
    ]

    configured_origins = [normalize_origin(
        origin) for origin in _csv_env("CORS_ALLOW_ORIGINS")]
    combined_origins = [normalize_origin(
        origin) for origin in default_origins] + configured_origins

    return dict.fromkeys(combined_origins)


def get_session_secret() -> str:
    return os.getenv("SESSION_SECRET", "dev-only-change-me")


def get_session_cookie_secure() -> bool:
    return os.getenv("AUTH_COOKIE_SECURE", "false").lower() == "true"


def get_session_cookie_domain() -> Optional[str]:
    return os.getenv("AUTH_COOKIE_DOMAIN", None)


def get_session_max_age_seconds() -> int:
    try:
        return int(os.getenv("AUTH_SESSION_MAX_AGE_SECONDS", "43200"))
    except ValueError:
        return 43200


def get_google_client_ids() -> List[str]:
    client_ids = _csv_env("GOOGLE_CLIENT_IDS")
    single_client_id = os.getenv("GOOGLE_CLIENT_ID")

    if single_client_id and single_client_id not in client_ids:
        client_ids.insert(0, single_client_id)

    return client_ids


def _authorized_emails() -> set[str]:
    return {email.lower() for email in _csv_env("AUTHORIZED_GOOGLE_EMAILS")}


def _authorized_domains() -> set[str]:
    return {
        domain.lower().lstrip("@")
        for domain in _csv_env("AUTHORIZED_GOOGLE_DOMAINS")
    }


def _ensure_google_client_ids_configured() -> List[str]:
    client_ids = get_google_client_ids()
    if not client_ids:
        raise HTTPException(
            status_code=500,
            detail="Google OAuth is not configured. Set GOOGLE_CLIENT_ID or GOOGLE_CLIENT_IDS.",
        )
    return client_ids


def _ensure_authorized_email(email: str) -> None:
    emails = _authorized_emails()
    domains = _authorized_domains()

    if not emails and not domains:
        raise HTTPException(
            status_code=500,
            detail=(
                "Google sign-in allowList is not configured. "
                "Set AUTHORIZED_GOOGLE_EMAILS or AUTHORIZED_GOOGLE_DOMAINS."
            ),
        )

    normalized_email = email.lower()
    email_domain = normalized_email.split("@")[-1]

    if normalized_email in emails or email_domain in domains:
        return

    raise HTTPException(
        status_code=403, detail="This Google account is not authorized.")


def verify_google_credential(credential: str) -> AuthenticatedUser:
    allowed_client_ids = _ensure_google_client_ids_configured()

    try:
        payload = id_token.verify_oauth2_token(
            credential,
            GoogleRequest(),
            audience=None,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=401, detail="Invalid Google credential.") from exc

    audience = payload.get("aud")
    issuer = payload.get("iss")
    email = payload.get("email")
    email_verified = payload.get("email_verified")

    if audience not in allowed_client_ids:
        raise HTTPException(
            status_code=401, detail="Google credential audience is not allowed.")

    if issuer not in {"accounts.google.com", "https://accounts.google.com"}:
        raise HTTPException(
            status_code=401, detail="Google credential issuer is invalid.")

    if not email or not email_verified:
        raise HTTPException(
            status_code=401, detail="Google account email is not verified.")

    _ensure_authorized_email(email)

    return AuthenticatedUser(
        email=email,
        name=payload.get("name") or email,
        picture=payload.get("picture"),
        first_name=payload.get("first_name"),
        last_name=payload.get("last_name"),
    )
