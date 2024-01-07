from fastapi import APIRouter, Depends

from src.schemas import User, UserInDB
from src.utils import get_current_user

router = APIRouter()


@router.get("/me", response_model=User)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)) -> User:
    """
    Endpoint to get information about the currently authenticated user.

    Args:
        current_user (UserInDB): The current authenticated user.

    Returns:
        Any: UserInDB information.
    """
    return User(**current_user)


@router.get("/items")
async def read_own_items(current_user: UserInDB = Depends(get_current_user)) -> list:
    """
    Endpoint to retrieve items owned by the currently authenticated user.

    Args:
        current_user (UserInDB): The current authenticated user.

    Returns:
        Any: List of items owned by the user.
    """
    return [{"item_id": "Foo", "owner": current_user["username"]}]
