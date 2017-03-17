import logging
import sys
from os.path import dirname

SAVE_PATH = dirname(dirname(dirname(__file__)))

logger = logging.getLogger()
formatter = logging.Formatter('\n%(asctime)s - %(name)s - %(levelname)s \n%(message)s')

error_handler = logging.FileHandler(SAVE_PATH + '/error.log', encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
logger.addHandler(error_handler)

warn_handler = logging.FileHandler(SAVE_PATH + '/warn.log', encoding='utf-8')
warn_handler.setLevel(logging.WARNING)
warn_handler.setFormatter(formatter)
logger.addHandler(warn_handler)


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
