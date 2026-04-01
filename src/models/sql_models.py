from pathlib import Path
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Field

base_dir = Path(__file__).parent.parent
db_dir = base_dir / "database"
db_dir.mkdir(exist_ok=True)

team_sqlite_file_name = db_dir / "team_data.db"
team_sqlite_url = "sqlite:///{team_sqlite_file_name}"

team_connect_args = {"check_same_thread": False}
team_engine = create_engine(team_sqlite_url, echo=True, connect_args=team_connect_args)


def create_team_db_and_tables():
    SQLModel.metadata.create_all(team_engine)


class Database_Data(SQLModel):
    team_number: int = Field(index=True)
    competition: str = Field(index=True)


class Database_Data_Plus(Database_Data):
    match_number: int = Field(index=True)
