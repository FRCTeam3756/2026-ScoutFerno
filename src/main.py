from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
import uvicorn

from .models.fastapi_models import team_lifespan
from .routers import all_data_router, prematch_data_router, autonomous_data_router, teleop_data_router, endgame_data_router, postmatch_data_router, security_router, video_router, interview_data_router, teams_data_router

app = FastAPI(lifespan=team_lifespan, root_path="/api", redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://scouting.ramferno.com",
                   "https://api.ramferno.com",
                   "http://localhost:5173",
                   "476905af-6beb-4714-b1c7-6fda8308185d.cfargotunnel.com",
                   "bab0278a-7e0b-43fd-810e-3158fae509f6.cfargotunnel.com"
    ],
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
app.include_router(teams_data_router.router)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    # Gabe, update this if you changed the host
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
    
