from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
import uvicorn

from .models.fastapi_models import team_lifespan
from .routers import all_data_router, prematch_data_router, autonomous_data_router, teleop_data_router, endgame_data_router, postmatch_data_router, security_router, video_router #, interview_data_router

app = FastAPI(lifespan=team_lifespan, root_path="/api")              

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://scouting.ramferno.com", "https://api.ramferno.com"], #Gabe, include link to domain and CF worker URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["127.0.0.1"]) #Gabe, update this if you changed the host

app.include_router(all_data_router.router)
app.include_router(prematch_data_router.router)
app.include_router(autonomous_data_router.router)
app.include_router(teleop_data_router.router)
app.include_router(endgame_data_router.router)
app.include_router(postmatch_data_router.router)
#app.include_router(interview_data_router.router)
app.include_router(security_router.router)
app.include_router(video_router.router)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000) #Gabe, update this if you changed the host
