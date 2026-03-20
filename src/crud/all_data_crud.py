from .auto_data_crud import read_auto_data, read_auto_data_by_match, read_auto_data_by_team, read_auto_data_by_team_match
from .interview_data_crud import read_interview_match_data, read_interview_match_data_by_team
from .teleop_data_crud import read_teleop_data, read_teleop_data_by_match, read_teleop_data_by_team, read_teleop_data_by_team_match
from ..models.all_data_models import All_Data


async def read_all_data():
    interview = list(await read_interview_match_data())
    auto = list(await read_auto_data())
    teleop = list(await read_teleop_data())
    return All_Data(auto=auto, interview=interview, teleop=teleop)


async def read_all_data_by_match(match_number: int):
    interview = list(await read_interview_match_data())
    auto = list(await read_auto_data_by_match(match_number))
    teleop = list(await read_teleop_data_by_match(match_number))
    return All_Data(auto=auto, interview=interview, teleop=teleop)


async def read_all_data_by_team(team_number: int):
    interview = list(await read_interview_match_data_by_team(team_number))
    auto = list(await read_auto_data_by_team(team_number))
    teleop = list(await read_teleop_data_by_team(team_number))
    return All_Data(auto=auto, interview=interview, teleop=teleop)


async def read_all_data_by_team_match(team_number: int, match_number: int):
    interview = list(await read_interview_match_data_by_team(team_number))
    auto = list(await read_auto_data_by_team_match(team_number, match_number))
    teleop = list(await read_teleop_data_by_team_match(team_number, match_number))
    return All_Data(auto=auto, interview=interview, teleop=teleop)

#Can't be in a table=true (all of the blank_data) but, needs the ID because its the key...