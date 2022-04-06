from flask import (
    Blueprint,
    abort,
    current_app,
    g,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import models
from models import User
from utils import define_current_user

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.before_request
def before_request():
    define_current_user()


@bp.route("/", methods=["GET"])
def users():
    """
    Display a list of all users
    :return: A list of objects of the User class.
    """
    if not g.user:
        error = "Please log in to continue."
        return render_template("denied.html", error=error)

    users_list = current_app.session.query(User).all()

    return render_template("users.html", users_list=users_list)


@bp.route("/delete", methods=["DELETE"])
def delete_user():
    """
    Delete a user from the database
    :return: A 204 No Content response.
    """
    if not g.user or not g.user.is_admin:
        abort(401)

    user_id = request.json.get("id")

    if not current_app.session.query(User).filter_by(id=user_id).first():
        return make_response(jsonify("User not found."), 404)

    current_app.session.query(User).filter_by(id=user_id).delete()
    current_app.session.commit()

    return make_response("", 204)


@bp.route("/add/", methods=["GET", "POST"])
def add_user():
    """
    Create a new user
    :return: Redirect to the users page.
    """
    if not g.user:
        error = "Please log in to continue."
        return render_template("denied.html", error=error)
    elif not g.user.is_admin:
        error = "Sorry. You are not admin user."
        return render_template("denied.html", error=error)

    if request.method == "GET":
        return render_template("edit.html", error=None)
    elif request.method == "POST":
        if not request.form.get("username"):
            error = f"Invalid username!"
            return render_template("edit.html", user=None, error=error)

        existing_user = current_app.session.query(User).filter_by(username=request.form.get("username")).first()
        if existing_user:
            error = f"Username '{request.form.get('username')}' already exists."
            return render_template("edit.html", user=None, error=error)

        username = request.form.get("username")
        password = request.form.get("password")
        is_admin = request.form.get("is_admin")

        new_user = models.User(username=username, password=password, is_admin=bool(is_admin))
        current_app.session.add(new_user)
        current_app.session.commit()

        return redirect(url_for("users.users"))


@bp.route("/edit/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    """
    Edit a user

    :param user_id: The id of the user to edit
    :return: Redirect to the users page.
    """
    if not g.user:
        error = "Please log in to continue."
        return render_template("denied.html", error=error)
    elif not g.user.is_admin:
        error = "Sorry. You are not admin user."
        return render_template("denied.html", error=error)

    if request.method == "GET":
        user = current_app.session.query(User).filter_by(id=user_id).first()
        if user:
            return render_template("edit.html", user=user, error=None)
        else:
            error = "Something went wrong. Current user is unavailable."
            return render_template("edit.html", user=user, error=error)
    elif request.method == "POST":
        user_by_username = current_app.session.query(User).filter_by(username=request.form.get("username")).first()
        editable_user = current_app.session.query(User).filter_by(id=user_id).first()

        if not editable_user:
            error = f"User with username '{request.form.get('username')}' does not exist."
            return render_template("edit.html", user=editable_user, error=error)

        if user_by_username and user_by_username != editable_user:
            error = f"Username '{request.form.get('username')}' already exists."
            return render_template("edit.html", user=editable_user, error=error)

        if editable_user.username == session["username"]:
            session["username"] = request.form.get("username")

        editable_user.username = request.form.get("username")
        editable_user.password = request.form.get("password")
        editable_user.is_admin = bool(request.form.get("is_admin"))

        current_app.session.flush()
        current_app.session.commit()

        return redirect(url_for("users.users"))
