import uuid
from typing import TYPE_CHECKING

from elasticsearch import AsyncElasticsearch

from app.adapter.dto import EsSearchType
from app.logger import get_logger
from app.settings import ORGZ_ELASTIC_HOST, ORGZ_ES_INDEX_NAME

if TYPE_CHECKING:
    from typing import List

    from app.adapter.dto import ActivityDto, ElasticQueryDto, OrganizationDto


class ElasticSearchAdapter:
    _logger = get_logger('ElasticSearchAdapter')

    def __init__(self):
        self._logger.info('Initializing ElasticSearchAdapter on host %s', ORGZ_ELASTIC_HOST)
        self._client = AsyncElasticsearch(hosts=[ORGZ_ELASTIC_HOST])

    async def init_index(self):
        async with self._client as client:
            exists = await client.indices.exists(index=ORGZ_ES_INDEX_NAME)
            if exists:
                return
            self._logger.info('Creating ElasticSearch index %s', ORGZ_ES_INDEX_NAME)
            await client.indices.create(
                index=ORGZ_ES_INDEX_NAME,
                body={
                    'settings': {
                        'analysis': {
                            'filter': {
                                'edge_ngram_filter': {
                                    'type': 'edge_ngram',
                                    'min_gram': 2,
                                    'max_gram': 15
                                }
                            },
                            'analyzer': {
                                'edge_ngram_analyzer': {
                                    'type': 'custom',
                                    'tokenizer': 'standard',
                                    'filter': ['lowercase', 'edge_ngram_filter']
                                }
                            }
                        }
                    },
                    'mappings': {
                        'properties': {
                            'name': {
                                'type': 'text',
                                'analyzer': 'edge_ngram_analyzer',
                                'search_analyzer': 'standard'
                            },
                            'type': {'type': 'keyword'},
                            'pk': {'type': 'keyword'}
                        }
                    }
                }
            )

    async def index_activity(self, activity: 'ActivityDto'):
        async with self._client as client:
            await client.index(
                index=ORGZ_ES_INDEX_NAME,
                document={
                    'type': EsSearchType.ACTIVITY.value,
                    'name': activity.name,
                    'pk': activity.activity_id,
                }
            )

    async def index_organization(self, organization: 'OrganizationDto'):
        async with self._client as client:
            await client.index(
                index=ORGZ_ES_INDEX_NAME,
                document={
                    'type': EsSearchType.ORGANIZATION.value,
                    'name': organization.name,
                    'pk': organization.organization_id,
                }
            )

    async def search(self, query: 'ElasticQueryDto') -> 'List[uuid.UUID]':
        async with self._client as client:
            result = await client.search(
                index=ORGZ_ES_INDEX_NAME,
                query={
                    'bool': {
                        'must': [
                            {'match': {'name': query.name}},
                            {'term': {'type': query.type.value}},
                        ]
                    }
                }
            )
            return [uuid.UUID(hit['_source']['pk']) for hit in result['hits']['hits']]  # noqa: WPS221

    async def clear_index(self):
        self._logger.info('Clearing ElasticSearch index %s', ORGZ_ES_INDEX_NAME)
        async with self._client as client:
            await client.delete_by_query(
                index=ORGZ_ES_INDEX_NAME,
                body={
                    'query': {
                        'match_all': {}
                    }
                },
                refresh=True
            )
