from typing import List

from fastapi import APIRouter, Depends

from app.adapter import DataBaseAdapter, get_database_adapter
from app.adapter.dto import ActivityTreeDto, NameQueryDto, name_query_dto

activity_router = APIRouter(prefix='/api/v1/act', tags=['activity'])


@activity_router.get('/all/', response_model=List[ActivityTreeDto])
async def get_all_activity_trees(
        adapter: DataBaseAdapter =  Depends(get_database_adapter),
) -> List[ActivityTreeDto]:
    return await adapter.get_all_activities_trees()


@activity_router.get('/name', response_model=List[ActivityTreeDto])
async def find_activities_by_name(
        query: NameQueryDto = Depends(name_query_dto),
        adapter: DataBaseAdapter =  Depends(get_database_adapter),
) -> List[ActivityTreeDto]:
    return await adapter.get_activity_tree_by_name(query.name)
