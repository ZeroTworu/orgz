import asyncio
import os

import pytest
from alembic import command
from alembic.config import Config

from app.adapter import DataBaseAdapter
from app.adapter.search import ElasticSearchAdapter
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

@pytest.fixture
async def db_adapter(migrate_db) -> 'AsyncGenerator[DataBaseAdapter]':
    adapter = ElasticSearchAdapter()
    await adapter.init_index()
    adapter = DataBaseAdapter()
    await adapter.init_data()
    yield adapter


@pytest.fixture
async def client() -> 'AsyncGenerator[AsyncClient]':
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        yield client
