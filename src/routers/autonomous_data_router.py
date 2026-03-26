from fastapi import APIRouter
# from fastapi import APIRouter, Depends
# from google.oauth2.credentials import Credentials

# from ..security.google_auth_guard import require_auth
from ..models.autonomous_data_models import Autonomous_Data, Autonomous_Data_Create, Autonomous_Data_Update
from ..crud.autonomous_data_crud import create_autonomous_data, delete_autonomous_data_by_match, delete_autonomous_data_by_team, delete_autonomous_data_by_team_match, update_autonomous_data, read_autonomous_data, read_autonomous_data_by_team, read_autonomous_data_by_match, read_autonomous_data_by_team_match

router = APIRouter(prefix="/data", tags=["Data"])


@router.post("/auto_data/", response_model=Autonomous_Data)
# async def create_autonomous_data_route(match_data: Autonomous_Data_Create, creds: Credentials = Depends(require_auth)):
async def create_autonomous_data_route(match_data: Autonomous_Data_Create):
    return await create_autonomous_data(match_data)


@router.get("/auto_data/", response_model=list[Autonomous_Data])
# async def read_autonomous_data_route(creds: Credentials = Depends(require_auth)):
async def read_autonomous_data_route():
    return await read_autonomous_data()


@router.get("/auto_data/team/{team_number}", response_model=list[Autonomous_Data])
# async def read_autonomous_data_by_team_route(team_number: int, creds: Credentials = Depends(require_auth)):
async def read_autonomous_data_by_team_route(team_number: int):
    return await read_autonomous_data_by_team(team_number)


@router.get("/auto_data/competition/{competition}/match/{match_number}", response_model=list[Autonomous_Data])
# async def read_autonomous_data_by_match_route(match_number: int, creds: Credentials = Depends(require_auth)):
async def read_autonomous_data_by_match_route(competition: str, match_number: int):
    return await read_autonomous_data_by_match(competition, match_number)


@router.get("/auto_data/competition/{competition}/team/{team_number}/match/{match_number}", response_model=list[Autonomous_Data])
# async def read_autonomous_data_by_team_match_route(team_number: int, match_number: int, creds: Credentials = Depends(require_auth)):
async def read_autonomous_data_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await read_autonomous_data_by_team_match(competition, team_number, match_number)


@router.patch("/auto_data/competition/{competition}/team/{team_number}/match/{match_number}", response_model=Autonomous_Data)
# async def update_autonomous_data_route(team_number: int, match_number: int, match_data: Autonomous_Data_Update, creds: Credentials = Depends(require_auth)):
async def update_autonomous_data_route(competition: str, team_number: int, match_number: int, match_data: Autonomous_Data_Update):
    return await update_autonomous_data(competition, team_number, match_number, match_data)


@router.delete("/auto_data/competition/{competition}/match/{match_number}")
# async def delete_autonomous_data_by_match_route(competition: str, match_number: int, creds: Credentials = Depends(require_auth)):
async def delete_autonomous_data_by_match_route(competition: str, match_number: int):
    return await delete_autonomous_data_by_match(competition, match_number)


@router.delete("/auto_data/team/{team_number}")
# async def delete_autonomous_data_by_team_route(team_number: int, creds: Credentials = Depends(require_auth)):
async def delete_autonomous_data_by_team_route(team_number: int):
    return await delete_autonomous_data_by_team(team_number)


@router.delete("/auto_data/competition/{competition}/team/{team_number}/match/{match_number}")
# async def delete_autonomous_data_by_team_match_route(competition: str, team_number: int, match_number: int, creds: Credentials = Depends(require_auth)):
async def delete_autonomous_data_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await delete_autonomous_data_by_team_match(competition, team_number, match_number)