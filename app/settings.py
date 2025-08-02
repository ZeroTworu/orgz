from os import getenv

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

ORGZ_DATA_BASE_DSN: 'str' = getenv('ORGZ_DATA_BASE_DSN', None)

ORGZ_DATA_BASE_ECHO: 'bool' = getenv('ORGZ_DATA_BASE_ECHO', 'on') == 'on'

ORGZ_FORCE_RECREATE: 'bool' = getenv('ORGZ_FORCE_RECREATE', 'yes') == 'yes'

ORGZ_LOG_LEVEL: 'str' = getenv('ORGZ_LOG_LEVEL', 'INFO')

ORGZ_ELASTIC_HOST: 'str' = getenv('ORGZ_ELASTIC_HOST', 'http://localhost:9200')

ORGZ_ES_INDEX_NAME: 'str' = getenv('ORGZ_ES_INDEX_NAME', 'orgz-index')
