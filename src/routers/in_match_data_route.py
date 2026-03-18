from fastapi import FastAPI

from ..models.fastapi_models import lifespan
from ..models.in_match_data_models import In_Match_Data, In_Match_Data_Create, In_Match_Data_Update
from ..crud.in_match_data_crud import create_in_match_data, delete_team_in_match_data, delete_match_in_match_data, update_in_match_data, read_in_match_data, read_in_match_data_by_team, read_in_match_data_by_match, read_in_match_data_by_team_match



app = FastAPI(lifespan=lifespan)


@app.post("/data/match_data/", response_model=In_Match_Data)
def create_in_match_data_route(match_data: In_Match_Data_Create):
    return create_in_match_data(match_data)


@app.get("/data/match_data/", response_model=list[In_Match_Data])
def read_in_match_data_route():
    return read_in_match_data()


@app.get("/data/match_data/team/{team_number}", response_model=list[In_Match_Data])
def read_in_match_data_by_team_route(team_number: int):
    return read_in_match_data_by_team(team_number)


@app.get("/data/match_data/match/{match_number}", response_model=list[In_Match_Data])
def read_in_match_data_by_match_route(match_number: int):
    return read_in_match_data_by_match(match_number)


@app.get("/data/match_data/team/{team_number}/match/{match_number}", response_model=list[In_Match_Data])
def read_in_match_data_by_team_match_route(team_number: int, match_number: int):
    return read_in_match_data_by_team_match(team_number, match_number)


@app.patch("/data/match_data/team/{team_number}/match/{match_number}", response_model=In_Match_Data)
def update_in_match_data_route(team_number: int, match_number: int, match_data: In_Match_Data_Update):
    return update_in_match_data(team_number, match_number, match_data)


@app.delete("/data/match_data/team/{team_number}/match/{match_number}")
def delete_match_in_match_data_route(team_number: int, match_number: int):
    return delete_match_in_match_data(team_number, match_number)


@app.delete("/data/match_data/team/{team_number}")
def delete_team_in_match_data_route(team_number: int):
    return delete_team_in_match_data(team_number)