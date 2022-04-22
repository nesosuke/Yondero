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
    # create db: metadata,attatchment,user
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            item_id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
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
        CREATE TABLE IF NOT EXISTS attatchment (
            object_id SERIAL PRIMARY KEY,
            item_id SERIAL NOT NULL,
            filepath TEXT, 
        )
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS user (
            user_id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()


def save_pdf(item_id: str, pdf: bytes) -> str:
    '''
    save PDF to database
    '''
    with conn.cursor() as cur:
        cur.execute(
            '''
            INSERT INTO pdf (item_id, pdf)
            VALUES (%s, %s)
                        ''',
            (item_id, pdf)
        )
        conn.commit()

        # check if pdf saved
        object_id = cur.fetchone()['object_id']
    if object_id is None:
        return None

    return 'OK'


def get_pdf(item_id: str) -> bytes:
    '''
    get PDF from database
    '''
    with conn.cursor() as cur:
        cur.execute(
            '''
            SELECT pdf FROM pdf WHERE item_id = %s
            ''',
            (item_id,)
        )
        row = cur.fetchone()
        if row is None:
            return None
        return row[0]


def get_user(username):
    '''
    get user
    '''
    with conn.cursor() as cur:
        cur.execute(
            '''
            SELECT * FROM user WHERE username = %s
            ''',
            (username,)
        )
        row = cur.fetchone()
        if row is None:
            return None
        return row







def get_item(item_id):
    '''
    get item
    '''
    with conn.cursor() as cur:
        cur.execute(
            '''
            SELECT * FROM item WHERE item_id = %s
            ''',
            (item_id,)
        )
        row = cur.fetchone()
        if row is None:
            return None
        return row


def save_item(user_id, title, authors, year, journal, volume, issue, pages, doi, url, abstract, keywords, tags):
    '''
    save item
    '''
    with conn.cursor() as cur:
        cur.execute(
            '''
            INSERT INTO item (user_id,title,authors,year,journal,volume,issue,pages,doi,url,abstract,keywords,tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''',
            (user_id, title, authors, year, journal, volume,
             issue, pages, doi, url, abstract, keywords, tags)
        )
        conn.commit()

        # check if item created
        item_id = cur.fetchone()['item_id']
    if item_id is None:
        return None

    return 'OK'


def update_item(item_id, user_id, title, authors, year, journal, volume, issue, pages, doi, url, abstract, keywords, tags):
    '''
    update item
    '''
    with conn.cursor() as cur:
        cur.execute(
            '''
            UPDATE item SET user_id = %s, title = %s, authors = %s, year = %s, journal = %s, volume = %s, issue = %s, pages = %s, doi = %s, url = %s, abstract = %s, keywords = %s, tags = %s WHERE item_id = %s
            ''',
            (user_id, title, authors, year, journal, volume, issue,
             pages, doi, url, abstract, keywords, tags, item_id)
        )
        conn.commit()

        # check if item updated
        item_id = cur.fetchone()['item_id']
    if item_id is None:
        return None

    return 'OK'


def delete_item(item_id):
    '''
    delete item
    '''
    with conn.cursor() as cur:
        cur.execute(
            '''
            DELETE FROM item WHERE item_id = %s
            ''',
            (item_id,)
        )
        conn.commit()

        # check if item deleted
        item_id = cur.fetchone()['item_id']
        user_id = cur.fetchone()['user_id']
    if item_id is not None and user_id is None:
        return 'OK'
    else:
        return None


def delete_pdf(item_id):
    '''
    delete pdf
    '''
    with conn.cursor() as cur:
        cur.execute(
            '''
            DELETE FROM pdf WHERE item_id = %s
            ''',
            (item_id,)
        )
        conn.commit()

        # check if pdf deleted
        object_id = cur.fetchone()['object_id']
        item_id = cur.fetchone()['item_id']
    if object_id is None and item_id is None:
        return 'OK'
    else:
        return None


def cite_item(user_id, doi):
    '''
    cite item
    '''
    with conn.cursor() as cur:
        cur.execute(
            '''
            SLECT * FROM item WHERE doi = %s, user_id = %s''',
            (doi, user_id)
        )
        row = cur.fetchone()
        if row is None:
            return None
        return row


def get_item(item_id):
    '''
    get item
    '''
    with conn.cursor() as cur:
        cur.execute(
            '''
            SELECT * FROM item WHERE item_id = %s
            ''',
            (item_id,)
        )
        row = cur.fetchone()
        if row is None:
            return None
        return row
