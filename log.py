import logging

def setup_custom_logger(name, level):
    # %(asctime)s - 
    formatter = logging.Formatter(fmt='%(filename)s - %(funcName)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
