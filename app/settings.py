from os import getenv

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

ORGZ_DATA_BASE_DSN: 'str' = getenv('ORGZ_DATA_BASE_DSN', None)

ORGZ_API_KEY_HEADER_NAME: 'str' = getenv('ORGZ_API_KEY_HEADER_NAME', 'X-ORGZ-API-KEY')

ORGZ_API_KEY: 'str' = getenv('ORGZ_API_KEY', None)

ORGZ_DATA_BASE_ECHO: 'bool' = getenv('ORGZ_DATA_BASE_ECHO', 'yes') == 'yes'

ORGZ_FORCE_RECREATE: 'bool' = getenv('ORGZ_FORCE_RECREATE', 'yes') == 'yes'

ORGZ_USE_FAKE_DATA: 'bool' = getenv('ORGZ_USE_FAKE_DATA', 'yes') == 'yes'

ORGZ_LOG_LEVEL: 'str' = getenv('ORGZ_LOG_LEVEL', 'INFO')

ORGZ_ELASTIC_HOST: 'str' = getenv('ORGZ_ELASTIC_HOST', 'http://localhost:9200')

ORGZ_ES_INDEX_NAME: 'str' = getenv('ORGZ_ES_INDEX_NAME', 'orgz-index')

if ORGZ_DATA_BASE_DSN is None:
    print('ORGZ_DATA_BASE_DSN is not set!')
    exit(-1)
if ORGZ_API_KEY is None:
    print('ORGZ_API_KEY is not set!')
    exit(-1)
