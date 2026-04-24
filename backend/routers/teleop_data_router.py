# from fastapi import APIRouter
from fastapi import APIRouter, Depends
from google.oauth2.credentials import Credentials

from ..security.google_auth_guard import require_auth
from ..models.teleop_data_models import Teleop_Data, Teleop_Data_Create, Teleop_Data_Update
from ..crud.teleop_data_crud import create_teleop_data, delete_teleop_data_by_match, delete_teleop_data_by_team, delete_teleop_data_by_team_match, update_teleop_data, read_teleop_data, read_teleop_data_by_team, read_teleop_data_by_match, read_teleop_data_by_team_match

router = APIRouter(prefix="/data", tags=["Data"])


@router.post("/teleop_data/", response_model=Teleop_Data)
async def create_teleop_data_route(match_data: Teleop_Data_Create, creds: Credentials = Depends(require_auth)):
# async def create_teleop_data_route(match_data: Teleop_Data_Create):
    return await create_teleop_data(match_data)


@router.get("/teleop_data/", response_model=list[Teleop_Data])
async def read_teleop_data_route(creds: Credentials = Depends(require_auth)):
# async def read_teleop_data_route():
    return await read_teleop_data()


@router.get("/teleop_data/team/{team_number}", response_model=list[Teleop_Data])
async def read_teleop_data_by_team_route(team_number: int, creds: Credentials = Depends(require_auth)):
# async def read_teleop_data_by_team_route(team_number: int):
    return await read_teleop_data_by_team(team_number)


@router.get("/teleop_data/competition/{competition}/match/{match_number}", response_model=list[Teleop_Data])
async def read_teleop_data_by_match_route(competition: str, match_number: int, creds: Credentials = Depends(require_auth)):
# async def read_teleop_data_by_match_route(competition: str, match_number: int):
    return await read_teleop_data_by_match(competition, match_number)


@router.get("/teleop_data/competition/{competition}/team/{team_number}/match/{match_number}", response_model=list[Teleop_Data])
async def read_teleop_data_by_team_match_route(competition: str, team_number: int, match_number: int, creds: Credentials = Depends(require_auth)):
# async def read_teleop_data_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await read_teleop_data_by_team_match(competition, team_number, match_number)


@router.patch("/teleop_data/competition/{competition}/team/{team_number}/match/{match_number}", response_model=Teleop_Data)
async def update_teleop_data_route(competition: str, team_number: int, match_number: int, match_data: Teleop_Data_Update, creds: Credentials = Depends(require_auth)):
# async def update_teleop_data_route(competition: str, team_number: int, match_number: int, match_data: Teleop_Data_Update):
    return await update_teleop_data(competition, team_number, match_number, match_data)


@router.delete("/telelop_data/competition/{competition}/match/{match_number}")
async def delete_teleop_data_by_match_route(competition: str, match_number: int, creds: Credentials = Depends(require_auth)):
# async def delete_teleop_data_by_match_route(competition: str, match_number: int):
    return await delete_teleop_data_by_match(competition, match_number)


@router.delete("/telelop_data/team/{team_number}")
async def delete_teleop_data_by_team_route(team_number: int, creds: Credentials = Depends(require_auth)):
# async def delete_teleop_data_by_team_route(team_number: int):
    return await delete_teleop_data_by_team(team_number)


@router.delete("/telelop_data/competition/{competition}/team/{team_number}/match/{match_number}")
async def delete_teleop_data_by_team_match_route(competition: str, team_number: int, match_number: int, creds: Credentials = Depends(require_auth)):
# async def delete_teleop_data_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await delete_teleop_data_by_team_match(competition, team_number, match_number)