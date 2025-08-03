from fastapi import FastAPI

from app.adapter import DataBaseAdapter
from app.adapter.store.elastic import ElasticSearchAdapter
from app.settings import ORGZ_FORCE_RECREATE, ORGZ_USE_FAKE_DATA


class LifespanContext:

    def __call__(self, app: 'FastAPI'):
        # Что бы постоянно не дёргать `await self._try_init()`
        self._init_not_called = True
        self._app = app
        self._search_adapter = ElasticSearchAdapter()
        self._database_adapter = DataBaseAdapter(search_adapter=self._search_adapter)

        self._app.state.search_adapter = self._search_adapter
        self._app.state.database_adapter = self._database_adapter
        return self

    async def __aenter__(self):
        if self._init_not_called:
            await self._try_init()
            self._init_not_called = False
        return {}

    async def __aexit__(self, *args, **kwargs):
        await self._search_adapter.close()
        await self._database_adapter.close()

    async def _try_init(self):
        search_adapter = self._app.state.search_adapter
        database_adapter = self._app.state.database_adapter

        await search_adapter.init_index()
        if ORGZ_FORCE_RECREATE and ORGZ_USE_FAKE_DATA:
            await search_adapter.clear_index()
            await database_adapter.clear_data()
        if ORGZ_USE_FAKE_DATA:
            await database_adapter.init_data()
