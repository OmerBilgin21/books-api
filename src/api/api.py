from fastapi import APIRouter

from src.endpoints import books, login, user_lists, users

api_router = APIRouter()

api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(login.router, prefix="", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(user_lists.router, prefix="/lists", tags=["lists"])
