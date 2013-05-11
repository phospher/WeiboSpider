import config
import utils
import sys
import os

sys.path.append(os.path.split(os.path.realpath(__file__))[0])

# Load logging module
if hasattr(config, 'LOGGING'):
    logging = __import__(config.LOGGING)
else:
    import filelogging as logging

# Load WeiboIterator
if hasattr(config, 'WEIBO_PROVIDER'):
    WeiboProvider = utils.importClass(config.WEIBO_PROVIDER)
else:
    from weibo import DefaultWeiboProvider as WeiboProvider

if __name__ == '__main__':
    logger = logging.createLogger(config)
    logger.info('Spider start')
    
