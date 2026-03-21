from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from ..models.auto_data_models import Auto_Data, Auto_Data_Create, Auto_Data_Update
from ..models.sql_models import team_engine


async def create_auto_data(match_data: Auto_Data_Create):
    with Session(team_engine) as session:
        db_data = Auto_Data.model_validate(match_data)
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


async def read_auto_data():
    with Session(team_engine) as session:
        match_data = session.exec(select(Auto_Data)).all()
        return match_data


async def read_auto_data_by_team(team_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Auto_Data).where(Auto_Data.team_number == team_number)
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Team data not found")
        return results
     

async def read_auto_data_by_match(match_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Auto_Data).where(Auto_Data.match_number == match_number)
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Match data not found")
        return results
    

async def read_auto_data_by_team_match(team_number: int, match_number: int, flagError: bool = True):
    with Session(team_engine) as session:
        statement = select(Auto_Data).where(
            Auto_Data.team_number == team_number,
            Auto_Data.match_number == match_number
            )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Team match data not found")
        return results


async def update_auto_data(team_number: int, match_number: int, match_data: Auto_Data_Update):
    with Session(team_engine) as session:
        statement = select(Auto_Data).where(
            Auto_Data.team_number == team_number,
            Auto_Data.match_number == match_number
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


async def delete_match_auto_data(team_number: int, match_number: int):
    with Session(team_engine) as session:
        statement = select(Auto_Data).where(
            Auto_Data.team_number == team_number,
            Auto_Data.match_number == match_number
        )

        match_data = session.exec(statement).first()

        if not match_data:
            raise HTTPException(status_code=404, detail="Data not found")
        session.delete(match_data)
        session.commit()
        return {"ok": True}
    

async def delete_team_auto_data(team_number: int):
    with Session(team_engine) as session:
        statement = select(Auto_Data).where(
            Auto_Data.team_number == team_number,
        )

        team_match_data = session.exec(statement).all()

        if not team_match_data:
            raise HTTPException(status_code=404, detail="Data not found")
        for match in team_match_data:
            session.delete(match)
        session.commit()
        return {"ok": True}