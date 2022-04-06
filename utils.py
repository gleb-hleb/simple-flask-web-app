import os
from importlib import import_module

import sqlalchemy
from flask import Flask, current_app, g, session

import models
from db import Base

# Getting project root path.
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


def register_blueprints(flask_app: Flask, path: str = "views") -> None:
    """
    For each Python file in the views directory, import the python file and register the blueprint

    :param flask_app: The Flask application object
    :type flask_app: Flask
    :param path: The path to the views folder, defaults to views
    :type path: str (optional)
    """
    files = [file for file in os.listdir(path) if os.path.splitext(file)[1] == ".py"]
    modules = list(map(lambda file: f"{path}.{os.path.splitext(file)[0]}", files))

    for module in modules:
        flask_app.register_blueprint(import_module(module).bp)


def seed_database(s, en) -> None:
    """
    Create the database if it doesn't exist, and seed it with a base user

    :param s: The Session object
    :param en: The engine object
    """
    try:
        if not sqlalchemy.inspect(en).has_table("users"):
            Base.metadata.create_all(bind=en)
            base_user = models.User(username="Admin", password="admin", is_admin=True)
            # Raw SQL example
            # s.execute(
            #     f"INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :is_admin) ",
            #     {"username": "Admin", "password": "admin", "is_admin": True},
            # )
            s.add(base_user)
            s.commit()
    except sqlalchemy.exc.OperationalError as err:
        print(f"Failed to seed database:\n{err}")


def define_current_user() -> None:
    """
    It defines the current user in session.
    """
    g.user = None

    try:
        if "id" in session:
            user = current_app.session.query(models.User).filter_by(id=session["id"]).first()
            g.user = user
    except sqlalchemy.exc.OperationalError:
        return


def clear_user_session(s) -> None:
    """
    Clear current user session data.

    :param s: The session object
    """
    s.pop("id", None)
    s.pop("username", None)
    s.pop("is_admin", None)


def fill_user_session(s, data) -> None:
    """
    Fill current user session with data

    :param s: The session object
    :param data: A dictionary of data to store in the session
    """
    for key, value in data.items():
        s[key] = value


def load_env(path: str = ".env") -> None:
    """
    Loads the environment variables from a .env file

    :param path: str = ".env", defaults to .env
    :type path: str (optional)
    """
    with open(path, "r") as f:
        env_dict = dict(tuple(line.replace("\n", "").split("=")) for line in f.readlines() if not line.startswith("#"))
        os.environ.update(env_dict)
