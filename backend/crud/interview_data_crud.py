from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from ..models.interview_data_models import Interview_Data, Interview_Data_Create, Interview_Data_Update
from ..models.sql_models import team_engine


async def create_interview_data(match_data: Interview_Data_Create):
    with Session(team_engine) as session:
        db_data = Interview_Data.model_validate(match_data)
        session.add(db_data)

        try:
            session.commit()
            session.refresh(db_data)
            return db_data
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400,
                detail="This team already has data"
            )


async def read_interview_data(flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Interview_Data).where(
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

async def read_interview_data_by_team_competition(competition: str, team_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Interview_Data).where(
            Interview_Data.team_number == team_number,
            Interview_Data.competition == competition
            )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Team data not found")
        return results


async def update_interview_data(competition: str, team_number: int):
    with Session(team_engine) as session:
        statement = select(Interview_Data).where(
            Interview_Data.competition == competition,
            Interview_Data.team_number == team_number,
        )

        db_match = session.exec(statement).first()

        if not db_match:
            raise HTTPException(status_code=404, detail="Team data not found")

        session.add(db_match)
        session.commit()
        session.refresh(db_match)

        return db_match
    
async def delete_interview_data(competition: str, team_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Interview_Data).where(
            Interview_Data.competition == competition,
            Interview_Data.team_number == team_number,
        )

        db_match = session.exec(statement).first()

        if flagError and not db_match:
            raise HTTPException(status_code=404, detail="Team data not found")

        session.delete(db_match)
        session.commit()
        return db_match

async def delete_interview_data_by_team(team_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Interview_Data).where(
            Interview_Data.team_number == team_number,
        )

        results = session.exec(statement).all()

        if flagError and not results:
            raise HTTPException(status_code=404, detail="Data not found")
        for match in results:
            session.delete(match)
        session.commit()
        return results
    
