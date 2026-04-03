from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from ..models.sql_models import team_engine
from ..models.teams_data_models import (
    Teams_Data,
    Teams_Data_Create,
    Teams_Data_Update,
)


async def create_teams_data(team_data: Teams_Data_Create):
    with Session(team_engine) as session:
        db_data = Teams_Data.model_validate(team_data)
        session.add(db_data)

        try:
            session.commit()
            session.refresh(db_data)
            return db_data
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400,
                detail="This team already has data for this competition.",
            )


async def read_teams_data(flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Teams_Data)
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Data not found")
        return results


async def read_teams_data_by_team(team_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Teams_Data).where(Teams_Data.team_number == team_number)
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Team data not found")
        return results


async def read_teams_data_by_team_competition(
    competition: str,
    team_number: int,
    flagError: bool = True,
):
    with Session(team_engine) as session:
        statement = select(Teams_Data).where(
            Teams_Data.competition == competition,
            Teams_Data.team_number == team_number,
        )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Team competition data not found")
        return results


async def update_teams_data(
    competition: str,
    team_number: int,
    team_data: Teams_Data_Update,
):
    with Session(team_engine) as session:
        statement = select(Teams_Data).where(
            Teams_Data.competition == competition,
            Teams_Data.team_number == team_number,
        )

        db_team = session.exec(statement).first()

        if not db_team:
            raise HTTPException(status_code=404, detail="Team data not found")

        update_data = team_data.model_dump(exclude_unset=True)
        db_team.sqlmodel_update(update_data)

        session.add(db_team)
        session.commit()
        session.refresh(db_team)

        return db_team


async def delete_teams_data_by_team(team_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Teams_Data).where(Teams_Data.team_number == team_number)
        results = session.exec(statement).all()

        if flagError and not results:
            raise HTTPException(status_code=404, detail="Data not found")

        for team_data in results:
            session.delete(team_data)
        session.commit()
        return results


async def delete_teams_data_by_team_competition(
    competition: str,
    team_number: int,
    flagError: bool = True,
):
    with Session(team_engine) as session:
        statement = select(Teams_Data).where(
            Teams_Data.competition == competition,
            Teams_Data.team_number == team_number,
        )
        results = session.exec(statement).all()

        if flagError and not results:
            raise HTTPException(status_code=404, detail="Data not found")

        for team_data in results:
            session.delete(team_data)
        session.commit()
        return results
