from typing import TYPE_CHECKING

from sqlalchemy import func

from app.adapter.dto import BuildingDto
from app.adapter.store.models import Building

if TYPE_CHECKING:
    from app.adapter.store.sql_adapter import DataBaseAdapter


class BuildingAdapter:

    srid = 4326

    async def add_building(
        self: 'DataBaseAdapter|BuildingAdapter',
        adress: 'str',
        longitude: 'float',
        latitude: 'float',
    ) -> 'BuildingDto':
        async with self._sc() as session:
            point = func.ST_SetSRID(func.ST_Point(longitude, latitude), self.srid)

            building = Building(
                adress=adress,
                cords=point,
            )

            session.add(building)

            await session.commit()
            await session.flush()
            return BuildingDto(
                adress=adress,
                cords=point,
                id=building.id,
            )
