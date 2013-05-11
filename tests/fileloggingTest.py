from unittest import TestCase
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
from mock import Mock
import logging
import sys
import os

sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0] + '/src/')

import filelogging

class CreateInfoLoggerTest(TestCase):
    def setUp(self):
        configMock = Mock()
        configMock.INFO_LOG_FILE_PATH = '/tmp/unittest.log'
        self.logger = filelogging.createInfoLogger(configMock)
    
    def test_withoutInfoLogFilePath(self):
        config = None
        self.assertRaises(RuntimeError, filelogging.createInfoLogger, (config))
    
    def test_withInfoLogFilePath(self):
        self.assertIsInstance(self.logger, Logger)
    
    def test_filename(self):
        handler = self.logger.handlers[0]
        self.assertEquals(handler.baseFilename, '/tmp/unittest.log')
    
    def test_infoLevel(self):
        self.assertTrue(self.logger.level & logging.INFO)


class CreateErrorLogerTest(TestCase):
    def setUp(self):
        configMock = Mock()
        configMock.ERROR_LOG_FILE_PATH = '/tmp/unittest.log'
        self.logger = filelogging.createErrorLogger(configMock)
    
    def test_withoutErrorLogFilePath(self):
        config = None
        self.assertRaises(RuntimeError, filelogging.createErrorLogger, (config))
    
    def test_withErrorLogFilePath(self):
        self.assertIsInstance(self.logger, Logger)
    
    def test_filename(self):
        handler = self.logger.handlers[0]
        self.assertEqual(handler.baseFilename, '/tmp/unittest.log')
    
    def test_errorLevel(self):
        self.assertTrue(self.logger.level & logging.ERROR)

if __name__ == '__main__':
    unittest.main()