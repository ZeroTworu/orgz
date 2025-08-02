from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.adapter import DataBaseAdapter, get_database_adapter
from app.adapter.dto import (NameQueryDto, OrganizationDto,
                             OrganizationGeoQueryDto, name_query_dto,
                             organization_geo_query_dto)

organizations_router = APIRouter(prefix='/api/v1/org', tags=['organization'])


@organizations_router.get('/id/{org_id}', response_model=OrganizationDto)
async def get_organization_by_id(
        org_id: UUID,
        adapter: DataBaseAdapter =  Depends(get_database_adapter),
) -> OrganizationDto|None:
    return await adapter.get_organization_by_id(org_id)


@organizations_router.get('/building/{building_id}', response_model=List[OrganizationDto])
async def get_organization_by_building_id(
        building_id: UUID,
        adapter: DataBaseAdapter =  Depends(get_database_adapter),
) -> List[OrganizationDto]:
    return await adapter.get_organizations_by_building_id(building_id)

@organizations_router.get('/activity/{activity_id}', response_model=List[OrganizationDto])
async def get_organization_by_activity_id(
        activity_id: UUID,
        adapter: DataBaseAdapter =  Depends(get_database_adapter),
) -> List[OrganizationDto]:
    return await adapter.get_organizations_by_activity_id(activity_id)


@organizations_router.get('/geo', response_model=List[OrganizationDto])
async def find_activities_by_geolocation(
        query: OrganizationGeoQueryDto = Depends(organization_geo_query_dto),
        adapter: DataBaseAdapter =  Depends(get_database_adapter),
) -> List[OrganizationDto]:
    return await adapter.get_organizations_by_geo_query(query)

@organizations_router.get('/activity_name', response_model=List[OrganizationDto])
async def find_organizations_by_activities_name(
        query: NameQueryDto = Depends(name_query_dto),
        adapter: DataBaseAdapter =  Depends(get_database_adapter),
) -> List[OrganizationDto]:
    return await adapter.get_organizations_by_activity_name(query.name)

@organizations_router.get('/organization_name', response_model=List[OrganizationDto])
async def find_organizations_by_name(
        query: NameQueryDto = Depends(name_query_dto),
        adapter: DataBaseAdapter =  Depends(get_database_adapter),
) -> List[OrganizationDto]:
    return await adapter.get_organizations_by_organization_name(query.name)
