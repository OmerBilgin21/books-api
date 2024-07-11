from motor.motor_asyncio import AsyncIOMotorCollection

from src.schemas import UserInDB

from .get_db import get_db


async def get_collection(collection_name: str) -> AsyncIOMotorCollection:
	"""Get the database collection.

	Args:
		collection_name (str): The name of the collection.

	Returns:
		AsyncIOMotorCollection: The collection.
	"""
	db = get_db()
	return db[collection_name]


async def get_all(collection_name: str) -> list[dict[str, str]]:
	"""Get all documents from a collection.

	Args:
		collection_name (str): The name of the collection.

	Returns:
		list: A list of documents.
	"""
	collection = await get_collection(collection_name)
	return [doc async for doc in collection.find({})]


async def get_user(username: str) -> UserInDB:
	"""Get a document from a collection by id.

	Args:
		collection_name (str): The name of the collection.
		username (str): User's username.

	Returns:
		dict: The document.
	"""
	collection = await get_collection("users")
	return await collection.find_one({"username": username})


async def create_one(collection_name: str, document: dict) -> dict:
	"""Create a document in a collection.

	Args:
		collection_name (str): The name of the collection.
		document (dict): The document to be created.

	Returns:
		dict: The created document.
	"""
	collection = await get_collection(collection_name)
	return await collection.insert_one(document)


async def get_one(collection_name: str, document_id: str) -> dict:
	"""Get a document from a collection by id.

	Args:
		collection_name (str): The name of the collection.
		document_id (str): The id of the document.

	Returns:
		dict: The document.
	"""
	collection = await get_collection(collection_name)
	return await collection.find_one({"_id": document_id})
