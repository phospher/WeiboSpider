import config

if __name__ == '__main__':
    
    # load logging module
    if hasattr(config, 'LOGGING'):
        logging = config.LOGGING
    else:
        import filelogging as logging
    
    
    logger = logging.createLogger()
    logger.info('Spider start')
    
