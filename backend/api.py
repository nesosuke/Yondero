from io import BytesIO
from flask import Blueprint, Flask, abort, jsonify, request, send_file, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

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


base_dir = 'attatchments'
max_filesize = 50*1024*1024


def find_attatchments_dir(base_dir: str, user_id: int) -> str:
    # TODO: 分離 -> fileio.py
    '''
    FS上の base_dir/{user_id} を探す．なければ作成する．
    '''
    dirpath = base_dir+'/'+str(user_id)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath


def validate_filesize(file: bytes, max_filesize: int) -> bool:
    # TODO: 分離 -> fileio.py
    if file.__sizeof__() > max_filesize:
        return False
    return True


def read_user_id(json_data) -> int | None:
    '''
    リクエストボディからuser_idを取得する
    '''
    try:
        user_id = json_data['user_id']
    except KeyError:
        abort(400)
    return user_id


def read_username_and_password(json_data) -> tuple | None:
    '''
    リクエストボディからusernameを取得する
    '''
    try:
        username = json_data['username']
        password = json_data['password']
    except KeyError:
        abort(400)
    return username, password


def read_item_id(json_data) -> int | None:
    '''
    リクエストボディからitem_idを取得する
    '''
    try:
        item_id = json_data['item_id']
    except KeyError:
        abort(400)
    return item_id


def read_file(data) -> bytes | None:
    '''
    リクエストボディからファイルを取得する
    '''
    try:
        file = data.files['file']
    except KeyError:
        abort(400)
    return file


def read_metadata(json_data) -> dict | None:
    '''
    リクエストボディからmetadataを取得する
    '''
    try:
        metadata = json_data['metadata']
    except KeyError:
        abort(400)
    return metadata


def save_file(target_dir: str, file: bytes, item_id: int) -> None:
    '''
    FSにファイルを保存する
    '''
    filename = file.filename
    filepath = target_dir+'/'+filename
    with open(filepath, 'wb') as f:
        f.write(file.read())


def load_file(filepath: str) -> bytes:
    '''
    FSからファイルを読み込む
    '''
    with open(filepath, 'rb') as f:
        return f.read()


@bp.route('/register', methods=['POST'])
def resister():
    '''
    register an user
    '''
    json_data = request.get_json()
    username, password = read_username_and_password(json_data)

    res = postgres.add_user(username, password)
    if res == 'something went wrong':
        abort(500)
    user_id = res
    return jsonify({'user_id': user_id})


@bp.route('/item/cite', methods=['POST'])
def item_cite():
    '''
    Return citation for item, BibTeX format
    #TODO style.pyでいい感じにできるまで保留
    '''
    return None


@bp.route('/item/new', methods=['POST'])
def item_new():
    '''
    Add new item to database
    '''
    json_data = request.get_json()
    user_id = read_user_id(json_data)
    metadata = read_metadata(json_data)
    res = postgres.add_metadata(user_id, metadata)
    if res == 'not found':
        abort(400)
    item_id = res
    return jsonify({'item_id': item_id})


@bp.route('/item/update', methods=['POST'])
def item_update():
    '''
    Update item in database 
    '''
    json_data = request.get_json()
    user_id = read_user_id(json_data)
    item_id = read_item_id(json_data)
    metadata = read_metadata(json_data)
    res = postgres.update_metadata(user_id, item_id, metadata)
    if res == 'not found':
        abort(400)
    return jsonify({'item_id': item_id})


@bp.route('/item/upload', methods=['POST'])
def item_upload():
    '''
    Upload file and metadata to server
    '''
    # data = request.get_data()
    req=request
    file = read_file(req)
    if not validate_filesize(file, max_filesize):
        abort(413)
    filename = secure_filename(file.filename)

    json_data = req.get_json()
    user_id = read_user_id(json_data)
    item_id = read_item_id(json_data)

    target_dir = find_attatchments_dir(base_dir, user_id)
    filepath = target_dir+'/'+filename

    save_file(target_dir, file, item_id)

    res = postgres.add_file(user_id, item_id, filepath)
    if res == 'something went wrong':
        abort(500)
    file_id = res

    res = postgres.find_item_id(file_id)
    if res == 'not found':
        abort(500)
    item_id = res

    return jsonify({'item_id': item_id})


@bp.route('/item/download', methods=['POST'])
def item_download():
    '''
    Return file from server
    '''
    json_data = request.get_json()
    user_id = read_user_id(json_data)
    item_id = read_item_id(json_data)

    res = postgres.find_file_id(user_id, item_id)
    if res == 'not found':
        abort(404)
    file_id = res

    res = postgres.find_file_path(file_id)
    if res == 'not found':
        abort(500)
    filepath = res
    filename = os.path.basename(filepath)

    file = load_file(filepath)
    return send_file(BytesIO(file), attachment_filename=filename, as_attachment=True)


@bp.route('/item/all', methods=['POST'])
def item_all():
    '''
    Return all items in database
    '''
    json_data = request.get_json()
    user_id = read_user_id(json_data)

    res = postgres.find_all_metadata(user_id)
    if res == 'not found':
        abort(404)
    metadata_list = res

    return jsonify(metadata_list)
