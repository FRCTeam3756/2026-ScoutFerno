from pydantic import BaseModel, EmailStr


class GoogleAuthRequest(BaseModel):
    credential: str


class AuthenticatedUser(BaseModel):
    email: EmailStr
    name: str
    picture: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class AuthSessionResponse(BaseModel):
    authenticated: bool
    user: AuthenticatedUser | None = None
