from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint
from pydantic import model_validator
from typing import Any, cast

class Auto_Data_Base(SQLModel):
    team_number: int = Field(index=True)
    match_number: int = Field(index=True)
    #Auto Data
    does_it_work: bool = Field(index=True) # Can delete later... part of auto type?
    auto_type: str = Field(index=True) # Shoot -> Climb? Collect -> Shoot -> Climb? Collect -> Shoot? Nothing?
    auto_fuel_scored: float = Field(default=0.0, index=True) # Increments of .05 (5%), and multiply with total amount
    total_auto_fuel_scored: int = Field(default=0, index=True)
    team_auto_fuel_scored: float | None = Field(default=None, index=True)
    auto_climb: int = Field(index=True) # Level 1, 2 or 3, 0 = didn't climb

    @model_validator(mode="before")
    @classmethod
    def compute_team_auto_fuel_scored(cls, values: Any) -> Any:
        if isinstance(values, dict):
            values_dict = cast(dict[str, Any], values)
            fuel = float(values_dict.get("auto_fuel_scored", 0))
            total = int(values_dict.get("total_auto_fuel_scored", 0))
            values_dict["team_auto_fuel_scored"] = fuel * total
        else:
            fuel = getattr(values, "auto_fuel_scored", 0)
            total = getattr(values, "total_auto_fuel_scored", 0)
            values.team_auto_fuel_scored = fuel * total
        return cast(dict[str, Any], values)
    
class Auto_Data(Auto_Data_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number", name="data_creation_constraint"),
    )
    
class Auto_Data_Create(Auto_Data_Base):
    pass


class Auto_Data_Update(SQLModel):
    does_it_work: bool | None = None
    auto_type: str | None = None
    auto_fuel_scored: float | None = None
    auto_climb: int | None = None


class Auto_Data_Read(Auto_Data_Base):
    pass

