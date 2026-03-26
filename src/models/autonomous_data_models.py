from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint
# from pydantic import model_validator
# from typing import Any, cast

from .sql_models import Database_Data_Plus


class Autonomous_Data_Base(Database_Data_Plus):
    auto_fuel_scored: int | None = Field(default=None, index=True)
    auto_collection_location: str | None = Field(default=None, index=True)
    auto_addition_actions: str | None = Field(default=None, index=True)
    auto_stuck: bool | None = Field(default=False, index=True)
    auto_climbed: bool | None = Field(default=None, index=True)


class Autonomous_Data(Autonomous_Data_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number",
                         "competition", name="autonomous_unique_constraint"),
    )


class Autonomous_Data_Create(Autonomous_Data_Base):
    pass


class Autonomous_Data_Update(SQLModel):
    auto_fuel_scored: int | None = None
    auto_collection_location: str | None = None
    auto_addition_actions: str | None = None
    auto_stuck: bool | None = None
    auto_climbed: bool | None = None
