import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


def get_envs() -> dict[str, str]:
    """Get the environment variables.

    This function retrieves the environment
    variables based on the value of the "ENV" variable.

    If the "ENV" variable is set to "dev",
    it loads the local environment variables from the ".env.local" file.

    Returns
        dict: A dictionary containing the current environment.
            The "env" key holds the value of the "ENV" variable.
    """
    if os.environ["ENV"] == "DEV":
        load_dotenv(dotenv_path=".env.local")
    return {
        "env": os.environ["ENV"],
        "secret_key": os.environ["SECRET_KEY"],
        "user_secret": os.environ["USER_SECRET"],
        "pass_secret": os.environ["PASS_SECRET"],
        "rapid_api_key": os.environ["BOOKS_API_KEY"],
        "rapid_api_host": os.environ["BOOKS_API_HOST"],
        "book_finder_key": os.environ["BOOK_FINDER_KEY"],
        "book_finder_host": os.environ["BOOK_FINDER_HOST"],
    }


ACCESS_TOKEN_EXPIRE_MINUTES = 1 * 60 * 24  # 1 day

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

BOOKS_API_EXTERNAL_BASE = "https://books-api7.p.rapidapi.com/books/"
BOOK_FINDER_EXTERNAL = "https://book-finder1.p.rapidapi.com/api/search"

POSSIBLE_SEARCH_CATEGORIES = [
    "Animals, Bugs & Pets",
    "Art, Creativity & Music",
    "General Literature",
    "Hobbies, Sports & Outdoors",
    "Science Fiction & Fantasy",
    "Real Life",
    "Science & Technology",
    "Mystery & Suspense",
    "Reference",
]

POSSIBLE_GENRES = [
    "Classics",
    "Historical",
    "Literature",
    "Historical fiction",
    "Fiction",
    "Fantasy",
    "19th Century",
    "Christmas",
]
