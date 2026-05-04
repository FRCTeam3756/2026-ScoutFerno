from typing import Optional
from pydantic import BaseModel, EmailStr


class GoogleAuthRequest(BaseModel):
    credential: str


class AuthenticatedUser(BaseModel):
    email: EmailStr
    name: str
    picture: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class AuthSessionResponse(BaseModel):
    authenticated: bool
    user: Optional[AuthenticatedUser] = None
