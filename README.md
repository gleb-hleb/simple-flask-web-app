# Simple flask web application

This repo demonstrates simple Flask app with user authentication, database
interactions and async requests API.

### Project required stack

- Python 3.7+
- Flask / FastAPI
- PostgreSQL
- SQLAlchemy/Asyncpg
- asyncio

### How to run?

All dependencies stored in `requirements.txt`. Install dependencies by entering
its folder and typing:

```shell
$ python pip install -r requirements.txt
```

Also, we need to create `.env` file with environment variables like this:

```dotenv
DB_URL=postgresql://username:password@host:port/db
SECRET_KEY=PASTE_HERE_SECRET_KEY
```

After installing all dependencies and adding environment variables, run the app by
entering its folder and typing:

```shell
$ python app.py
```

By default, application will run at `http://127.0.0.1:5000`

At first launch application will seed database with base data.

Base user login credentials:

- username: `Admin`
- password: `admin`

---

### API reference

The app has the following routes:

1. `/` serves up the *home.html* file
2. `/auth`
    - `GET` serves up the *login.html* file
    - `POST` logs a user in and generates a session
3. `/auth/logout` logs a user out
4. `/users` serves up the *users.html* file
5. `/users/delete` delete a user
6. `/users/add`
    - `GET` serves up the *edit.html* file
    - `POST` create a new user
7. `/edit/<user_id>`
    - `GET` serves up the *edit.html* file with preloaded user data form
    - `POST` edit a user
8. `/load/source/<source_id>` load data from source file by *source_id*
9. `/load/all` load all data from source files *asynchronously*

