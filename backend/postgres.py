import psycopg2
from typing_extensions import Literal

db_config = {
    'host': 'db',
    'port': 5432,
    'dbname': 'yondero',
    'user': 'postgres',
    'password': 'postgres'
}
conn = psycopg2.connect(**db_config)


def init_db():
    # create db: documents, metadata, attachments
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            document_id SERIAL PRIMARY KEY,
            metadata_id INTEGER NOT NULL,
            FOREIGN KEY (metadata_id) REFERENCES metadata(metadata_id),
            attachment_id INTEGER NOT NULL,
            FOREIGN KEY (attachment_id) REFERENCES attatchments(attachment_id),
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            metadata_id SERIAL PRIMARY KEY,
            document_type TEXT NOT NULL,
            title TEXT NOT NULL,
            authors TEXT[],
            year INTEGER,
            journal TEXT,
            volume TEXT,
            issue TEXT,
            pages TEXT,
            abstract TEXT,
            doi TEXT,
            url TEXT
            )   
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS attatchments (
            attachment_id SERIAL PRIMARY KEY,
            filepath TEXT,
            )
        ''')
        conn.commit()
