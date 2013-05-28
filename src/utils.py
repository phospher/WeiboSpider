from functools import wraps
import time
import weibo

def importClass(classFullname):
    moduleName, className = classFullname.rsplit('.', 1)
    module = __import__(moduleName)
    return module.getattr(module, className)

def weiboAPIRetryDecorator(func):
    @wraps(func)
    def retryFunc(*args, **kw):
        try:
            return func(*args, **kw)
        except weibo.APIError, ex:
            if ex.error_code == 10022 or ex.error_code == 10023:
                interval = config.API_RETRY_INTERVAL if hasattr(config, 'API_RETRY_INTERVAL') else 3600
                time.sleep(interval)
                return func(*args, **kw)
            else:
                raise ex
    return retryFunc

def assertConfig(configName):
    assert hasattr(config, configName), ('%s must be set' % configName)