from typing import TYPE_CHECKING

from app.adapter.store.sql_adapter import DataBaseAdapter
from app.settings import ORGZ_PYTEST_ON

if TYPE_CHECKING:
    from typing import AsyncGenerator

_db_adapter: 'DataBaseAdapter' = DataBaseAdapter()


async def get_database_adapter() -> 'AsyncGenerator[DataBaseAdapter, None]':
    if ORGZ_PYTEST_ON:
        yield DataBaseAdapter()
    else:
        yield _db_adapter


def get_database_sync_adapter() -> 'DataBaseAdapter':
    if ORGZ_PYTEST_ON:
        return DataBaseAdapter()
    else:
        return _db_adapter
