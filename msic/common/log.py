import logging, sys

logger = logging.getLogger()
fh = logging.FileHandler('../error.log')
fh.setLevel(logging.ERROR)
formatter = logging.Formatter('\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)


def handle_exception(exc_type, exc_value, exc_traceback):
	if issubclass(exc_type, KeyboardInterrupt):
		sys.__excepthook__(exc_type, exc_value, exc_traceback)
		return
	logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


def warn(msg):
	logger.warning(msg)


def info(msg):
	logger.info(msg)


def debug(msg):
	logger.debug(msg)


def error(e: Exception):
	logger.error("Exception %s" % e)
