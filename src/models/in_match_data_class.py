from sqlmodel import Field,  SQLModel
from sqlalchemy import UniqueConstraint

class Match_Data_Base(SQLModel):
    team_number: int = Field(index=True)
    match_number: int = Field(index=True)
    ball_storage: int = Field(index=True)
    drivetrain_type: str = Field(index=True)
    balls: int = Field(index=True)

    

class Match_Data(Match_Data_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    __table_args__ = (
        UniqueConstraint("team_number", "match_number", name="data_creation_constraint"),
    )
    

class Match_Data_Create(Match_Data_Base):
    pass


class Match_Data_Update(SQLModel):
    ball_storage: int | None = None
    drivetrain_type: str | None = None
    balls: int | None = None
