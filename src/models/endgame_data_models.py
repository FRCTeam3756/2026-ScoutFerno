from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint

from .sql_models import Database_Data_Plus

class Endgame_Data_Base(Database_Data_Plus):
    climbed: bool | None =  Field(default=False, index = True)
    climb_position: str | None = Field(default=None, index = True)
    mechanical_issue: bool | None =Field(default=False, index = True)
    died: bool | None =Field(default=False, index = True)
    fell_over: bool | None =Field(default=False, index = True)
class Endgame_Data(Endgame_Data_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number", "competition", name="endgame_unique_constraint"),
    )
    
class Endgame_Data_Create(Endgame_Data_Base):
    pass


class Endgame_Data_Update(SQLModel):
    climbed: bool | None = None
    climb_position: str | None = None
    mechanical_issue: bool | None = None
    died: bool | None = None
    fell_over: bool | None = None