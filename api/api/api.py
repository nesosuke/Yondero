from msilib.schema import Binary
from os import abort

from flask import Blueprint, Flask, jsonify, request, url_for
from flask_cors import CORS
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)

from .api import bibtex,db

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
        # "/item/{uid}/delete", # POST
        # "/register",
        "/login",
        "/logout",
    ]

    res = {"endpoints": endpoints}
    return jsonify(res)


@login_required
@url_api.route('/item/cite', methods=['POST'])
def return_cite() -> str:
    '''
    return citation text for an item
    '''
    req_body = request.get_json()
    doi = req_body['doi']
    style = req_body['style']

    itemdata = db.get_item_data_from_doi(doi)
    if itemdata is None:
        abort(404)

    res = bibtex.bibtex_dump(itemdata)

    return res


@login_required
@url_api.route('/item/<item_id>', methods=['POST'])
def return_itemdata(item_id: str) -> dict:
    '''
    return item data
    '''
    itemdata = db.get_item_data_from_uid(item_id)
    if itemdata is None:
        abort(404)

    res = bibtex.bibtex_dump(itemdata)

    return res


@login_required
@url_api.route('/item/<uid>/download', methods=['POST'])
def download_item(item_id: str):
    '''
    give PDF to client
    '''

    pdffile = db.get_pdf(item_id)  # TODO
    if pdffile is None:
        abort(404)

    return pdffile


@login_required
@url_api.route('/item/<uid>/upload', methods=['POST'])
def upload_item(item_id: str):
    '''
    upload PDF to server
    '''

    pdf = request.files['pdf']
    if pdf is None:
        abort(400)

    if db.get_pdf(item_id) is not None:
        abort(409)

    db.upload_pdf(item_id, pdf)

    if db.get_pdf(item_id) is None:
        abort(500)

    return "OK"

