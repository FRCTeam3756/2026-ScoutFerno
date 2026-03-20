from fastapi import APIRouter, Depends
from google.oauth2.credentials import Credentials

from ..security.google_auth_guard import require_auth
from ..models.auto_data_models import Auto_Data, Auto_Data_Create, Auto_Data_Update
from ..crud.auto_data_crud import create_auto_data, delete_team_auto_data, delete_match_auto_data, update_auto_data, read_auto_data, read_auto_data_by_team, read_auto_data_by_match, read_auto_data_by_team_match

router = APIRouter(prefix="/data", tags=["Data"])


@router.post("/auto_data/", response_model=Auto_Data)
async def create_auto_data_route(match_data: Auto_Data_Create, creds: Credentials = Depends(require_auth)):
    return await create_auto_data(match_data)


@router.get("/auto_data/", response_model=list[Auto_Data])
async def read_auto_data_route(creds: Credentials = Depends(require_auth)):
    return await read_auto_data()


@router.get("/auto_data/team/{team_number}", response_model=list[Auto_Data])
async def read_auto_data_by_team_route(team_number: int, creds: Credentials = Depends(require_auth)):
    return await read_auto_data_by_team(team_number)


@router.get("/auto_data/match/{match_number}", response_model=list[Auto_Data])
async def read_auto_data_by_match_route(match_number: int, creds: Credentials = Depends(require_auth)):
    return await read_auto_data_by_match(match_number)


@router.get("/auto_data/team/{team_number}/match/{match_number}", response_model=list[Auto_Data])
async def read_auto_data_by_team_match_route(team_number: int, match_number: int, creds: Credentials = Depends(require_auth)):
    return await read_auto_data_by_team_match(team_number, match_number)


@router.patch("/auto_data/team/{team_number}/match/{match_number}", response_model=Auto_Data)
async def update_auto_data_route(team_number: int, match_number: int, match_data: Auto_Data_Update, creds: Credentials = Depends(require_auth)):
    return await update_auto_data(team_number, match_number, match_data)


@router.delete("/auto_data/team/{team_number}/match/{match_number}")
async def delete_match_auto_data_route(team_number: int, match_number: int, creds: Credentials = Depends(require_auth)):
    return await delete_match_auto_data(team_number, match_number)


@router.delete("/auto_data/team/{team_number}")
async def delete_team_auto_data_route(team_number: int, creds: Credentials = Depends(require_auth)):
    return await delete_team_auto_data(team_number)