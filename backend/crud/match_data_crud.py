from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from ..models.match_data_models import Match_Data, Match_Data_Create, Match_Data_Submission, Match_Data_Update
from ..database.scouting_db import engine


def _flatten_match_submission(match_data: Match_Data_Submission) -> Match_Data_Create:
    section_payloads = (
        match_data.prematch.model_dump(exclude_none=True),
        match_data.autonomous.model_dump(exclude_none=True),
        match_data.teleop.model_dump(exclude_none=True),
        match_data.endgame.model_dump(exclude_none=True),
        match_data.postmatch.model_dump(exclude_none=True),
    )

    flattened_data = {}
    for section_payload in section_payloads:
        flattened_data.update(section_payload)

    if match_data.user is not None:
        flattened_data["scouter"] = match_data.user

    required_fields = ("team_number", "match_number", "competition")
    missing_fields = [field for field in required_fields if flattened_data.get(field) is None]
    if missing_fields:
        raise HTTPException(
            status_code=422,
            detail=f"Missing required match identifier fields: {', '.join(missing_fields)}",
        )

    return Match_Data_Create.model_validate(flattened_data)


async def create_matches(match_data: Match_Data_Submission):
    with Session(engine) as session:
        db_data = Match_Data.model_validate(_flatten_match_submission(match_data))
        session.add(db_data)

        try:
            session.commit()
            session.refresh(db_data)
            return db_data
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400,
                detail="This team already has match data for this competition and match.",
            )


async def read_matches(flagError: bool = True):
    with Session(engine) as session:
        statement = select(Match_Data)
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Data not found")
        return results


async def read_matches_by_team(team_number: int, flagError: bool = True):
    with Session(engine) as session:
        statement = select(Match_Data).where(
            Match_Data.team_number == team_number
        )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Team data not found")
        return results


async def read_matches_by_match(competition: str, match_number: int, flagError: bool = True):
    with Session(engine) as session:
        statement = select(Match_Data).where(
            Match_Data.competition == competition,
            Match_Data.match_number == match_number
        )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(status_code=404, detail="Match data not found")
        return results


async def read_matches_by_team_match(competition: str, team_number: int, match_number: int, flagError: bool = True):
    with Session(engine) as session:
        statement = select(Match_Data).where(
            Match_Data.competition == competition,
            Match_Data.team_number == team_number,
            Match_Data.match_number == match_number
        )
        results = session.exec(statement).all()
        if flagError and not results:
            raise HTTPException(
                status_code=404, detail="Team match data not found")
        return results


async def update_matches(competition: str, team_number: int, match_number: int, match_data: Match_Data_Update):
    with Session(engine) as session:
        statement = select(Match_Data).where(
            Match_Data.competition == competition,
            Match_Data.team_number == team_number,
            Match_Data.match_number == match_number
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


async def delete_matches_by_match(competition: str, match_number: int, flagError: bool = True):
    with Session(engine) as session:
        statement = select(Match_Data).where(
            Match_Data.competition == competition,
            Match_Data.match_number == match_number
        )

        results = session.exec(statement).all()

        if flagError and not results:
            raise HTTPException(status_code=404, detail="Data not found")
        for match in results:
            session.delete(match)
        session.commit()
        return results


async def delete_matches_by_team(team_number: int, flagError: bool = True):
    with Session(engine) as session:
        statement = select(Match_Data).where(
            Match_Data.team_number == team_number,
        )

        results = session.exec(statement).all()

        if flagError and not results:
            raise HTTPException(status_code=404, detail="Data not found")
        for match in results:
            session.delete(match)
        session.commit()
        return results


async def delete_matches_by_team_match(competition: str, match_number: int, team_number: int, flagError: bool = True):
    with Session(engine) as session:
        statement = select(Match_Data).where(
            Match_Data.competition == competition,
            Match_Data.match_number == match_number,
            Match_Data.team_number == team_number
        )

        results = session.exec(statement).all()

        if flagError and not results:
            raise HTTPException(status_code=404, detail="Data not found")
        for match in results:
            session.delete(match)
        session.commit()
        return results
