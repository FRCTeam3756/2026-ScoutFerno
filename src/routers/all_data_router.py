from fastapi import APIRouter
#, from fastapi import APIRouter, Depends
# from google.oauth2.credentials import Credentials

# from ..security.google_auth_guard import require_auth
from ..crud.all_data_crud import read_all_data, read_all_data_by_match, read_all_data_by_team, read_all_data_by_team_match, create_all_data
from ..models.all_data_models import All_Data, All_Data_Create


router = APIRouter(prefix="/data", tags=["Data"])


@router.get("/all_data/", response_model=All_Data)
# async def read_all_data_route(creds: Credentials = Depends(require_auth)):
async def read_all_data_route():
    return await read_all_data()


@router.get("/all_data/team/{team_number}", response_model=All_Data)
# async def read_all_data_by_team_route(team_number, creds: Credentials = Depends(require_auth)):
async def read_all_data_by_team_route(team_number: int):
    return await read_all_data_by_team(team_number)


@router.get("/all_data/competition/{competition}/match/{match_number}", response_model=All_Data)
# async def read_all_data_by_match_route(match_number, creds: Credentials = Depends(require_auth)):
async def read_all_data_by_match_route(competition: str, match_number: int):
    return await read_all_data_by_match(competition, match_number)

@router.get("/all_data/competition/{competition}/team/{team_number}/match/{match_number}", response_model=All_Data)
# async def read_all_data_by_team_match_route(team_number, match_number, creds: Credentials = Depends(require_auth)):
async def read_all_data_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await read_all_data_by_team_match(competition, team_number, match_number)


@router.post("/all_data/", response_model=All_Data_Create)
async def create_all_data_route(match_data: All_Data_Create):
    return await create_all_data(match_data)