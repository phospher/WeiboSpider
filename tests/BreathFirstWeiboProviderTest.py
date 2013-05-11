import unittest
from mock import Mock
from collections import deque
import sys
import os

sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0] + '/src/')

from weibospider import *
from models import *

class MockContext(object):
    def __init__(self):
        self._userQueue = deque()
    
    def dequeueUser(self):
        if len(self._userQueue) == 0:
            return None
        else:
            return self._userQueue.popleft()
        
    def enqueueUsers(self, userList):
        self._userQueue.extend(userList)
    
    def existsUser(self, userName):
        return False
        
class BreadthFirstWeiboProviderTest(unittest.TestCase):
                   
    def setUp(self):
        self._context = MockContext()
        firstUser = UserModel()
        firstUser.name = 'phospher'
        self._context.enqueueUsers([firstUser])
        
        self._weiboAPI = Mock()
        def mockGetWeibo(userName, maxWeiboCount):
            weiboResult = []
            for i in range(1, 4):
                weibo = WeiboModel()
                weibo.id = i
                weibo.userName = userName
                weiboResult.append(weibo)
            return weiboResult
        self._weiboAPI.getWeibo = Mock(side_effect=mockGetWeibo)
        
        userResult = []
        for i in range(1, 4):
            user = UserModel()
            user.name = 'phospher%s' % i
            userResult.append(user)
        self._weiboAPI.getFollowingUser = Mock(side_effect=lambda v:userResult if v == 'phospher' else [])
    
    def test_getWeibosWithNoUserRaiseStopIteration(self):
        context = MockContext()
        target = BreadthFirstWeiboProvider(self._weiboAPI, context)
        self.assertRaises(StopIteration, target.getWeibos().next)
    
    def test_getWeibosWithNoUserGetWeiboNotCalling(self):
        context = MockContext()
        target = BreadthFirstWeiboProvider(self._weiboAPI, context)
        for item in target.getWeibos():
            pass
        self.assertEqual(self._weiboAPI.getWeibo.call_count, 0)
    
    def test_getWeibosReturnWeibos(self):
        target = BreadthFirstWeiboProvider(self._weiboAPI, self._context)
        actual = list(target.getWeibos())
        self.assertEqual(len(actual), 12)
    
    def test_getWeibosAssertWeiboOrder(self):
        target = BreadthFirstWeiboProvider(self._weiboAPI, self._context)
        actual = list(target.getWeibos())
        self.assertTrue(actual[0].userName == 'phospher' and actual[3].userName == 'phospher1' \
                       and actual[6].userName == 'phospher2' and actual[9].userName == 'phospher3')
    
    def test_getWeibosWithNoWeiboAssertGetWeiboCallTimes(self):
        self._weiboAPI.getWeibo = Mock(return_value=[])
        target = BreadthFirstWeiboProvider(self._weiboAPI, self._context)
        actual = list(target.getWeibos())
        self.assertEqual(self._weiboAPI.getWeibo.call_count, 4)
    
    def test_getWeibosWithNoWeiboAssertResultCount(self):
        self._weiboAPI.getWeibo = Mock(return_value=[])
        target = BreadthFirstWeiboProvider(self._weiboAPI, self._context)
        actual = list(target.getWeibos())
        self.assertEqual(len(actual), 0)
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
        
