import asyncio
import json
import os
import socket
import urllib
from urllib import request

from flask import Blueprint, jsonify, make_response

from utils import ROOT_PATH

bp = Blueprint("load", __name__, url_prefix="/load")
loop = asyncio.get_event_loop()


def return_response(url):
    """
    It takes an url as an input, and returns the response as a json object

    :param url: The URL of the API endpoint
    :return: A list of dictionaries or empty list.
    """
    try:
        response = request.urlopen(url, timeout=2).read().decode("utf-8")
    except socket.timeout:
        return []
    except urllib.error.HTTPError:
        return []

    return json.loads(response)


@asyncio.coroutine
def fetch(url):
    """
    It takes a URL, runs it through a thread pool executor, and returns the response

    :param url: The URL to fetch
    :return: A coroutine object.
    """
    data = yield from loop.run_in_executor(None, lambda: return_response(url))
    return data


@bp.route("/source/<source_id>", methods=["GET"])
def get_data(source_id):
    """
    It takes a source_id as an argument,
    and returns the data associated with that source_id

    :param source_id: The id of the source we want to get data from
    :return: A JSON object with the data from the source file.
    """
    path = os.path.join(ROOT_PATH, "static", "json", f"source{source_id}.json")

    try:
        with open(path) as f:
            data = json.load(f)
    except FileNotFoundError:
        return make_response(jsonify([]), 404)

    return make_response(jsonify(data), 200)


@bp.route("/all", methods=["GET"])
def get_all_data():
    """
    It makes a bunch of calls to the API, and returns the sotred results
    :return: A list of dictionaries
    """
    calls = [fetch(f"http://127.0.0.1:5000/load/source/{i}") for i in range(1, 5)]
    done, _ = loop.run_until_complete(asyncio.wait(calls))
    # Firstly I wrote lists extraction with itertools, but in task was sad to use
    # minimum libs. So I rewrote with python native lists.
    # done = itertools.chain(*[item.result() for item in done])
    done = [item for chunk in done for item in chunk.result()]
    done = sorted(done, key=lambda x: x["id"])

    return make_response(jsonify(done), 200)
