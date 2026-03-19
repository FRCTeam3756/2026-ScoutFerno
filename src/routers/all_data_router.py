from fastapi import APIRouter#, Depends
#from google.oauth2.credentials import Credentials

#from ..security.goole_auth_guard import require_auth
from ..crud.all_data_crud import read_all_data, read_all_data_by_match, read_all_data_by_team, read_all_data_by_team_match
from ..models.all_data_models import All_Data



router = APIRouter()



@router.get("/data/all_data/", response_model=list[All_Data])
async def read_all_data_route():#(creds: Credentials = Depends(require_auth)):
    return await read_all_data()


@router.get("/data/all_data/team/{team_number}", response_model=list[All_Data])
async def read_all_data_by_team_route(team_number: int):#creds: Credentials = Depends(require_auth)):
    return await read_all_data_by_team(team_number)


@router.get("/data/all_data/match/{match_number}", response_model=list[All_Data])
async def read_all_data_by_match_route(match_number: int):#creds: Credentials = Depends(require_auth)):
    return await read_all_data_by_match(match_number)

@router.get("/data/all_data/team/{team_number}/match/{match_number}", response_model=list[All_Data])
async def read_all_data_by_team_match_route(team_number: int, match_number: int):#creds: Credentials = Depends(require_auth)):
    return await read_all_data_by_team_match(team_number, match_number)

