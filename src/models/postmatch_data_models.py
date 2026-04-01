from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint
from typing import Optional

from .sql_models import Database_Data_Plus


class Postmatch_Data_Base(Database_Data_Plus):
    scoring_efficiency: Optional[float] = Field(default=None, index=True)
    scored_how: Optional[str] = Field(default=None, index=True)
    scoring_location: Optional[str] = Field(default=None, index=True)
    feeding_skills: Optional[int] = Field(default=None, index=True)
    passed_how: Optional[str] = Field(default=None, index=True)
    defense_skill: Optional[int] = Field(default=None, index=True)
    cards: Optional[str] = Field(default=None, index=True)
    comments: Optional[str] = Field(default=None, index=True)


class Postmatch_Data(Postmatch_Data_Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number",
                         "competition", name="postmatch_unique_constraint"),
    )


class Postmatch_Data_Create(Postmatch_Data_Base):
    pass


class Postmatch_Data_Update(SQLModel):
    scoring_efficiency: Optional[float] = None
    scored_how: Optional[str] = None
    scoring_location: Optional[str] = None
    feeding_skills: Optional[int] = None
    passed_how: Optional[str] = None
    defense_skill: Optional[int] = None
    cards: Optional[str] = None
    comments: Optional[str] = None
