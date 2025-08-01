from os import getenv

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

ORGZ_DATA_BASE_DSN: 'str' = getenv('ORGZ_DATA_BASE_DSN', None)

ORGZ_DATA_BASE_ECHO: 'bool' = getenv('ORGZ_DATA_BASE_ECHO', 'on') == 'on'

ORGZ_LOG_LEVEL: 'str' = getenv('ORGZ_LOG_LEVEL', 'INFO')
