from unittest import TestCase
from logging import Logger
from mock import Mock
import sys
sys.path.append('..')

import filelogging

class CreateLoggerTestWithoutLogFilePath(TestCase):
    def runTest(self):
        config = None
        self.assertRaises(RuntimeError, filelogging.createLogger, (config))
        
class CreateLoggerTestWithLogFilePath(TestCase):
    def runTest(self):
        configMock = Mock()
        configMock.LOG_FILE_PATH = '/tmp/log'
        logger = filelogging.createLogger(configMock)
        self.assertIsInstance(logger, Logger)
