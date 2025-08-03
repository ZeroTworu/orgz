from asyncio import gather

from fastapi import APIRouter, Depends

from app.adapter import (DataBaseAdapter, ElasticSearchAdapter,
                         get_database_adapter_dep, get_search_adapter_dep)

infra_router = APIRouter(prefix='/api/v1/infra', tags=['Инфраструктурные задачи'])


@infra_router.post(
    '/reindex/',
    description=
    """
        Перестройка Elastic Search Index.
    """
)
async def get_all_activity_trees(
        search_adapter: ElasticSearchAdapter =  Depends(get_search_adapter_dep),
        database_adapter: DataBaseAdapter =  Depends(get_database_adapter_dep),
) -> dict[str,str]:
    await search_adapter.clear_index()
    await database_adapter.reindex_buildings()
    await database_adapter.reindex_activities()
    await database_adapter.reindex_organizations()
    return {'status': 'ok'}


@infra_router.post(
    '/reinit/',
    description=
    """
        Очистка БД и Elastic Search Index с последующей заливкой тестовых данных.
    """
)
async def get_all_activity_trees(
        search_adapter: ElasticSearchAdapter =  Depends(get_search_adapter_dep),
        database_adapter: DataBaseAdapter =  Depends(get_database_adapter_dep),
) -> dict[str,str]:
    await search_adapter.clear_index()
    await database_adapter.clear_data()
    await database_adapter.init_data()
    return {'status': 'ok'}
