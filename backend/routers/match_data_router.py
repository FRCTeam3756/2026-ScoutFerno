from typing import List

from fastapi import APIRouter, Depends

from ..crud import match_data_crud
from ..models.match_data_models import Match_Data, Match_Data_Submission
from ..security.google_auth_guard import require_auth


router = APIRouter(prefix="", tags=["Data"],
                   dependencies=[Depends(require_auth)])


@router.post("/matches/", response_model=Match_Data)
async def create_matches_route(matches: Match_Data_Submission):
    return await match_data_crud.create_matches(matches)


@router.get("/matches/", response_model=List[Match_Data])
async def read_matches_root_route():
    return await match_data_crud.read_matches(flagError=False)


@router.get("/matches/all_teams", response_model=List[Match_Data])
async def read_matches_route():
    return await match_data_crud.read_matches(flagError=False)


@router.get("/matches/team/{team_number}", response_model=List[Match_Data])
async def read_matches_by_team_route(team_number: int):
    return await match_data_crud.read_matches_by_team(team_number, flagError=False)


@router.get("/matches/competition/{competition}/match/{match_number}", response_model=List[Match_Data])
async def read_matches_by_match_route(competition: str, match_number: int):
    return await match_data_crud.read_matches_by_match(competition, match_number, flagError=False)


@router.get("/matches/competition/{competition}/team/{team_number}/match/{match_number}", response_model=List[Match_Data])
async def read_matches_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await match_data_crud.read_matches_by_team_match(competition, team_number, match_number, flagError=False)


@router.delete("/matches/competition/{competition}/match/{match_number}")
async def delete_matches_by_match_route(competition: str, match_number: int):
    return await match_data_crud.delete_matches_by_match(competition, match_number)


@router.delete("/matches/team/{team_number}")
async def delete_matches_by_team_route(team_number: int):
    return await match_data_crud.delete_matches_by_team(team_number)


@router.delete("/matches/competition/{competition}/team/{team_number}/match/{match_number}")
async def delete_matches_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await match_data_crud.delete_matches_by_team_match(competition, team_number, match_number)
