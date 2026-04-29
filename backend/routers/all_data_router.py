from fastapi import APIRouter, Depends

from ..crud.all_data_crud import read_all_data, read_all_data_by_match, read_all_data_by_team, read_all_data_by_team_match, create_all_data, delete_all_data_by_team, delete_all_data_by_team_match, delete_all_data_by_match, update_all_data
from ..models.all_data_models import All_Data, All_Data_Create, All_Data_Interview, All_Data_Update
from ..security.google_auth_guard import require_auth


router = APIRouter(prefix="/data", tags=["Data"], dependencies=[Depends(require_auth)])


@router.get("/all_data/", response_model=All_Data_Interview)
async def read_all_data_route():
    return await read_all_data()


@router.get("/all_data/team/{team_number}", response_model=All_Data_Interview)
async def read_all_data_by_team_route(team_number: int):
    return await read_all_data_by_team(team_number)


@router.get("/all_data/competition/{competition}/match/{match_number}", response_model=All_Data)
async def read_all_data_by_match_route(competition: str, match_number: int):
    return await read_all_data_by_match(competition, match_number)


@router.get("/all_data/competition/{competition}/team/{team_number}/match/{match_number}", response_model=All_Data_Interview)
async def read_all_data_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await read_all_data_by_team_match(competition, team_number, match_number)


@router.post("/all_data/", response_model=All_Data)
async def create_all_data_route(match_data: All_Data_Create):
    return await create_all_data(match_data)


@router.delete("/all_data/competition/{competition}/match/{match_number}")
async def delete_all_data_by_match_route(competition: str, match_number: int):
    return await delete_all_data_by_match(competition, match_number)


@router.delete("/all_data/team/{team_number}")
async def delete_all_data_by_team_route(team_number: int):
    return await delete_all_data_by_team(team_number)


@router.delete("/all_data/competition/{competition}/team/{team_number}/match/{match_number}")
async def delete_all_data_by_team_match_route(competition: str, team_number: int, match_number: int):
    return await delete_all_data_by_team_match(competition, team_number, match_number)


@router.patch("/all_data/competition/{competition}/team/{team_number}/match/{match_number}")
async def update_all_data_by_team_match_route(competition: str, team_number: int, match_number: int, match_data: All_Data_Update):
    return await update_all_data(competition, team_number, match_number, match_data)
