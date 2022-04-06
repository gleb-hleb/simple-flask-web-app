from flask import Blueprint, render_template

from utils import define_current_user

bp = Blueprint("home", __name__)


@bp.before_request
def before_request():
    define_current_user()


@bp.route("/", methods=["GET"])
def home():
    return render_template("home.html")
