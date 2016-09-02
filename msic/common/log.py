import logging

logger = logging.getLogger()
fh = logging.FileHandler('../error.log')
fh.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s /n')
fh.setFormatter(formatter)

logger.addHandler(fh)


def warn(msg):
	logger.warning(msg)


def info(msg):
	logger.info(msg)


def debug(msg):
	logger.debug(msg)


def error(e: Exception):
	logger.error("Exception %s" % e)
