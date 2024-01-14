from pydantic import BaseModel

from .out import Out


class User(Out):
    username: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class UserInDB(User):
    hashed_password: str


class UserCreate(User):
    password: str
