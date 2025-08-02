from app.adapter.search.elastic import ElasticSearchAdapter

_search_adapter: 'ElasticSearchAdapter' = ElasticSearchAdapter()


def get_search_adapter() -> 'ElasticSearchAdapter':
    return _search_adapter

