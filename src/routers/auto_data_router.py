from fastapi import APIRouter
# from fastapi import APIRouter, Depends
# from google.oauth2.credentials import Credentials

# from ..security.google_auth_guard import require_auth
from ..models.auto_data_models import Auto_Data, Auto_Data_Create, Auto_Data_Update
from ..crud.auto_data_crud import create_auto_data, delete_team_auto_data, delete_match_auto_data, update_auto_data, read_auto_data, read_auto_data_by_team, read_auto_data_by_match, read_auto_data_by_team_match

router = APIRouter(prefix="/data", tags=["Data"])


@router.post("/auto_data/", response_model=Auto_Data)
# async def create_auto_data_route(match_data: Auto_Data_Create, creds: Credentials = Depends(require_auth)):
async def create_auto_data_route(match_data: Auto_Data_Create):
    return await create_auto_data(match_data)


@router.get("/auto_data/year/{year}", response_model=list[Auto_Data])
# async def read_auto_data_route(creds: Credentials = Depends(require_auth)):
async def read_auto_data_route(year: int):
    return await read_auto_data(year)


@router.get("/auto_data/year/{year}/team/{team_number}", response_model=list[Auto_Data])
# async def read_auto_data_by_team_route(team_number: int, creds: Credentials = Depends(require_auth)):
async def read_auto_data_by_team_route(year: int, team_number: int):
    return await read_auto_data_by_team(year, team_number)


@router.get("/auto_data/year/{year}/competition/{competition}/match/{match_number}", response_model=list[Auto_Data])
# async def read_auto_data_by_match_route(match_number: int, creds: Credentials = Depends(require_auth)):
async def read_auto_data_by_match_route(year: int, competition: str, match_number: int):
    return await read_auto_data_by_match(year, competition, match_number)


@router.get("/auto_data/year/{year}/competition/{competition}/team/{team_number}/match/{match_number}", response_model=list[Auto_Data])
# async def read_auto_data_by_team_match_route(team_number: int, match_number: int, creds: Credentials = Depends(require_auth)):
async def read_auto_data_by_team_match_route(year: int, competition: str, team_number: int, match_number: int):
    return await read_auto_data_by_team_match(year, competition, team_number, match_number)


@router.patch("/auto_data/year/{year}/competition/{competition}/team/{team_number}/match/{match_number}", response_model=Auto_Data)
# async def update_auto_data_route(team_number: int, match_number: int, match_data: Auto_Data_Update, creds: Credentials = Depends(require_auth)):
async def update_auto_data_route(year: int, competition: str, team_number: int, match_number: int, match_data: Auto_Data_Update):
    return await update_auto_data(year, competition, team_number, match_number, match_data)


@router.delete("/auto_data/year/{year}/competition/{competition}/team/{team_number}/match/{match_number}")
# async def delete_match_auto_data_route(team_number: int, match_number: int, creds: Credentials = Depends(require_auth)):
async def delete_match_auto_data_route(year: int, competition: str, team_number: int, match_number: int):
    return await delete_match_auto_data(year, competition, team_number, match_number)


@router.delete("/auto_data/year/{year}/team/{team_number}")
# async def delete_team_auto_data_route(team_number: int, creds: Credentials = Depends(require_auth)):
async def delete_team_auto_data_route(year: int, team_number: int):
    return await delete_team_auto_data(year, team_number)