# from fastapi import APIRouter, HTTPException
# import googleapiclient.discovery as discovery
# import json
# from google.oauth2.credentials import Credentials

# from security.google_auth import authenticate_google, TOKEN_PATH, SCOPES

# router = APIRouter(prefix="/auth", tags=["Auth"])


# @router.get("/login")
# def login():
#     try:
#         creds = authenticate_google()
#         service = discovery.build("oauth2", "v2", credentials=creds)
#         user_info = service.userinfo().get().execute()
#         return {
#             "name": user_info.get("name"),
#             "email": user_info.get("email"),
#             "picture": user_info.get("picture")
#         }
#     except Exception as e:
#         raise HTTPException(status_code=401, detail=str(e))


# @router.get("/status")
# def auth_status():
#     if not TOKEN_PATH.exists():
#         return {"authenticated": False}
#     try:
#         creds = Credentials.from_authorized_user_info(
#             info=json.loads(TOKEN_PATH.read_text()),
#             scopes=SCOPES,
#         )
        
#         return {"authenticated": creds.valid, "expired": creds.expired}
#     except Exception:
#         return {"authenticated": False}


# @router.get("/logout")
# def logout():
#     if TOKEN_PATH.exists():
#         TOKEN_PATH.unlink()  
#     return {"message": "Logged out successfully"}
