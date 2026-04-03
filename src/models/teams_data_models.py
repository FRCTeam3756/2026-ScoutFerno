from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel

from .sql_models import Database_Data


class Teams_Data_Base(Database_Data):
    name: Optional[str] = Field(default=None, index=True)
    country: Optional[str] = Field(default=None, index=True)
    state: Optional[str] = Field(default=None, index=True)
    district: Optional[str] = Field(default=None, index=True)
    rookie_year: Optional[int] = Field(default=None, index=True)
    active: Optional[bool] = Field(default=None, index=True)

    record_wins: Optional[int] = Field(default=None, index=True)
    record_losses: Optional[int] = Field(default=None, index=True)
    record_ties: Optional[int] = Field(default=None, index=True)
    record_count: Optional[int] = Field(default=None, index=True)
    record_winrate: Optional[float] = Field(default=None, index=True)

    norm_epa_current: Optional[float] = Field(default=None, index=True)
    norm_epa_recent: Optional[float] = Field(default=None, index=True)
    norm_epa_mean: Optional[float] = Field(default=None, index=True)
    norm_epa_max: Optional[float] = Field(default=None, index=True)


class Teams_Data(Teams_Data_Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint(
            "team_number",
            "competition",
            name="teams_unique_constraint",
        ),
    )


class Teams_Data_Create(Teams_Data_Base):
    pass


class Teams_Data_Update(SQLModel):
    name: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    rookie_year: Optional[int] = None
    active: Optional[bool] = None

    record_wins: Optional[int] = None
    record_losses: Optional[int] = None
    record_ties: Optional[int] = None
    record_count: Optional[int] = None
    record_winrate: Optional[float] = None

    norm_epa_current: Optional[float] = None
    norm_epa_recent: Optional[float] = None
    norm_epa_mean: Optional[float] = None
    norm_epa_max: Optional[float] = None
