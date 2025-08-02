from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.adapter import get_database_sync_adapter
from app.adapter.search import get_search_adapter
from app.http.api.activity import activity_router
from app.http.api.organization import organizations_router
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


app = FastAPI(title='Organizations Zero Two', lifespan=lifespan)

app.include_router(organizations_router)

app.include_router(activity_router)
