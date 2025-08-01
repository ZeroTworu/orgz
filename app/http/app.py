from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.adapter import get_database_sync_adapter


@asynccontextmanager
async def lifespan(_: 'FastAPI'):
    adapter = get_database_sync_adapter()
    await adapter.init_data()
    yield


app = FastAPI(title='Organizations Zero Two', lifespan=lifespan)

