from motor.motor_asyncio import AsyncIOMotorClient

from src.config import get_envs


def get_db() -> AsyncIOMotorClient:
	"""Get the database client.

	Returns
		MongoClient: The database client.
	"""
	envs = get_envs()
	username = envs["user_secret"]
	password = envs["pass_secret"]
	connection_url = "mongodb+srv://{username}:{password}@books-api-db.uictcty.mongodb.net/?retryWrites=true&w=majority".format(
		username=username,
		password=password,
	)
	client = AsyncIOMotorClient(connection_url)
	return client["books-db"]
