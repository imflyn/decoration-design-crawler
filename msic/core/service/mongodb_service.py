from pymongo import MongoClient, errors
from pymongo.database import Database
from pymongo.collection import Collection

MAX_POOL_SIZE = 5


def get_client(host: str, port: int) -> MongoClient:
	try:
		client = MongoClient(host, port, maxPoolSize=MAX_POOL_SIZE)
		print("Connected successfully!!!")
		return client
	except errors.ConnectionFailure as e:
		print("Could not connect to MongoDB: %s" % e)


def get_db(client: MongoClient, db_name: str) -> Database:
	db = Database(client, db_name)
	return db


def get_collection(db: Database, name: str) -> Collection:
	collection = Collection(db, name)
	return collection


def insert(collection: Collection, data):
	collection.insert_one(data)


if __name__ == '__main__':
	mongo_client = get_client(MongoClient.HOST, MongoClient.PORT)
	db = get_db(mongo_client, "test")
	collection = get_collection(db, "test1")
	insert(collection, {"test": "helloworld"})
