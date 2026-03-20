from fastapi import APIRouter, Depends
from google.oauth2.credentials import Credentials

from ..security.goole_auth_guard import require_auth
from ..crud.interview_data_crud import create_interview_match_data, read_interview_match_data, update_interview_match_data, delete_interview_match_data, read_interview_match_data_by_team
from ..models.interview_data_models import Interview_Match_Data, Interview_Match_Data_Create, Interview_Match_Data_Update


router = APIRouter(prefix="/data", tags=["Data"])


@router.post("/interview_match_data/", response_model=Interview_Match_Data)
async def create_interview_match_data_route(interview_match_data: Interview_Match_Data_Create, creds: Credentials = Depends(require_auth)):
    return await create_interview_match_data(interview_match_data)


@router.get("/interview_match_data/", response_model=list[Interview_Match_Data])
async def read_interview_match_data_route(creds: Credentials = Depends(require_auth)):
    return await read_interview_match_data()


@router.get("/interview_match_data/team/{team_number}", response_model=list[Interview_Match_Data])
async def read_interview_match_data_by_team_route(team_number: int, creds: Credentials = Depends(require_auth)):
    return await read_interview_match_data_by_team(team_number)


@router.patch("/interview_match_data/team/{team_number}", response_model=Interview_Match_Data)
async def update_interview_match_data_route(team_number: int, interview_match_data: Interview_Match_Data_Update, creds: Credentials = Depends(require_auth)):
    return await update_interview_match_data(team_number, interview_match_data)


@router.delete("/interview_match_data/team/{team_number}")
async def delete_interview_match_data_route(team_number: int, creds: Credentials = Depends(require_auth)):
    return await delete_interview_match_data(team_number)