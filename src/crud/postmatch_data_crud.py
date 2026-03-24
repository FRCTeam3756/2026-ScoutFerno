from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from ..models.postmatch_data_models import Postmatch_Data, Postmatch_Data_Create, Postmatch_Data_Update
from ..models.sql_models import team_engine


async def create_postmatch_data(match_data: Postmatch_Data_Create):
    with Session(team_engine) as session:
        db_data = Postmatch_Data.model_validate(match_data)
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


async def read_postmatch_data(flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Postmatch_Data).where(
            )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Data not found")
        return results


async def read_postmatch_data_by_team(team_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Postmatch_Data).where(
            Postmatch_Data.team_number == team_number
            )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Team data not found")
        return results
     

async def read_postmatch_data_by_match(competition: str, match_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Postmatch_Data).where(
            Postmatch_Data.competition == competition,
            Postmatch_Data.match_number == match_number
            )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Match data not found")
        return results
    

async def read_postmatch_data_by_team_match(competition: str, team_number: int, match_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Postmatch_Data).where(
            Postmatch_Data.competition == competition,
            Postmatch_Data.team_number == team_number,
            Postmatch_Data.match_number == match_number
            )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Team match data not found")
        return results


async def update_postmatch_data(competition: str, team_number: int, match_number: int, match_data: Postmatch_Data_Update):
    with Session(team_engine) as session:
        statement = select(Postmatch_Data).where(
            Postmatch_Data.competition == competition,
            Postmatch_Data.team_number == team_number,
            Postmatch_Data.match_number == match_number
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


async def delete_match_postmatch_data(competition: str, team_number: int, match_number: int):
    with Session(team_engine) as session:
        statement = select(Postmatch_Data).where(
            Postmatch_Data.competition == competition,
            Postmatch_Data.team_number == team_number,
            Postmatch_Data.match_number == match_number
        )

        match_data = session.exec(statement).first()

        if not match_data:
            raise HTTPException(status_code=404, detail="Data not found")
        session.delete(match_data)
        session.commit()
        return {"ok": True}
    

async def delete_team_postmatch_data(team_number: int):
    with Session(team_engine) as session:
        statement = select(Postmatch_Data).where(
            Postmatch_Data.team_number == team_number,
        )

        team_match_data = session.exec(statement).all()

        if not team_match_data:
            raise HTTPException(status_code=404, detail="Data not found")
        for match in team_match_data:
            session.delete(match)
        session.commit()
        return {"ok": True}