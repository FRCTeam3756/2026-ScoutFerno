from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from ..models.interview_data_models import Interview_Match_Data, Interview_Match_Data_Create, Interview_Match_Data_Update
from ..models.sql_models import engine


async def create_interview_match_data(interview_match_data: Interview_Match_Data_Create):
    with Session(engine) as session:
        db_data = Interview_Match_Data.model_validate(interview_match_data)
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


async def read_interview_match_data():
    with Session(engine) as session:
        interview_match_data = session.exec(select(Interview_Match_Data)).all()
        return interview_match_data


async def read_interview_match_data_by_team(team_number: int):
    with Session(engine) as session:
        statement = select(Interview_Match_Data).where(Interview_Match_Data.team_number == team_number)
        results = session.exec(statement).all()
        if not results:
            raise HTTPException(status_code=404, detail="Team data not found")
        return results
    

async def update_interview_match_data(team_number: int, interview_match_data: Interview_Match_Data_Update):
    with Session(engine) as session:
        statement = select(Interview_Match_Data).where(
            Interview_Match_Data.team_number == team_number
        )

        db_interview_match_data = session.exec(statement).first()

        if not db_interview_match_data:
            raise HTTPException(status_code=404, detail="Team data not found")
        
        interview_match_data_data = interview_match_data.model_dump(exclude_unset=True)
        db_interview_match_data.sqlmodel_update(interview_match_data_data)

        session.add(db_interview_match_data)
        session.commit()
        session.refresh(db_interview_match_data)

        return db_interview_match_data
    

async def delete_interview_match_data(team_number: int):
    with Session(engine) as session:
        statement = select(Interview_Match_Data).where(
            Interview_Match_Data.team_number == team_number
        )

        interview_match_data = session.exec(statement).first()
       
        if not interview_match_data:
            raise HTTPException(status_code=404, detail="Data not found")
        session.delete(interview_match_data)
        session.commit()
        return {"ok": True}


