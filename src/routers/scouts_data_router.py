from fastapi import APIRouter

from ..crud.scouts_data_crud import (
    create_scout_data,
    delete_scout_data,
    delete_scout_data_by_individual,
    read_scout_data,
    read_scout_data_by_individual,
    update_scout_data,
    update_scout_data_by_individual,
)
from ..models.scouts_data_models import Scout_Data, Scout_Data_Create, Scout_Data_Update

router = APIRouter(prefix="/data", tags=["Data"])


@router.post("/scout_data/", response_model=Scout_Data)
async def create_scout_data_route(scout_data: Scout_Data_Create):
    return await create_scout_data(scout_data)


@router.get("/scout_data/", response_model=list[Scout_Data])
async def read_scout_data_route():
    return await read_scout_data()


@router.get("/scout_data/{scout_id}", response_model=Scout_Data)
async def read_scout_data_by_individual_route(scout_id: int):
    return await read_scout_data_by_individual(scout_id)


@router.patch("/scout_data/scout/{scout_name}", response_model=Scout_Data)
async def update_scout_data_route(scout_name: str, scout_data: Scout_Data_Update):
    return await update_scout_data(scout_name, scout_data)


@router.patch("/scout_data/{scout_id}", response_model=Scout_Data)
async def update_scout_data_by_individual_route(scout_id: int, scout_data: Scout_Data_Update):
    return await update_scout_data_by_individual(scout_id, scout_data)


@router.delete("/scout_data/scout/{scout_name}")
async def delete_scout_data_route(scout_name: str):
    return await delete_scout_data(scout_name)


@router.delete("/scout_data/{scout_id}")
async def delete_scout_data_by_individual_route(scout_id: int):
    return await delete_scout_data_by_individual(scout_id)
