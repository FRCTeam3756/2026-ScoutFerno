from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from ..models.outside_match_data_models import Outside_Match_Data, Outside_Match_Data_Create, Outside_Match_Data_Update
from ..models.sql_models import engine


def create_outside_match_data(outside_match_data: Outside_Match_Data_Create):
    with Session(engine) as session:
        db_data = Outside_Match_Data.model_validate(outside_match_data)
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


def read_outside_match_data():
    with Session(engine) as session:
        outside_match_data = session.exec(select(Outside_Match_Data)).all()
        return outside_match_data


def read_outside_match_data_by_team(team_number: int):
    with Session(engine) as session:
        statement = select(Outside_Match_Data).where(Outside_Match_Data.team_number == team_number)
        results = session.exec(statement).all()
        if not results:
            raise HTTPException(status_code=404, detail="Team data not found")
        return results
    

def update_outside_match_data(team_number: int, outside_match_data: Outside_Match_Data_Update):
    with Session(engine) as session:
        statement = select(Outside_Match_Data).where(
            Outside_Match_Data.team_number == team_number
        )

        db_outside_match_data = session.exec(statement).first()

        if not db_outside_match_data:
            raise HTTPException(status_code=404, detail="Team data not found")
        
        outside_match_data_data = outside_match_data.model_dump(exclude_unset=True)
        db_outside_match_data.sqlmodel_update(outside_match_data_data)

        session.add(db_outside_match_data)
        session.commit()
        session.refresh(db_outside_match_data)

        return db_outside_match_data
    

def delete_outside_match_data(team_number: int):
    with Session(engine) as session:
        statement = select(Outside_Match_Data).where(
            Outside_Match_Data.team_number == team_number
        )

        outside_match_data = session.exec(statement).first()
       
        if not outside_match_data:
            raise HTTPException(status_code=404, detail="Data not found")
        session.delete(outside_match_data)
        session.commit()
        return {"ok": True}


