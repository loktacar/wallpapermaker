import logging

def setup_custom_logger(name, level):
    # %(asctime)s - 
    formatter = logging.Formatter(fmt='  %(asctime)s - %(thread)d - %(pathname)s:%(lineno)d - %(funcName)s()\n%(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

