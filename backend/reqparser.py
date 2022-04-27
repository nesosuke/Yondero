from cgi import FieldStorage
from flask import abort
from werkzeug.utils import secure_filename


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


def read_filename(file: bytes) -> str:
    '''
    リクエストボディのファイルからファイル名を取得する
    '''
    return secure_filename(file.filename)


def read_metadata(json_data) -> dict | None:
    '''
    リクエストボディからmetadataを取得する
    '''
    try:
        metadata = json_data['metadata']
    except KeyError:
        abort(400)
    return metadata


def parse_multipart_formdata(request):
    '''
    リクエストボディからファイルとmetadataを取得する
    '''
    env = {'REQUEST_METHOD': 'POST'}
    form = FieldStorage(
        environ=env,
        keep_blank_values=True
    )
    try:
        file = form['file']
    except KeyError:
        file = None

    try:
        metadata = form['metadata']
    except KeyError:
        metadata = None
    return file, metadata
