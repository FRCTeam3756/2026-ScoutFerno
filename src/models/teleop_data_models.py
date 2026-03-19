from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint

class Teleop_Data_Base(SQLModel):
    team_number: int = Field(index=True)
    match_number: int = Field(index=True)
    #Teleop Data
    teleop_fuel_scored: float = Field(index=True) # Increments of .05 (5%), and multiply with total
    total_teleop_fuel_scored: int = Field(index=True)
    shooting_posistion: str = Field(index=True) # Close, Medium, Far
    moving_shoot: bool = Field(index=True) # Do they move when they shoot (can be str)
    teleop_climb: int = Field(index=True) # Level 1, 2 or 3, 0 = didn't climb
    climb_speed: str = Field(index=True) # Fast, Medium, Slow
    driver_skill: str = Field(index=True) # Amazing, good, decent, okay, terrible
   
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


class Teleop_Data_Read(Teleop_Data_Base):
    pass