from fastapi import APIRouter, Depends

from src.schemas import UserInDB, UserLists
from src.utils import get_current_user

router = APIRouter()


@router.post("")
async def create_user_list(
    list_attr: UserLists,
    current_user: UserInDB = Depends(get_current_user),
) -> dict[str, str]:
    pass


@router.get("")
async def get_user_lists(
    current_user: UserInDB = Depends(get_current_user),
) -> list[dict]:
    return [{}]
