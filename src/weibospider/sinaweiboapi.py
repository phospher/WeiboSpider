import re
import config
import utils
import time
from models import WeiboModel
from models import UserModel

def sinaWeiboAutoAuth(apiClient, userName, password, virtualBrowser):
    url = apiClient.get_authorize_url()
    
    # Open authorize and complete the authorization automatically
    virtualBrowser.open(url)
    virtualBrowser.select_form(name='authZForm')
    virtualBrowser['userId'] = userName
    virtualBrowser['passwd'] = password
    virtualBrowser.submit()
    
    # Get the authorization code for requesting access token
    redirectUrl = virtualBrowser.response().geturl()
    searchResult = re.search('[?&]code=(\S+)', redirectUrl)
    code = searchResult.group(1) if searchResult is not None else ''
    
    request = apiClient.request_access_token(code)
    apiClient.set_access_token(request.access_token, request.expires_in)



class SinaWeiboAPI(object):
    def __init__(self, weiboAPIModule, virtualBrowser, appKey, appSecret, RedirectUri, userName, password):
        self._apiClient = weiboAPIModule.APIClient(app_key=appKey, app_secret=appSecret, redirect_uri=RedirectUri)
        sinaWeiboAutoAuth(self._apiClient, userName, password, virtualBrowser)
    
    @utils.weiboAPIRetryDecorator
    def getWeibo(self, userName, weiboMaxCount):
        result = []
        page = 0
        while len(result) < weiboMaxCount:
            page += 1
            r = self._apiClient.statuses.user_timeline.get(screen_name=userName, page=page)
            if len(r.statuses) == 0:
                break
            for statuse in r.statuses:
                weiboModel = WeiboModel()
                weiboModel.userName = userName
                weiboModel.text = statuse.text
                if hasattr(statuse, 'retweeted_status'):
                    weiboModel.retweetedText = statuse.retweeted_status.text
                weiboModel.time = time.strptime(statuse.created_at, '%a %b %d %H:%M:%S +0800 %Y')
                weiboModel.id = statuse.id
                result.append(weiboModel)
                if len(result) >= weiboMaxCount:
                    break
        
        return result

    @utils.weiboAPIRetryDecorator
    def getFollowingUser(self, userName):
        result = []
        cursor = 0
        while True:
            r = self._apiClient.friendships.friends.get(screen_name=userName, cursor=cursor, count=200)
            if len(r.users) == 0:
                break
            for user in r.users:
                userModel = UserModel()
                userModel.id = user.id
                userModel.name = user.screen_name
                result.append(userModel)
            if r.next_cursor == 0:
                break
            else:
                cursor = r.next_cursor

        return result

            
                
