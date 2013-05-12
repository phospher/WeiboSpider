import config

class RedisPersistence(object):

	CONNECTION_POOL = None
	HOST = config.RedisPersistence_HOST if hasattr(config, 'RedisPersistence_HOST') and config.RedisPersistence_HOST is not None else 'localhost'
	PORT = config.RedisPersistence_PORT if hasattr(config, 'RedisPersistence_PORT') and config.RedisPersistence_PORT is not None else 6379
	DB = config.RedisPersistence_DB if hasattr(config, 'RedisPersistence_DB') and config.RedisPersistence_DB is not None else 1

	WEIBO_KEY_SET_KEY = 'weibo_key_set'

	def __init__(self, redisModule):
		if not RedisPersistence.CONNECTION_POOL:
			RedisPersistence.CONNECTION_POOL = redisModule.ConnectionPool(host=RedisPersistence.HOST, port=RedisPersistence.PORT, db=RedisPersistence.DB)
		self._redisClient = redisModule.Redis(connection_pool=RedisPersistence.CONNECTION_POOL)

	def AddWeibo(self, weiboModel):
		if self._redisClient.sadd(RedisPersistence.WEIBO_KEY_SET_KEY, weiboModel.id) == 1:
			self._redisClient.hmset('weibo_' + weiboModel.id, weiboModel)
		