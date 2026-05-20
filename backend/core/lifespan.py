from contextlib import asynccontextmanager
from fastapi import FastAPI

from ..database.scouting_db import create_db_and_tables


@asynccontextmanager
async def team_lifespan(app: FastAPI):
    create_db_and_tables()
    yield
