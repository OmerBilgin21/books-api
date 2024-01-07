from fastapi import APIRouter

from src.utils import fetch_external_books

router = APIRouter()


@router.get("")
async def get_books() -> dict:
    """
    Retrieves a list of books.

    Returns
        dict: A dictionary containing the book data.
    """
    res = fetch_external_books(extra_url="find/genres")
    print(f"{len(res)} books found.")
    return {"data": res}
