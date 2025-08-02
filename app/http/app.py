from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi

from app.adapter import get_database_sync_adapter
from app.adapter.search import get_search_adapter
from app.http.api.activity import activity_router
from app.http.api.building import building_router
from app.http.api.organization import organizations_router
from app.http.api_key import verify_api_key
from app.settings import ORGZ_FORCE_RECREATE


@asynccontextmanager
async def lifespan(_: 'FastAPI'):
    db_adapter = get_database_sync_adapter()
    search_adapter = get_search_adapter()

    await search_adapter.init_index()
    if ORGZ_FORCE_RECREATE:
        await search_adapter.clear_index()
        await db_adapter.clear_data()
    await db_adapter.init_data()

    yield


app = FastAPI(title='Organizations Zero Two', lifespan=lifespan, dependencies=[Depends(verify_api_key)])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version='1.0.0',
        description='Organizations Zero Two with static API key',
        routes=app.routes,
    )
    openapi_schema['components']['securitySchemes'] = {
        'APIKeyHeader': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-ORGZ-Key',
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(organizations_router)

app.include_router(activity_router)

app.include_router(building_router)
