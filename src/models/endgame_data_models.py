from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint

from .sql_models import Database_Data_Plus

class Endgame_Data_Base(Database_Data_Plus):
    climbed: bool | None =  Field(default=False, index = True)
    climb_Position: int | None = Field(default=None, index = True)
class Endgame_Data(Endgame_Data_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number", name="data_creation_constraint"),
    )
    
class Endgame_Data_Create(Endgame_Data_Base):
    pass


class Endgame_Data_Update(SQLModel):
     climbed: bool | None = None
     climb_Position: int | None = None