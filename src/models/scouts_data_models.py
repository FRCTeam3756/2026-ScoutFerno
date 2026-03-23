from sqlmodel import SQLModel, Field

class Scout_Data_Base(SQLModel):
    scout_name: str = Field(index=True)
    grade: int | None = Field(default=None, index=True)
    phone_number: str | None = Field(default=None, index=True)
    matches_scouted: int = Field(default=0, index=True)

class Scout_Data(Scout_Data_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

class Scout_Data_Create(Scout_Data_Base):
    pass

class Scout_Data_Update(SQLModel):
    scout_name: str | None = None
    team_number: int | None = None
    grade: int | None = None
    phone_number: str | None = None
