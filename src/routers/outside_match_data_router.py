from fastapi import APIRouter

from ..crud.outside_match_data_crud import create_outside_match_data, read_outside_match_data, update_outside_match_data, delete_outside_match_data, read_outside_match_data_by_team
from ..models.outside_match_data_models import Outside_Match_Data, Outside_Match_Data_Create, Outside_Match_Data_Update


router = APIRouter()


@router.post("/data/outside_match_data/", response_model=Outside_Match_Data)
def create_outside_match_data_route(outside_match_data: Outside_Match_Data_Create):
    return create_outside_match_data(outside_match_data)


@router.get("/data/outside_match_data/", response_model=list[Outside_Match_Data])
def read_outside_match_data_route():
    return read_outside_match_data()


@router.get("/data/outside_match_data/team/{team_number}", response_model=list[Outside_Match_Data])
def read_outside_match_data_by_team_route(team_number: int):
    return read_outside_match_data_by_team(team_number)


@router.patch("/data/outside_match_data/team/{team_number}", response_model=Outside_Match_Data)
def update_outside_match_data_route(team_number: int, outside_match_data: Outside_Match_Data_Update):
    return update_outside_match_data(team_number, outside_match_data)


@router.delete("/data/outside_match_data/team/{team_number}")
def delete_outside_match_data_route(team_number: int):
    return delete_outside_match_data(team_number)