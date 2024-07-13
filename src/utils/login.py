from typing import Any

from src.config.config import COLLECTION_NAMES
from src.db.crud import create_one
from src.schemas import UserCreate

from .security import get_password_hash


async def create_user(user: UserCreate) -> Any:
	"""_summary_

	Args:
		user (UserCreate): _description_

	Returns:
		_type_: _description_
	"""
	new_user = {
		"username": user.username,
		"hashed_password": get_password_hash(user.password),
		"email": user.email,
	}
	return await create_one(COLLECTION_NAMES["users"], new_user)
