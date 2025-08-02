from typing import TYPE_CHECKING

import pytest
if TYPE_CHECKING:
    from app.adapter import DataBaseAdapter

@pytest.mark.asyncio
async def test_get_simple_activity_tree_by_name(db_adapter: 'DataBaseAdapter'):
    uids = await db_adapter.get_simple_activity_tree_by_name('Развле')
    assert len(uids) == 5
