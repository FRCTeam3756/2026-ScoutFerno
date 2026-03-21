from fastapi import APIRouter
#, from fastapi import APIRouter, Depends
# from google.oauth2.credentials import Credentials

# from ..security.google_auth_guard import require_auth
from ..crud.all_data_crud import read_all_data, read_all_data_by_match, read_all_data_by_team, read_all_data_by_team_match
from ..models.all_data_models import All_Data


router = APIRouter(prefix="/data", tags=["Data"])


@router.get("/all_data/year/{year}", response_model=All_Data)
# async def read_all_data_route(year: int, creds: Credentials = Depends(require_auth)):
async def read_all_data_route(year: int):
    return await read_all_data(year)


@router.get("/all_data/year/{year}/team/{team_number}", response_model=All_Data)
# async def read_all_data_by_team_route(team_number: int, creds: Credentials = Depends(require_auth)):
async def read_all_data_by_team_route(year: int, team_number: int):
    return await read_all_data_by_team(year, team_number)


@router.get("/all_data/year/{year}/competition/{competition}/match/{match_type}/{match_number}", response_model=All_Data)
# async def read_all_data_by_match_route(match_number: int, creds: Credentials = Depends(require_auth)):
async def read_all_data_by_match_route(competition: str, year: int, match_type: str, match_number: int):
    return await read_all_data_by_match(year, competition, match_type, match_number)

@router.get("/all_data/year/{year}/competition/{competition}/team/{team_number}/match/{match_type}/{match_number}", response_model=All_Data)
# async def read_all_data_by_team_match_route(team_number: int, match_number: int, creds: Credentials = Depends(require_auth)):
async def read_all_data_by_team_match_route(year: int, competition: str, team_number: int, match_type: str, match_number: int):
    return await read_all_data_by_team_match(year, competition, team_number, match_type, match_number)

