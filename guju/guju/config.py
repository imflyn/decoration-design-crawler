import logging

from requests.packages.urllib3.connectionpool import log as requests_log
from selenium.webdriver.remote.remote_connection import LOGGER as selenium_log

from msic import config
from msic.core.service import mongodb_service

selenium_log.setLevel(logging.WARNING)
requests_log.setLevel(logging.WARNING)

DATABASE_NAME = "guju"

# MongoDB
mongodb = mongodb_service.get_db(config.mongodb_client, DATABASE_NAME)

IMAGES_STORE = 'D:/scrapy'

USE_PROXY = False
