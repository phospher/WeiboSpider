import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

def _initLogger(loggerName, logFilePath, logLevel):
    handler = TimedRotatingFileHandler(filename=logFilePath, when='D')
    formatter = Formatter('%(asctime)s--%(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger('SpiderInfoLogger')
    logger.addHandler(handler)
    logger.setLevel(logLevel)
    return logger

def createInfoLogger(config):
    if not hasattr(config, 'INFO_LOG_FILE_PATH'):
        raise RuntimeError('INFO_LOG_FILE_PATH is not defined')
    
    logFilePath = config.INFO_LOG_FILE_PATH
    return _initLogger('SpiderInfoLogger', logFilePath, logging.INFO)

def createErrorLogger(config):
    if not hasattr(config, 'ERROR_LOG_FILE_PATH'):
        raise RuntimeError('ERROR_LOG_FILE_PATH is not defined')
    
    logFilePath = config.ERROR_LOG_FILE_PATH
    return _initLogger('SpiderErrorLogger', logFilePath, logging.ERROR)
    
    
