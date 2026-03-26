from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint
# from pydantic import model_validator
# from typing import Any, cast

from .sql_models import Database_Data_Plus


class Teleop_Data_Base(Database_Data_Plus):
    alliance_won_auto: bool | None = Field(default=None, index=True)
    teleop_fuel_scored: int | None = Field(default=0, index=True)
    field_usability: str | None = Field(default=None, index=True)
    defended_by_opponent: bool | None = Field(default=None, index=True)
    fuel_fed_passed: int | None = Field(default=None, index=True)
    opp_zone_actions: str | None = Field(default=None, index=True)


class Teleop_Data(Teleop_Data_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number",
                         "competition", name="teleop_unique_constraint"),
    )


class Teleop_Data_Create(Teleop_Data_Base):
    pass


class Teleop_Data_Update(SQLModel):
    alliance_won_auto: bool | None = None
    teleop_fuel_scored: int | None = None
    field_usability: str | None = None
    defended_by_opponent: bool | None = None
    fuel_fed_passed: int | None = None
    opp_zone_actions: str | None = None
