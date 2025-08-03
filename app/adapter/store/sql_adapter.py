from typing import TYPE_CHECKING
from urllib.parse import urlparse, urlunparse

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.adapter.store.activity import ActivityAdapter
from app.adapter.store.building import BuildingAdapter
from app.adapter.store.db_init import InitDataBaseAdapter
from app.adapter.store.organization import OrganizationAdapter
from app.settings import ORGZ_DATA_BASE_DSN, ORGZ_DATA_BASE_ECHO

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine
    from app.adapter.store.elastic import ElasticSearchAdapter

from app.logger import get_logger


class DataBaseAdapter(  # noqa:  WPS215
    ActivityAdapter,
    BuildingAdapter,
    InitDataBaseAdapter,
    OrganizationAdapter,
):
    _logger = get_logger('DataBaseAdapter')

    def __init__(self, search_adapter: 'ElasticSearchAdapter'):
        super().__init__()
        self._search_adapter = search_adapter
        self._engine: 'AsyncEngine' = create_async_engine(ORGZ_DATA_BASE_DSN, echo=ORGZ_DATA_BASE_ECHO, future=True)
        self._async_session_maker: 'async_sessionmaker[AsyncSession]' = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
        )
        self._logger.info(f'Initializing DatabaseAdapter on {self._censor_password(ORGZ_DATA_BASE_DSN)}')

    def get_session(self) -> 'AsyncSession':
        return self._async_session_maker()

    async def close(self):
        self._logger.info('Closing DatabaseAdapter...')
        await self._engine.dispose()

    def _censor_password(self, dsn: 'str') -> 'str':
        parsed = urlparse(dsn)
        if parsed.password:
            netloc = f'{parsed.username}:****@{parsed.hostname}'
            if parsed.port:
                netloc = f'{netloc}:{parsed.port}'
            parsed = parsed._replace(netloc=netloc)
        return str(urlunparse(parsed))
