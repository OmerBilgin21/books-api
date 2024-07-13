from typing import Any

from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import (
	BulkWriteError,
	CollectionInvalid,
	ConnectionFailure,
	InvalidDocument,
	NetworkTimeout,
	WriteError,
)

from src.config.config import COLLECTION_NAMES
from src.schemas import UserInDB

from .get_db import get_db


def handle_db_exceptions(func: Any) -> Any:
	"""Decorator for all database functions.

	Intends to improve error handling and generate more informative errors.
	"""

	def wrapper(*args: Any, **kwargs: Any) -> Any:
		try:
			return func(*args, **kwargs)
		except BulkWriteError as bwe:
			raise HTTPException(status_code=500, detail="Bulk Write Error!") from bwe
		except CollectionInvalid as cie:
			raise HTTPException(
				status_code=500,
				detail="Collection is invalid! Check collection name!",
			) from cie
		except ConnectionFailure as cfe:
			raise HTTPException(
				status_code=500,
				detail="Connection failure. Check DB_CONNECTION_STR \
				and DB_SOURCE environment variables!",
			) from cfe
		except InvalidDocument() as ide:
			raise HTTPException(status_code=500, detail="Invalid Document!") from ide
		except WriteError as we:
			raise HTTPException(
				status_code=500,
				detail="Write error. Check document!",
			) from we
		except NetworkTimeout as ne:
			raise HTTPException(
				status_code=500,
				detail="Network timeout error. Check database server health!",
			) from ne
		except Exception as e:
			raise HTTPException(status_code=500, detail="Unknown error") from e

	return wrapper


@handle_db_exceptions
async def get_collection(collection_name: str) -> AsyncIOMotorCollection:
	"""Get the database collection.

	Args:
		collection_name (str): The name of the collection.

	Returns:
		AsyncIOMotorCollection: The collection.
	"""
	db = get_db()
	return db[collection_name]


@handle_db_exceptions
async def get_all(collection_name: str) -> list[dict[str, str]]:
	"""Get all documents from a collection.

	Args:
		collection_name (str): The name of the collection.

	Returns:
		list: A list of documents.
	"""
	collection = await get_collection(collection_name)
	return [doc async for doc in collection.find({})]


@handle_db_exceptions
async def get_user(username: str) -> UserInDB:
	"""Get a document from a collection by id.

	Args:
		collection_name (str): The name of the collection.
		username (str): User's username.

	Returns:
		dict: The document.
	"""
	collection = await get_collection(COLLECTION_NAMES["users"])
	return await collection.find_one({"username": username})


@handle_db_exceptions
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


@handle_db_exceptions
async def get_one(collection_name: str, document_id: str) -> dict:
	"""Get a document from a collection by id.

	Args:
		collection_name (str): The name of the collection.
		document_id (str): The id of the document.

	Returns:
		dict: The document.
	"""
	collection = await get_collection(collection_name)
	return await collection.find_one({"_id": ObjectId(document_id)})


@handle_db_exceptions
async def find_book_lists_with_same_name(book_list_name: str) -> list[dict]:
	"""Get the book lists with the search parameter name

	Args:
		book_list_name (str): search parameter

	Returns:
		list[dict]: Book list(s) if any
	"""
	book_listc = await get_collection(COLLECTION_NAMES["book_lists"])
	return await book_listc.find({"name": book_list_name}).to_list(length=None)


@handle_db_exceptions
async def find_users_book_lists(user_id: ObjectId) -> list[dict]:
	"""Find book lists of a user

	Args:
		user_id (ObjectId): id of related user

	Returns:
		list[dict]: book list(s) if any
	"""
	book_listc = await get_collection(COLLECTION_NAMES["book_lists"])
	return await book_listc.find({"userId": user_id}).to_list(length=None)


@handle_db_exceptions
async def add_book_to_book_list(
	book_list_id: ObjectId,
	book_array: list[ObjectId],
) -> dict:
	"""Adds the given book to the given book list

	Args:
		book_list_id (ObjectId): id of related book list
		book_array (ObjectId): Updated "books" array of the given book list

	Returns:
		dict: Updated book list
	"""
	book_listc = await get_collection(COLLECTION_NAMES["book_lists"])
	return await book_listc.find_one_and_update(
		{"_id": ObjectId(book_list_id)},
		{"$set": {"books": book_array}},
	)
