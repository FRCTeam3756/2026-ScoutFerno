from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint
from typing import Optional
# from pydantic import model_validator
# from typing import Any, cast

from .sql_models import Database_Data_Plus


class Match_Data_Base(Database_Data_Plus):
    robot_position: Optional[str] = Field(default=None, index=True)
    no_show: Optional[bool] = Field(default=None, index=True)

    auto_fuel_scored: Optional[int] = Field(default=None, index=True)
    auto_collection_location: Optional[str] = Field(default=None, index=True)
    auto_addition_actions: Optional[str] = Field(default=None, index=True)
    auto_stuck: Optional[bool] = Field(default=False, index=True)
    auto_climbed: Optional[bool] = Field(default=None, index=True)

    alliance_won_auto: Optional[bool] = Field(default=None, index=True)
    teleop_fuel_scored: Optional[int] = Field(default=0, index=True)
    field_usability: Optional[str] = Field(default=None, index=True)
    defended_by_opponent: Optional[bool] = Field(default=None, index=True)
    fuel_fed_passed: Optional[int] = Field(default=None, index=True)
    opp_zone_actions: Optional[str] = Field(default=None, index=True)

    climbed: Optional[bool] =  Field(default=False, index = True)
    climb_position: Optional[str] = Field(default=None, index = True)
    mechanical_issue: Optional[bool] =Field(default=False, index = True)
    died: Optional[bool] =Field(default=False, index = True)
    fell_over: Optional[bool] =Field(default=False, index = True)

    scoring_efficiency: Optional[float] = Field(default=None, index=True)
    scored_how: Optional[str] = Field(default=None, index=True)
    scoring_location: Optional[str] = Field(default=None, index=True)
    feeding_skills: Optional[int] = Field(default=None, index=True)
    passed_how: Optional[str] = Field(default=None, index=True)
    defense_skill: Optional[int] = Field(default=None, index=True)
    cards: Optional[str] = Field(default=None, index=True)
    comments: Optional[str] = Field(default=None, index=True)


class Match_Data(Match_Data_Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number",
                         "competition", name="match_unique_constraint"),
    )


class Match_Data_Create(Match_Data_Base):
    pass


class Match_Data_Update(SQLModel):
    robot_position: Optional[str] = None
    no_show: Optional[bool] = None

    auto_fuel_scored: Optional[int] = None
    auto_collection_location: Optional[str] = None
    auto_addition_actions: Optional[str] = None
    auto_stuck: Optional[bool] = None
    auto_climbed: Optional[bool] = None

    alliance_won_auto: Optional[bool] = None
    teleop_fuel_scored: Optional[int] = None
    field_usability: Optional[str] = None
    defended_by_opponent: Optional[bool] = None
    fuel_fed_passed: Optional[int] = None
    opp_zone_actions: Optional[str] = None

    climbed: Optional[bool] = None
    climb_position: Optional[str] = None
    mechanical_issue: Optional[bool] = None
    died: Optional[bool] = None
    fell_over: Optional[bool] = None
    
    scoring_efficiency: Optional[float] = None
    scored_how: Optional[str] = None
    scoring_location: Optional[str] = None
    feeding_skills: Optional[int] = None
    passed_how: Optional[str] = None
    defense_skill: Optional[int] = None
    cards: Optional[str] = None
    comments: Optional[str] = None
