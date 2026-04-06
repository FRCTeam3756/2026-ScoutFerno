import statbotics; sb = statbotics.Statbotics()

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from typing import Any

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


async def get_team_data(team_number: int, competition: str) -> dict[str, Any]:
    try:
        team_data = sb.get_team_event(team_number, competition)
    except UserWarning as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    if team_data is None:
        raise HTTPException(status_code=404, detail="Team data not found")
    return team_data


async def get_team_profile(team_number: int) -> dict[str, Any]:
    try:
        team_profile = sb.get_team(team_number)
    except UserWarning as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    if team_profile is None:
        raise HTTPException(status_code=404, detail="Team profile not found")
    return team_profile


async def build_team_data_from_statbotics(
    team_number: int,
    competition: str,
    team_profile: dict[str, Any],
    team_event_data: dict[str, Any],
) -> Teams_Data_Create:
    epa = team_event_data.get("epa") or {}
    epa_stats = epa.get("stats") or {}
    record = team_event_data.get("record") or {}
    total_record = record.get("total") or {}

    return Teams_Data_Create(
        team_number=team_number,
        competition=competition,
        name=team_profile.get("name"),
        country=team_profile.get("country"),
        state=team_profile.get("state"),
        district=team_profile.get("district"),
        rookie_year=team_profile.get("rookie_year"),
        active=team_profile.get("active"),
        record_wins=total_record.get("wins"),
        record_losses=total_record.get("losses"),
        record_ties=total_record.get("ties"),
        record_count=total_record.get("count"),
        record_winrate=total_record.get("winrate"),
        norm_epa_current=epa_stats.get("pre_elim"),
        norm_epa_recent=epa_stats.get("start"),
        norm_epa_mean=epa_stats.get("mean"),
        norm_epa_max=epa_stats.get("max"),
    )