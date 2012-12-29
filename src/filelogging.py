import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler



def createLogger(config):
    if not hasattr(config, 'LOG_FILE_PATH'):
        raise RuntimeError('LOG_FILE_PATH is not defined')
    
    logFilePath = config.LOG_FILE_PATH
    handler = TimedRotatingFileHandler(filename=logFilePath, when='D', encoding='utf8')
    formatter = Formatter('%(asctime)s--%(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger('SpiderLogger')
    logger.addHandler(handler)
    return logger
