from typing import List

from fastapi import APIRouter, Depends

from app.adapter import DataBaseAdapter, get_database_adapter_dep
from app.adapter.dto import (BuildingDto, GeoQueryDto, SimpleSearchQueryDto,
                             geo_query_dto, simple_search_query_dto)

building_router = APIRouter(prefix='/api/v1/building', tags=['Здания'])


@building_router.get(
    '/address',
    response_model=List[BuildingDto],
    description=
    """
        Искать здания по адресу.

        Возможно частичное совпадение.
    """
)
async def find_buildings_by_address(
        query: SimpleSearchQueryDto = Depends(simple_search_query_dto),
        adapter: DataBaseAdapter =  Depends(get_database_adapter_dep),
) -> List[BuildingDto]:
    return await adapter.find_buildings_by_address(query.name)


@building_router.get(
    '/geo',
    response_model=List[BuildingDto],
    description=
    """
        Список зданий, 
        которые находятся в заданном радиусе/прямоугольной области относительно указанной точки на карте.
    """
)
async def find_buildings_by_geo_query(
        query: GeoQueryDto = Depends(geo_query_dto),
        adapter: DataBaseAdapter =  Depends(get_database_adapter_dep),
) -> List[BuildingDto]:
    return await adapter.find_buildings_by_geo_query(query)
