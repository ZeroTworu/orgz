from typing import TYPE_CHECKING

import pytest
if TYPE_CHECKING:
    from app.adapter import DataBaseAdapter

@pytest.mark.asyncio
async def test_get_simple_activity_tree_by_name(db_adapter: 'DataBaseAdapter'):
    uids = await db_adapter.find_simple_activity_tree_by_name('Развле')
    assert len(uids) == 5


@pytest.mark.asyncio
async def test_all_activity_trees(db_adapter: 'DataBaseAdapter'):
    uids = await db_adapter.get_all_activities_trees()
    assert len(uids) == 3

@pytest.mark.asyncio
async def test_activity_trees_name_search(db_adapter: 'DataBaseAdapter'):
    uids = await db_adapter.find_activity_tree_by_name('Нас')
    assert len(uids) == 1
    assert len(uids[0].children) == 1
