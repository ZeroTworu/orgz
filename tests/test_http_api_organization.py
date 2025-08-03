import os
import pytest
from typing import TYPE_CHECKING
from starlette.status import HTTP_200_OK

from app.adapter.dto.activity import SearchType

if TYPE_CHECKING:
    from httpx import AsyncClient
    from app.adapter import DataBaseAdapter

API_HEADERS = {
    'X-ORGZ-Key': os.getenv('ORGZ_API_KEY', 'test-api-key'),
}


@pytest.mark.asyncio
async def test_get_organization_by_id(client: 'AsyncClient', db_adapter: 'DataBaseAdapter'):
    orgs = await db_adapter.find_organizations_by_organization_name('Копыта')
    org = orgs[0]
    response = await client.get(f'/api/v1/organization/id/{org.organization_id}', headers=API_HEADERS)
    assert response.status_code == HTTP_200_OK
    assert response.json()['id'] == str(org.organization_id)


@pytest.mark.asyncio
async def test_get_organization_by_building_id(client: 'AsyncClient', db_adapter: 'DataBaseAdapter'):
    orgs = await db_adapter.find_organizations_by_organization_name('Копыта')
    building_id = orgs[0].building.building_id
    response = await client.get(f'/api/v1/organization/building/{building_id}', headers=API_HEADERS)
    assert response.status_code == HTTP_200_OK
    for item in response.json():
        assert item['building']['id'] == str(building_id)


@pytest.mark.asyncio
async def test_get_organization_by_activity_id(client: 'AsyncClient', db_adapter: 'DataBaseAdapter'):
    orgs = await db_adapter.find_organizations_by_organization_name('Копыта')
    activity_id = orgs[0].activity.activity_id
    response = await client.get(f'/api/v1/organization/activity/{activity_id}', headers=API_HEADERS)
    assert response.status_code == HTTP_200_OK
    for item in response.json():
        assert item['activity']['id'] == str(activity_id)


@pytest.mark.asyncio
async def test_get_organization_by_geo(client: 'AsyncClient'):
    response = await client.get(
        '/api/v1/organization/geo',
        params={
            'longitude': 46.5454,
            'latitude': 46.3232,
            'mode': 'radius',
            'radius_meters': 500,
        },
        headers=API_HEADERS,
    )
    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    for org in data:
        assert 'building' in org
        assert 'cords' in org['building']


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'search_type,search_str,expected_in',
    [
        (SearchType.ACTIVITY_NAME, 'еда', 'рогатая няша'),
        (SearchType.ORGANIZATION_NAME, 'няша', 'рогатая няша'),
        (SearchType.BUILDING_ADDRESS, 'короленко', 'рогатая няша'),
    ],
)
async def test_search_endpoint(
    client: 'AsyncClient',
    search_type: SearchType,
    search_str: str,
    expected_in: str,
):
    response = await client.get(
        '/api/v1/organization/search',
        params={
            'search_str': search_str,
            'search_type': search_type.value,
        },
        headers=API_HEADERS,
    )
    assert response.status_code == HTTP_200_OK
    results = response.json()
    assert isinstance(results, list)
    assert any(
        expected_in.lower() in str(org['name']).lower()
        for org in results
    ), f'{expected_in} not found in response'