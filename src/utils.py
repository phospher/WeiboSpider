from functools import wraps

def importClass(classFullname):
    moduleName, className = classFullname.rsplit('.', 1)
    module=__import__(moduleName)
    return module.getattr(module, className)

def weiboAPIRetryDecorator(func):
    @wraps(func)
    def retryFunc(*args, **kw):
        try:
            return func(*args, **kw)
        except ex:
            interval = config.API_RETRY_INTERVAL if hasattr(config, 'API_RETRY_INTERVAL') else 3600
            time.sleep(interval)
            return func(*args, **kw)
    return retryFunc