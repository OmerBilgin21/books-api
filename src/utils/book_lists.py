from bson import ObjectId

from src.config.config import COLLECTION_NAMES
from src.db.crud import create_one, find_book_lists_with_same_name, get_one
from src.schemas import BookList, BookListCreate, BookListOut


async def create_book_list(
	book_list: BookListCreate,
	user_id: ObjectId,
) -> BookListOut | bool:
	"""Creates book list and returns it

	Args:
		book_list (BookList): Incoming book list
		user_id (ObjectId): id of related user

	Returns:
		BookList: Created book list
	"""
	new_book_list = prepare_book_list_create(
		book_list=book_list,
		user_id=user_id,
	)

	if not isinstance(new_book_list["name"], str) or new_book_list["name"] == "":
		return False

	book_lists_with_same_name = await find_book_lists_with_same_name(
		new_book_list["name"],
	)
	if (
		isinstance(book_lists_with_same_name, list)
		and len(book_lists_with_same_name) > 0
	):
		return False

	created_list_result = await create_one(
		collection_name=COLLECTION_NAMES["book_lists"],
		document=new_book_list,
	)

	return await get_one(
		collection_name=COLLECTION_NAMES["book_lists"],
		document_id=ObjectId(created_list_result.inserted_id),
	)


def prepare_book_list_create(book_list: BookListCreate, user_id: ObjectId) -> BookList:
	"""Prepare the book lists of a user to be inserted to db on creation

	Args:
		user_id (ObjectId): id of owner
		book_list (BookListCreate): New book list without preparation

	Returns:
		BookList: New book list
	"""
	book_list = book_list.dict()

	return {**book_list, "books": [], "userId": ObjectId(user_id)}
