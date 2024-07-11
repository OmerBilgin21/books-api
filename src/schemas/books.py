from pydantic import BaseModel

from .out import Out


class SearchQueryString(BaseModel):
	title: str | None = None
	author: str | None = None
	series: str | None = None
	book_type: str | None = None  # fiction, nonfiction
	categories: list[str] | None = None  # semicolon separated list of categories
	lexile_min: int = -650  # -650 to 2150
	lexile_max: int = 2150  # -650 to 2150
	results_per_page: int = 25  # 1 to 100
	page: int = 1  # page of the result


class Book(BaseModel):
	page_count: int | None
	title: str | None
	cover: str | None
	author: str | None
	genres: list[str] | None
	# TODO(@omer): add buy_url to this schema
	plot: str | None


class BookOut(Out, Book):
	pass
