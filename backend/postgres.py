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
            item_id serial PRIMARY KEY NOT NULL,
            user_id serial NOT NULL,
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
            file_id serial UNIQUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS attatchments (
            file_id serial PRIMARY KEY NOT NULL,
            item_id serial NOT NULL,
            filepath TEXT
        )
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id serial PRIMARY KEY NOT NULL,
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
        SELECT file_id FROM metadata WHERE (user_id=%s AND item_id=%s)
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
        SELECT filepath FROM attatchments WHERE (file_id=%s)
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
        SELECT * FROM metadata WHERE (user_id=%s AND item_id=%s)
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
        RETURNING item_id
        ''', (user_id, metadata['title'], metadata['authors'], metadata['year'], metadata['journal'], metadata['volume'], metadata['issue'], metadata['pages'], metadata['doi'], metadata['url'], metadata['abstract'], metadata['keywords'], metadata['tags'], metadata['note']))
        res = cur.fetchone()[0]
        conn.commit()
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
        UPDATE metadata SET title=%s,authors=%s,year=%s,journal=%s,volume=%s,issue=%s,pages=%s,doi=%s,url=%s,abstract=%s,keywords=%s,tags=%s,note=%s 
        WHERE (user_id=%s AND item_id=%s)
        RETURNING item_id
        ''', (metadata['title'], metadata['authors'], metadata['year'], metadata['journal'], metadata['volume'], metadata['issue'], metadata['pages'], metadata['doi'], metadata['url'], metadata['abstract'], metadata['keywords'], metadata['tags'], metadata['note'], user_id, item_id))
        res = cur.fetchone()[0]
        conn.commit()
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
        SELECT user_id FROM users WHERE (username=%s)
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
        SELECT username FROM users WHERE (user_id=%s)
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
        SELECT password FROM users WHERE (user_id =%s)
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
            RETURNING user_id
            ''', (username, password_hash))
            res = cur.fetchone()[0]
            conn.commit()
        except:
            return 'something went wrong'
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
        SELECT password FROM users WHERE (username=%s)
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
        SELECT item_id FROM metadata WHERE (file_id=%s)
        ''', (file_id,))
        res = cur.fetchone()
    if res is None:
        return 'not found'
    item_id = res[0]
    return item_id


def add_file(user_id: int, item_id: int, filepath: str) -> int | Literal['something went wrong']:
    '''
    DB files にファイルを挿入 -> file_id
    '''
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO files (user_id,item_id,filepath) VALUES (%s,%s,%s)
        RETURNING file_id
        ''', (user_id, item_id, filepath))
        res = cur.fetchone()[0]
        conn.commit()
    if res is None:
        return 'something went wrong'
    file_id = res
    return file_id


def replace_file(user_id: int, item_id: int, filepath: str) -> int | Literal['something went wrong']:
    '''
    DB attatchments にファイルを挿入 -> item_id
    '''
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE attatchments SET filepath=%s 
        WHERE user_id=%s AND item_id=%s
        RETURNING file_id
        ''', (filepath, user_id, item_id))
        res = cur.fetchone()[0]
        conn.commit()
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
        SELECT * FROM metadata WHERE (user_id=%s)
        ''', (user_id,))
        res = cur.fetchall()
    if res is None:
        return 'not found'
    metadata_list = [dict(zip(row[0].keys(), row[0])) for row in res]
    return metadata_list
