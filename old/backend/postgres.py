import psycopg2

db_config = {
    'host': 'db',
    'port': 5432,
    'dbname': 'yondero',
    'user': 'postgres',
    'password': 'postgres'
}
conn = psycopg2.connect(**db_config)


def init_db():
    # create db: documents, metadata, files
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            metadata_id SERIAL PRIMARY KEY,
            document_type TEXT,
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
        CREATE TABLE IF NOT EXISTS files (
            file_id SERIAL PRIMARY KEY,
            filepath TEXT
            )
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            document_id SERIAL PRIMARY KEY,
            metadata_id INTEGER REFERENCES metadata(metadata_id),
            file_id INTEGER REFERENCES files(file_id),
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
        ''')

        conn.commit()


def metadata_to_dict(metadata: list) -> dict:
    '''
    Convert metadata list to dictionary
    '''
    metadata_dict = {
        'metadata_id': metadata[0],
        'document_type': metadata[1],
        'title': metadata[2],
        'authors': metadata[3],
        'year': metadata[4],
        'journal': metadata[5],
        'volume': metadata[6],
        'issue': metadata[7],
        'pages': metadata[8],
        'abstract': metadata[9],
        'doi': metadata[10],
        'url': metadata[11]
    }
    del metadata_dict['metadata_id']
    return metadata_dict

# handle documents table


def add_document(metadata_id: int) -> int:
    '''
    Create a new document record in Table: documents
    '''
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO documents (metadata_id) VALUES (%s)
        RETURNING document_id
        ''', (metadata_id,))
        document_id = cur.fetchone()[0]
        conn.commit()
    return document_id


def get_metadata_id(document_id: int) -> int:
    '''
    Get metadata_id of a document by document_id from Table: documents
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT metadata_id FROM documents WHERE document_id = %s
        ''', (document_id,))
        data = cur.fetchone()
        if data is None:
            return None
        metadata_id = data[0]
        return metadata_id


def get_file_id(document_id: int) -> int:
    '''
    Get file_id of a document by document_id from Table: documents
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT file_id FROM documents WHERE document_id = %s
        ''', (document_id,))
        data = cur.fetchone()
        if data is None:
            return None
        file_id = data[0]
        return file_id


def update_file_id(document_id: int, file_id: int) -> bool:
    '''
    Update file_id of a document by document_id in Table: documents
    '''
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE documents SET file_id = %s
        WHERE document_id = %s
        RETURNING file_id
        ''', (file_id, document_id))
        conn.commit()
        file_id = cur.fetchone()[0]
        if file_id is not None:
            return True
        else:
            return False


def update_metadata_id(document_id: int, metadata_id: int) -> bool:
    '''
    Update metadata_id of a document by document_id in Table: documents
    '''
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE documents SET metadata_id = %s
        WHERE document_id = %s
        RETURNING metadata_id
        ''', (metadata_id, document_id))
        conn.commit()
        metadata_id = cur.fetchone()[0]
        if metadata_id is not None:
            return True
        else:
            return False


# handle metadata table


def get_metadata(metadata_id: int) -> dict:
    '''
    Get metadata of a document by document_id from Table: metadata
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT * FROM metadata WHERE metadata_id = %s
        ''', (metadata_id,))
        res = cur.fetchone()
        if res is None:
            return None
        metadata = metadata_to_dict(res)
        return metadata


def get_all_metadata():
    '''
    Get all metadata records from Table: metadata
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT * FROM metadata
        ''')
        data = cur.fetchall()
        metadata_list = [metadata_to_dict(datum) for datum in data]
        # TODO　FIXME: metadataに document_id を追加する
        return metadata_list


def add_metadata(metadata: dict) -> int:
    '''
    Create a new metadata record in Table: metadata
    '''
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO metadata (document_type, title, authors, year, journal, volume, issue, pages, abstract, doi, url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING metadata_id
        ''', (metadata['document_type'], metadata['title'], metadata['authors'], metadata['year'], metadata['journal'], metadata['volume'], metadata['issue'], metadata['pages'], metadata['abstract'], metadata['doi'], metadata['url']))
        metadata_id = cur.fetchone()[0]
        conn.commit()
    return metadata_id


def update_metadata(metadata_id, metadata):
    '''
    Update metadata record of a document by metadata_id in Table: metadata
    '''
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE metadata SET document_type = %s, title = %s, authors = %s, year = %s, journal = %s, volume = %s, issue = %s, pages = %s, abstract = %s, doi = %s, url = %s
        WHERE metadata_id = %s
        ''', (metadata['document_type'], metadata['title'], metadata['authors'], metadata['year'], metadata['journal'], metadata['volume'], metadata['issue'], metadata['pages'], metadata['abstract'], metadata['doi'], metadata['url'], metadata_id))
        conn.commit()
    return metadata_id


def delete_metadata(metadata_id):
    '''
    Delete metadata record of a document by metadata_id in Table: metadata
    '''
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM metadata WHERE metadata_id = %s
        ''', (metadata_id,))
        conn.commit()
        cur.execute('''
        SELECT * FROM metadata WHERE metadata_id = %s
        ''', (metadata_id,))
        metadata = cur.fetchone()
        if metadata is None:
            return True
        else:
            return False


# handle files table
def get_filepath(file_id):
    '''
    Get filepath of a file by file_id from Table: files
    '''
    with conn.cursor() as cur:
        cur.execute('''
        SELECT filepath FROM files WHERE file_id = %s
        ''', (file_id,))
        if cur.fetchone() is None:
            return None
        filepath = cur.fetchone()[0]
    return filepath


def add_file(filepath: str) -> int:
    '''
    Create a new file record in Table: files
    '''
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO files (filepath)
        VALUES (%s)
        RETURNING file_id
        ''', (filepath,))
        file_id = cur.fetchone()[0]
        conn.commit()
    return file_id


def update_file(file_id, filepath):
    '''
    Update file record of a document by file_id in Table: files
    '''
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE files SET filepath = %s
        WHERE file_id = %s
        ''', (filepath, file_id))
        conn.commit()
    return file_id


def delete_file(file_id):
    '''
    Delete file record of a document by file_id in Table: files
    '''
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM files WHERE file_id = %s
        ''', (file_id,))
        conn.commit()
        cur.execute('''
        SELECT * FROM files WHERE file_id = %s
        ''', (file_id,))
        file = cur.fetchone()
        if file is None:
            return True
        else:
            return False


# delete
def delete_document(document_id):
    '''
    Delete document record of a document by document_id in Table: documents
    '''
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM documents WHERE document_id = %s
        ''', (document_id,))
        conn.commit()
        cur.execute('''
        SELECT * FROM documents WHERE document_id = %s
        ''', (document_id,))
        document = cur.fetchone()
        if document is None:
            return True
        else:
            return False
