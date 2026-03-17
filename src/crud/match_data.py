from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from models.in_match_data_class import Match_Data, Match_Data_Create, Match_Data_Update
from models.sql_models import engine
from models.fastapi_models import lifespan


app = FastAPI(lifespan=lifespan)


@app.post("/data/match_data/", response_model=Match_Data)
def create_data(match_data: Match_Data_Create):
    with Session(engine) as session:
        db_data = Match_Data.model_validate(match_data)
        session.add(db_data)

        try:
            session.commit()
            session.refresh(db_data)
            return db_data
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400,
                detail="This team already has data for this match."
            )


@app.get("/data/match_data/", response_model=list[Match_Data])
def read_match_data():
    with Session(engine) as session:
        match_data = session.exec(select(Match_Data)).all()
        return match_data


@app.get("/data/match_data/team/{team_number}", response_model=list[Match_Data])
def read_match_data_by_team(team_number: int):
    with Session(engine) as session:
        statement = select(Match_Data).where(Match_Data.team_number == team_number)
        results = session.exec(statement).all()
        if not results:
            raise HTTPException(status_code=404, detail="Team data not found")
        return results
    

@app.patch("/data/match_data/team/{team_number}/match/{match_number}", response_model=Match_Data)
def update_team_match_data(team_number: int, match_number: int, match_data: Match_Data_Update):
    with Session(engine) as session:
        statement = select(Match_Data).where(
            Match_Data.team_number == team_number,
            Match_Data.match_number == match_number
        )

        db_match = session.exec(statement).first()

        if not db_match:
            raise HTTPException(status_code=404, detail="Match data not found")

        update_data = match_data.model_dump(exclude_unset=True)
        db_match.sqlmodel_update(update_data)

        session.add(db_match)
        session.commit()
        session.refresh(db_match)

        return db_match

@app.delete("/data/match_data/team/{team_number}/match/{match_number}")
def delete_team_one_match_data(team_number: int, match_number: int):
    with Session(engine) as session:
        statement = select(Match_Data).where(
            Match_Data.team_number == team_number,
            Match_Data.match_number == match_number
        )

        match_data = session.exec(statement).first()

        if not match_data:
            raise HTTPException(status_code=404, detail="Data not found")
        session.delete(match_data)
        session.commit()
        return {"ok": True}
    

@app.delete("/data/match_data/team/{team_number}")
def delete_team_match_data(team_number: int):
    with Session(engine) as session:
        statement = select(Match_Data).where(
            Match_Data.team_number == team_number,
        )

        team_match_data = session.exec(statement).all()

        if not team_match_data:
            raise HTTPException(status_code=404, detail="Data not found")
        for match in team_match_data:
            session.delete(match)
        session.commit()
        return {"ok": True}