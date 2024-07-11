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
	return current_user
