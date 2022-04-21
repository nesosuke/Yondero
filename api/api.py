from os import abort

from flask import Blueprint, Flask, jsonify, request, url_for
from flask_cors import CORS
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)

from . import postgres, style

api = Flask(__name__)
CORS(api)

url_api = Blueprint('api', __name__, url_prefix='/api/v1')


@url_api.route('/', methods=['GET'])
def root() -> object:
    '''
    return available endpoints
    '''
    endpoints = [
        "/item/cite"    # POST
        "/item/{uid}",  # POST
        "/item/{uid}/download",  # POST
        "/item/{uid}/upload",  # POST
        "/item/{uid}/delete",  # POST
        "/register",
        "/login",
        "/logout",
    ]

    res = {"endpoints": endpoints}
    return jsonify(res)


@login_required
@url_api.route('/item/<uid>/download', methods=['POST'])
def download_pdf(item_id: str):
    '''
    give PDF to client
    '''

    pdffile = postgres.get_pdf(item_id)  # TODO
    if pdffile is None:
        abort(404)

    return pdffile


@login_required
@url_api.route('/item/<uid>/upload', methods=['POST'])
def upload_pdf(item_id: str):
    '''
    upload PDF to server
    '''

    pdf = request.files['pdf']
    if pdf is None:
        abort(400)

    if postgres.get_pdf(item_id) is not None:
        abort(409)

    postgres.save_pdf(item_id, pdf)

    if postgres.get_pdf(item_id) is None:
        abort(500)

    return "OK"


@url_api.route('/login', methods=['POST'])
def login():
    '''
    login
    '''
    req_body = request.get_json()
    username = req_body['username']
    password = req_body['password']

    user = postgres.get_user(username)
    if user is None:
        abort(404)

    if user.check_password(password):
        login_user(user)
        return "OK"
    else:
        abort(401)


@url_api.route('/logout', methods=['POST'])
def logout():
    '''
    logout
    '''
    logout_user()
    return "OK"


@url_api.route('/register', methods=['POST'])
def register():
    '''
    register
    '''
    req_body = request.get_json()
    username = req_body['username']
    password = req_body['password']

    user = postgres.get_user(username)
    if user is not None:
        abort(409)

    user = postgres.create_user(username, password)
    if user is None:
        abort(500)

    return "OK"


@login_required
@url_api.route('/item/<item_id>/delete', methods=['POST'])
def delete_item(item_id: str):
    '''
    delete item
    '''
    if postgres.get_item(item_id) is None:
        abort(404)

    if postgres.delete_item(item_id) is None:
        abort(500)

    return "OK"


@login_required
@url_api.route('/item/cite', methods=['POST'])
def cite_item():
    '''
    cite item
    '''
    req_body = request.get_json()
    doi = req_body['doi']

    uid = login_user.get_id()

    item = postgres.create_item(uid, doi)
    if item is None:
        abort(404)
