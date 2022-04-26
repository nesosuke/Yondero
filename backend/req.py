from flask import abort


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
    リクエストボディからファイル名を取得する
    '''
    return file.filename


def read_metadata(json_data) -> dict | None:
    '''
    リクエストボディからmetadataを取得する
    '''
    try:
        metadata = json_data['metadata']
    except KeyError:
        abort(400)
    return metadata
