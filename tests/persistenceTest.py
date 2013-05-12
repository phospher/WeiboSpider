import os
import sys
import unittest

sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0] + '/src/')

from testutils import RedisModuleMock
from mock import Mock
from models import WeiboModel
from persistence import RedisPersistence

class RedisPersistenceTest(unittest.TestCase):

	def setUp(self):
		self._redisMock = Mock()
		self._redisMock.sadd = Mock();
		self._redisMock.hmset = Mock()
		self._param1 = WeiboModel()
		self._param1.id = 1001

	def _processTest(self, saddReturnValue):
		self._redisMock.sadd.return_value = saddReturnValue
		RedisPersistence(RedisModuleMock(self._redisMock)).addWeibo(self._param1)

	def test_AddWeiboModelWhenNotExists(self):
		self._processTest(1)
		self._redisMock.hmset.assert_called_once_with('weibo_' + str(self._param1.id), self._param1)

	def test_NotAddWeiboModelWhenExists(self):
		self._processTest(0)
		self.assertEquals(self._redisMock.hmset.call_count, 0)

if __name__ == '__main__':
	unittest.main()