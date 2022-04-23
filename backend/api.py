from flask import Blueprint, Flask, abort, jsonify, request, url_for
from flask_cors import CORS

from . import postgres, style
# HTTP status code は適当（デバッグ用）
# 認証難しすぎワロタ
# user = {
#     'username': 'admin',
#     'password': 'admin',
# }
# user_id=1
# 認証難しすぎワロタ（ここまで）

api = Flask(__name__)
CORS(api)

bp = Blueprint('api', __name__, url_prefix='/api/v1')

@bp.route('/register', methods=['POST'])
def resister():
    '''
    register an user
    '''
    if not request.get_json():
        abort(410)
    data = request.get_json()
    
    # TODO: generalize

    user_id=postgres.create_user(data['username'], data['password'])
    if user_id is None:
        abort(418)
    return jsonify({'user_id': user_id})

@bp.route('/item/cite', methods=['POST'])
def item_cite():
    '''
    Return citation for item, BibTeX format -> 200,404,500
    '''
    user_id=request.headers.get('user_id',default=None)
    if user_id is None:
        abort(418)

    if not request.get_json():
        abort(410)
    data = request.get_json()
    item_id = data['item_id']

    res = postgres.get_metadata(item_id)
    if res is None:
        abort(404)
    metadata = res

    # TODO: to style data into bibtex format
    citation = ''
    citation = metadata

    return citation


@bp.route('/item/new', methods=['POST'])
def item_new():
    '''
    Add new item to database -> 200,400,500
    '''
    user_id=request.headers.get('user_id',default=None)
    if user_id is None:
        abort(418)
        
    if request.get_json() is None:
        abort(401)
    data = request.get_json()  # not included item_id
    data = dict(data)
    data['user_id'] = user_id

    res = postgres.add_metadata(data)
    if res is None:
        abort(412)
    item_id = res
    created_at = postgres.get_metadata(item_id)['created_at']

    return_data = {
        'item_id': item_id,
        'created_at': created_at
    }

    return jsonify(return_data)


@bp.route('/item/update', methods=['POST'])
def item_update():
    '''
    Update item in database -> 200,400,500
    '''
    user_id=request.headers.get('user_id',default=None)
    if user_id is None:
        abort(418)
    if not request.get_json():
        abort(410)
    data = request.get_json()  # include item_id
    data = dict(data)
    data['user_id'] = user_id

    res = postgres.update_metadata(data)
    if res is None:
        abort(403)
    item_id = res

    return_data = {
        'item_id': item_id
    }

    return jsonify(return_data)


@bp.route('/item/upload', methods=['POST'])
def item_upload():
    '''
    Upload file and metadata to server -> 200,409,500
    '''
    if 'file' not in request.files: #FIXME: file is not included in request.files
        abort(401)
    user_id=request.headers.get('user_id',default=None)
    if user_id is None:
        abort(418)

    filedata = request.files['file']
    filename = filedata.filename
    if 'item_id' in request.get_json():
        item_id = request.get_json()['item_id']
        metadata = postgres.get_metadata(item_id)
        if metadata is None:
            abort(403)
        res = postgres.update_attatchment(filedata, filename, item_id)
        if res is None:
            abort(404)
        object_id = res
        return_data = {
            'object_id': object_id
        }
        return jsonify(return_data)
    else:
        # TODO: to get NEW item_id from database
        res = postgres.save_new_attatchment(filedata, filename, user_id)
        if res is None:
            abort(500)
        object_id = res
        return_data = {
            'object_id': object_id
        }
        return jsonify(return_data)


@bp.route('/item/download', methods=['GET'])
def item_download():
    '''
    Return file from server -> 200,404,500
    '''
    user_id=request.headers.get('user_id',default=None)
    if user_id is None:
        abort(410)

    if not request.get_json():
        abort(418)
    data = request.get_json()    
    item_id = data['item_id']

    res = postgres.get_attatchment(item_id)
    if res is None:
        abort(404)
    file = res
    return file


@bp.route('/item/all')
def item_all():
    '''
    Return all items in database -> 200,404,500
    '''
    user_id=request.headers.get('user_id',default=None)
    if user_id is None:
        abort(410)

    res = postgres.get_all_metadata(user_id)
    if res is None:
        abort(404)
    return jsonify(res)

    # TODO: to get user_id from database
    if request.get_json('user_id') is None:
        abort(400)
    user_id = request.get_json()['user_id']
    res = postgres.get_all_metadata(user_id)
    if res is None:
        abort(404)
    metadata = res
    return jsonify(metadata)


