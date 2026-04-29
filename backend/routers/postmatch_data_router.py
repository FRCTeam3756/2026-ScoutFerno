from fastapi import APIRouter, Depends

from ..models.postmatch_data_models import Postmatch_Data, Postmatch_Data_Create, Postmatch_Data_Update
from ..crud.postmatch_data_crud import create_postmatch_data, delete_postmatch_data_by_match, delete_postmatch_data_by_team, delete_postmatch_data_by_team_match, update_postmatch_data, read_postmatch_data, read_postmatch_data_by_team, read_postmatch_data_by_match, read_postmatch_data_by_team_match
from ..security.google_auth_guard import require_auth

router = APIRouter(prefix="/data", tags=["Data"], dependencies=[Depends(require_auth)])


@router.post("/postmatch_data/", response_model=Postmatch_Data)
async def create_postmatch_data_route(match_data: Postmatch_Data_Create):
    return await create_postmatch_data(match_data)


@router.get("/postmatch_data/", response_model=list[Postmatch_Data])
async def read_postmatch_data_route():
    return await read_postmatch_data()


@router.get("/postmatch_data/team/{team_number}", response_model=list[Postmatch_Data])
async def read_postmatch_data_by_team_route(team_number: int):
    return await read_postmatch_data_by_team(team_number)


@router.get("/postmatch_data/competition/{competition}/match/{match_number}", response_model=list[Postmatch_Data])
async def read_postmatch_data_by_match_route(competition: str, match_number: int):
    return await read_postmatch_data_by_match(competition, match_number)


@router.get("/postmatch_data/competition/{competition}/team/{team_number}/match/{match_number}", response_model=list[Postmatch_Data])
async def read_postmatch_data_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await read_postmatch_data_by_team_match(competition, team_number, match_number)


@router.patch("/postmatch_data/competition/{competition}/team/{team_number}/match/{match_number}", response_model=Postmatch_Data)
async def update_postmatch_data_route(competition: str, team_number: int, match_number: int, match_data: Postmatch_Data_Update):
    return await update_postmatch_data(competition, team_number, match_number, match_data)


@router.delete("/postmatch_data/competition/{competition}/match/{match_number}")
async def delete_postmatch_data_by_match_route(competition: str, match_number: int):
    return await delete_postmatch_data_by_match(competition, match_number)


@router.delete("/postmatch_data/team/{team_number}")
async def delete_postmatch_data_by_team_route(team_number: int):
    return await delete_postmatch_data_by_team(team_number)


@router.delete("/postmatch_data/competition/{competition}/team/{team_number}/match/{match_number}")
async def delete_postmatch_data_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await delete_postmatch_data_by_team_match(competition, team_number, match_number)
