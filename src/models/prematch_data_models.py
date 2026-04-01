from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint
from typing import Optional

from .sql_models import Database_Data_Plus


class Prematch_Data_Base(Database_Data_Plus):
    scouter: Optional[str] = Field(default=None, index=True)
    robot_position: Optional[str] = Field(default=None, index=True)
    no_show: Optional[bool] = Field(default=None, index=True)


class Prematch_Data(Prematch_Data_Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number",
                         "competition", name="prematch_unique_constraint"),
    )


class Prematch_Data_Create(Prematch_Data_Base):
    pass


class Prematch_Data_Update(SQLModel):
    scouter: Optional[str] = None
    robot_position: Optional[str] = None
    no_show: Optional[bool] = None
