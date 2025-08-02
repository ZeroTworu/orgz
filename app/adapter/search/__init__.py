from app.adapter.search.elastic import ElasticSearchAdapter
from app.settings import ORGZ_PYTEST_ON

_search_adapter: 'ElasticSearchAdapter' = ElasticSearchAdapter()


def get_search_adapter() -> 'ElasticSearchAdapter':
    if ORGZ_PYTEST_ON:
        return ElasticSearchAdapter()
    return _search_adapter

