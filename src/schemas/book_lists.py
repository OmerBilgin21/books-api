from pydantic import BaseModel

from .oid import Oid
from .out import Out


class BookListCreate(BaseModel):
	name: str
	description: str


class BookList(BookListCreate):
	books: list[Oid | None]
	userId: Oid


class BookListOut(BookList, Out):
	pass
