from fastapi import FastAPI

from .models.fastapi_models import team_lifespan
from .routers import all_data_router, teleop_data_router, auto_data_router, interview_data_router, security_router

app = FastAPI(lifespan=team_lifespan)

app.include_router(all_data_router.router)
app.include_router(teleop_data_router.router)
app.include_router(auto_data_router.router)
app.include_router(interview_data_router.router)
app.include_router(security_router.router)