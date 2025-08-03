from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.adapter import get_database_sync_adapter
from app.adapter.search import get_search_adapter
from app.http.api.activity import activity_router
from app.http.api.building import building_router
from app.http.api.infra import infra_router
from app.http.api.organization import organizations_router
from app.http.api_key import OrgzXAuth
from app.settings import (ORGZ_API_KEY_HEADER_NAME, ORGZ_FORCE_RECREATE,
                          ORGZ_USE_FAKE_DATA)


@asynccontextmanager
async def lifespan(_: 'FastAPI'):
    db_adapter = get_database_sync_adapter()
    search_adapter = get_search_adapter()

    await search_adapter.init_index()
    if ORGZ_FORCE_RECREATE and ORGZ_USE_FAKE_DATA:
        await search_adapter.clear_index()
        await db_adapter.clear_data()
    if ORGZ_USE_FAKE_DATA:
        await db_adapter.init_data()

    yield

orgz_x_auth = OrgzXAuth(name=ORGZ_API_KEY_HEADER_NAME)

app = FastAPI(title='Organizations Zero Two', lifespan=lifespan, dependencies=[Depends(orgz_x_auth)])

app.include_router(organizations_router)

app.include_router(activity_router)

app.include_router(building_router)

app.include_router(infra_router)
