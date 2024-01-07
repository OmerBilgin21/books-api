from typing import Any

import requests

from src.config import BASE_EXT_API_URL, get_envs


def fetch_external_books(
    extra_url: str = "get/random/",
) -> Any:
    """_summary_

    Args:
        extra_url (str, optional): _description_. Defaults to "get/random/".

    Returns:
        Any: _description_
    """
    url = BASE_EXT_API_URL + extra_url
    envs = get_envs()
    rapid_api_key = envs["rapid_api_key"]
    rapid_api_host = envs["rapid_api_host"]

    querystring = {
        "genres[]": [
            "fantasy",
            "fiction",
            "Classics",
        ],
    }
    print(f"=== url === {url}")
    headers = {
        "X-RapidAPI-Key": "{rapid_api_key}".format(rapid_api_key=rapid_api_key),
        "X-RapidAPI-Host": "{rapid_api_host}".format(rapid_api_host=rapid_api_host),
    }

    return requests.get(url, headers=headers, params=querystring, timeout=10).json()
