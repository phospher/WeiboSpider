import re

def sinaWeiboAutoAuth(apiClient, userName, password, virtualBrowser):
    url = apiClient.get_authorize_url()
    
    #Open authorize and complete the authorization automatically
    virtualBrowser.open(url)
    virtualBrowser.select_form(name='authZForm')
    virtualBrowser['userId'] = userName
    virtualBrowser['passwd'] = password
    virtualBrowser.submit()
    
    #Get the authorization code for requesting access token
    redirectUrl = virtualBrowser.response().geturl()
    searchResult = re.search(r'[?&]code=(\S+)', redirectUrl)
    code = searchResult.group(1)
    
    request = apiClient.request_access_token(code)
    apiClient.set_access_token(request.access_token, request.expires_in)

class SinaWeiboAPI(object):
    def __init__(self, weiboAPIModule):
        pass
