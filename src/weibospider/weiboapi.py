import re
from weibospider import WeiboModel
import time

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
    searchResult = re.search(r'[?&]code=(\S+)', redirectUrl)
    code = searchResult.group(1)
    
    request = apiClient.request_access_token(code)
    apiClient.set_access_token(request.access_token, request.expires_in)

class SinaWeiboAPI(object):
    def __init__(self, weiboAPIModule, virtualBrowser, appKey, appSecret, RedirectUri, userName, password):
        self._apiClient = weiboAPIModule.APIClient(app_key=appKey, app_secret=appSecret, redirect_uri=RedirectUri)
        sinaWeiboAutoAuth(self._apiClient, userName, password, virtualBrowser)
    
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
                if 'retweeted_status' in statuse:
                    weiboModel.retweetedText = statuse.retweeted_status.text
                weiboModel.time = time.strptime(statuse.created_at, '%a %b %d %H:%M:%S +0800 %Y')
                weiboModel.id = statuse.id
                result.append(weiboModel)
        
        return result
            
                
