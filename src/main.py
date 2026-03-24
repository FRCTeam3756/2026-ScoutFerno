from fastapi import FastAPI

from .models.fastapi_models import team_lifespan
from .routers import all_data_router, prematch_data_router, autonomous_data_router, teleop_data_router, endgame_data_router, postmatch_data_router, security_router, video_router #, interview_data_router

app = FastAPI(lifespan=team_lifespan)              

app.include_router(all_data_router.router)
app.include_router(prematch_data_router.router)
app.include_router(autonomous_data_router.router)
app.include_router(teleop_data_router.router)
app.include_router(endgame_data_router.router)
app.include_router(postmatch_data_router.router)
#app.include_router(interview_data_router.router)
app.include_router(security_router.router)
app.include_router(video_router.router)
