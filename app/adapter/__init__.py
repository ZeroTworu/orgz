from typing import TYPE_CHECKING

from app.adapter.store.sql_adapter import DataBaseAdapter

if TYPE_CHECKING:
    from typing import AsyncGenerator

_db_adapter: 'DataBaseAdapter' = DataBaseAdapter()


async def get_database_adapter() -> 'AsyncGenerator[DataBaseAdapter, None]':
    yield _db_adapter


def get_database_sync_adapter() -> 'DataBaseAdapter':
    return _db_adapter
