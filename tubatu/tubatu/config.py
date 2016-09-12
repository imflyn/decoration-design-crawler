import logging

import redis
from requests.packages.urllib3.connectionpool import log as requests_log
from selenium.webdriver.remote.remote_connection import LOGGER as selenium_log

from msic.core.service import mongodb_service

selenium_log.setLevel(logging.WARNING)
requests_log.setLevel(logging.WARNING)

SECTION_DATABASE = "database"
MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 27017

DATABASE_NAME = "tubatu"

mongodb_client = mongodb_service.get_client(MONGODB_HOST, MONGODB_PORT)
mongodb = mongodb_service.get_db(mongodb_client, DATABASE_NAME)

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

REDIS_DATABASE_NAME = 0

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE_NAME)
