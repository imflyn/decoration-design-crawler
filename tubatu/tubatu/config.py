import logging

import redis
from requests.packages.urllib3.connectionpool import log as requests_log
from selenium.webdriver.remote.remote_connection import LOGGER as selenium_log

from msic import config
from msic.core.service import mongodb_service

selenium_log.setLevel(logging.WARNING)
requests_log.setLevel(logging.WARNING)

DATABASE_NAME = "tubatu"

# MongoDB
mongodb = mongodb_service.get_db(config.mongodb_client, DATABASE_NAME)

REDIS_DATABASE_NAME = 0

# Redis
redis_client = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=REDIS_DATABASE_NAME)
