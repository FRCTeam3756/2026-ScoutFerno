from sqlalchemy import create_engine
from sqlmodel import SQLModel

team_sqlite_file_name = "src/database/team_data.db"
team_sqlite_url = f"sqlite:///{team_sqlite_file_name}"

team_connect_args = {"check_same_thread": False}
team_engine = create_engine(team_sqlite_url, echo=True, connect_args=team_connect_args)


def create_team_db_and_tables():
    SQLModel.metadata.create_all(team_engine)