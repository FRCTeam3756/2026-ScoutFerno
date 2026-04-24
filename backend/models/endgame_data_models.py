from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint
from typing import Optional

from .sql_models import Database_Data_Plus

class Endgame_Data_Base(Database_Data_Plus):
    climbed: Optional[bool] =  Field(default=False, index = True)
    climb_position: Optional[str] = Field(default=None, index = True)
    mechanical_issue: Optional[bool] =Field(default=False, index = True)
    died: Optional[bool] =Field(default=False, index = True)
    fell_over: Optional[bool] =Field(default=False, index = True)
    
class Endgame_Data(Endgame_Data_Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number", "competition", name="endgame_unique_constraint"),
    )
    
class Endgame_Data_Create(Endgame_Data_Base):
    pass


class Endgame_Data_Update(SQLModel):
    climbed: Optional[bool] = None
    climb_position: Optional[str] = None
    mechanical_issue: Optional[bool] = None
    died: Optional[bool] = None
    fell_over: Optional[bool] = None