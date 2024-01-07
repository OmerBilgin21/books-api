from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from src.config import (
    get_envs,
    oauth2_scheme,
    pwd_context,
)
from src.db import get_user as get_user_from_db
from src.schemas import TokenData, UserInDB

SECRET_KEY = get_envs()["secret_key"]
ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> Any:
    """
    Verify the plain password against the hashed password using the CryptContext.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        Any: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> Any:
    """
    Hash the given password using the CryptContext.

    Args:
        password (str): The password to be hashed.

    Returns:
        Any: The hashed password.
    """
    return pwd_context.hash(password)


async def get_user(username: str) -> UserInDB:
    """
    Retrieve a user from the given database by username.

    Args:
        username (str): The username of the user.

    Returns:
        Any: UserInDB object if found, raises HTTPException otherwise.
    """
    user_from_db = await get_user_from_db(username=username)
    if user_from_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user_from_db


async def authenticate_user(username: str, password: str) -> Any:
    """
    Authenticate a user by verifying the provided username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        Any: UserInDB object if authentication is successful, False otherwise.
    """
    user = await get_user(username=username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> Any:
    """
    Create an access token using the provided data and optional expiration delta.

    Args:
        data (dict): The data to be encoded in the token.
        expires_delta (timedelta | None): Optional expiration delta.

    Returns:
        Any: The generated access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """
    Get the current user based on the provided access token.

    Args:
        token (str): The access token.

    Returns:
        Any: The current user if authentication is successful.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception  # noqa: B904
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
