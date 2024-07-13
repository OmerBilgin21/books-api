from pydantic import BaseModel

from .out import Out


class User(BaseModel):
	username: str
	email: str
	allow_nsfw: bool = False


class Token(BaseModel):
	access_token: str
	token_type: str


class TokenData(BaseModel):
	username: str = None


class UserInDB(User):
	hashed_password: str


class UserOut(User, Out):
	pass


class UserCreate(User):
	password: str
