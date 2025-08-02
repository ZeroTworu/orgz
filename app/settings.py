from os import getenv

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

ORGZ_DATA_BASE_DSN: 'str' = getenv('ORGZ_DATA_BASE_DSN', None)

ORGZ_API_KEY: 'str' = getenv('ORGZ_API_KEY', None)

ORGZ_DATA_BASE_ECHO: 'bool' = getenv('ORGZ_DATA_BASE_ECHO', 'on') == 'on'

ORGZ_FORCE_RECREATE: 'bool' = getenv('ORGZ_FORCE_RECREATE', 'yes') == 'yes'

ORGZ_LOG_LEVEL: 'str' = getenv('ORGZ_LOG_LEVEL', 'INFO')

ORGZ_ELASTIC_HOST: 'str' = getenv('ORGZ_ELASTIC_HOST', 'http://localhost:9200')

ORGZ_ES_INDEX_NAME: 'str' = getenv('ORGZ_ES_INDEX_NAME', 'orgz-index')

ORGZ_PYTEST_ON: 'bool' = getenv('ORGZ_PYTEST_ON', 'no') == 'yes'

if ORGZ_DATA_BASE_DSN is None:
    print('ORGZ_DATA_BASE_DSN is not set!')
    exit(-1)
if ORGZ_API_KEY is None:
    print('ORGZ_API_KEY is not set!')
    exit(-1)
