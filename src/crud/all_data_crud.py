from .prematch_data_crud import read_prematch_data, read_prematch_data_by_match, read_prematch_data_by_team, read_prematch_data_by_team_match, create_prematch_data, delete_prematch_data_by_match, delete_prematch_data_by_team, delete_prematch_data_by_team_match, update_prematch_data
from .autonomous_data_crud import read_autonomous_data, read_autonomous_data_by_match, read_autonomous_data_by_team, read_autonomous_data_by_team_match, create_autonomous_data, delete_autonomous_data_by_match, delete_autonomous_data_by_team, delete_autonomous_data_by_team_match, update_autonomous_data
from .teleop_data_crud import read_teleop_data, read_teleop_data_by_match, read_teleop_data_by_team, read_teleop_data_by_team_match, create_teleop_data, delete_teleop_data_by_match, delete_teleop_data_by_team, delete_teleop_data_by_team_match, update_teleop_data
from .endgame_data_crud import read_endgame_data, read_endgame_data_by_match, read_endgame_data_by_team, read_endgame_data_by_team_match, create_endgame_data, delete_endgame_data_by_match, delete_endgame_data_by_team, delete_endgame_data_by_team_match, update_endgame_data
from .postmatch_data_crud import read_postmatch_data, read_postmatch_data_by_match, read_postmatch_data_by_team, read_postmatch_data_by_team_match, create_postmatch_data, delete_postmatch_data_by_match, delete_postmatch_data_by_team, delete_postmatch_data_by_team_match, update_postmatch_data
from .interview_data_crud import read_interview_data, read_interview_data_by_team, delete_interview_data, delete_interview_data_by_team
from ..models.all_data_models import All_Data, All_Data_Create, All_Data_Delete, All_Data_Update, All_Data_Interview, All_Data_Interview_Delete

async def create_all_data(match_data: All_Data_Create):
    prematch = await create_prematch_data(match_data.prematch)
    autonomous = await create_autonomous_data(match_data.autonomous)
    teleop = await create_teleop_data(match_data.teleop)
    endgame = await create_endgame_data(match_data.endgame)
    postmatch = await create_postmatch_data(match_data.postmatch)
    return All_Data(prematch=[prematch], autonomous=[autonomous], teleop=[teleop], endgame=[endgame], postmatch=[postmatch])


async def read_all_data():
    prematch = list(await read_prematch_data(False))
    autonomous = list(await read_autonomous_data(False))
    teleop = list(await read_teleop_data(False))
    endgame = list(await read_endgame_data(False))
    postmatch = list(await read_postmatch_data(False))
    interview = list(await read_interview_data(False))
    return All_Data_Interview(prematch=prematch, autonomous=autonomous, teleop=teleop, endgame=endgame, postmatch=postmatch, interview=interview)


async def read_all_data_by_match(competition: str, match_number: int):
    prematch = list(await read_prematch_data_by_match(competition, match_number, False))
    autonomous = list(await read_autonomous_data_by_match(competition, match_number, False))
    teleop = list(await read_teleop_data_by_match(competition, match_number, False))
    endgame = list(await read_endgame_data_by_match(competition, match_number, False))
    postmatch = list(await read_postmatch_data_by_match(competition, match_number, False))
    return All_Data(prematch=prematch, autonomous=autonomous, teleop=teleop, endgame=endgame, postmatch=postmatch)


async def read_all_data_by_team(team_number: int):
    prematch = list(await read_prematch_data_by_team(team_number, False))
    autonomous = list(await read_autonomous_data_by_team(team_number, False))
    teleop = list(await read_teleop_data_by_team(team_number, False))
    endgame = list(await read_endgame_data_by_team(team_number, False))
    postmatch = list(await read_postmatch_data_by_team(team_number, False))
    interview = list(await read_interview_data_by_team(team_number, False))
    return All_Data_Interview(prematch=prematch, autonomous=autonomous, teleop=teleop, endgame=endgame, postmatch=postmatch, interview=interview)


async def read_all_data_by_team_match(competition: str, team_number: int, match_number: int):
    prematch = list(await read_prematch_data_by_team_match(competition, team_number, match_number, False))
    autonomous = list(await read_autonomous_data_by_team_match(competition, team_number, match_number, False))
    teleop = list(await read_teleop_data_by_team_match(competition, team_number, match_number, False))
    endgame = list(await read_endgame_data_by_team_match(competition, team_number, match_number, False))
    postmatch = list(await read_postmatch_data_by_team_match(competition, team_number, match_number, False))
    interview = list(await read_interview_data_by_team(competition, team_number, False))
    return All_Data_Interview(prematch=prematch, autonomous=autonomous, teleop=teleop, endgame=endgame, postmatch=postmatch, interview=interview)

async def update_all_data(competition: str, team_number: int, match_number: int, match_data:All_Data_Update):
    prematch = await update_prematch_data(competition, team_number, match_number, match_data.prematch)
    autonomous = await update_autonomous_data(competition, team_number, match_number, match_data.autonomous)
    teleop = await update_teleop_data(competition, team_number, match_number, match_data.teleop)
    endgame = await update_endgame_data(competition, team_number, match_number, match_data.endgame)
    postmatch = await update_postmatch_data(competition, team_number, match_number, match_data.postmatch)
    return All_Data(prematch=[prematch], autonomous=[autonomous], teleop=[teleop], endgame=[endgame], postmatch=[postmatch])

async def delete_all_data_by_match(competition: str, match_number: int):
    prematch = list(await delete_prematch_data_by_match(competition, match_number, False))
    autonomous = list(await delete_autonomous_data_by_match(competition, match_number, False))
    teleop = list(await delete_teleop_data_by_match(competition, match_number, False))
    endgame = list(await delete_endgame_data_by_match(competition, match_number, False))
    postmatch = list(await delete_postmatch_data_by_match(competition, match_number, False))
    return All_Data_Delete(prematch=prematch, autonomous=autonomous, teleop=teleop, endgame=endgame, postmatch=postmatch)

async def delete_all_data_by_team(team_number: int):
    prematch = list(await delete_prematch_data_by_team(team_number, False))
    autonomous = list(await delete_autonomous_data_by_team(team_number, False))
    teleop = list(await delete_teleop_data_by_team(team_number, False))
    endgame = list(await delete_endgame_data_by_team(team_number, False))
    postmatch = list(await delete_postmatch_data_by_team(team_number, False))
    interview = list(await delete_interview_data_by_team(team_number, False))
    return All_Data_Interview_Delete(prematch=prematch, autonomous=autonomous, teleop=teleop, endgame=endgame, postmatch=postmatch, interview=interview)

async def delete_all_data_by_team_match(competition: str, team_number: int, match_number: int):
    prematch = list(await delete_prematch_data_by_team_match(competition, match_number, team_number, False))
    autonomous = list(await delete_autonomous_data_by_team_match(competition, match_number, team_number, False))
    teleop = list(await delete_teleop_data_by_team_match(competition, match_number, team_number, False))
    endgame = list(await delete_endgame_data_by_team_match(competition, match_number, team_number, False))
    postmatch = list(await delete_postmatch_data_by_team_match(competition, match_number, team_number, False))
    interview = list(await delete_interview_data_by_team(competition, team_number, False))
    return All_Data_Interview_Delete(prematch=prematch, autonomous=autonomous, teleop=teleop, endgame=endgame, postmatch=postmatch, interview=interview)

