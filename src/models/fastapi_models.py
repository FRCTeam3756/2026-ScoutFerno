from contextlib import asynccontextmanager
from fastapi import FastAPI

from .sql_models import create_team_db_and_tables

@asynccontextmanager
async def team_lifespan(app: FastAPI):
    create_team_db_and_tables()
    yield