### BOOKS API

##### How to run this project:

- Clone the repository
- Create a MongoDB Atlas deployment or run MongoDB locally
- Give the username and password that has read/write access to your db by passing `USER_SECRET` and `PASS_SECRET` in either docker environments or in your `.env.local` file.
- This project is using two external APIs: [Book Finder](https://rapidapi.com/dfskGT/api/book-finder1/) and [Books-API](https://rapidapi.com/akshithp111/api/books-api7) subscribe to both of them via signing up to [RAPID API](https://rapidapi.com/hub).
- Pass in the RapidAPI-Key and RapidAPI-Host for both of them as `BOOKS_API_KEY`, `BOOKS_API_HOST`, `BOOK_FINDER_KEY` AND `BOOK_FINDER_HOST`.
- Pass in a `SECRET_KEY` environment variable to be used for JWT tokens on authentication. (`SECRET_KEY` could be anything but I'd recommend a 32 bit key. It can be obtained with this command: `openssl rand -base64 32`.)

###### Next, run the commands below.

```
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export ENV=DEV
python3 main.py
```

Note: python 3.10 is recommended (author's version) but shouldn't be essential. Therefore `python3.10 -m venv venv` could be replaced with `python3 -m venv venv`.

At this point the project _should_ be running.
Hot reloading is because we exported ENV as DEV so your changes should take place in real time.
To check out the endpoints and try them: Go to http://localhost:8080/docs.
To learn more about docs and FastAPI check out their website https://fastapi.tiangolo.com/learn/

Note: To use most of the endpoints you need to have an authenticated user. One should be creatable with `/signup` endpoint.

Have fun!
