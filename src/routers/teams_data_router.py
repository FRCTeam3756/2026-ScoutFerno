# import statbotics
# from fastapi import APIRouter

# from ..crud.teams_data_crud import (
#     create_teams_data,
#     delete_teams_data_by_team,
#     delete_teams_data_by_team_competition,
#     read_teams_data,
#     read_teams_data_by_team,
#     read_teams_data_by_team_competition,
#     update_teams_data,
#     build_team_data_from_statbotics,
#     get_team_profile,
#     get_team_data
# )
# from ..models.teams_data_models import (
#     Teams_Data,
#     Teams_Data_Create,
#     Teams_Data_Update,
# )

# router = APIRouter(prefix="/data", tags=["Data"])

# sb = statbotics.Statbotics()




# @router.post("/teams_data/", response_model=Teams_Data)
# async def create_teams_data_route(team_data: Teams_Data_Create):
#     return await create_teams_data(team_data)


# @router.post(
#     "/teams_data/statbotics/competition/{competition}/team/{team_number}",
#     response_model=Teams_Data,
# )
# async def import_statbotics_team_data_route(
#     competition: str,
#     team_number: int,
# ):
#     team_profile = get_team_profile(team_number)
#     team_event_data = get_team_data(team_number, competition)
#     team_data = build_team_data_from_statbotics(
#         team_number,
#         competition,
#         team_profile,
#         team_event_data,
#     )
#     return await create_teams_data(team_data)


# @router.get("/teams_data/", response_model=list[Teams_Data])
# async def read_teams_data_route():
#     return await read_teams_data()


# @router.get("/teams_data/team/{team_number}", response_model=list[Teams_Data])
# async def read_teams_data_by_team_route(team_number: int):
#     return await read_teams_data_by_team(team_number)


# @router.get("/teams_data/statbotics/competition/{competition}/team/{team_number}")
# async def read_statbotics_team_data_route(
#     competition: str,
#     team_number: int,
# ):
#     return get_team_data(team_number, competition)


# @router.get(
#     "/teams_data/competition/{competition}/team/{team_number}",
#     response_model=list[Teams_Data],
# )
# async def read_teams_data_by_team_competition_route(
#     competition: str,
#     team_number: int,
# ):
#     return await read_teams_data_by_team_competition(competition, team_number)


# @router.patch(
#     "/teams_data/competition/{competition}/team/{team_number}",
#     response_model=Teams_Data,
# )
# async def update_teams_data_route(
#     competition: str,
#     team_number: int,
#     team_data: Teams_Data_Update,
# ):
#     return await update_teams_data(competition, team_number, team_data)


# @router.delete("/teams_data/team/{team_number}")
# async def delete_teams_data_by_team_route(team_number: int):
#     return await delete_teams_data_by_team(team_number)


# @router.delete("/teams_data/competition/{competition}/team/{team_number}")
# async def delete_teams_data_by_team_competition_route(
#     competition: str,
#     team_number: int,
# ):
#     return await delete_teams_data_by_team_competition(competition, team_number)
