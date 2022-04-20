import psycopg2
from werkzeug.security import generate_password_hash,check_password_hash

db_donfig = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'yondero',
    'user': 'yondero',
    'password': 'yondero'


}
conn = psycopg2.connect(**db_donfig)


def init_db():
    #create db: item,pdf,user
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS item (
            item_id TEXT PRIMARY KEY AUTOINCREMENT,
            uid TEXT,
            title TEXT,
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
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS pdf (
            object_id TEXT PRIMARY KEY AUTOINCREMENT,
            item_id TEXT PRIMARY KEY,
            pdf BYTEA
        )
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS user (
            uid TEXT PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            password TEXT,
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
            ON CONFLICT (item_id)
            DO UPDATE SET pdf = %s
            ''',
            (item_id, pdf, pdf)
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



def create_user(username,password,email):
    '''
    create user
    '''
    password=generate_password_hash(password)
    with conn.cursor() as cur:
        cur.execute(
            '''
            INSERT INTO user (username,password,email)
            VALUES (%s, %s, %s)
            ''',
            (username,password,email)
        )
        conn.commit()

        # check if user created
        uid = cur.fetchone()['uid']
    if uid is None:
        return None
    
    return 'OK'

def check_password(username,password):
    '''
    check password
    '''
    with conn.cursor() as cur:
        cur.execute(
            '''
            SELECT password FROM user WHERE username = %s
            ''',
            (username,)
        )
        row = cur.fetchone()
        if row is None:
            return None
        if row['password']==check_password_hash(password):
            return True
        else:
            return False

def change_password(username,password):
    '''
    change password
    '''
    password=generate_password_hash(password)
    with conn.cursor() as cur:
        cur.execute(
            '''
            UPDATE user SET password = %s WHERE username = %s
            ''',
            (password,username)
        )
        conn.commit()

        # check if user created
        uid = cur.fetchone()['uid']
    if uid is None:
        return None
    
    return 'OK'

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

def save_item(uid,title,authors,year,journal,volume,issue,pages,doi,url,abstract,keywords,tags):
    '''
    save item
    '''
    with conn.cursor() as cur:
        cur.execute(
            '''
            INSERT INTO item (uid,title,authors,year,journal,volume,issue,pages,doi,url,abstract,keywords,tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''',
            (uid,title,authors,year,journal,volume,issue,pages,doi,url,abstract,keywords,tags)
        )
        conn.commit()

        # check if item created
        item_id = cur.fetchone()['item_id']
    if item_id is None:
        return None
    
    return 'OK'


def update_item(item_id,uid,title,authors,year,journal,volume,issue,pages,doi,url,abstract,keywords,tags):
    '''
    update item
    '''
    with conn.cursor() as cur:
        cur.execute(
            '''
            UPDATE item SET uid = %s, title = %s, authors = %s, year = %s, journal = %s, volume = %s, issue = %s, pages = %s, doi = %s, url = %s, abstract = %s, keywords = %s, tags = %s WHERE item_id = %s
            ''',
            (uid,title,authors,year,journal,volume,issue,pages,doi,url,abstract,keywords,tags,item_id)
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
        uid=cur.fetchone()['uid']
    if item_id is not None and uid is None:
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
        

def cite_item(uid,doi):
    '''
    cite item
    '''
    with conn.cursor() as cur:
        cur.execute(
            '''
            SLECT * FROM item WHERE doi = %s, uid = %s''',
            (doi,uid)
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