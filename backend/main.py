from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
import uvicorn

from .models.fastapi_models import team_lifespan
from .routers import all_data_router, prematch_data_router, autonomous_data_router, teleop_data_router, endgame_data_router, postmatch_data_router, security_router, video_router, interview_data_router
from .security.google_auth import (
    SESSION_COOKIE_NAME,
    get_cors_origins,
    get_session_cookie_domain,
    get_session_cookie_secure,
    get_session_max_age_seconds,
    get_session_secret,
)

app = FastAPI(lifespan=team_lifespan, root_path="/api", redirect_slashes=False)

app.add_middleware(
    SessionMiddleware,
    secret_key=get_session_secret(),
    session_cookie=SESSION_COOKIE_NAME,
    same_site="lax",
    https_only=get_session_cookie_secure(),
    max_age=get_session_max_age_seconds(),
    domain=get_session_cookie_domain(),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["127.0.0.1"])

app.include_router(all_data_router.router)
app.include_router(prematch_data_router.router)
app.include_router(autonomous_data_router.router)
app.include_router(teleop_data_router.router)
app.include_router(endgame_data_router.router)
app.include_router(postmatch_data_router.router)
app.include_router(interview_data_router.router)
app.include_router(security_router.router)
app.include_router(video_router.router)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
