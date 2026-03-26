import json
from pathlib import Path
from typing import Optional

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

################################################################

TOKEN_PATH = Path("src/security/token.json")
CREDENTIALS_PATH = Path("src/security/oauth_credentials.json")
SCOPES: Optional[list[str]] = None #["https://www.googleapis.com/auth/spreadsheets"]


def authenticate_google() -> Credentials:
    creds = None
    
    if TOKEN_PATH.exists():
        try:
            creds = Credentials.from_authorized_user_info(
                info=json.loads(TOKEN_PATH.read_text()),
                scopes=SCOPES,
            )
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH),
                scopes=SCOPES,
            )
            creds = flow.run_local_server(port=0)

        if creds:
            TOKEN_PATH.write_text(creds.to_json())
    
    return creds

if __name__ == "__main__":
    creds = authenticate_google()
    print(creds)