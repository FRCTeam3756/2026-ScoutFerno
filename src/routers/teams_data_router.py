from typing import Any

import statbotics
from fastapi import APIRouter, HTTPException

from ..crud.teams_data_crud import (
    create_teams_data,
    delete_teams_data_by_team,
    delete_teams_data_by_team_competition,
    read_teams_data,
    read_teams_data_by_team,
    read_teams_data_by_team_competition,
    update_teams_data,
)
from ..models.teams_data_models import (
    Teams_Data,
    Teams_Data_Create,
    Teams_Data_Update,
)

router = APIRouter(prefix="/data", tags=["Data"])

sb = statbotics.Statbotics()


def get_team_data(team_number: int, competition: str) -> dict[str, Any]:
    try:
        team_data = sb.get_team_event(team_number, competition)
    except UserWarning as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    if team_data is None:
        raise HTTPException(status_code=404, detail="Team data not found")
    return team_data


def get_team_profile(team_number: int) -> dict[str, Any]:
    try:
        team_profile = sb.get_team(team_number)
    except UserWarning as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    if team_profile is None:
        raise HTTPException(status_code=404, detail="Team profile not found")
    return team_profile


def build_team_data_from_statbotics(
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


@router.post("/teams_data/", response_model=Teams_Data)
async def create_teams_data_route(team_data: Teams_Data_Create):
    return await create_teams_data(team_data)


@router.post(
    "/teams_data/statbotics/competition/{competition}/team/{team_number}",
    response_model=Teams_Data,
)
async def import_statbotics_team_data_route(
    competition: str,
    team_number: int,
):
    team_profile = get_team_profile(team_number)
    team_event_data = get_team_data(team_number, competition)
    team_data = build_team_data_from_statbotics(
        team_number,
        competition,
        team_profile,
        team_event_data,
    )
    return await create_teams_data(team_data)


@router.get("/teams_data/", response_model=list[Teams_Data])
async def read_teams_data_route():
    return await read_teams_data()


@router.get("/teams_data/team/{team_number}", response_model=list[Teams_Data])
async def read_teams_data_by_team_route(team_number: int):
    return await read_teams_data_by_team(team_number)


@router.get(
    "/teams_data/competition/{competition}/team/{team_number}",
    response_model=list[Teams_Data],
)
async def read_teams_data_by_team_competition_route(
    competition: str,
    team_number: int,
):
    return await read_teams_data_by_team_competition(competition, team_number)


@router.patch(
    "/teams_data/competition/{competition}/team/{team_number}",
    response_model=Teams_Data,
)
async def update_teams_data_route(
    competition: str,
    team_number: int,
    team_data: Teams_Data_Update,
):
    return await update_teams_data(competition, team_number, team_data)


@router.delete("/teams_data/team/{team_number}")
async def delete_teams_data_by_team_route(team_number: int):
    return await delete_teams_data_by_team(team_number)


@router.delete("/teams_data/competition/{competition}/team/{team_number}")
async def delete_teams_data_by_team_competition_route(
    competition: str,
    team_number: int,
):
    return await delete_teams_data_by_team_competition(competition, team_number)
