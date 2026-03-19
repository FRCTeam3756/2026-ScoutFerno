from fastapi import APIRouter#, Depends
#from google.oauth2.credentials import Credentials

#from ..security.goole_auth_guard import require_auth
from ..models.auto_data_models import Auto_Data, Auto_Data_Create, Auto_Data_Update
from ..crud.all_data_crud import read_all_data
from ..models.interview_data_models import Interview_Match_Data, Interview_Match_Data_Create, Interview_Match_Data_Update


router = APIRouter()



@router.get("/data/all_data/", response_model=list[Auto_Data])
def read_all_data_route():#(creds: Credentials = Depends(require_auth)):
    return read_all_data


@router.get("/data/all_data/team/{team_number}", response_model=list[Auto_Data])
def read_auto_data_by_team_route(team_number: int, ):#creds: Credentials = Depends(require_auth)):
    return read_auto_data_by_team(team_number)


@router.get("/data/all_data/match/{match_number}", response_model=list[Auto_Data])
def read_auto_data_by_match_route(match_number: int, ):#creds: Credentials = Depends(require_auth)):
    return read_auto_data_by_match(match_number)


@router.get("/data/all_data/team/{team_number}/match/{match_number}", response_model=list[Auto_Data])
def read_auto_data_by_team_match_route(team_number: int, match_number: int, ):#creds: Credentials = Depends(require_auth)):
    return read_auto_data_by_team_match(team_number, match_number)

