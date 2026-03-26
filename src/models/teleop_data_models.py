from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint
# from pydantic import model_validator
# from typing import Any, cast

from .sql_models import Database_Data_Plus

class Teleop_Data_Base(Database_Data_Plus):
    alliance_won_auto: bool | None = Field(default=None, index=True)
    teleop_fuel_scored: int | None = Field(default=0, index=True) # Increments of .05 (5%), and multiply with tota
    field_usibillity: str | None = Field(default=None, index=True)
    defended_by_oponenet: bool | None = Field(default=None, index=True)
    fuel_fed_passed: int | None = Field(default=None, index=True)
    opp_zone_actions: str | None = Field(default=None, index=True)

    # @model_validator(mode="before")
    # @classmethod
    # def compute_team_teleop_fuel_scored(cls, values: Any) -> Any:
    #     if isinstance(values, dict):
    #         values_dict = cast(dict[str, Any], values)
    #         fuel = float(values_dict.get("teleop_fuel_scored", 0))
    #         total = int(values_dict.get("total_teleop_fuel_scored", 0))
    #         values_dict["team_teleop_fuel_scored"] = fuel * total
    #     else:
    #         fuel = getattr(values, "teleop_fuel_scored", 0)
    #         total = getattr(values, "total_teleop_fuel_scored", 0)
    #         values.team_teleop_fuel_scored = fuel * total
    #     return cast(dict[str, Any], values)
class Teleop_Data(Teleop_Data_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number", name="data_creation_constraint"),
    )
    

class Teleop_Data_Create(Teleop_Data_Base):
    pass


class Teleop_Data_Update(SQLModel):
    alliance_won_auto: bool | None = None
    teleop_fuel_scored: int | None = None
    field_usibillity: str | None = None
    defended_by_oponenet: bool | None = None
    fuel_fed_passed: int | None = None
    opp_zone_actions: str | None = None



