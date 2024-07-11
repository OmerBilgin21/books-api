from fastapi import APIRouter

from src.config import POSSIBLE_SEARCH_CATEGORIES
from src.schemas import Book, SearchQueryString
from src.utils import fetch_external_books, find_external_books

router = APIRouter()


@router.get("", response_model=list[Book] | None)
async def get_books() -> list[Book] | None:
	"""
	Retrieves a list of books.

	Returns
	    dict: A dictionary containing the book data.
	"""
	return fetch_external_books(extra_url="find/genres")


@router.get("/categories-to-search", response_model=list[str])
async def get_possible_categories() -> list[str]:
	"""
	Retrieves a list of categories that users can search books from.

	Returns
	    dict: A dictionary containing the book data.
	"""
	return POSSIBLE_SEARCH_CATEGORIES


@router.post("/search", response_model=list[Book] | None)
async def search_books(
	search_params: SearchQueryString,
) -> list[Book] | None:
	"""_summary_

	Args:
	    search_params (SearchQueryString): search criteria and parameters.

	Returns:
	    dict: Found book/books if any.
	"""
	return find_external_books(search_params)


@router.get("/random", response_model=list[Book] | None)
async def get_random_books() -> list[Book] | None:
	"""
	Retrieves a random book.

	Returns
	    dict: A dictionary containing the book data.
	"""
	return fetch_external_books()
