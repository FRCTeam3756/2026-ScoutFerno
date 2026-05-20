from pathlib import Path
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Field

base_dir = Path(__file__).parent.parent

db_dir = base_dir / "database"
db_dir.mkdir(exist_ok=True)

sqlite_file_name = db_dir / "scouting.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}

engine = create_engine(
    sqlite_url,
    echo=True,
    connect_args=connect_args
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


class Database_Data(SQLModel):
    team_number: int = Field(index=True)
    competition: str = Field(index=True)


class Database_Data_Plus(Database_Data):
    match_number: int = Field(index=True)
