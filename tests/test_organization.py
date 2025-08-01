from typing import TYPE_CHECKING

import pytest
from sqlalchemy import select

from app.adapter.dto.organization import (OrganizationDto,
                                          OrganizationGeoQueryDto, GeoSearchMode)
from app.adapter.dto.building import BuildingDto
from app.adapter.dto.activity import ActivityDto
from app.adapter.search import ElasticSearchAdapter
from app.adapter.store.models import Activity, Building

if TYPE_CHECKING:
    from app.adapter import DataBaseAdapter

@pytest.mark.asyncio
async def test_get_organizations_by_building_id(db_adapter: 'DataBaseAdapter'):
    sc = db_adapter.get_session()
    async with sc() as session:
        building = (await session.execute(select(Building).where(Building.adress == 'Москва, ул. Пушкина, д. 4б офис 1.'))).first()

        result = await db_adapter.get_organizations_by_building_id(building[0].id)

        assert isinstance(result, list)
        assert all(isinstance(o, OrganizationDto) for o in result)
        assert all(isinstance(o.activity, ActivityDto) for o in result)
        assert all(isinstance(o.building, BuildingDto) for o in result)
        assert len(result) > 0


@pytest.mark.asyncio
async def test_get_organizations_by_activity_id(db_adapter: 'DataBaseAdapter'):
    sc = db_adapter.get_session()
    async with sc() as session:
        building = (await session.execute(select(Activity).where(Activity.name == 'Еда'))).first()

        result = await db_adapter.get_organizations_by_activity_id(building[0].id)

        assert isinstance(result, list)
        assert all(isinstance(o, OrganizationDto) for o in result)
        assert all(isinstance(o.activity, ActivityDto) for o in result)
        assert all(isinstance(o.building, BuildingDto) for o in result)
        assert len(result) > 0


@pytest.mark.asyncio
async def test_get_organizations_by_geo_query_empty(db_adapter: 'DataBaseAdapter'):
    query = OrganizationGeoQueryDto(
        longitude=44.5450,
        latitude=45.3200,
        mode=GeoSearchMode.RADIUS,
        radius_meters=1.0,
    )

    result = await db_adapter.get_organizations_by_geo_query(query)

    assert isinstance(result, list)
    assert len(result) == 0

@pytest.mark.asyncio
async def test_get_organizations_by_geo_query_radius_count_6(db_adapter: 'DataBaseAdapter'):
    query = OrganizationGeoQueryDto(
        longitude=45.5450,
        latitude=45.3200,
        mode=GeoSearchMode.RADIUS,
        radius_meters=1.0,
    )

    result = await db_adapter.get_organizations_by_geo_query(query)

    assert isinstance(result, list)
    assert all(isinstance(o, OrganizationDto) for o in result)
    assert all(isinstance(o.activity, ActivityDto) for o in result)
    assert all(isinstance(o.building, BuildingDto) for o in result)
    assert len(result) == 6

@pytest.mark.asyncio
async def test_get_organizations_by_geo_query_bbox(db_adapter: 'DataBaseAdapter'):
    query = OrganizationGeoQueryDto(
        longitude=45.5450,
        latitude=45.3200,
        mode=GeoSearchMode.BBOX,
        bbox_padding=100000,
    )

    result = await db_adapter.get_organizations_by_geo_query(query)

    assert isinstance(result, list)
    assert all(isinstance(o, OrganizationDto) for o in result)
    assert all(isinstance(o.activity, ActivityDto) for o in result)
    assert all(isinstance(o.building, BuildingDto) for o in result)
    assert len(result) == 6


@pytest.mark.asyncio
async def test_get_organizations_by_activity_name(db_adapter: 'DataBaseAdapter'):

    result = await db_adapter.get_organizations_by_activity_name('Еда')
    assert isinstance(result, list)
    assert len(result) == 2

@pytest.mark.asyncio
async def test_get_organizations_by_organization_name(db_adapter: 'DataBaseAdapter'):

    result = await db_adapter.get_organizations_by_organization_name('Рога')
    assert isinstance(result, list)
    assert len(result) == 2
