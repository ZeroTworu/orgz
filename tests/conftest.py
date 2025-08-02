import asyncio
import os

import pytest
from alembic import command
from alembic.config import Config

from app.adapter import DataBaseAdapter
from app.adapter.search import ElasticSearchAdapter
from httpx import AsyncClient, ASGITransport


from app.http.app import app


@pytest.fixture
def event_loop():
    return asyncio.get_event_loop()

@pytest.fixture
def alembic_config() -> 'Config':
    return Config(os.path.join(os.path.dirname(__file__), '../alembic.ini'))

@pytest.fixture(autouse=True)
def migrate_db(alembic_config: 'Config'):
    command.upgrade(alembic_config, 'head')

@pytest.fixture
async def db_adapter(migrate_db) -> 'DataBaseAdapter':
    adapter = DataBaseAdapter()
    await adapter.init_data()
    return adapter


@pytest.fixture
async def search_adapter() -> 'ElasticSearchAdapter':
    adapter = ElasticSearchAdapter()
    await adapter.init_index()
    return adapter

@pytest.fixture
async def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        return client
