from sqlmodel import SQLModel, Field

class Outside_Match_Data_Base(SQLModel):
    team_number: int = Field(index=True)
    ball_storage: int = Field(index=True)
    drivetrain_type: str = Field(index=True)
    balls: int | None = Field(default=None, index=True)
    

class Outside_Match_Data(Outside_Match_Data_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)


class Outside_Match_Data_Create(Outside_Match_Data_Base):
    pass


class Outside_Match_Data_Update(SQLModel):
    ball_storage: int | None = None
    drivetrain_type: str | None = None
    balls: int | None = None