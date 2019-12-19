import logging

# logger = logging.getLogger("amazon_slackwatch_events")
# logging.basicConfig(format="%(module)s:%(levelname)s:%(message)s", level=logging.DEBUG)
# logger.setLevel(logging.DEBUG)


def getLogger(mod_name):
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
