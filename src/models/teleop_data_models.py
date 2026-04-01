from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint
from typing import Optional
# from pydantic import model_validator
# from typing import Any, cast

from .sql_models import Database_Data_Plus


class Teleop_Data_Base(Database_Data_Plus):
    alliance_won_auto: Optional[bool] = Field(default=None, index=True)
    teleop_fuel_scored: Optional[int] = Field(default=0, index=True)
    field_usability: Optional[str] = Field(default=None, index=True)
    defended_by_opponent: Optional[bool] = Field(default=None, index=True)
    fuel_fed_passed: Optional[int] = Field(default=None, index=True)
    opp_zone_actions: Optional[str] = Field(default=None, index=True)


class Teleop_Data(Teleop_Data_Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number",
                         "competition", name="teleop_unique_constraint"),
    )


class Teleop_Data_Create(Teleop_Data_Base):
    pass


class Teleop_Data_Update(SQLModel):
    alliance_won_auto: Optional[bool] = None
    teleop_fuel_scored: Optional[int] = None
    field_usability: Optional[str] = None
    defended_by_opponent: Optional[bool] = None
    fuel_fed_passed: Optional[int] = None
    opp_zone_actions: Optional[str] = None
