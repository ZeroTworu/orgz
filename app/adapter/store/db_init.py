from typing import TYPE_CHECKING

from sqlalchemy import select

from app.adapter.store.models import Activity, Building, Organization

if TYPE_CHECKING:
    from app.adapter.store.sql_adapter import DataBaseAdapter


class InitDataBaseAdapter:

    def __init__(self):
        self._anime = None
        self._eat = None
        self._passenger_cars = None

        self._office1 = None
        self._office2 = None
        self._office3 = None

    async def init_data(self: 'DataBaseAdapter'):
        # Деятельность#
        await self._init_activity()
        # Здания
        await self._init_building()
        # Организации
        await self._init_organization()

    async def _init_activity(self: 'DataBaseAdapter'):  # noqa: WPS210, WPS213, WPS217

        async with self._sc() as session:
            result = await session.execute(select(Activity))
            if result.scalars().first() is None:
                self._logger.warning('Init Activity...')

                self._eat = await self.add_activity('Еда')
                cars = await self.add_activity('Автомобили')
                entertainment = await self.add_activity('Развлечения')

                await self.add_activity('Мясная продукция', self._eat.activity_id)
                await self.add_activity('Молочная продукция', self._eat.activity_id)
                await self.add_activity('Грузовые', cars.activity_id)

                self._passenger_cars = await self.add_activity('Легковые', cars.activity_id)
                cartoon = await self.add_activity('Мультфильмы', entertainment.activity_id)
                games = await self.add_activity('Настольные игры', entertainment.activity_id)

                await self.add_activity('Запчасти', self._passenger_cars.activity_id)
                await self.add_activity('Аксессуары', self._passenger_cars.activity_id)

                self._anime = await self.add_activity('Аниме', cartoon.activity_id)
                await self.add_activity('Warhammer 40000', games.activity_id)

                self._logger.warning('Init Activity done.')

    async def _init_building(self: 'DataBaseAdapter'):  # noqa: WPS210, WPS213, WPS217
        async with self._sc() as session:
            result = await session.execute(select(Building))
            if result.scalars().first() is None:
                self._logger.warning('Init Building...')

                self._office1 = await self.add_building(
                    'Москва, ул. Пушкина, д. 4б офис 1.',
                    46.5454,
                    46.3232,
                )
                self._office2 = await self.add_building(
                    'Москва, ул. Пушкина, д. 4б офис 2.',
                    46.5454,
                    46.3232,
                )

                self._office3 = await self.add_building(
                    'Москва, ул. Пушкина, д. 5б офис 1.',
                    45.5454,
                    45.3232,
                )

            self._logger.warning('Init Building done.')

    async def _init_organization(self: 'DataBaseAdapter'):  # noqa: WPS210, WPS213, WPS217
        async with self._sc() as session:
            result = await session.execute(select(Organization))
            if result.scalars().first() is None:
                self._logger.warning('Init Organization...')

                await self.add_organization('ООО "Рога и Копыта"', self._eat, self._office1)
                await self.add_organization('ИП Рогов Василий"', self._passenger_cars, self._office2)
                await self.add_organization('Studio Deen', self._anime, self._office3)

            self._logger.warning('Init Organization done.')
