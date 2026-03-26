from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint

from .sql_models import Database_Data_Plus


class Postmatch_Data_Base(Database_Data_Plus):
    scoring_efficiency: float | None = Field(default=None, index=True)
    scored_how: str | None = Field(default=None, index=True)
    scoring_location: str | None = Field(default=None, index=True)
    feeding_skills: int | None = Field(default=None, index=True)
    passed_how: str | None = Field(default=None, index=True)
    defense_skill: int | None = Field(default=None, index=True)
    cards: str | None = Field(default=None, index=True)
    comments: str | None = Field(default=None, index=True)


class Postmatch_Data(Postmatch_Data_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number",
                         "competition", name="postmatch_unique_constraint"),
    )


class Postmatch_Data_Create(Postmatch_Data_Base):
    pass


class Postmatch_Data_Update(SQLModel):
    scoring_efficiency: float | None = None
    scored_how: str | None = None
    scoring_location: str | None = None
    feeding_skills: int | None = None
    passed_how: str | None = None
    defense_skill: int | None = None
    cards: str | None = None
    comments: str | None = None
