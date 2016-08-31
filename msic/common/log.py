import logging

logger = logging.getLogger()


def warn(msg):
	logger.warning(msg)


def info(msg):
	logger.info(msg)


def debug(msg):
	logger.debug(msg)


def error(msg):
	logger.error(msg)
