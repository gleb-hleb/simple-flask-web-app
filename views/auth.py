import sqlalchemy
from flask import Blueprint, current_app, make_response, redirect, render_template, request, session, url_for

from models import User
from utils import clear_user_session, fill_user_session

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/", methods=["GET", "POST"])
def login():
    """
    If the user is successfully logged in, redirect to the users page.
    If the user is not logged in, check if the username and password are valid.
    If they are, fill the user session and redirect to the users page.
    If they are not, display an error message
    :return: A response object.
    """
    error = None

    if request.method == "POST":
        clear_user_session(session)

        username = request.form.get("username")
        password = request.form.get("password")

        try:
            user = current_app.session.query(User).filter_by(username=username).first()
        except sqlalchemy.exc.OperationalError:
            error = "Something went wrong. Please try again later."
            return render_template("login.html", error=error)

        if not user or user.password != password:
            error = "Invalid Credentials. Please try again."
        else:
            fill_user_session(session, {"id": user.id, "username": user.username, "is_admin": user.is_admin})
            return redirect(url_for("users.users"))

    return render_template("login.html", error=error)


@bp.route("/logout", methods=["GET"])
def logout():
    """
    It clears the user session and redirects the user to the home page
    :return: A redirect to the home page.
    """
    clear_user_session(session)

    return redirect(url_for("home.home"))
