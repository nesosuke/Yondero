from flask import Blueprint, Flask, abort, jsonify, request, send_file
from requests import Response
from flask_cors import CORS
import os

from . import postgres, reqparser, style, fileio
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

base_dir = 'attachments'
limit_filesize = 50*1024*1024
allowed_extensions = ['pdf', 'doc', 'docx', 'md', 'txt', 'ppt', 'pptx']
document_type = ['article', 'book', 'booklet', 'conference', 'inbook', 'incollection', 'inproceedings',
                 'manual', 'mastersthesis', 'misc', 'phdthesis', 'proceedings', 'techreport', 'unpublished']


def find_attachments_dir(base_dir: str) -> str:
    '''
    FS上の base_dir を探す．なければ作成する．
    '''
    dirpath = base_dir
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath


def validate_metadata(metadata: dict) -> bool:
    '''
    metadataを検証する
    '''
    if metadata is None:
        return False
    if 'title' not in metadata:
        return False
    return True


@bp.route('/', methods=['GET'])
def index():
    return 'hello world'


@bp.route('/documents', methods=['GET'])
def get_documents():
    '''
    get all metadata
    '''
    data = postgres.get_all_metadata()
    if data is None:
        abort(404)
    return jsonify(data)


@bp.route('/documents', methods=['POST'])
def post_document():
    '''
    add a new document file or/and a new metadata
    '''
    # body is metadata
    # metadata: JSON
    body = request.get_json()
    metadata = body
    if not validate_metadata(metadata):
        abort(400)

    metadata_id = postgres.add_metadata(metadata)
    if metadata_id is None:
        abort(500)

    document_id = postgres.add_document(metadata_id)
    if document_id is None:
        abort(500)

    return jsonify({'document_id': document_id}), 201


@bp.route('/documents/<int:document_id>', methods=['GET'])
def get_document_metadata(document_id):
    '''
    get metadata of a document
    '''
    metadata_id = postgres.get_metadata_id(document_id)
    data = postgres.get_metadata(metadata_id)
    if data is None:
        abort(404)

    return jsonify(data)


@bp.route('/documents/<int:document_id>', methods=['PUT'])
def put_document_metadata(document_id):
    metadata_id = postgres.get_metadata_id(document_id)
    if postgres.get_metadata(metadata_id) is None:
        abort(404)

    body = request.get_json()
    metadata = body

    metadata_id = postgres.update_metadata(metadata_id, metadata)
    if metadata_id is None:
        abort(500)

    return jsonify({'metadata_id': metadata_id})


@bp.route('/documents/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    ''' 
    delete a document, and related metadata and file
    '''
    metadata_id = postgres.get_metadata_id(document_id)
    if postgres.get_metadata(metadata_id) is None:
        abort(404)

    postgres.delete_document(document_id)
    
    postgres.delete_metadata(metadata_id)

    file_id = postgres.get_file_id(document_id)
    if file_id is not None:
        filepath = postgres.get_filepath(file_id)
        fileio.delete_file(filepath)
        postgres.delete_file(file_id)

    

    return '', 200


@bp.route('/documents/<int:document_id>/file', methods=['GET'])
def get_document_file(document_id):
    '''
    get file of a document
    '''
    file_id = postgres.get_file_id(document_id)
    data = postgres.get_filepath(file_id)
    if data is None:
        abort(404)

    return send_file(data, as_attachment=True)


@bp.route('/documents/<int:document_id>/file', methods=['POST'])
def post_document_file(document_id):
    '''
    upload file of a document
    '''
    file_id = postgres.get_file_id(document_id)
    if postgres.get_filepath(file_id) is not None:
        abort(409)

    body = request.get_json()
    file = reqparser.read_file(body)
    if not fileio.validate_filesize(file, limit_filesize):
        abort(413)
    if not fileio.validate_filetype(file, allowed_extensions):
        abort(415)

    # TODO: ユーザー機能を追加の予約用．find_attachments_dir(base_dir, user_id)とする．
    target_dir = find_attachments_dir(base_dir)
    filename = reqparser.read_filename(file)
    filepath = os.path.join(target_dir, filename)

    if os.path.exists(filepath):
        abort(409)
    filepath = fileio.save_file(filepath, file)

    file_id = postgres.add_file(filepath)
    if file_id is None:
        abort(500)

    if postgres.update_file_id(document_id, file_id):
        abort(500)

    return '', 201


@bp.route('/documents/<int:document_id>/file', methods=['PUT'])
def put_document_file(document_id):
    '''
    update file of a document
    '''
    file_id = postgres.get_file_id(document_id)
    result_file = postgres.get_filepath(file_id)
    if result_file is None:
        abort(404)

    body = request.get_json()
    file = reqparser.read_file(body)
    if not fileio.validate_filesize(file, limit_filesize):
        abort(413)
    if not fileio.validate_filetype(file, allowed_extensions):
        abort(415)

    # TODO: ユーザー機能を追加の予約用．find_attachments_dir(base_dir, user_id)とする．
    target_dir = find_attachments_dir(base_dir)
    filename = reqparser.read_filename(file)
    filepath = os.path.join(target_dir, filename)

    fileio.delete_file(filepath)
    filepath = fileio.save_file(filepath, file)

    result_file = postgres.update_file(file_id, filepath)
    if result_file is None:
        abort(500)

    return Response(status=200)


@bp.route('/documents/<int:document_id>/file', methods=['DELETE'])
def delete_document_file(document_id):
    '''
    delete file of a document
    '''
    file_id = postgres.get_file_id(document_id)
    filepath = postgres.get_filepath(file_id)
    if filepath is None:
        abort(404)
    fileio.delete_file(filepath)

    result_file = postgres.delete_file(file_id)
    if result_file is False:
        abort(500)

    return Response(status=200)
