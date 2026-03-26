from fastapi import APIRouter
# from fastapi import APIRouter, Depends
# from google.oauth2.credentials import Credentials

# from ..security.google_auth_guard import require_auth
from ..models.endgame_data_models import Endgame_Data, Endgame_Data_Create, Endgame_Data_Update
from ..crud.endgame_data_crud import create_endgame_data, delete_endgame_data_by_match, delete_endgame_data_by_team, delete_endgame_data_by_team_match, update_endgame_data, read_endgame_data, read_endgame_data_by_team, read_endgame_data_by_match, read_endgame_data_by_team_match

router = APIRouter(prefix="/data", tags=["Data"])


@router.post("/endgame_data/", response_model=Endgame_Data)
# async def create_endgame_data_route(match_data: Endgame_Data_Create, creds: Credentials = Depends(require_auth)):
async def create_endgame_data_route(match_data: Endgame_Data_Create):
    return await create_endgame_data(match_data)


@router.get("/endgame_data/", response_model=list[Endgame_Data])
# async def read_endgame_data_route(creds: Credentials = Depends(require_auth)):
async def read_endgame_data_route():
    return await read_endgame_data()


@router.get("/endgame_data/team/{team_number}", response_model=list[Endgame_Data])
# async def read_endgame_data_by_team_route(team_number: int, creds: Credentials = Depends(require_auth)):
async def read_endgame_data_by_team_route(team_number: int):
    return await read_endgame_data_by_team(team_number)


@router.get("/endgame_data/competition/{competition}/match/{match_number}", response_model=list[Endgame_Data])
# async def read_endgame_data_by_match_route(match_number: int, creds: Credentials = Depends(require_auth)):
async def read_endgame_data_by_match_route(competition: str, match_number: int):
    return await read_endgame_data_by_match(competition, match_number)


@router.get("/endgame_data/competition/{competition}/team/{team_number}/match/{match_number}", response_model=list[Endgame_Data])
# async def read_endgame_data_by_team_match_route(team_number: int, match_number: int, creds: Credentials = Depends(require_auth)):
async def read_endgame_data_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await read_endgame_data_by_team_match(competition, team_number, match_number)


@router.patch("/endgame_data/competition/{competition}/team/{team_number}/match/{match_number}", response_model=Endgame_Data)
# async def update_endgame_data_route(team_number: int, match_number: int, match_data: Endgame_Data_Update, creds: Credentials = Depends(require_auth)):
async def update_endgame_data_route(competition: str, team_number: int, match_number: int, match_data: Endgame_Data_Update):
    return await update_endgame_data(competition, team_number, match_number, match_data)


@router.delete("/endgame_data/competition/{competition}/match/{match_number}")
# async def delete_endgame_data_by_match_route(competition: str, match_number: int, creds: Credentials = Depends(require_auth)):
async def delete_endgame_data_by_match_route(competition: str, match_number: int):
    return await delete_endgame_data_by_match(competition, match_number)


@router.delete("/endgame_data/team/{team_number}")
# async def delete_endgame_data_by_team_route(team_number: int, creds: Credentials = Depends(require_auth)):
async def delete_endgame_data_by_team_route(team_number: int):
    return await delete_endgame_data_by_team(team_number)


@router.delete("/endgame_data/competition/{competition}/team/{team_number}/match/{match_number}")
# async def delete_endgame_data_by_team_match_route(competition: str, team_number: int, match_number: int, creds: Credentials = Depends(require_auth)):
async def delete_endgame_data_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await delete_endgame_data_by_team_match(competition, team_number, match_number)