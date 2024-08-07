# api
import uvicorn

# local
from app import app
from src.config.config import get_envs

if __name__ == "__main__":
	env = get_envs()["env"]
	if env == "dev":
		print("hot reloading")
		uvicorn.run(
			"main:app",
			host="0.0.0.0",
			port=8000,
			reload=True,
			log_level="info",
		)
	else:
		uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
