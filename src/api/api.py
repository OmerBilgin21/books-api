from fastapi import APIRouter

from src.endpoints import book_lists, books, login, users

api_router = APIRouter()

api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(login.router, prefix="", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(book_lists.router, prefix="/lists", tags=["lists"])
