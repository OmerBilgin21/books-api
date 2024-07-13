from typing import Any

from pydantic import BaseModel, HttpUrl

from .out import Out


class Book(BaseModel):
	etag: str | None = None
	selfLink: HttpUrl | None = None
	volumeInfo: Any | None = None
	saleInfo: Any | None = None
	accessInfo: Any | None = None
	searchInfo: Any | None = None
	googleId: str


class BookInDb(BaseModel):
	title: str
	categories: list[str]
	googleId: str
	author: list[str]
	publisher: str
	subject: str
	nsfw: bool


class BookInDbOut(BookInDb, Out):
	pass


class BookOut(Book, Out):
	pass
