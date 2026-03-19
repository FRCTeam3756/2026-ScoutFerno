from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint

class Auto_Data_Base(SQLModel):
    team_number: int = Field(index=True)
    match_number: int = Field(index=True)
    #Auto Data
    does_it_work: bool = Field(index=True) # Can delete later... part of auto type?
    auto_type: str = Field(index=True) # Shoot -> Climb? Collect -> Shoot -> Climb? Collect -> Shoot? Nothing?
    auto_fuel_scored: float = Field(index=True) # Increments of .05 (5%), and multiply with total amount
    total_auto_fuel_scored: int = Field(index=True)
    auto_climb: int = Field(index=True) # Level 1, 2 or 3, 0 = didn't climb


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
