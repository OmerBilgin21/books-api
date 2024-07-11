from typing import Any

import requests

from src.config import BOOKS_API_EXTERNAL_BASE, POSSIBLE_GENRES, get_envs

from .prepare_book_save import change_books_structure


def fetch_external_books(
	genres: list[str] | None = None,
	extra_url: str = "get/random/",
) -> Any:
	"""_summary_

	Args:
	    genres (list[str]): _description_
	    extra_url (str, optional): _description_. Defaults to "get/random/".

	Returns:
	    Any: _description_
	"""
	# there's no option to get random books from a genre
	# because it's the default behaviour anyway
	if genres and extra_url == "get/random/":
		return None

	url = BOOKS_API_EXTERNAL_BASE + extra_url
	envs = get_envs()
	rapid_api_key = envs["rapid_api_key"]
	rapid_api_host = envs["rapid_api_host"]
	headers = {
		"X-RapidAPI-Key": "{rapid_api_key}".format(rapid_api_key=rapid_api_key),
		"X-RapidAPI-Host": "{rapid_api_host}".format(rapid_api_host=rapid_api_host),
	}

	querystring = {
		"genres[]": [
			# because this gives the classics of any genre
			# which is desired behaviour
			"Classics",
		],
	}

	if genres and isinstance(genres, list):
		querystring["genres[]"] = [x for x in genres if x in POSSIBLE_GENRES]
	found = requests.get(url, headers=headers, params=querystring, timeout=10).json()

	if found and len(found) > 0:
		return (
			change_books_structure("from-fetcher", found)
			if isinstance(found, list)
			else change_books_structure("from-fetcher", [found])
		)
	return None
