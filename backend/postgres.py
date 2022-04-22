import os
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
attatchment_base_dir = 'attatchment/'


# initialize attatchment dir
def get_attatchment_dir(user_id):
    if os.path.exists(attatchment_base_dir + user_id):
        path = attatchment_base_dir + user_id + '/'
        return path
    os.mkdir(attatchment_base_dir + user_id)
    path = attatchment_base_dir + user_id + '/'
    return path

def limit_filesize(filedata, max_filesize=50 * 1024 * 1024):
    if len(filedata) > max_filesize:
        raise ValueError('File size is too large')
    return filedata


def init_db():
    # create db: metadata,attatchment,users
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            item_id SERIAL PRIMARY KEY NOT NULL,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
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
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS attatchments (
            object_id SERIAL PRIMARY KEY NOT NULL,
            item_id SERIAL NOT NULL,
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


# handle user
def get_user_id_from_username(username):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT user_id FROM users WHERE username = %s
        ''', (username,))
        user_id = cur.fetchone()
    if user_id is None:
        return None
    return user_id[0]


def create_user(username, password):
    password_hash = generate_password_hash(password)
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO users (username, password) VALUES (%s, %s)
        ''', (username, password_hash))
        conn.commit()
        user_id = cur.lastrowid
    if user_id is None:
        return None
    return user_id


def check_password(username, password):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT password FROM users WHERE username = %s
        ''', (username,))
        password_hash = cur.fetchone()
    if password_hash is None:
        return False
    return check_password_hash(password_hash[0], password)

# handle metadata


def add_metadata(metadata: dict):
    '''
    Add metadata to database
    '''
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO metadata (user_id, title, authors, year, journal, volume, issue, pages, doi, url, abstract, keywords, tags, note) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (metadata['user_id'], metadata['title'], metadata['authors'], metadata['year'], metadata['journal'], metadata['volume'], metadata['issue'], metadata['pages'], metadata['doi'], metadata['url'], metadata['abstract'], metadata['keywords'], metadata['tags'], metadata['note']))
        conn.commit()
    item_id = cur.lastrowid
    if item_id is None:
        return None
    return item_id


def get_metadata(item_id):
    '''
    Return metadata from database
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT * FROM metadata WHERE item_id = %s
        ''', (item_id,))
        metadata = cur.fetchone()
    if metadata is None:
        return None
    metadata = dict(zip(metadata.keys(), metadata))
    return metadata


def update_metadata(item_id, metadata: dict):
    '''
    Update metadata in database
    '''
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE metadata SET user_id = %s, title = %s, authors = %s, year = %s, journal = %s, volume = %s, issue = %s, pages = %s, doi = %s, url = %s, abstract = %s, keywords = %s, tags = %s, note = %s WHERE item_id = %s
        ''', (metadata['user_id'], metadata['title'], metadata['authors'], metadata['year'], metadata['journal'], metadata['volume'], metadata['issue'], metadata['pages'], metadata['doi'], metadata['url'], metadata['abstract'], metadata['keywords'], metadata['tags'], metadata['note'], item_id))
        conn.commit()
    item_id = cur.lastrowid
    if item_id is None:
        return None

    return item_id


def get_all_metadata(user_id):
    '''
    Return all metadata from database
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT * FROM metadata WHERE user_id = %s
        ''', (user_id,))
        metadata = cur.fetchall()
    if metadata is None:
        return None
    metadata = [dict(zip(metadata.keys(), metadata)) for metadata in metadata]
    return metadata


# handle attatchment file
def save_new_attatchment(filedata, filename, user_id):
    '''
    Save new file to local, S3, or database
    '''
    if filedata is None:
        return None
    filedata = limit_filesize(filedata)

    filepath = get_attatchment_dir(user_id)+filename
    with open(filepath, 'wb') as f:
        f.write(filedata)

    title = filename
    metadata = {'title': title}
    res = add_metadata(metadata)
    if res is None:
        return None
    item_id = res

    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO attatchment (item_id, filepath) VALUES (%s, %s)
        ''', (item_id, filepath))
        conn.commit()
        object_id = cur.lastrowid
    if object_id is None:
        return None
    return object_id


def update_attatchment(filedata, filename, item_id):
    '''
    replace file to local, S3, or database
    '''
    if filedata is None:
        return None
    filedata = limit_filesize(filedata)
    if get_metadata(item_id) is None:
        return None
    user_id = get_metadata(item_id)['user_id']
    filepath = get_attatchment_dir(user_id)+filename
    with open(filepath, 'wb') as f:
        f.write(filedata)

    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO attatchment (item_id, filepath) VALUES (%s, %s)
        ''', (item_id, filepath))
        conn.commit()
        object_id = cur.lastrowid
    if object_id is None:
        return None
    return object_id


def get_attatchment(item_id):
    '''
    Return file from local, S3, or database
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT filepath FROM attatchment WHERE item_id = %s
        ''', (item_id,))
        filepath = cur.fetchone()
    if filepath is None:
        return None
    filepath = filepath[0]

    with open(filepath, 'rb') as f:
        return f.read()
