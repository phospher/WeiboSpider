from unittest import TestCase
import sys
from mock import Mock
import os

sys.path.append(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0] + '/src/')

from weibospider.context import RedisContext
from weibospider import UserModel

class RedisModuleMock(object):
    
    def __init__(self, redisMock):
        self._redisMock = redisMock
    
    def ConnectionPool(self, *args, **kwargs):
        return None
    
    def Redis(self, *args, **kwargs):
        return self._redisMock

class RedisContextTest(TestCase):
    def _dequeueUserInitialize(self):
        redisMock = Mock()
        redisMock.lpop = Mock(return_value='test_user')
        target = RedisContext(RedisModuleMock(redisMock))
        return target.dequeueUser()
    
    def test_dequeueUserReturnUserModelObject(self):
        actual = self._dequeueUserInitialize()
        self.assertIsInstance(actual, UserModel)
    
    def test_dequeueUserReturnCorrectUserName(self):
        actual = self._dequeueUserInitialize()
        self.assertEqual(actual.name, 'test_user')
    
    def test_existsUserReturnCorrectResult(self):
        redisMock = Mock()
        redisMock.sismember = Mock(side_effect=lambda k, v:True if v == 'test_user' else False)
        target = RedisContext(RedisModuleMock(redisMock))
        self.assertTrue(target.existsUser('test_user'))
    
    def _enqueueUsersTest(self, assertMethod):
        redisMock = Mock()
        redisMock.sadd = Mock(side_effect=lambda k, v:0 if v == 'test_user2' else 1)
        userBuff = []
        redisMock.rpush = Mock()
        
        param1 = []
        for i in range(0, 3):
            user = UserModel()
            user.name = 'test_user%s' % i
            param1.append(user)
        target = RedisContext(RedisModuleMock(redisMock))
        target.enqueueUsers(param1)
        
        assertMethod(redisMock)
    
    def test_enqueueUsersInsertTwoUsers(self):
        def assertRpushCallTwice(redisMock):
            self.assertEqual(redisMock.rpush.call_count, 2)
        
        self._enqueueUsersTest(assertRpushCallTwice)
    
    def test_enqueueUsersTestUser0InsertedOnce(self):
        def assertTestUser1Inserted(redisMock):
            user0List = [x for x in redisMock.rpush.call_args_list if x[0][1] == 'test_user0']
            self.assertEqual(len(user0List), 1)
        
        self._enqueueUsersTest(assertTestUser1Inserted)
        
if __name__ == '__main__':
    unittest.main()