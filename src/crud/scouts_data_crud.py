from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from ..models.scouts_data_models import Scout_Data, Scout_Data_Create, Scout_Data_Update
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
                detail="A scout with this data could not be created.",
            )


async def read_scout_data(flagError: bool = True):
    with Session(scout_engine) as session:
        statement = select(Scout_Data)
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Scout data not found")
        return results


async def read_scout_data_by_individual(scout_id: int, flagError: bool = True):
    with Session(scout_engine) as session:
        statement = select(Scout_Data).where(Scout_Data.id == scout_id)
        result = session.exec(statement).first()
        if flagError and not result:
            raise HTTPException(status_code=404, detail="Scout data not found")
        return result


async def update_scout_data(scout_name: str, scout_data: Scout_Data_Update):
    with Session(scout_engine) as session:
        statement = select(Scout_Data).where(Scout_Data.scout_name == scout_name)
        db_scout = session.exec(statement).first()

        if not db_scout:
            raise HTTPException(status_code=404, detail="Scout data not found")

        update_data = scout_data.model_dump(exclude_unset=True)
        db_scout.sqlmodel_update(update_data)

        session.add(db_scout)
        session.commit()
        session.refresh(db_scout)

        return db_scout


async def update_scout_data_by_individual(scout_id: int, scout_data: Scout_Data_Update):
    with Session(scout_engine) as session:
        statement = select(Scout_Data).where(Scout_Data.id == scout_id)
        db_scout = session.exec(statement).first()

        if not db_scout:
            raise HTTPException(status_code=404, detail="Scout data not found")

        update_data = scout_data.model_dump(exclude_unset=True)
        db_scout.sqlmodel_update(update_data)

        session.add(db_scout)
        session.commit()
        session.refresh(db_scout)

        return db_scout


async def delete_scout_data(scout_name: str):
    with Session(scout_engine) as session:
        statement = select(Scout_Data).where(Scout_Data.scout_name == scout_name)
        scout_data = session.exec(statement).first()

        if not scout_data:
            raise HTTPException(status_code=404, detail="Scout data not found")

        session.delete(scout_data)
        session.commit()
        return {"ok": True}


async def delete_scout_data_by_individual(scout_id: int):
    with Session(scout_engine) as session:
        statement = select(Scout_Data).where(Scout_Data.id == scout_id)
        scout_data = session.exec(statement).first()

        if not scout_data:
            raise HTTPException(status_code=404, detail="Scout data not found")

        session.delete(scout_data)
        session.commit()
        return {"ok": True}
