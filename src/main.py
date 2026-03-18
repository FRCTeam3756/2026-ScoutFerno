from fastapi import FastAPI

from .models.fastapi_models import lifespan
from .routers import in_match_data_router, outside_match_data_router

app = FastAPI(lifespan=lifespan)

app.include_router(in_match_data_router.router)
app.include_router(outside_match_data_router.router)
