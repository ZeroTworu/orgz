import asyncio
import os

import pytest
from alembic import command
from alembic.config import Config

from app.adapter import DataBaseAdapter
from app.adapter import ElasticSearchAdapter
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator

from app.http.app import app

@pytest.fixture(autouse=True)
def migrate_db():
    alembic_config = Config(os.path.join(os.path.dirname(__file__), '../alembic.ini'))
    command.upgrade(alembic_config, 'head')

@pytest.fixture(autouse=True)
async def search_adapter():
    adapter = ElasticSearchAdapter()
    await adapter.init_index()
    yield adapter

@pytest.fixture
async def db_adapter(migrate_db, search_adapter) -> 'AsyncGenerator[DataBaseAdapter]':
    adapter = DataBaseAdapter(search_adapter=search_adapter)
    await adapter.init_data()
    yield adapter


@pytest.fixture
async def client(db_adapter) -> 'AsyncGenerator[AsyncClient]':
    app.state.database_adapter = db_adapter
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        yield client
