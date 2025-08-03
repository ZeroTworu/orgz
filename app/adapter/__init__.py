from fastapi import Request

from app.adapter.store.elastic import ElasticSearchAdapter
from app.adapter.store.sql_adapter import DataBaseAdapter


async def get_database_adapter_dep(request: Request) -> DataBaseAdapter:
    return request.app.state.database_adapter


async def get_search_adapter_dep(request: Request) -> ElasticSearchAdapter:
    return request.app.state.search_adapter
