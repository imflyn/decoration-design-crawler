from msic.core.service import mongodb_service

MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 27017

DATABASE_NAME = 'common'
mongodb_client = mongodb_service.get_client(MONGODB_HOST, MONGODB_PORT)
mongodb = mongodb_service.get_db(mongodb_client, DATABASE_NAME)

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
