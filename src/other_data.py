from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager


class Other_Data_Base(SQLModel):
    team_number: int = Field(index=True)
    ball_storage: int = Field(index=True)
    drivetrain_type: str = Field(index=True)
    balls: int | None = Field(default=None, index=True)
    

class Other_Data(Other_Data_Base, table=True):
    id: int | None = Field(default=None, primary_key=True)


class Other_Data_Create(Other_Data_Base):
    pass


class DataUpdate(SQLModel):
    ball_storage: int | None = None
    drivetrain_type: str | None = None
    balls: int | None = None


sqlite_file_name = "team_data.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI()


@app.post("/data/other_data/", response_model=Other_Data)
def create_data(other_data: Other_Data_Create):
    with Session(engine) as session:
        db_data = Other_Data.model_validate(other_data)
        session.add(db_data)
        session.commit()
        session.refresh(db_data)
        return db_data


@app.get("/data/other_data/", response_model=list[Other_Data])
def read_other_data():
    with Session(engine) as session:
        other_data = session.exec(select(Other_Data)).all()
        return other_data


@app.get("/data/other_data/team/{team_number}", response_model=list[Other_Data])
def read_other_data_by_team(team_number: int):
    with Session(engine) as session:
        statement = select(Other_Data).where(Other_Data.team_number == team_number)
        results = session.exec(statement).all()
        if not results:
            raise HTTPException(status_code=404, detail="Team data not found")
        return results
    

@app.patch("/data/other_data/team/{team_number}", response_model=Other_Data)
def update_other_data(team_number: int, other_data: DataUpdate):
    with Session(engine) as session:
        statement = select(Other_Data).where(
            Other_Data.team_number == team_number
        )

        db_other_data = session.exec(statement).first()

        if not db_other_data:
            raise HTTPException(status_code=404, detail="Team data not found")
        
        other_data_data = other_data.model_dump(exclude_unset=True)
        db_other_data.sqlmodel_update(other_data_data)

        session.add(db_other_data)
        session.commit()
        session.refresh(db_other_data)

        return db_other_data
    

@app.delete("/data/other_data/team/{team_number}")
def delete_data(team_number: int):
    with Session(engine) as session:
        statement = select(Other_Data).where(
            Other_Data.team_number == team_number
        )

        other_data = session.exec(statement).first()
       
        if not other_data:
            raise HTTPException(status_code=404, detail="Data not found")
        session.delete(other_data)
        session.commit()
        return {"ok": True}