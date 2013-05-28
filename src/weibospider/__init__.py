__all__ = ['context', 'BreadthFirstWeiboProvider', 'sinaweiboapi']

import config
import utils

class BreadthFirstWeiboProvider(object):
    
    WEIBO_COUNT = 500
    
    def __init__(self, weiboAPI, context):
        self._weiboAPI = weiboAPI
        self._context = context
    
    def getWeibos(self):
        user = self._context.dequeueUser()
        while user is not None:
            for weibo in self._weiboAPI.getWeibo(user.name, BreadthFirstWeiboProvider.WEIBO_COUNT):
                yield weibo
            else:
                userList = self._weiboAPI.getFollowingUser(user.name)
                saveUserList = [x for x in userList if not self._context.existsUser(x.name)]
                self._context.enqueueUsers(saveUserList)
                user = self._context.dequeueUser()
        else:
            raise StopIteration

            
def createWeiboAPI():
    utils.assertConfig('VirtualBrowserClass')
    utils.assertConfig('WeiboAPIModule')
    utils.assertConfig('AppKey')
    utils.assertConfig('AppSecret')
    utils.assertConfig('RedirectURL')
    utils.assertConfig('UserName')
    utils.assertConfig('Password')
    utils.assertConfig('WeiboAPIProcessClass')
    return config.WeiboAPIProcessClass(config.WeiboAPIModule, config.VirtualBrowserClass(), configName.AppKey, config.AppSecret, configName.RedirectURL, config.UserName, config.Password) 

def createWeiboProvider():
    utils.assertConfig('WeiboProviderclass')
    utils.assertConfig('ContextFactory')
    return config.WeiboProviderclass(createWeiboAPI(), config.ContextFactory())