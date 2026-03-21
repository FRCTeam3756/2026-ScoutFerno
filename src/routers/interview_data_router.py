from fastapi import APIRouter
# from fastapi import APIRouter, Depends
# from google.oauth2.credentials import Credentials

# from ..security.google_auth_guard import require_auth
from ..crud.interview_data_crud import create_interview_data, read_interview_data, update_interview_data, delete_interview_data, read_interview_data_by_team
from ..models.interview_data_models import Interview_Data, Interview_Data_Create, Interview_Data_Update


router = APIRouter(prefix="/data", tags=["Data"])


@router.post("/interview_data/", response_model=Interview_Data)
# async def create_interview_data_route(interview_data: Interview_Data_Create, creds: Credentials = Depends(require_auth)):
async def create_interview_data_route(interview_data: Interview_Data_Create):
    return await create_interview_data(interview_data)


@router.get("/interview_data/year/{year}", response_model=list[Interview_Data])
# async def read_interview_data_route(creds: Credentials = Depends(require_auth)):
async def read_interview_data_route(year: int):
    return await read_interview_data(year)


@router.get("/interview_data/year/{year}/team/{team_number}", response_model=list[Interview_Data])
# async def read_interview_data_by_team_route(team_number: int, creds: Credentials = Depends(require_auth)):
async def read_interview_data_by_team_route(year: int, team_number: int):
    return await read_interview_data_by_team(year, team_number)


@router.patch("/interview_data/year/{year}/team/{team_number}", response_model=Interview_Data)
# async def update_interview_data_route(team_number: int, interview_data: Interview_Data_Update, creds: Credentials = Depends(require_auth)):
async def update_interview_data_route(year: int, team_number: int, interview_data: Interview_Data_Update):
    return await update_interview_data(year, team_number, interview_data)


@router.delete("/interview_data/year/{year}/team/{team_number}")
# async def delete_interview_data_route(team_number: int, creds: Credentials = Depends(require_auth)):
async def delete_interview_data_route(year: int, team_number: int):
    return await delete_interview_data(year, team_number)