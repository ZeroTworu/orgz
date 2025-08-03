from asyncio import gather
from typing import TYPE_CHECKING

from sqlalchemy import func, select

from app.adapter.dto import (BuildingDto, ElasticQueryDto, EsSearchType,
                             GeoQueryDto)
from app.adapter.store.models import Building

if TYPE_CHECKING:
    from typing import List

    from app.adapter.store.sql_adapter import DataBaseAdapter


class BuildingAdapter:
    srid = 4326

    async def add_building(
            self: 'DataBaseAdapter|BuildingAdapter',
            adress: 'str',
            longitude: 'float',
            latitude: 'float',
    ) -> 'BuildingDto':
        async with self._async_session_maker() as session:
            point = func.ST_SetSRID(func.ST_Point(longitude, latitude), self.srid)

            building = Building(
                adress=adress,
                cords=point,
            )

            session.add(building)

            await session.commit()
            await session.flush()
            dto = BuildingDto(
                adress=adress,
                cords=point,
                id=building.id,
            )

            await self._search_adapter.index_building(dto)
            return dto

    async def find_buildings_by_address(
            self: 'DataBaseAdapter|BuildingAdapter',
            address: 'str',
    ) -> 'List[BuildingDto]':
        async with self._async_session_maker() as session:
            uids = await self._search_adapter.search(ElasticQueryDto(name=address, type=EsSearchType.BUILDING))
            async with self._async_session_maker() as session:
                result = await session.execute(
                    select(Building).where(Building.id.in_(uids))
                )
                return [
                    BuildingDto(id=building.id, cords=building.cords, adress=building.adress)
                    for building in result.scalars().all()
                ]

    async def find_buildings_by_geo_query(
            self: 'DataBaseAdapter',
            query: 'GeoQueryDto'
    ) -> 'List[BuildingDto]':
        async with self._async_session_maker() as session:
            result = await session.execute(
                select(Building)
                .where(query.condition)
                .distinct()
            )

            return [
                BuildingDto(id=building.id, cords=building.cords, adress=building.adress)
                for building in result.scalars().all()
            ]

    async def reindex_buildings(self: 'DataBaseAdapter'):
        async with self._async_session_maker() as session:
            buildings = [
                BuildingDto.model_validate(building)
                for building in (await session.execute(select(Building))).scalars().all()
            ]

            await gather(
                *map(
                    self._search_adapter.index_building,
                    buildings,
                )
            )
