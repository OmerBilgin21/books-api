from requests import request

from src.config.config import (
	GOOGLE_API_BASE_URL,
	POSSIBLE_SEARCH_PARAMETERS,
	get_envs,
)
from src.schemas import Book


async def fetch_book_volumes(
	search_params: dict | None,
	search_category: str | None,
) -> list[Book]:
	"""Fetches data from Google Books API

	Args:
		search_params (dict | None): Parameter to search
		search_category (str | None): Attribute to search in
			Important: if no spesific attribute is intended to be searched,
			send the search_category as "free"

	Returns:
		list: List of found/fetched books
	"""
	request_url = GOOGLE_API_BASE_URL + "/volumes"
	api_key = get_envs()["google_api_key"]

	if isinstance(search_params, str) and isinstance(search_category, str):
		if search_category not in POSSIBLE_SEARCH_PARAMETERS:
			return None
		request_url = request_url + "?q="
		if search_category == "free":
			request_url = request_url + search_params
		else:
			request_url = request_url + f"{search_params}+{search_category}:keyes"

	request_url = request_url + f"&key={api_key}"

	fetched_books = request(
		method="GET",
		# url=request_url,
		url=request_url,
		timeout=10000,
	)
	fetched_books = fetched_books.json()

	# TODO(OmerBilgin21): volumeInfo and categories will be used to generate suggestions
	# and maturityRating to avoid legal trouble

	if hasattr(fetched_books, "items") and fetched_books["totalItems"] > 0:
		for book in fetched_books["items"]:
			book["googleId"] = book["id"]
			del book["kind"]
			del book["id"]
		return fetched_books["items"]

	return []
