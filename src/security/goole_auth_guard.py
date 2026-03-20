from fastapi import HTTPException
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import json

from google_auth import TOKEN_PATH, SCOPES



def require_auth() -> Credentials:
    if not TOKEN_PATH.exists():
        raise HTTPException(status_code=401, detail="Not logged in")
    
    creds = Credentials.from_authorized_user_info(
        info=json.loads(TOKEN_PATH.read_text()),
        scopes=SCOPES,
    )
    
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                TOKEN_PATH.write_text(creds.to_json())  # persist refreshed token
            except Exception:
                raise HTTPException(status_code=401, detail="Token refresh failed, please login again")
        else:
            raise HTTPException(status_code=401, detail="Token expired, please login again")

    return creds   
