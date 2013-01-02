class DefaultWeiboProvider(object):
    def __init__(self, weiboAPI):
        self._weiboAPI = weiboAPI
    
    def __iter__(self):      
        return self
    
    def next(self):        
        return self._weiboAPI.next()