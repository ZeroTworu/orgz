import asyncio
import os

import pytest
from alembic import command
from alembic.config import Config

from app.adapter import DataBaseAdapter


@pytest.fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop()

@pytest.fixture(scope='session')
def alembic_config() -> 'Config':
    return Config(os.path.join(os.path.dirname(__file__), '../alembic.ini'))

@pytest.fixture(scope='session', autouse=True)
def migrate_db(alembic_config: 'Config'):
    command.upgrade(alembic_config, 'head')

@pytest.fixture
async def db_adapter(migrate_db) -> 'DataBaseAdapter':
    adapter = DataBaseAdapter()
    await adapter.init_data()
    return adapter
