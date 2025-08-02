from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from app.adapter.dto import (ActivityDto, BuildingDto, ElasticQueryDto,
                             EsSearchType, OrganizationDto,
                             OrganizationGeoQueryDto)
from app.adapter.search import ElasticSearchAdapter, get_search_adapter
from app.adapter.store.models import Organization

if TYPE_CHECKING:
    from typing import List
    from uuid import UUID

    from sqlalchemy import Result
    from app.adapter.store.sql_adapter import DataBaseAdapter

from asyncio import gather


class OrganizationAdapter:

    async def add_organization(
            self: 'DataBaseAdapter',
            name: 'str',
            activity: 'ActivityDto',
            building: 'BuildingDto',
    ) -> 'OrganizationDto':
        search_adapter = get_search_adapter()
        async with self._sc() as session:
            record = Organization(
                name=name,
                activity_id=activity.activity_id,
                building_id=building.building_id,
            )

            session.add(record)

            await session.commit()
            await session.flush()
            dto = OrganizationDto(
                name=name,
                id=record.id,
                activity=activity,
                building=building,
            )
            await search_adapter.index_organization(dto)
            return dto

    async def get_organizations_by_building_id(
            self: 'DataBaseAdapter',
            building_id: 'UUID|str',
    ) -> 'List[OrganizationDto]':
        async with self._sc() as session:
            result: 'Result[tuple[Organization]]' = await session.execute(
                select(Organization)
                .options(
                    joinedload(Organization.building),
                    joinedload(Organization.activity),
                )
                .where(Organization.building_id == building_id)
                .distinct()
            )
            return [OrganizationDto.model_validate(res) for res in result.scalars().all()]

    async def get_organizations_by_activity_id(
            self: 'DataBaseAdapter',
            activity_id: 'UUID|str',
    ) -> 'List[OrganizationDto]':
        async with self._sc() as session:
            result: 'Result[tuple[Organization]]' = await session.execute(
                select(Organization)
                .options(
                    joinedload(Organization.building),
                    joinedload(Organization.activity),
                )
                .where(Organization.activity_id == activity_id)
                .distinct()
            )
            return [OrganizationDto.model_validate(res) for res in result.scalars().all()]

    async def get_organizations_by_geo_query(
            self: 'DataBaseAdapter',
            query: 'OrganizationGeoQueryDto'
    ) -> 'List[OrganizationDto]':
        async with self._sc() as session:
            result = await session.execute(
                select(Organization)
                .options(
                    joinedload(Organization.building),
                    joinedload(Organization.activity),
                )
                .where(query.condition)
                .distinct()
            )

            return [OrganizationDto.model_validate(org) for org in result.scalars().all()]

    async def get_organization_by_id(
            self: 'DataBaseAdapter',
            organization_id: 'UUID|str',
    ) -> 'OrganizationDto|None':
        async with self._sc() as session:
            result: 'Result[tuple[Organization]]' = await session.execute(
                select(Organization)
                .options(
                    joinedload(Organization.building),
                    joinedload(Organization.activity),
                )
                .where(Organization.id == organization_id)
            )

            try:
                organization = result.scalars().one()
            except NoResultFound:
                return None

            return OrganizationDto.model_validate(organization)

    async def get_organizations_by_activity_name(
            self: 'DataBaseAdapter',
            activity_name: 'str',
            es: 'ElasticSearchAdapter' = None,
    ) -> 'List[OrganizationDto]':
        if es is None:
            es = get_search_adapter()

        id_list = await es.search(ElasticQueryDto(
            name=activity_name,
        ))

        activity_ids = await gather(
            *map(
                self.get_simple_activity_tree_by_id,
                id_list,
            ),
        )
        activity_ids = [_uuid for uuids in activity_ids for _uuid in uuids]
        result = await gather(
            *map(
                self.get_organizations_by_activity_id,
                activity_ids,
            ),
        )

        return [org for orgs in result for org in orgs]

    async def get_organizations_by_organization_name(
            self: 'DataBaseAdapter',
            organization_name: 'str',
            es: 'ElasticSearchAdapter' = None,
    ) -> 'List[OrganizationDto]':
        if es is None:
            es = get_search_adapter()

        id_list = await es.search(ElasticQueryDto(
            name=organization_name,
            type=EsSearchType.ORGANIZATION,
        ))

        result = await gather(
            *map(
                self.get_organization_by_id,
                id_list,
            ),
        )

        return result
