import os


def save_file(filepath: str, file: bytes) -> str:
    '''
    FSにファイルを保存する
    '''
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
    if os.path.exists(filepath):
        os.remove(filepath)


def update_file(filepath: str, file: bytes):
    '''
    FSにファイルを更新する
    '''
    delete_file(filepath)
    save_file(filepath, file)


def validate_filesize(file: bytes, limit_filesize: int) -> bool:
    # TODO: 分離 -> fileio.py
    if file.__sizeof__() > limit_filesize:
        return False
    return True


def validate_filetype(file: bytes, allowed_extensions) -> bool:
    '''
    ファイルタイプを検証する
    '''
    filename = file.filename
    ext = filename.rsplit('.', 1)[1]
    if ext not in allowed_extensions:
        return False
    return True
