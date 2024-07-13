from fastapi import APIRouter, Depends, HTTPException

from src.db.crud import find_users_book_lists
from src.schemas import BookListCreate, BookListOut, UserInDB
from src.utils import create_book_list, get_current_user

router = APIRouter()


@router.post("", response_model=BookListOut)
async def new_book_list(
	book_list: BookListCreate,
	current_user: UserInDB = Depends(get_current_user),
) -> BookListOut:
	"""Create a new book list for current user

	Args:
		book_list (BookListCreate): Incoming data for book list to create
		current_user (UserInDB): Authenticated user

	Returns:
		BookListOut: Created book lists
	"""
	created_book_list = await create_book_list(
		book_list=book_list,
		user_id=current_user.id,
	)
	if created_book_list is False:
		raise HTTPException(
			status_code=400,
			detail="Invalid name or a list with the same name already exists!",
		)
	return created_book_list


@router.get("", response_model=list[BookListOut])
async def get_my_book_lists(
	current_user: UserInDB = Depends(get_current_user),
) -> list[BookListOut]:
	"""Get book lists of a user

	Returns:
		list[BookListOut]: List of book lists of current user
	"""
	return await find_users_book_lists(user_id=current_user.id)
