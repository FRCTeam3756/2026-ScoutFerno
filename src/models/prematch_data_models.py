from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint

from .sql_models import Database_Data_Plus

class Prematch_Data_Base(Database_Data_Plus):
    scouter : str | None = Field(default=None, index=True)
    robot_position: str | None = Field(default=None, index=True)
    no_show: bool | None = Field(default=None, index=True)
    
class Prematch_Data(Prematch_Data_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number", name="data_creation_constraint"),
    )
    
class Prematch_Data_Create(Prematch_Data_Base):
    pass


class Prematch_Data_Update(SQLModel):
    scouter : str | None = None 
    robot_position: str | None = None
    no_show: bool | None = None

    

    