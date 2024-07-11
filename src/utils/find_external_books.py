from typing import Any

import requests

from src.config import BOOK_FINDER_EXTERNAL, POSSIBLE_SEARCH_CATEGORIES, get_envs
from src.schemas import SearchQueryString

from .prepare_book_save import change_books_structure


def find_external_books(querystring: SearchQueryString) -> Any:
	"""_summary_

	Args:
	    querystring (SearchQueryString): _description_

	Returns:
	    Any: found book/books if any. None otherwise.
	"""
	envs = get_envs()
	book_finder_key = envs["book_finder_key"]
	book_finder_host = envs["book_finder_host"]
	headers = {
		"X-RapidAPI-Key": "{book_finder_key}".format(book_finder_key=book_finder_key),
		"X-RapidAPI-Host": "{book_finder_host}".format(
			book_finder_host=book_finder_host,
		),
	}

	if querystring.categories and isinstance(querystring.categories, list):
		querystring.categories = [
			x for x in querystring.categories if x in POSSIBLE_SEARCH_CATEGORIES
		]

	found = requests.get(
		url=BOOK_FINDER_EXTERNAL,
		headers=headers,
		params=querystring,
		timeout=10,
	).json()

	if not found or "total_results" not in found or found["total_results"] == 0:
		return None

	return change_books_structure("from-finder", found["results"])
