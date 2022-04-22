from os import abort

from flask import Blueprint, Flask, jsonify, request, url_for
from flask_cors import CORS
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)

from . import postgres, style

# 認証難しすぎワロタ
user = {
    'username': 'admin',
    'password': 'admin',
    'email': 'admin@neso.tech'
}
# 認証難しすぎワロタ（ここまで）

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


@url_api.route('/item/<uid>/download', methods=['POST'])
def download_pdf(item_id: str):
    '''
    give PDF to client
    '''

    pdffile = postgres.get_pdf(item_id)  # TODO
    if pdffile is None:
        abort(404)

    return pdffile


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
