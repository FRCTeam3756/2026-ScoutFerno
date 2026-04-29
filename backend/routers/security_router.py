from fastapi import APIRouter, Request, Response

from ..models.auth_models import AuthSessionResponse, GoogleAuthRequest
from ..security.google_auth import SESSION_COOKIE_NAME, SESSION_USER_KEY, verify_google_credential
from ..security.google_auth_guard import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/google", response_model=AuthSessionResponse)
def login_with_google(payload: GoogleAuthRequest, request: Request) -> AuthSessionResponse:
    user = verify_google_credential(payload.credential)
    request.session[SESSION_USER_KEY] = user.model_dump(mode="json")
    return AuthSessionResponse(authenticated=True, user=user)


@router.get("/session", response_model=AuthSessionResponse)
def read_auth_session(request: Request) -> AuthSessionResponse:
    user = get_current_user(request)
    return AuthSessionResponse(authenticated=user is not None, user=user)


@router.get("/status", response_model=AuthSessionResponse)
def auth_status(request: Request) -> AuthSessionResponse:
    user = get_current_user(request)
    return AuthSessionResponse(authenticated=user is not None, user=user)


@router.post("/logout", response_model=AuthSessionResponse)
def logout(request: Request, response: Response) -> AuthSessionResponse:
    request.session.clear()
    response.delete_cookie(SESSION_COOKIE_NAME)
    return AuthSessionResponse(authenticated=False, user=None)
