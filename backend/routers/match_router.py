from fastapi import APIRouter, Depends

from ..crud.match_data_crud import read_match_data, read_match_data_by_match, read_match_data_by_team, read_match_data_by_team_match, delete_match_data_by_team, delete_match_data_by_team_match, delete_match_data_by_match, update_match_data
from ..models.match_data_models import Match_Data
from ..security.google_auth_guard import require_auth


router = APIRouter(prefix="", tags=["Data"], dependencies=[Depends(require_auth)])


@router.get("/match_data/", response_model=Match_Data)
async def read_match_data_route():
    return await read_match_data()


@router.get("/match_data/team/{team_number}", response_model=Match_Data)
async def read_match_data_by_team_route(team_number: int):
    return await read_match_data_by_team(team_number)


@router.get("/match_data/competition/{competition}/match/{match_number}", response_model=Match_Data)
async def read_match_data_by_match_route(competition: str, match_number: int):
    return await read_match_data_by_match(competition, match_number)


@router.get("/match_data/competition/{competition}/team/{team_number}/match/{match_number}", response_model=Match_Data)
async def read_match_data_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await read_match_data_by_team_match(competition, team_number, match_number)


@router.delete("/match_data/competition/{competition}/match/{match_number}")
async def delete_match_data_by_match_route(competition: str, match_number: int):
    return await delete_match_data_by_match(competition, match_number)


@router.delete("/match_data/team/{team_number}")
async def delete_match_data_by_team_route(team_number: int):
    return await delete_match_data_by_team(team_number)


@router.delete("/match_data/competition/{competition}/team/{team_number}/match/{match_number}")
async def delete_match_data_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await delete_match_data_by_team_match(competition, team_number, match_number)