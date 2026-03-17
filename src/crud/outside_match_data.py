from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

from models.outside_match_data_models import Outside_Match_Data, Outside_Match_Data_Create, Outside_Match_Data_Update
from models.sql_models import engine
from models.fastapi_models import lifespan


app = FastAPI(lifespan=lifespan)


@app.post("/data/other_data/", response_model=Outside_Match_Data)
def create_data(other_data: Outside_Match_Data_Create):
    with Session(engine) as session:
        db_data = Outside_Match_Data.model_validate(other_data)
        session.add(db_data)
        session.commit()
        session.refresh(db_data)
        return db_data


@app.get("/data/other_data/", response_model=list[Outside_Match_Data])
def read_other_data():
    with Session(engine) as session:
        other_data = session.exec(select(Outside_Match_Data)).all()
        return other_data


@app.get("/data/other_data/team/{team_number}", response_model=list[Outside_Match_Data])
def read_other_data_by_team(team_number: int):
    with Session(engine) as session:
        statement = select(Outside_Match_Data).where(Outside_Match_Data.team_number == team_number)
        results = session.exec(statement).all()
        if not results:
            raise HTTPException(status_code=404, detail="Team data not found")
        return results
    

@app.patch("/data/other_data/team/{team_number}", response_model=Outside_Match_Data)
def update_other_data(team_number: int, other_data: Outside_Match_Data_Update):
    with Session(engine) as session:
        statement = select(Outside_Match_Data).where(
            Outside_Match_Data.team_number == team_number
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
        statement = select(Outside_Match_Data).where(
            Outside_Match_Data.team_number == team_number
        )

        other_data = session.exec(statement).first()
       
        if not other_data:
            raise HTTPException(status_code=404, detail="Data not found")
        session.delete(other_data)
        session.commit()
        return {"ok": True}