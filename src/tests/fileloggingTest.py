from unittest import TestCase
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
from mock import Mock
import logging
import sys
sys.path.append('..')

import filelogging

def getMockLogger():
    configMock = Mock()
    configMock.LOG_FILE_PATH = '/tmp/unittest.log'
    logger = filelogging.createLogger(configMock)
    return logger

class CreateLoggerTestWithoutLogFilePath(TestCase):
    def runTest(self):
        config = None
        self.assertRaises(RuntimeError, filelogging.createLogger, (config))
        
class CreateLoggerTestWithLogFilePath(TestCase):
    def runTest(self):
        self.assertIsInstance(getMockLogger(), Logger)

class CreateLoggerTestWithFileName(TestCase):
    def runTest(self):
        logger = getMockLogger()
        handler = logger.handlers[0]
        self.assertEquals(handler.baseFilename, '/tmp/unittest.log')

class CreateLoggerTestWithInfoLevel(TestCase):
    def runTest(self):
        logger = getMockLogger()
        self.assertTrue(logger.level & logging.INFO)
