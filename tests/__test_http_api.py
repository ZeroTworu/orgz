import pytest
from httpx import AsyncClient

from app.adapter import DataBaseAdapter


@pytest.mark.asyncio
async def test_get_organization_by_id(client: AsyncClient, db_adapter: DataBaseAdapter):
    orgs = await db_adapter.get_organizations_by_organization_name('Копыта')
    org = orgs[0]
    response = await client.get(f'/api/v1/org/id/{org.organization_id}')
    assert response.status_code == 200
    assert response.json()['id'] == str(org.organization_id)


@pytest.mark.asyncio
async def test_get_organization_by_building_id(client: AsyncClient, db_adapter: DataBaseAdapter):
    orgs = await db_adapter.get_organizations_by_organization_name('Копыта')
    building_id = orgs[0].building.building_id
    response = await client.get(f'/api/v1/org/building/{building_id}')
    assert response.status_code == 200
    for item in response.json():
        assert item['building']['id'] == str(building_id)


@pytest.mark.asyncio
async def test_get_organization_by_activity_id(client: AsyncClient, db_adapter: DataBaseAdapter):
    orgs = await db_adapter.get_organizations_by_organization_name('Копыта')
    activity_id = orgs[0].activity.activity_id
    response = await client.get(f'/api/v1/org/activity/{activity_id}')
    assert response.status_code == 200
    for item in response.json():
        assert item['activity']['id'] == str(activity_id)


@pytest.mark.asyncio
async def test_get_organization_by_activity_name(client: AsyncClient):
    response = await client.get('/api/v1/org/activity_name', params={'name': 'еда'})
    assert response.status_code == 200
    for org in response.json():
        assert org['activity']['name'].lower() in ['еда', 'молочная продукция']


@pytest.mark.asyncio
async def test_get_organization_by_organization_name(client: AsyncClient):
    response = await client.get('/api/v1/org/organization_name', params={'name': 'рога'})
    assert response.status_code == 200
    for org in response.json():
        assert 'рога' in org['name'].lower()


@pytest.mark.asyncio
async def test_get_organization_by_geo(client: AsyncClient):
    response = await client.get(
        '/api/v1/org/geo',
        params={
            'longitude': 46.5454,
            'latitude': 46.3232,
            'mode': 'radius',
            'radius_meters': 500,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for org in data:
        assert 'building' in org
        assert 'cords' in org['building']
