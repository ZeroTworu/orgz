from typing import List

from fastapi import APIRouter, Depends

from app.adapter import DataBaseAdapter, get_database_adapter
from app.adapter.dto import (ActivityTreeDto, SimpleSearchQueryDto,
                             simple_search_query_dto)

activity_router = APIRouter(prefix='/api/v1/activity', tags=['Виды Деятельности'])


@activity_router.get(
    '/all/',
    response_model=List[ActivityTreeDto],
    description=
    """
        Получения дерева всех видов деятельности.
    """
)
async def get_all_activity_trees(
        adapter: DataBaseAdapter =  Depends(get_database_adapter),
) -> List[ActivityTreeDto]:
    return await adapter.get_all_activities_trees()


@activity_router.get(
    '/name',
    response_model=List[ActivityTreeDto],
    description=
    """
        Искать вид деятельности по названию.
    
        Возможно частичное совпадение.
    """
)
async def find_activities_by_name(
        query: SimpleSearchQueryDto = Depends(simple_search_query_dto),
        adapter: DataBaseAdapter =  Depends(get_database_adapter),
) -> List[ActivityTreeDto]:
    return await adapter.find_activity_tree_by_name(query.name)
