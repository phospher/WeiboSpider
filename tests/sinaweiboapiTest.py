import os
from mock import Mock
import unittest
import sys

sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0] + '/src/')

from weibospider.sinaweiboapi import SinaWeiboAPI

class WeiboAPIModuleMock(object):

	def __init__(self, mockObject):
		self._mockObject = mockObject

	def APIClient(self, *args, **kwargs):
		return self._mockObject

class SinaWeiboAPITest(unittest.TestCase):

	def setUp(self):
		self._weiboList = []

		self._virtualBrowser = Mock()
		self._virtualBrowser.__setitem__ = Mock()
		self._virtualBrowser.response = Mock(return_value=Mock())
		self._virtualBrowser.response().geturl = Mock(return_value='')
		
		self._weiboResult = Mock()

		def getWeibo(*args, **kwargs):
			startIndex = (kwargs['page'] - 1) * 10
			endIndex = kwargs['page'] * 10
			result = Mock()
			result.statuses = self._weiboList[startIndex:endIndex]
			return result
		self._defaultweiboapiMock = Mock()
		self._defaultweiboapiMock.statuses.user_timeline.get = Mock(side_effect=getWeibo)
	
	def test_ReturnEmptyWeiboResultWhenAPIReturnNoResult(self):
		self._weiboResult.statuses = []
		weiboapiMock = Mock()
		weiboapiMock.statuses.user_timeline.get = Mock(return_value=self._weiboResult)
		target = SinaWeiboAPI(WeiboAPIModuleMock(weiboapiMock), self._virtualBrowser, None, None, '', None, None)
		result = target.getWeibo(None, 100)
		self.assertEquals(len(result), 0)

	def _processDefaultGetWeibo(self, maxWeiboCount):
		target = SinaWeiboAPI(WeiboAPIModuleMock(self._defaultweiboapiMock), self._virtualBrowser, None, None, '', None, None)
		return target.getWeibo(None, maxWeiboCount)

	def _initWeiboList(self, weiboCount):
		for i in range(0, weiboCount):
			statusMock = Mock()
			statusMock.created_at = 'Tue May 24 18:04:53 +0800 2011'
			self._weiboList.append(statusMock)

	def test_ReturnResultLessThenMaxCountInOnePage(self):
		self._initWeiboList(2)
		result = self._processDefaultGetWeibo(100)
		self.assertEquals(len(result), 2)

	def test_ReturnMaxResultInOnePage(self):
		self._initWeiboList(6)
		result = self._processDefaultGetWeibo(3)
		self.assertEquals(len(result), 3)

	def test_ReturnResultLessThenMaxCountInMulpage(self):
		self._initWeiboList(20)
		result = self._processDefaultGetWeibo(20)
		self.assertEquals(len(result), 20)

	def test_ReturnMaxResultInMulpage(self):
		self._initWeiboList(20)
		result = self._processDefaultGetWeibo(12)
		self.assertEquals(len(result), 12)

if __name__ == '__main__':
	unittest.main()


