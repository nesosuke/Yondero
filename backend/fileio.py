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
