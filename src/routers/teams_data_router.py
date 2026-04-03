import statbotics
# from fastapi import APIRouter, Depends
# from google.oauth2.credentials import Credentials

# from ..security.google_auth_guard import require_auth
from ..models.teams_data_models import Teams_Data, Teams_Data_Create, Teams_Data_Update
from ..crud.teams_data_crud import create_teams_data, delete_teams_data_by_team, delete_teams_data_by_team_competition, update_teams_data, read_teams_data, read_teams_data_by_team, read_teams_data_by_team_competition

sb = statbotics.Statbotics()

def get_team_data(team_number: int, competition: str):
    team_data = sb.get_team(team_number, competition)
    if team_data is None:
        raise HTTPException(status_code=404, detail="Team data not found")
    return team_data


