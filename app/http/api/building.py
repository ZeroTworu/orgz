from typing import List

from fastapi import APIRouter, Depends

from app.adapter import DataBaseAdapter, get_database_adapter
from app.adapter.dto import (BuildingDto, GeoQueryDto, NameQueryDto,
                             geo_query_dto, name_query_dto)

building_router = APIRouter(prefix='/api/v1/building', tags=['Здания'])


@building_router.get('/address', response_model=List[BuildingDto])
async def find_buildings_by_address(
        query: NameQueryDto = Depends(name_query_dto),
        adapter: DataBaseAdapter =  Depends(get_database_adapter),
) -> List[BuildingDto]:
    return await adapter.find_buildings_by_address(query.name)


@building_router.get('/geo', response_model=List[BuildingDto])
async def find_buildings_by_geo_query(
        query: GeoQueryDto = Depends(geo_query_dto),
        adapter: DataBaseAdapter =  Depends(get_database_adapter),
) -> List[BuildingDto]:
    return await adapter.find_buildings_by_geo_query(query)
