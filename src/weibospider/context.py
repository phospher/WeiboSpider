from weibo import UserModel

class RedisContext(object):
    
    CONNECTION_POOL = None
    HOST = 'localhost'
    PORT = 6379
    
    USER_LIST_KEY = 'weibospider_user_list'
    USER_SET_KEY = 'weibospider_user_set'
    
    def __init__(self, redisModule):
        if not RedisContext.CONNECTION_POOL:
            RedisContext.CONNECTION_POOL = redisModule.ConnectionPool(host=RedisContext.HOST, port=RedisContext.PORT)
        self.redisClient = redisModule.Redis(connection_pool=RedisContext.CONNECTION_POOL)
    
    def dequeueUser(self):
        result = UserModel()
        result.name = self.redisClient.lpop(RedisContext.USER_LIST_KEY)
        return result
    
    def existsUser(self, userName):
        return self.redisClient.sismember(RedisContext.USER_SET_KEY, userName)
    
    def enqueueUsers(self, userList):
        for user in userList:
            if self.redisClient.sadd(RedisContext.USER_SET_KEY, user.name) > 0:
                self.redisClient.rpush(RedisContext.USER_LIST_KEY, user.name)
