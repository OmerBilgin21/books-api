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
	env = os.environ.get("ENV", "dev")
	if env == "dev":
		load_dotenv(dotenv_path=".env.local")
	return {
		"env": env,
		"secret_key": os.environ.get("SECRET_KEY", "default-secret-key"),
		"db_connection_str": os.environ.get("DB_CONNECTION_STR", "localhost"),
		"db_source": os.environ.get("DB_SOURCE", "LOCAL"),
	}


ACCESS_TOKEN_EXPIRE_MINUTES = 1 * 60 * 24  # 1 day
GOOGLE_API_BASE_URL = "https://www.googleapis.com/books/v1"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

COLLECTION_NAMES = {
	"book_lists": "bookLists",
	"users": "users",
}
