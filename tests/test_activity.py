from typing import TYPE_CHECKING

import pytest
if TYPE_CHECKING:
    from app.adapter import DataBaseAdapter
    from app.adapter.search import ElasticSearchAdapter

@pytest.mark.asyncio
async def test_get_simple_activity_tree_by_name(db_adapter: 'DataBaseAdapter', search_adapter: 'ElasticSearchAdapter'):
    uids = await db_adapter.get_simple_activity_tree_by_name('Развле', search_adapter)
    assert len(uids) == 5


@pytest.mark.asyncio
async def test_all_activity_trees(db_adapter: 'DataBaseAdapter'):
    uids = await db_adapter.get_all_activities_trees()
    assert len(uids) == 3

@pytest.mark.asyncio
async def test_all_activity_trees(db_adapter: 'DataBaseAdapter', search_adapter: 'ElasticSearchAdapter'):
    uids = await db_adapter.get_activity_tree_by_name('Нас', search_adapter)
    assert len(uids) == 1
    assert len(uids[0].children) == 1
