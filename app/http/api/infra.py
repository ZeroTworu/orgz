from asyncio import gather

from fastapi import APIRouter, Depends

from app.adapter import DataBaseAdapter, get_database_adapter
from app.adapter.search import ElasticSearchAdapter, get_search_adapter

infra_router = APIRouter(prefix='/api/v1/infra', tags=['Инфраструктурные задачи'])


@infra_router.post(
    '/reindex/',
    description=
    """
        Перестройка Elastic Search Index.
    """
)
async def get_all_activity_trees(
        search_adapter: ElasticSearchAdapter =  Depends(get_search_adapter),
        database_adapter: DataBaseAdapter =  Depends(get_database_adapter),
) -> dict[str,str]:
    await search_adapter.clear_index()
    await database_adapter.reindex_buildings(search_adapter=search_adapter)
    # await database_adapter.reindex_activities(search_adapter=search_adapter)
    # await database_adapter.reindex_organizations(search_adapter=search_adapter)
    return {'status': 'ok'}


@infra_router.post(
    '/reinit/',
    description=
    """
        Очистка БД и Elastic Search Index с последующей заливкой тестовых данных.
    """
)
async def get_all_activity_trees(
        search_adapter: ElasticSearchAdapter =  Depends(get_search_adapter),
        database_adapter: DataBaseAdapter =  Depends(get_database_adapter),
) -> dict[str,str]:
    await search_adapter.clear_index()
    await database_adapter.clear_data()
    await database_adapter.init_data()
    return {'status': 'ok'}
