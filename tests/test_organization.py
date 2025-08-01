import pytest
from sqlalchemy import select

from app.adapter import DataBaseAdapter
from app.adapter.dto.organizations import OrganizationDto
from app.adapter.store.models import Building


@pytest.mark.asyncio
async def test_get_organizations_by_building_id(db_adapter: DataBaseAdapter):
    async with db_adapter.get_session()() as session:
        building = (await session.execute(select(Building).where(Building.adress == 'Москва, ул. Пушкина, д. 4б офис 1.'))).first()

        result = await db_adapter.get_organizations_by_building_id(building[0].id)

        assert isinstance(result, list)
        assert all(isinstance(o, OrganizationDto) for o in result)
        assert len(result) > 0
