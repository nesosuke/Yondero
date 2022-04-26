from io import BytesIO
from flask import Blueprint, Flask, abort, jsonify, request, send_file, url_for
from requests import Response
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
limit_filesize = 50*1024*1024
allowed_extensions = ['pdf', 'doc', 'docx', 'md', 'txt', 'ppt', 'pptx']
document_type = ['article', 'book', 'booklet', 'conference', 'inbook', 'incollection', 'inproceedings',
                 'manual', 'mastersthesis', 'misc', 'phdthesis', 'proceedings', 'techreport', 'unpublished']


def find_attatchments_dir(base_dir: str) -> str:
    # TODO: 分離 -> fileio.py
    '''
    FS上の base_dir を探す．なければ作成する．
    '''
    dirpath = base_dir
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath


def read_filename(file: bytes) -> str:
    '''
    リクエストボディからファイル名を取得する
    '''
    return file.filename


def validate_filesize(file: bytes, limit_filesize: int) -> bool:
    # TODO: 分離 -> fileio.py
    if file.__sizeof__() > limit_filesize:
        return False
    return True


def validate_filetype(file: bytes) -> bool:
    '''
    ファイルタイプを検証する
    '''
    filename = read_filename(file)
    ext = filename.rsplit('.', 1)[1]
    if ext not in allowed_extensions:
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


def validate_metadata(metadata: dict) -> bool:
    '''
    metadataを検証する
    '''
    if 'document_type' not in metadata:
        return False
    if 'title' not in metadata:
        return False
    return True


def save_file(target_dir: str, file: bytes) -> str:
    '''
    FSにファイルを保存する
    '''
    filename = file.filename
    filepath = target_dir+'/'+filename
    with open(filepath, 'wb') as f:
        f.write(file.read())
    return filepath


def load_file(filepath: str) -> bytes:
    '''
    FSからファイルを読み込む
    '''
    with open(filepath, 'rb') as f:
        return f.read()


def delete_file(filepath: str):
    '''
    FSからファイルを削除する
    '''
    os.remove(filepath)


def update_file(filepath: str, file: bytes):
    '''
    FSにファイルを更新する
    '''
    delete_file(filepath)
    save_file(filepath, file)


@bp.route('/', methods=['GET'])
def index():
    return 'hello world'


@bp.route('/documents', methods=['GET'])
def get_documents():
    '''
    get all metadata
    '''
    data = postgres.get_all_metadata()
    if data == 'something went wrong':
        abort(500)
    elif data is None:
        abort(404)
    return jsonify(data)


@bp.route('/documents', methods=['POST'])
def post_document():
    '''
    add a new document file or/and a new metadata
    '''
    body = request.get_json()

    if 'file' not in body and 'metadata' not in body:
        abort(400)

    elif 'file' not in body:  # metadata only
        metadata = read_metadata(body)
        if not validate_metadata(metadata):
            abort(400)

        result_metadata = postgres.add_metadata(metadata)
        if result_metadata == 'conflict':
            abort(409)

        return Response(status=201)

    elif 'metadata' not in body:  # file only
        file = read_file(body)
        if not validate_filesize(file, limit_filesize):
            abort(413)
        if not validate_filetype(file):
            abort(415)

        filename = read_filename(file)
        target_dir = find_attatchments_dir(base_dir)
        filepath = save_file(target_dir, file)
        if os.path.exists(filepath):
            abort(409)
        result_file = postgres.add_file(filepath)
        if result_file == 'conflict':
            abort(409)

        metadata = {
            'document_type': 'misc',
            'title': filename
        }
        result_metadata = postgres.add_metadata(metadata)
        if result_metadata == 'conflict':
            abort(409)

        return Response(status=201)

    else:  # both file and metadata
        file = read_file(body)
        metadata = read_metadata(body)

        if not validate_metadata(metadata):
            abort(400)
        if not validate_filesize(file, limit_filesize):
            abort(413)
        if not validate_filetype(file):
            abort(415)

        target_dir = find_attatchments_dir(base_dir)
        filepath = save_file(target_dir, file)
        if os.path.exists(filepath):
            abort(409)

        result_file = postgres.add_file(filepath)
        result_metadata = postgres.add_metadata(metadata)
        if result_file == 'conflict' or result_metadata == 'conflict':
            abort(409)

        return Response(status=201)


@bp.route('/documents/<int:document_id>/metadata', methods=['GET'])
def get_document_metadata(document_id):
    '''
    get metadata of a document
    '''
    data = postgres.get_metadata(document_id)
    if data is None:
        abort(404)

    return jsonify(data)


@bp.route('/documents/<int:document_id>/metadata', methods=['PUT'])
def put_document_metadata(document_id):
    if postgres.get_metadata(document_id) is None:
        abort(404)

    body = request.get_json()
    metadata = read_metadata(body)

    result_metadata = postgres.update_metadata(document_id, metadata)
    if result_metadata is None:
        abort(500)

    return Response(status=200)


@bp.route('/documents/<int:document_id>', methods=['GET'])
def get_file(document_id):
    '''
    get file of a document
    '''
    data = postgres.get_filepath(document_id)
    if data is None:
        abort(404)

    return send_file(data, as_attachment=True)


@bp.route('/documents/<int:document_id>', methods=['POST'])
def post_file(document_id):
    '''
    upload file of a document
    '''
    if postgres.get_filepath(document_id) is not None:
        abort(409)

    body = request.get_json()
    file = read_file(body)
    if not validate_filesize(file, limit_filesize):
        abort(413)
    if not validate_filetype(file):
        abort(415)

    filename = read_filename(file)
    target_dir = find_attatchments_dir(base_dir)
    filepath = save_file(target_dir, file)
    if os.path.exists(filepath):
        abort(409)

    result_file = postgres.add_file(filepath)
    if result_file is None:
        abort(500)

    metadata = {
        'document_type': 'misc',
        'title': filename
    }
    result_metadata = postgres.add_metadata(metadata)
    if result_metadata is None:
        abort(500)

    return Response(status=201)


@bp.route('/documents/<int:document_id>', methods=['PUT'])
def put_file(document_id):
    '''
    update file of a document
    '''
    result_file = postgres.get_filepath(document_id)
    if result_file is None:
        abort(404)

    body = request.get_json()
    file = read_file(body)
    if not validate_filesize(file, limit_filesize):
        abort(413)
    if not validate_filetype(file):
        abort(415)

    target_dir = find_attatchments_dir(base_dir)
    filepath = save_file(target_dir, file)

    delete_file(filepath)
    filepath = save_file(target_dir, file)

    result_file = postgres.update_file(document_id, filepath)
    if result_file is None:
        abort(500)

    return Response(status=200)


@bp.route('/documents/<int:document_id>', methods=['DELETE'])
def delete_file(document_id):
    '''
    delete file of a document
    '''
    filepath = postgres.get_filepath(document_id)
    if filepath is None:
        abort(404)

    result_file = postgres.delete_file(document_id)
    if result_file is None:
        abort(500)

    result_metadata = postgres.delete_metadata(document_id)
    if result_metadata is None:
        abort(500)

    delete_file(filepath)
    return Response(status=200)
