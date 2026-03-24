from .prematch_data_crud import read_prematch_data, read_prematch_data_by_match, read_prematch_data_by_team, read_prematch_data_by_team_match
from .autonomous_data_crud import read_auto_data, read_auto_data_by_match, read_auto_data_by_team, read_auto_data_by_team_match
from .teleop_data_crud import read_teleop_data, read_teleop_data_by_match, read_teleop_data_by_team, read_teleop_data_by_team_match
from .endgame_data_crud import read_endgame_data, read_endgame_data_by_match, read_endgame_data_by_team, read_endgame_data_by_team_match
from .postmatch_data_crud import read_postmatch_data, read_postmatch_data_by_match, read_postmatch_data_by_team, read_postmatch_data_by_team_match
from ..models.all_data_models import All_Data


async def read_all_data():
    prematch = list(await read_prematch_data(False))
    auto = list(await read_auto_data(False))
    teleop = list(await read_teleop_data(False))
    endgame = list(await read_endgame_data(False))
    postmatch = list(await read_postmatch_data(False))
    return All_Data(prematch=prematch, auto=auto, teleop=teleop, endgame=endgame, postmatch=postmatch)


async def read_all_data_by_match(competition: str, match_number: int):
    prematch = list(await read_prematch_data_by_match(competition, match_number, False))
    auto = list(await read_auto_data_by_match(competition, match_number, False))
    teleop = list(await read_teleop_data_by_match(competition, match_number, False))
    endgame = list(await read_endgame_data_by_match(competition, match_number, False))
    postmatch = list(await read_postmatch_data_by_match(competition, match_number, False))
    return All_Data(prematch=prematch, auto=auto, teleop=teleop, endgame=endgame, postmatch=postmatch)


async def read_all_data_by_team(team_number: int):
    prematch = list(await read_prematch_data_by_team(team_number, False))
    auto = list(await read_auto_data_by_team(team_number, False))
    teleop = list(await read_teleop_data_by_team(team_number, False))
    endgame = list(await read_endgame_data_by_team(team_number, False))
    postmatch = list(await read_postmatch_data_by_team(team_number, False))
    return All_Data(prematch=prematch, auto=auto, teleop=teleop, endgame=endgame, postmatch=postmatch)


async def read_all_data_by_team_match(competition: str, team_number: int, match_number: int):
    prematch = list(await read_prematch_data_by_team_match(competition, team_number, match_number, False))
    auto = list(await read_auto_data_by_team_match(competition, team_number, match_number, False))
    teleop = list(await read_teleop_data_by_team_match(competition, team_number, match_number, False))
    endgame = list(await read_endgame_data_by_team_match(competition, team_number, match_number, False))
    postmatch = list(await read_postmatch_data_by_team_match(competition, team_number, match_number, False))
    return All_Data(prematch=prematch, auto=auto, teleop=teleop, endgame=endgame, postmatch=postmatch)
