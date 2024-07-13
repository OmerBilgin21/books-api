from fastapi import APIRouter

from src.schemas import Book

router = APIRouter()


@router.get("", response_model=list[Book] | None)
async def get_books() -> list[Book] | None:
	"""
	Retrieves a list of books.

	Returns
		dict: A dictionary containing the book data.
	"""
	return []
