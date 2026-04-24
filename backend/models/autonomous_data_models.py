from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint
from typing import Optional
# from pydantic import model_validator
# from typing import Any, cast

from .sql_models import Database_Data_Plus


class Autonomous_Data_Base(Database_Data_Plus):
    auto_fuel_scored: Optional[int] = Field(default=None, index=True)
    auto_collection_location: Optional[str] = Field(default=None, index=True)
    auto_addition_actions: Optional[str] = Field(default=None, index=True)
    auto_stuck: Optional[bool] = Field(default=False, index=True)
    auto_climbed: Optional[bool] = Field(default=None, index=True)


class Autonomous_Data(Autonomous_Data_Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number",
                         "competition", name="autonomous_unique_constraint"),
    )


class Autonomous_Data_Create(Autonomous_Data_Base):
    pass


class Autonomous_Data_Update(SQLModel):
    auto_fuel_scored: Optional[int] = None
    auto_collection_location: Optional[str] = None
    auto_addition_actions: Optional[str] = None
    auto_stuck: Optional[bool] = None
    auto_climbed: Optional[bool] = None
