from motor.motor_asyncio import AsyncIOMotorClient

from src.config.config import get_envs


def get_db() -> AsyncIOMotorClient:
	"""Get the database client.

	Returns
		MongoClient: The database client.
	"""
	envs = get_envs()
	if envs["db_source"] == "LOCAL":
		client = AsyncIOMotorClient(host=envs["db_connection_str"], port=27017)
	else:
		client = AsyncIOMotorClient(host=envs["db_connection_str"])
	return client["books-db"]
