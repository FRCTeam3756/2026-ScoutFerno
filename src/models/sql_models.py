from sqlalchemy import create_engine
from sqlmodel import SQLModel, Field

team_sqlite_file_name = "src/database/team_data.db"
team_sqlite_url = f"sqlite:///{team_sqlite_file_name}"

team_connect_args = {"check_same_thread": False}
team_engine = create_engine(team_sqlite_url, echo=True, connect_args=team_connect_args)


def create_team_db_and_tables():
    SQLModel.metadata.create_all(team_engine)


scout_sqlite_file_name = "src/database/scout_data.db"
scout_sqlite_url = f"sqlite:///{scout_sqlite_file_name}"

scout_connect_args = {"check_same_thread": False}
scout_engine = create_engine(scout_sqlite_url, echo=True, connect_args=scout_connect_args)


def create_scout_db_and_tables():
    SQLModel.metadata.create_all(scout_engine)

class Database_Data(SQLModel):
    team_number: int = Field(index=True)
    competition: str = Field(index=True)
    year: int = Field(index=True)


class Database_Data_Plus(Database_Data):
    match_number: int = Field(index=True)
    match_type: str = Field(index=True)
    winner: str = Field(index=True)
    alliance: str = Field(index=True)