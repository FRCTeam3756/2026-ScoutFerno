from typing import Optional
from fastapi import HTTPException, Request

from ..models.auth_models import AuthenticatedUser
from .google_auth import SESSION_USER_KEY


def get_current_user(request: Request) -> Optional[AuthenticatedUser]:
    user_data = request.session.get(SESSION_USER_KEY)
    if not user_data:
        return None

    try:
        return AuthenticatedUser.model_validate(user_data)
    except Exception:
        request.session.pop(SESSION_USER_KEY, None)
        return None


def require_auth(request: Request) -> AuthenticatedUser:
    user = get_current_user(request)
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required.")
    return user
