from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint
from pydantic import model_validator
from typing import Any, cast

from .sql_models import Database_Data_Plus

class Teleop_Data_Base(Database_Data_Plus):
    teleop_fuel_scored: float = Field(default=0.0, index=True) # Increments of .05 (5%), and multiply with total
    total_teleop_fuel_scored: int = Field(default=0, index=True)
    team_teleop_fuel_scored: float | None = Field(default=None, index=True)
    shooting_posistion: str = Field(index=True) # Close, Medium, Far
    moving_shoot: bool = Field(index=True) # Do they move when they shoot (can be str)
    teleop_climb: int = Field(index=True) # Level 1, 2 or 3, 0 = didn't climb
    climb_speed: str = Field(index=True) # Fast, Medium, Slow
    driver_skill: str = Field(index=True) # Amazing, good, decent, okay, terrible
   
    @model_validator(mode="before")
    @classmethod
    def compute_team_teleop_fuel_scored(cls, values: Any) -> Any:
        if isinstance(values, dict):
            values_dict = cast(dict[str, Any], values)
            fuel = float(values_dict.get("teleop_fuel_scored", 0))
            total = int(values_dict.get("total_teleop_fuel_scored", 0))
            values_dict["team_teleop_fuel_scored"] = fuel * total
        else:
            fuel = getattr(values, "teleop_fuel_scored", 0)
            total = getattr(values, "total_teleop_fuel_scored", 0)
            values.team_teleop_fuel_scored = fuel * total
        return cast(dict[str, Any], values)
class Teleop_Data(Teleop_Data_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number", name="data_creation_constraint"),
    )
    

class Teleop_Data_Create(Teleop_Data_Base):
    pass


class Teleop_Data_Update(SQLModel):
    teleop_fuel_scored: float | None = None
    shooting_posistion: str | None = None
    moving_shoot: bool | None = None
    teleop_climb: int | None = None
    climb_speed: str | None = None
    driver_skill: str | None = None


