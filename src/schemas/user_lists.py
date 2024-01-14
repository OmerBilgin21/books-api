from pydantic import BaseModel

from .oid import Oid
from .out import Out


class UserListCreate(BaseModel):
    name: str
    description: str


class UserLists(Out):
    name: str
    description: str
    books: list[Oid]
