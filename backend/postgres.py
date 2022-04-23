import os
from typing_extensions import Literal
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

db_config = {
    'host': 'db',
    'port': 5432,
    'dbname': 'yondero',
    'user': 'postgres',
    'password': 'postgres'
}
conn = psycopg2.connect(**db_config)


def init_db():
    # create db: metadata,attatchment,users
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            item_id SERIAL PRIMARY KEY NOT NULL,
            user_id integer NOT NULL,
            title TEXT NOT NULL,
            type TEXT,
            authors TEXT,
            year INTEGER,
            journal TEXT,
            volume TEXT,
            issue TEXT,
            pages TEXT,
            doi TEXT,
            url TEXT,
            abstract TEXT,
            keywords TEXT,
            tags TEXT,
            note TEXT,
            file_id integer UNIQUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS attatchments (
            file_id SERIAL PRIMARY KEY NOT NULL,
            item_id integer NOT NULL,
            filepath TEXT
        )
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at   TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()


def find_file_id(user_id: int, item_id: int) -> int | Literal['not found']:
    '''
    DB metadata からfile_idを探す -> int
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT file_id FROM metadata (user_id,item_id) VALUES (%s,%s)
        ''', (user_id, item_id))
        res = cur.fetchone()
    if res is None:
        return "not found"
    file_id = res[0]
    return file_id


def find_file_path(file_id: int) -> str | Literal['not found']:
    '''
    DB attatchments からfilepathを探す -> str
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT filepath FROM attatchments (file_id) VALUES (%s)
        ''', (file_id,))
        res = cur.fetchone()
    if res is None:
        return "not found"
    filepath = res[0]
    return filepath


def find_metadata(user_id: int, item_id: int) -> dict | Literal['not found']:
    '''
    DB metadata からmetadataを探す -> dict
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT * FROM metadata (user_id,item_id) VALUES (%s,%s)
        ''', (user_id, item_id))
        res = cur.fetchone()
    if res is None:
        return "not found"
    metadata = dict(zip(res[0].keys(), res[0]))
    del metadata['file_id']
    return metadata


def add_metadata(user_id: int, metadata: dict) -> int | Literal['not found']:
    '''
    DB metadata にmetadataを挿入 -> int
    '''
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO metadata (user_id,title,authors,year,journal,volume,issue,pages,doi,url,abstract,keywords,tags,note) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''', (user_id, metadata['title'], metadata['authors'], metadata['year'], metadata['journal'], metadata['volume'], metadata['issue'], metadata['pages'], metadata['doi'], metadata['url'], metadata['abstract'], metadata['keywords'], metadata['tags'], metadata['note']))
        conn.commit()
    res = cur.lastrowid
    if res is None:
        return "not found"
    item_id = res
    return item_id


def update_metadata(user_id: int, item_id: int, metadata: dict) -> int | Literal['not found']:
    '''
    DB metadata にmetadataを更新 -> int
    '''
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE metadata (user_id,item_id,title,authors,year,journal,volume,issue,pages,doi,url,abstract,keywords,tags,note) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''', (user_id, item_id, metadata['title'], metadata['authors'], metadata['year'], metadata['journal'], metadata['volume'], metadata['issue'], metadata['pages'], metadata['doi'], metadata['url'], metadata['abstract'], metadata['keywords'], metadata['tags'], metadata['note']))
        conn.commit()
    res = cur.lastrowid
    if res is None:
        return "not found"
    item_id = res
    return item_id


def find_user_id(username: str) -> int | Literal['not found']:
    '''
    DB users からuser_idを探す -> int
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT user_id FROM users (username) VALUES (%s)
        ''', (username,))
        res = cur.fetchone()
    if res is None:
        return 'not found'
    user_id = res[0]
    return user_id


def find_username(user_id: int) -> str | Literal['not found']:
    '''
    DB users からusernameを探す -> str
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT username FROM users (user_id) VALUES (%s)
        ''', (user_id,))
        res = cur.fetchone()
    if res is None:
        return 'not found'
    username = res[0]
    return username


def find_password(user_id: int) -> str | Literal['not found']:
    '''
    DB users からpasswordを探す -> str
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT password FROM users (user_id) VALUES (%s)
        ''', (user_id,))
        res = cur.fetchone()
    if res is None:
        return 'not found'
    password = res[0]
    return password


def add_user(username: str, password: str) -> int | Literal['something went wrong']:
    '''
    DB users にユーザーを作成 -> int
    '''
    password_hash = generate_password_hash(password)
    with conn.cursor() as cur:
        try:
            cur.execute('''
            INSERT INTO users (username,password) VALUES (%s,%s)
            ''', (username, password_hash))
            conn.commit()
        except:
            return 'something went wrong'
    res = cur.lastrowid
    if res is None:
        return 'something went wrong'
    user_id = res
    return user_id


def is_valid_user(username: str, password: str) -> bool:
    '''
    # 将来的（認証の難しさによる）
    DB users からusernameとpasswordが一致するか確認 -> bool
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT password FROM users (username) VALUES (%s)
        ''', (username,))
        res = cur.fetchone()
    if res is None:
        return False
    password_hash = res[0]
    return check_password_hash(password_hash, password)


def find_item_id(file_id: int) -> int | Literal['not found']:
    '''
    DB metadata からitem_idを探す -> int
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT item_id FROM metadata (file_id) VALUES (%s)
        ''', (file_id,))
        res = cur.fetchone()
    if res is None:
        return 'not found'
    item_id = res[0]
    return item_id


def add_file(user_id: int, item_id: int, filepath: str) -> int | Literal['something went wrong']:
    '''
    DB files にファイルを挿入 -> item_id
    '''
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO files (user_id,item_id,filepath) VALUES (%s,%s,%s)
        ''', (user_id, item_id, filepath))
        conn.commit()
    res = cur.lastrowid
    if res is None:
        return 'something went wrong'
    file_id = res
    return file_id


def replace_file(user_id: int, item_id: int, filepath: str) -> int | Literal['something went wrong']:
    '''
    DB files にファイルを挿入 -> item_id
    '''
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE files (user_id,item_id,filepath) VALUES (%s,%s,%s)
        ''', (user_id, item_id, filepath))
        conn.commit()
    res = cur.lastrowid
    if res is None:
        return 'something went wrong'
    file_id = res
    return file_id


def find_all_metadata(user_id: int) -> list | Literal['not found']:
    '''
    DB metadata から全てのmetadataを探す -> list
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT * FROM metadata (user_id) VALUES (%s)
        ''', (user_id,))
        res = cur.fetchall()
    if res is None:
        return 'not found'
    metadata_list = [dict(zip(row[0].keys(), row[0])) for row in res]
    return metadata_list
