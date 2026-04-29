from pydantic import BaseModel, EmailStr


class GoogleAuthRequest(BaseModel):
    credential: str


class AuthenticatedUser(BaseModel):
    email: EmailStr
    name: str
    picture: str | None = None
    given_name: str | None = None
    family_name: str | None = None


class AuthSessionResponse(BaseModel):
    authenticated: bool
    user: AuthenticatedUser | None = None
