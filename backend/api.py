from flask import Blueprint, Flask, jsonify, request, url_for
from flask_cors import CORS

from . import postgres, style

# 認証難しすぎワロタ
user = {
    'username': 'admin',
    'password': 'admin',
}
# 認証難しすぎワロタ（ここまで）

api = Flask(__name__)
CORS(api)

bp = Blueprint('api', __name__, url_prefix='/api/v1')


@bp.route('/item/cite', methods=['POST'])
def item_cite():
    '''
    Return citation for item, BibTeX format -> 200,404,500
    '''
    item_id = request.form['item_id']

    # TODO: to get item data from database

    data = {}

    # TODO: to style data into bibtex format
    citation = ''

    return citation


@bp.route('/item/new', methods=['POST'])
def item_new():
    '''
    Add new item to database -> 200,400,500
    '''
    data = request.form  # not included item_id

    # TODO: to add new item to database
    # TODO: to return item_id, added_at
    item_id = 0
    added_at = '2020-01-01T00:00:00Z'

    data['item_id'] = item_id
    data['added_at'] = added_at

    return jsonify(data)


@bp.route('/item/update', methods=['POST'])
def item_update():
    '''
    Update item in database -> 200,400,500
    '''
    data = request.form  # include item_id

    # TODO: to update item in database

    message = 'Success'

    return jsonify(message)


@bp.route('/item/upload', methods=['POST'])
def item_upload():
    '''
    Upload file and metadata to server -> 200,409,500
    '''
    if 'item_id' in request.headers:
        item_id = request.headers['item_id']
    else:
        # TODO: to get NEW item_id from database
        pass
    title = request.headers['title']

    file = request.files['file']
    file_name = file.filename
    file_ext = file_name.split('.')[-1]

    # TODO: to upload file to server(like S3), OR to save file to local, OR to add file to database -> item_id

    message = 'Success'

    return jsonify(message)


@bp.route('/item/download', methods=['GET'])
def item_download():
    '''
    Return file from server -> 200,404,500
    '''
    item_id = request.headers['item_id']

    # TODO: to get file from S3, OR to get file from local, OR to get file from database

    file = bytes('')

    return file


@bp.route('/item/all')
def item_all():
    '''
    Return all items in database -> 200,404,500
    '''
    # TODO: to get user_id from database
    username = user['username']
    user_id = 1

    # TODO: to get all items from database
    items = []

    return jsonify(items)


@bp.route('/stats', methods=['GET'])
def stats():
    '''
    Return statistics of items in database -> 200,404,500
    '''
    # TODO: to get user_id from database
    username = user['username']
    user_id = 1

    # TODO: to get statistics from database
    stats = {}

    return jsonify(stats)
