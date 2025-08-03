from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.adapter import DataBaseAdapter, get_database_adapter_dep
from app.adapter.dto import (GeoQueryDto, OrganizationDto, SearchQueryDto,
                             geo_query_dto, search_query_dto)
from app.adapter.dto.search import SearchType

organizations_router = APIRouter(prefix='/api/v1/organization', tags=['Организации'])


@organizations_router.get(
    '/id/{org_id}',
    response_model=OrganizationDto,
    description=
    """
        Возвращает организацию по её ID
    """
)
async def get_organization_by_id(
        org_id: UUID,
        adapter: DataBaseAdapter =  Depends(get_database_adapter_dep),
) -> OrganizationDto|None:
    return await adapter.get_organization_by_id(org_id)


@organizations_router.get(
    '/building/{building_id}',
    response_model=List[OrganizationDto],
    description=
    """
        Возвращает организации принадлежашие соотве, по ID здания, поиск зданий доступен в секции \"Здания\"
    """
)
async def get_organization_by_building_id(
        building_id: UUID,
        adapter: DataBaseAdapter =  Depends(get_database_adapter_dep),
) -> List[OrganizationDto]:
    return await adapter.get_organizations_by_building_id(building_id)

@organizations_router.get(
    '/activity/{activity_id}',
    response_model=List[OrganizationDto],
    description
    ="""
        Список всех организаций, которые относятся к указанному виду деятельности.
        
        По ID вида деятельности, поиск зданий доступен в секции \"Виды Деятельности\"
    """
)
async def get_organization_by_activity_id(
        activity_id: UUID,
        adapter: DataBaseAdapter =  Depends(get_database_adapter_dep),
) -> List[OrganizationDto]:
    return await adapter.get_organizations_by_activity_id(activity_id)


@organizations_router.get(
    '/geo',
    response_model=List[OrganizationDto],
    description=
    """
        Список организаций, 
        которые находятся в заданном радиусе/прямоугольной области относительно указанной точки на карте.
    """
)
async def find_activities_by_geolocation(
        query: GeoQueryDto = Depends(geo_query_dto),
        adapter: DataBaseAdapter =  Depends(get_database_adapter_dep),
) -> List[OrganizationDto]:
    return await adapter.find_organizations_by_geo_query(query)


@organizations_router.get(
    '/search',
    response_model=List[OrganizationDto],
    description=
    """
        Поиск организаций по названию.
        
        Поиск организаций по виду деятельности и всех дочерних видов.
        
        Поиск организаций по адресу.
        
        Возможно частичное совпадение.
    """
)
async def find_organizations_by_every_thing(
        query: SearchQueryDto = Depends(search_query_dto),
        adapter: DataBaseAdapter =  Depends(get_database_adapter_dep),
) -> List[OrganizationDto]:
    match query.search_type:
        case SearchType.ACTIVITY_NAME:
            return await adapter.find_organizations_by_activity_name(query.search_str)
        case SearchType.ORGANIZATION_NAME:
            return await adapter.find_organizations_by_organization_name(query.search_str)
        case SearchType.BUILDING_ADDRESS:
            return await adapter.find_organizations_by_building_address(query.search_str)
        case _:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f'Unknown search type {query.search_type}')
