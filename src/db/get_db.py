from motor.motor_asyncio import AsyncIOMotorClient

from src.config import get_envs


def get_db() -> AsyncIOMotorClient:
	"""Get the database client.

	Returns
		MongoClient: The database client.
	"""
	envs = get_envs()
	client = AsyncIOMotorClient(host=envs["db_connection_str"], post=27017)
	return client["books-db"]
