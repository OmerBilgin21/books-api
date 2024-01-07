# fastapi
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# config
from src.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

# schemas
from src.schemas import Token, UserCreate

# utils
from src.utils import (
    authenticate_user,
    create_access_token,
    create_user,
)

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict[str, str]:
    """
    Endpoint to obtain an access token by providing a valid username and password.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing username and password.

    Returns:
        Any: The access token and token type.
    """  # noqa: E501
    user = await authenticate_user(
        username=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", response_model=dict)
async def signup(
    user: UserCreate = None,
) -> dict[str, str]:
    """_summary_

    Args:
        user (dict): _description_. Defaults to None.

    Raises:
        HTTPException: _description_

    Returns:
        dict[str, str]: _description_
    """
    if not user or user.username is None or user.password is None or user.email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    res = await create_user(user=user)
    if res is None:
        return {"message": "User creation failed"}

    return {"message": "User created successfully"}
