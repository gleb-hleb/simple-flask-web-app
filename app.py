import os

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from utils import load_env
from utils import register_blueprints, seed_database

load_env()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

# Registering all the blueprints in the views folder.
register_blueprints(app)

# This is creating a connection to the database.
engine = create_engine(os.getenv("DB_URL"))

# It creates a session object that is bound to the engine object.
app.session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# It creates the database if it doesn't exist, and seed it with a base user.
seed_database(app.session, engine)

if __name__ == "__main__":
    app.run()
