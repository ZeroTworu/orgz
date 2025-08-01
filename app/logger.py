import logging

from app.settings import ORGZ_LOG_LEVEL


def get_logger(name: 'str'):
    handler = logging.StreamHandler()
    handler.formatter = logging.Formatter(fmt=f'[%(asctime)s {name}]: %(message)s', datefmt='%H:%M:%S')
    logger = logging.getLogger(name)
    logger.setLevel(logging.getLevelName(ORGZ_LOG_LEVEL))
    logger.addHandler(handler)
    return logger
