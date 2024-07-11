from src.schemas import Book


def change_books_structure(source: str, books: list[dict]) -> list[Book] | None:
	"""Change the structure of the books from different sources to the preferred structure.

	Args:
		source (str): _description_
		books (list[dict]): _description_

	Returns:
		list[Book]: new list of books of preferred structure. Defaults to empty list.
	"""  # noqa: E501
	if source == "from-finder":
		return [
			{
				"page_count": int(book["page_count"])
				if isinstance(book["page_count"], str)
				else book["page_count"],
				"author": book["authors"][0],
				"title": book["title"],
				"cover": book["published_works"][0]["cover_art_url"],
				"genres": [
					item.strip() if isinstance(item, str) else item
					for sublist in book["categories"]
					for item in (sublist.split(",") if "," in sublist else [sublist])
				]
				+ book["subcategories"],
				"plot": book["summary"],
			}
			for book in books
		]
	if source == "from-fetcher":
		return [
			{
				"page_count": book["pages"],
				"author": book["author"]["first_name"]
				+ " "
				+ book["author"]["last_name"],
				"title": book["title"],
				"cover": book["cover"],
				"genres": book["genres"],
				"plot": book["plot"],
			}
			for book in books
		]
	return None
