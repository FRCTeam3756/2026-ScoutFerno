from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from ..models.interview_data_models import Interview_Data, Interview_Data_Create, Interview_Data_Update
from ..models.sql_models import team_engine


async def create_interview_data(interview_data: Interview_Data_Create):
    with Session(team_engine) as session:
        db_data = Interview_Data.model_validate(interview_data)
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


async def read_interview_data(competition: str, year: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Interview_Data).where(
            Interview_Data.competition == competition,
            Interview_Data.year == year
        )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Data not found")
        return results


async def read_interview_data_by_team(team_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Interview_Data).where(
            Interview_Data.team_number == team_number
        )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Team data not found")
        return results
    

async def update_interview_data(team_number: int, interview_data: Interview_Data_Update):
    with Session(team_engine) as session:
        statement = select(Interview_Data).where(
            Interview_Data.team_number == team_number
        )

        db_interview_data = session.exec(statement).first()

        if not db_interview_data:
            raise HTTPException(status_code=404, detail="Team data not found")
        
        interview_data_data = interview_data.model_dump(exclude_unset=True)
        db_interview_data.sqlmodel_update(interview_data_data)

        session.add(db_interview_data)
        session.commit()
        session.refresh(db_interview_data)

        return db_interview_data
    

async def delete_interview_data(team_number: int):
    with Session(team_engine) as session:
        statement = select(Interview_Data).where(
            Interview_Data.team_number == team_number
        )

        interview_data = session.exec(statement).first()
       
        if not interview_data:
            raise HTTPException(status_code=404, detail="Data not found")
        session.delete(interview_data)
        session.commit()
        return {"ok": True}


