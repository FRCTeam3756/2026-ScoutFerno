from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from ..models.scout_data import Scout_Data, Scout_Data_Create, Scout_Data_Update
from ..models.sql_models import scout_engine


async def create_scout_data(scout_data: Scout_Data_Create):
    with Session(scout_engine) as session:
        db_data = Scout_Data.model_validate(scout_data)
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


async def read_scout_data(flagError: bool = True):
    with Session(scout_engine) as session:
        statement = select(Scout_Data).where(
            )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Data not found")
        return results


async def read_scout_data_by_individual(scout_name: str, team_number: int, flagError: bool = True):
    with Session(scout_engine) as session:
        statement = select(Scout_Data).where(
            Scout_Data.scout_name == scout_name,
            )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Team data not found")
        return results


async def update_scout_data(scout_name: str, scout_data: Scout_Data_Update):
    with Session(scout_engine) as session:
        statement = select(Scout_Data).where(
            Scout_Data.scout_name == scout_name,
        )

        db_match = session.exec(statement).first()

        if not db_match:
            raise HTTPException(status_code=404, detail="Match data not found")

        update_data = scout_data.model_dump(exclude_unset=True)
        db_match.sqlmodel_update(update_data)

        session.add(db_match)
        session.commit()
        session.refresh(db_match)

        return db_match
    
async def update_scout_data_by_individual(scout_name: str, scout_data: Scout_Data_Update):
 with Session(scout_engine) as session:
    statement = select(Scout_Data).where(
        Scout_Data.scout_name == scout_name,
    )

    db_match = session.exec(statement).first()

    if not db_match:
        raise HTTPException(status_code=404, detail="Match data not found")

    update_data = scout_data.model_dump(exclude_unset=True)
    db_match.sqlmodel_update(update_data)

    session.add(db_match)
    session.commit()
    session.refresh(db_match)

    return db_match


async def delete_scout_data(scout_name: str):
    with Session(scout_engine) as session:
        statement = select(Scout_Data).where(
            Scout_Data.scout_name == scout_name,
        )

        match_data = session.exec(statement).first()

        if not match_data:
            raise HTTPException(status_code=404, detail="Data not found")
        session.delete(match_data)
        session.commit()
        return {"ok": True}
    

async def delete_scout_data_by_individual(scout_name: str):
    with Session(scout_engine) as session:
        statement = select(Scout_Data).where(
            Scout_Data.scout_name == scout_name,
        )

        team_match_data = session.exec(statement).all()

        if not team_match_data:
            raise HTTPException(status_code=404, detail="Data not found")
        for match in team_match_data:
            session.delete(match)
        session.commit()
        return {"ok": True}