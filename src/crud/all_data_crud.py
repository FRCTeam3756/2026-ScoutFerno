from .auto_data_crud import read_auto_data, read_auto_data_by_match, read_auto_data_by_team, read_auto_data_by_team_match
from .interview_data_crud import read_interview_data, read_interview_data_by_team
from .teleop_data_crud import read_teleop_data, read_teleop_data_by_match, read_teleop_data_by_team, read_teleop_data_by_team_match
from ..models.all_data_models import All_Data


async def read_all_data(year: int):
    interview = list(await read_interview_data(year, False))
    auto = list(await read_auto_data(year, False))
    teleop = list(await read_teleop_data(year, False))
    return All_Data(auto=auto, interview=interview, teleop=teleop)


async def read_all_data_by_match(year: int, competition: str, match_number: int):
    interview = list(await read_interview_data(year, False))
    auto = list(await read_auto_data_by_match(year, competition, match_number, False))
    teleop = list(await read_teleop_data_by_match(year, competition, match_number, False))
    return All_Data(auto=auto, interview=interview, teleop=teleop)


async def read_all_data_by_team(year: int, team_number: int):
    interview = list(await read_interview_data_by_team(year, team_number, False))
    auto = list(await read_auto_data_by_team(year, team_number, False))
    teleop = list(await read_teleop_data_by_team(year, team_number, False))

    return All_Data(auto=auto, interview=interview, teleop=teleop)


async def read_all_data_by_team_match(year: int, competition: str, team_number: int, match_number: int):
    interview = list(await read_interview_data_by_team(year, team_number, False))
    auto = list(await read_auto_data_by_team_match(year, competition, team_number, match_number, False))
    teleop = list(await read_teleop_data_by_team_match(year, competition, team_number, match_number, False))
    return All_Data(auto=auto, interview=interview, teleop=teleop)
