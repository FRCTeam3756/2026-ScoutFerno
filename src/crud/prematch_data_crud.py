from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from ..models.prematch_data_models import Prematch_Data, Prematch_Data_Create, Prematch_Data_Update
from ..models.sql_models import team_engine


async def create_prematch_data(match_data: Prematch_Data_Create):
    with Session(team_engine) as session:
        db_data = Prematch_Data.model_validate(match_data)
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


async def read_prematch_data(flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Prematch_Data).where(
            )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Data not found")
        return results


async def read_prematch_data_by_team(team_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Prematch_Data).where(
            Prematch_Data.team_number == team_number
            )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Team data not found")
        return results
     

async def read_prematch_data_by_match(competition: str, match_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Prematch_Data).where(
            Prematch_Data.competition == competition,
            Prematch_Data.match_number == match_number
            )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Match data not found")
        return results
    

async def read_prematch_data_by_team_match(competition: str, team_number: int, match_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Prematch_Data).where(
            Prematch_Data.competition == competition,
            Prematch_Data.team_number == team_number,
            Prematch_Data.match_number == match_number
            )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Team match data not found")
        return results


async def update_prematch_data(competition: str, team_number: int, match_number: int, match_data: Prematch_Data_Update):
    with Session(team_engine) as session:
        statement = select(Prematch_Data).where(
            Prematch_Data.competition == competition,
            Prematch_Data.team_number == team_number,
            Prematch_Data.match_number == match_number
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


async def delete_prematch_data_by_match(competition: str, match_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Prematch_Data).where(
            Prematch_Data.competition == competition,
            Prematch_Data.match_number == match_number
        )

        results = session.exec(statement).all()

        if flagError and not results:
            raise HTTPException(status_code=404, detail="Data not found")
        for match in results:
            session.delete(match)
        session.commit()
        return results
    

async def delete_prematch_data_by_team(team_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Prematch_Data).where(
            Prematch_Data.team_number == team_number,
        )

        results = session.exec(statement).all()

        if flagError and not results:
            raise HTTPException(status_code=404, detail="Data not found")
        for match in results:
            session.delete(match)
        session.commit()
        return results
    

async def delete_prematch_data_by_team_match(competition: str, match_number: int, team_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Prematch_Data).where(
            Prematch_Data.competition == competition,
            Prematch_Data.match_number == match_number,
            Prematch_Data.team_number == team_number
        )

        results = session.exec(statement).all()

        if flagError and not results:
            raise HTTPException(status_code=404, detail="Data not found")
        for match in results:
            session.delete(match)
        session.commit()
        return results