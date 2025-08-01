from typing import TYPE_CHECKING

from app.adapter.dto.organizations import OrganizationDto
from app.adapter.store.models import Organization

if TYPE_CHECKING:
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
