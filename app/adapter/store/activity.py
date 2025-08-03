import uuid
from typing import TYPE_CHECKING

from sqlalchemy import case, select, update
from sqlalchemy.exc import NoResultFound

from app.adapter.store.models import Activity

if TYPE_CHECKING:
    from app.adapter.store.sql_adapter import DataBaseAdapter
    from sqlalchemy import Result, Sequence
    from typing import List

from asyncio import gather

from app.adapter.dto import ActivityDto, ActivityTreeDto, ElasticQueryDto


class ActivityAdapter:  # noqa: WPS214

    async def add_activity(self: 'DataBaseAdapter', name: 'str', parent_id: 'uuid.UUID | None' = None) -> 'ActivityDto':
        if parent_id is None:
            activity = await self._add_as_root(name)
        else:
            activity = await self._add_under_parent(name, parent_id)
        await self._search_adapter.index_activity(activity)
        return activity

    async def get_all_activities_trees(self: 'DataBaseAdapter') -> 'List[ActivityTreeDto]':
        async with self._async_session_maker() as session:
            roots: 'Sequence[uuid.UUID]' = (await session.execute(
                select(Activity.id).where(Activity.parent_id.is_(None))
            )).scalars().all()

            results = await gather(
                *map(
                    self.get_activity_tree_by_root_id,
                    roots,
                ),
            )
            return list(
                filter(
                    lambda activity: activity is not None,
                    results,
                )
            )

    async def get_activity_tree_by_root_id(
            self: 'DataBaseAdapter',
            activity_id: 'uuid.UUID|str'
    ) -> 'ActivityTreeDto|None':
        async with self._async_session_maker() as session:
            root: 'Result[tuple[Activity]]' = await session.execute(
                select(Activity).where(Activity.id == activity_id)
            )

            try:
                root: 'Activity' = root.scalar_one()
            except NoResultFound:
                self._logger.warning('Activity tree not found')
                return None

            descendants = (
                await session.execute(
                    select(Activity)
                    .where(
                        (Activity.lft >= root.lft) &
                        (Activity.rgt <= root.rgt)
                    )
                    .order_by(Activity.lft)
                )
            ).scalars().all()

        return self._build_tree(root, descendants)

    async def find_simple_activity_tree_by_name(
            self: 'DataBaseAdapter',
            name: 'str',
    ) -> 'List[uuid.UUID]':

        uids = await self._search_adapter.search(ElasticQueryDto(name=name))
        if not bool(uids):
            return []
        results = await gather(
            *map(
                self.get_simple_activity_tree_by_id,
                uids,
            ),
        )
        return [_uuid for uuids in results for _uuid in uuids]

    async def find_activity_tree_by_name(
            self: 'DataBaseAdapter',
            name: 'str',
    ) -> 'List[ActivityTreeDto]':

        uids = await self._search_adapter.search(ElasticQueryDto(name=name))
        if not bool(uids):
            return []
        results = await gather(
            *map(
                self.get_activity_tree_by_root_id,
                uids,
            ),
        )
        return list(
            filter(
                lambda activity: activity is not None,
                results,
            )
        )

    async def get_simple_activity_tree_by_id(
            self: 'DataBaseAdapter',
            activity_id: 'uuid.UUID|str'
    ) -> 'List[uuid.UUID]':
        async with self._async_session_maker() as session:
            root: 'Result[tuple[Activity]]' = await session.execute(
                select(Activity).where(Activity.id == activity_id)
            )

            try:
                root: 'Activity' = root.scalar_one()
            except NoResultFound:
                self._logger.warning('Activity tree not found')
                return []

            descendants = (
                await session.execute(
                    select(Activity.id)
                    .where(
                        (Activity.lft >= root.lft) &
                        (Activity.rgt <= root.rgt)
                    )
                    .order_by(Activity.lft)
                )
            ).scalars().all()

            return [scalar for scalar in descendants]

    async def reindex_activities(self: 'DataBaseAdapter'):
        async with self._async_session_maker() as session:
            activities = [
                ActivityDto.model_validate(activity)
                for activity in (await session.execute(select(Activity))).scalars().all()
            ]
            await gather(
                *map(
                    self._search_adapter.index_activity,
                    activities,
                )
            )

    def _build_tree(self: 'DataBaseAdapter', root: 'Activity', descendants: 'Sequence[Activity]') -> 'ActivityTreeDto':
        id_to_node: dict[uuid.UUID, ActivityTreeDto] = {}

        root_node = ActivityTreeDto(
            id=root.id,
            name=root.name,
            children=[],
            parent_id=root.parent_id,
        )
        id_to_node[root.id] = root_node

        for node in descendants:
            dto = ActivityTreeDto(
                id=node.id,
                name=node.name,
                children=[],
                parent_id=node.parent_id
            )
            id_to_node[node.id] = dto

        for node in descendants:
            parent = id_to_node.get(node.parent_id)
            if parent:
                parent.children.append(id_to_node[node.id])
            if node.parent_id == root.id:
                root_node.children.append(id_to_node[node.id])

        return root_node

    async def _add_as_root(self: 'DataBaseAdapter', name: 'str') -> 'ActivityDto':
        async with self._async_session_maker() as session:
            max_rgt = (
                await session.execute(
                    select(Activity.rgt).order_by(Activity.rgt.desc()).limit(1)
                )
            ).scalar()
            insert_lft = 1 if max_rgt is None else (max_rgt + 1)

            new_node = Activity(
                name=name,
                parent_id=None,
                lft=insert_lft,
                rgt=insert_lft + 1,
            )
            session.add(new_node)
            await session.commit()
            await session.flush()
            return ActivityDto.model_validate(new_node)

    async def _add_under_parent(self: 'DataBaseAdapter', name: 'str', parent_id: 'uuid.UUID') -> 'ActivityDto':
        async with self._async_session_maker() as session:
            parent: Activity = (
                await session.execute(select(Activity).where(Activity.id == parent_id))
            ).scalar_one()

            insert_lft = parent.rgt

            await session.execute(
                update(Activity)
                .where((Activity.rgt >= insert_lft) | (Activity.lft > insert_lft))
                .values(
                    lft=case(
                        (Activity.lft > insert_lft, Activity.lft + 2),
                        else_=Activity.lft
                    ),
                    rgt=case(
                        (Activity.rgt >= insert_lft, Activity.rgt + 2),
                        else_=Activity.rgt
                    ),
                )
            )

            new_node = Activity(
                name=name,
                parent_id=parent_id,
                lft=insert_lft,
                rgt=insert_lft + 1,
            )

            session.add(new_node)
            await session.commit()
            await session.flush()
            return ActivityDto.model_validate(new_node)
