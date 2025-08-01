from typing import TYPE_CHECKING

from sqlalchemy import select

from app.adapter.dto.organizations import OrganizationDto
from app.adapter.store.models import Organization

if TYPE_CHECKING:
    from typing import List
    from uuid import UUID

    from sqlalchemy import Result

    from app.adapter.dto.organizations import ActivityDto, BuildingDto
    from app.adapter.store.sql_adapter import DataBaseAdapter


class OrganizationAdapter:

    async def add_organization(
        self: 'DataBaseAdapter',
        name: 'str',
        activity: 'ActivityDto',
        building: 'BuildingDto',
    ) -> 'OrganizationDto':
        async with self._sc() as session:

            record = Organization(
                name=name,
                activity_id=activity.activity_id,
                building_id=building.building_id,
            )

            session.add(record)

            await session.commit()
            await session.flush()
            return OrganizationDto.model_validate(record)

    async def get_organizations_by_building_id(
            self: 'DataBaseAdapter',
            building_id: 'UUID|str',
    ) -> 'List[OrganizationDto]':
        async with self._sc() as session:
            result: 'Result[tuple[Organization]]' = await session.execute(
                select(Organization).where(Organization.building_id == building_id)
            )
            return [OrganizationDto.model_validate(res) for res in result.scalars().all()]
