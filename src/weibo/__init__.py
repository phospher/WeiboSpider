__all__ = ['DefaultWeiboProvider']

class DefaultWeiboProvider(object):
    
    WEIBO_COUNT = 500
    
    def __init__(self, weiboAPI, context):
        self._weiboAPI = weiboAPI
        self._context = context
    
    def nextWeibo(self):
        for user in self._context.getNextUser():
            for weibo in self._weiboAPI.getWeibo(user.name, WEIBO_COUNT):
                yield weibo
            else:
                userList = self._weiboAPI.getFollowingUser(user.name)
                saveUserList = [x for x in userList if not self._context.existsUser(x.name)]
                self._context.addUsers(saveUserList)
        else:
            raise StopIteration
            

class WeiboModel(object):
    def __init__(self):
        self.userName = None
        self.text = None
        self.retweetedText = None
        self.time = None
        self.id = None
