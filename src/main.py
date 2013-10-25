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

import persistence
import weibospider

if __name__ == '__main__':
    logger = logging.createLogger(config)
    logger.info('Spider start')
    weiboProvider = weibospider.createWeiboProvider()
    persistence = persistence.createRedisPersistence()
    for weibo in weiboProvider.getWeibos():
        persistence.addWeibo(weibo)
    logger.info('Spider End')