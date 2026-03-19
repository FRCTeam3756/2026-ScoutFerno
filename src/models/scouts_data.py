from sqlmodel import SQLModel, Field

class Scout_Info_Base(SQLModel):
    scout_name: str = Field(index=True)
    team_number: int | None = Field(default=None, index=True)
    grade: int | None = None
    phone_number: str | None = None
    matches_scouted: int = Field(default=0, index=True)

class Scout_Info(Scout_Info_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)

class Scout_Info_Create(Scout_Info_Base):
    pass

class Scout_Info_Update(SQLModel):
    scout_name: str | None = None
    team_number: int | None = None
    grade: int | None = None
    phone_number: str | None = None
