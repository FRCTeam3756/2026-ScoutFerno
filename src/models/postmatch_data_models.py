from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint

from .sql_models import Database_Data_Plus

class Postmatch_Data_Base(Database_Data_Plus):
   mech_issue: bool | None = Field(default=False, index = True)
   died: bool | None = Field(default=False, index = True)
   tipped: bool | None = Field(default=False, index = True)
   scoring_efficiency: float | None = Field(default=None, index = True)
   scored_how: str | None = Field(default=None, index = True)
   tele_score: int | None = Field(default=None, index = True)
   feeding_skills: int | None = Field(default=None, index = True)
   passed_how: str | None = Field(default=None, index = True)
   defense_skill: int | None = Field(default=None, index = True)
   cards: str | None = Field(default=None, index = True)
    
class Postmatch_Data(Postmatch_Data_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number", name="data_creation_constraint"),
    )
    
class Postmatch_Data_Create(Postmatch_Data_Base):
    pass


class Postmatch_Data_Update(SQLModel):
    mech_issue: bool | None = None
    died: bool | None = None
    tipped: bool | None = None
    scoring_efficiency: float | None =  None
    scored_how: str | None = None
    tele_score: int | None = None
    feeding_skills: int | None = None 
    passed_how: str | None = None
    defense_skill: int | None = None
    cards: str | None = None