from models import UserModel
import config
import utils

class RedisContext(object):
    
    CONNECTION_POOL = None
    HOST = config.RedisContext_HOST if hasattr(config, 'RedisContext_HOST') and config.RedisContext_HOST is not None else 'localhost'
    PORT = config.RedisContext_PORT if hasattr(config, 'RedisContext_HOST') and config.RedisContext_PORT is not None else 6379
    DB = config.RedisContext_DB if hasattr(config, 'RedisContext_DB') and config.RedisContext_DB is not None else 0
    
    USER_LIST_KEY = 'weibospider_user_list'
    USER_SET_KEY = 'weibospider_user_set'
    
    def __init__(self, redisModule):
        if not RedisContext.CONNECTION_POOL:
            RedisContext.CONNECTION_POOL = redisModule.ConnectionPool(host=RedisContext.HOST, port=RedisContext.PORT, db=RedisContext.DB)
        self._redisClient = redisModule.Redis(connection_pool=RedisContext.CONNECTION_POOL)
    
    def dequeueUser(self):
        result = UserModel()
        result.name = self._redisClient.lpop(RedisContext.USER_LIST_KEY)
        return result
    
    def existsUser(self, userName):
        return self._redisClient.sismember(RedisContext.USER_SET_KEY, userName)
    
    def enqueueUsers(self, userList):
        for user in userList:
            if self._redisClient.sadd(RedisContext.USER_SET_KEY, user.name) > 0:
                self._redisClient.rpush(RedisContext.USER_LIST_KEY, user.name)

def createRedisContext():
    utils.assertConfig('ContextRedisModule')
    return RedisContext(config.ContextRedisModule)