from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.adapter.store.activity import ActivityAdapter
from app.adapter.store.models import Activity
from app.settings import ORGZ_DATA_BASE_DSN, ORGZ_DATA_BASE_ECHO

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine

from app.logger import get_logger


class DataBaseAdapter(ActivityAdapter):
    _logger = get_logger('DataBaseAdapter')

    def __init__(self):
        self._engine: 'AsyncEngine' = create_async_engine(ORGZ_DATA_BASE_DSN, echo=ORGZ_DATA_BASE_ECHO, future=True)
        self._sc: 'async_sessionmaker[AsyncSession]' = async_sessionmaker(self._engine, expire_on_commit=False)

    def get_session(self) -> 'async_sessionmaker[AsyncSession]':
        return self._sc

    async def init_data(self):  # noqa: WPS210, WPS213, WPS217
        async with self._sc() as session:
            result = await session.execute(select(Activity))
            if result.scalars().first() is not None:
                self._logger.info('Activity already initialized')
                return

            self._logger.warning('Init Activity...')

            eat = await self.add_activity('Еда')
            cars = await self.add_activity('Автомобили')
            entertainment = await self.add_activity('Развлечения')

            await self.add_activity('Мясная продукция', eat.id)
            await self.add_activity('Молочная продукция', eat.id)
            await self.add_activity('Грузовые', cars.id)

            passenger_cars = await self.add_activity('Легковые', cars.id)
            cartoon = await self.add_activity('Мультфильмы', entertainment.id)
            games = await self.add_activity('Настольные игры', entertainment.id)

            await self.add_activity('Запчасти', passenger_cars.id)
            await self.add_activity('Аксессуары', passenger_cars.id)

            await self.add_activity('Аниме', cartoon.id)
            await self.add_activity('Warhammer 40000', games.id)

            self._logger.warning('Init Activity done.')
