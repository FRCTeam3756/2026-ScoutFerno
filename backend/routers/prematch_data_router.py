from fastapi import APIRouter
# from fastapi import APIRouter, Depends
# from google.oauth2.credentials import Credentials

# from ..security.google_auth_guard import require_auth
from ..models.prematch_data_models import Prematch_Data, Prematch_Data_Create, Prematch_Data_Update
from ..crud.prematch_data_crud import create_prematch_data, delete_prematch_data_by_match, delete_prematch_data_by_team, delete_prematch_data_by_team_match, update_prematch_data, read_prematch_data, read_prematch_data_by_team, read_prematch_data_by_match, read_prematch_data_by_team_match

router = APIRouter(prefix="/data", tags=["Data"])


@router.post("/prematch_data/", response_model=Prematch_Data)
# async def create_prematch_data_route(match_data: Prematch_Data_Create, creds: Credentials = Depends(require_auth)):
async def create_prematch_data_route(match_data: Prematch_Data_Create):
    return await create_prematch_data(match_data)


@router.get("/prematch_data/", response_model=list[Prematch_Data])
# async def read_prematch_data_route(creds: Credentials = Depends(require_auth)):
async def read_prematch_data_route():
    return await read_prematch_data()


@router.get("/prematch_data/team/{team_number}", response_model=list[Prematch_Data])
# async def read_prematch_data_by_team_route(team_number: int, creds: Credentials = Depends(require_auth)):
async def read_prematch_data_by_team_route(team_number: int):
    return await read_prematch_data_by_team(team_number)


@router.get("/prematch_data/competition/{competition}/match/{match_number}", response_model=list[Prematch_Data])
# async def read_prematch_data_by_match_route(match_number: int, creds: Credentials = Depends(require_auth)):
async def read_prematch_data_by_match_route(competition: str, match_number: int):
    return await read_prematch_data_by_match(competition, match_number)


@router.get("/prematch_data/competition/{competition}/team/{team_number}/match/{match_number}", response_model=list[Prematch_Data])
# async def read_prematch_data_by_team_match_route(team_number: int, match_number: int, creds: Credentials = Depends(require_auth)):
async def read_prematch_data_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await read_prematch_data_by_team_match(competition, team_number, match_number)


@router.patch("/prematch_data/competition/{competition}/team/{team_number}/match/{match_number}", response_model=Prematch_Data)
# async def update_prematch_data_route(team_number: int, match_number: int, match_data: Prematch_Data_Update, creds: Credentials = Depends(require_auth)):
async def update_prematch_data_route(competition: str, team_number: int, match_number: int, match_data: Prematch_Data_Update):
    return await update_prematch_data(competition, team_number, match_number, match_data)


@router.delete("/prematch_data/competition/{competition}/match/{match_number}")
# async def delete_prematch_data_by_match_route(competition: str, match_number: int, creds: Credentials = Depends(require_auth)):
async def delete_prematch_data_by_match_route(competition: str, match_number: int):
    return await delete_prematch_data_by_match(competition, match_number)


@router.delete("/prematch_data/team/{team_number}")
# async def delete_prematch_data_by_team_route(team_number: int, creds: Credentials = Depends(require_auth)):
async def delete_prematch_data_by_team_route(team_number: int):
    return await delete_prematch_data_by_team(team_number)


@router.delete("/prematch_data/competition/{competition}/team/{team_number}/match/{match_number}")
# async def delete_prematch_data_by_team_match_route(competition: str, team_number: int, match_number: int, creds: Credentials = Depends(require_auth)):
async def delete_prematch_data_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await delete_prematch_data_by_team_match(competition, team_number, match_number)