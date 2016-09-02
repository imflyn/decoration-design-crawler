from msic.core.service import mongodb_service

SECTION_DATABASE = "database"
MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 27017

DATABASE_NAME = "tubatu"

mongodb_client = mongodb_service.get_client(MONGODB_HOST, MONGODB_PORT)
mongodb = mongodb_service.get_db(mongodb_client, DATABASE_NAME)
