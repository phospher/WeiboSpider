class RedisModuleMock(object):
    
    def __init__(self, redisMock):
        self._redisMock = redisMock
    
    def ConnectionPool(self, *args, **kwargs):
        return None
    
    def Redis(self, *args, **kwargs):
        return self._redisMock