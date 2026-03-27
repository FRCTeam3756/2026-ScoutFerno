from fastapi import APIRouter, Depends
from google.oauth2.credentials import Credentials

from ..security.google_auth_guard import require_auth
from ..crud.interview_data_crud import create_interview_data, read_interview_data, read_interview_data_by_team, read_interview_data_by_team_competition, update_interview_data, delete_interview_data
from ..models.interview_data_models import Interview_Data, Interview_Data_Create, Interview_Data_Update


router = APIRouter(prefix="/data", tags=["Data"])


@router.post("/interview_data/", response_model=Interview_Data)
async def create_interview_data_route(interview_data: Interview_Data_Create, creds: Credentials = Depends(require_auth)):
    return await create_interview_data(interview_data)


@router.get("/interview_data/", response_model=list[Interview_Data])
async def read_interview_data_route(creds: Credentials = Depends(require_auth)):
    return await read_interview_data()


@router.get("/interview_data/team/{team_number}", response_model=list[Interview_Data])
async def read_interview_data_by_team_route(team_number: int, creds: Credentials = Depends(require_auth)):
    return await read_interview_data_by_team(team_number)


@router.get("/interview_data/competition/{competition}/team/{team_number}", response_model=list[Interview_Data])
async def read_interview_data_by_competition_team_route(competition: str, team_number: int, creds: Credentials = Depends(require_auth)):
    return await read_interview_data_by_team_competition(competition, team_number)