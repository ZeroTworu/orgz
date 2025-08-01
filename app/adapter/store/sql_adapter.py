from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.adapter.store.activity import ActivityAdapter
from app.adapter.store.building import BuildingAdapter
from app.adapter.store.db_init import InitDataBaseAdapter
from app.adapter.store.organization import OrganizationAdapter
from app.settings import ORGZ_DATA_BASE_DSN, ORGZ_DATA_BASE_ECHO

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine

from app.logger import get_logger


class DataBaseAdapter(  # noqa:  WPS215
    ActivityAdapter,
    BuildingAdapter,
    InitDataBaseAdapter,
    OrganizationAdapter,
):
    _logger = get_logger('DataBaseAdapter')

    def __init__(self):
        super().__init__()
        self._engine: 'AsyncEngine' = create_async_engine(ORGZ_DATA_BASE_DSN, echo=ORGZ_DATA_BASE_ECHO, future=True)
        self._sc: 'async_sessionmaker[AsyncSession]' = async_sessionmaker(self._engine, expire_on_commit=False)

    def get_session(self) -> 'async_sessionmaker[AsyncSession]':
        return self._sc
