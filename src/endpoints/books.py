# types
from typing import Literal

from bson import ObjectId

# external
from fastapi import APIRouter, Depends, HTTPException

# internal
from src.config.config import COLLECTION_NAMES
from src.db.crud import add_book_to_book_list, create_one, get_one
from src.schemas import Book, BookInDb, BookListOut, UserInDB
from src.utils import fetch_book_volumes, get_current_user

router = APIRouter()


@router.get("/search", response_model=list[Book | None])
async def search_book(
	search_category: Literal[
		"title",
		"author",
		"publisher",
		"subject",
		"free",
	],
	search_param: str,
) -> list[Book]:
	"""
	Retrieves a list of books.

	Returns
		dict: A dictionary containing the book data.
	"""
	return await fetch_book_volumes(
		search_category=search_category,
		search_params=search_param,
	)


@router.post("/{book_list_id}/add-book")
async def add_book_to_list(
	book_list_id: str,
	book: BookInDb,
	current_user: UserInDB = Depends(get_current_user),
) -> BookListOut:
	"""Adds a book to given book list

	Args:
		book_list_id (str): Id of related book list
		book (BookInDb): Book to add
		current_user (UserInDB, optional): Authenticated user.
			Defaults to Depends(get_current_user).

	Raises:
		HTTPException: 400 if book list id is invalid

	Returns:
		BookListOut: Book list after the addition if successful
	"""
	if ObjectId.is_valid(ObjectId(book_list_id)) is False:
		raise HTTPException(status_code=400, detail="Invalid book list id!")

	book_list = await get_one(
		collection_name=COLLECTION_NAMES["book_lists"],
		document_id=ObjectId(book_list_id),
	)

	if book_list is None:
		raise HTTPException(status_code=404, detail="Book list not found!")

	if hasattr(book_list, "userId") and book_list["userId"] != str(current_user.id):
		raise HTTPException(
			status_code=400,
			detail="Book list doesn't belong to this user.",
		)

	book_add_result = await create_one(
		collection_name=COLLECTION_NAMES["books"],
		document=book.dict(),
	)
	book_add_result = book_add_result.inserted_id
	added_book = await get_one(
		collection_name=COLLECTION_NAMES["books"],
		document_id=book_add_result,
	)
	if added_book is None:
		raise HTTPException(status_code=500, detail="Book addition failed!")

	book_list["books"].append(added_book["_id"])

	return await add_book_to_book_list(
		book_array=book_list["books"],
		book_list_id=book_list["_id"],
	)
