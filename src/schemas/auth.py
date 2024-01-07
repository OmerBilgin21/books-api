from pydantic import BaseModel


class User(BaseModel):
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
