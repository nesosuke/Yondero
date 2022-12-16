# Manage DB(sqlite3)
import sqlite3
DB_NAME = 'test.sqlite3'
tables = ['entries']
SCHEMA_FILE = 'schema.sql'
key_to_remove = ['entry_id', 'updated_at',
                 'created_at', 'filepath', 'filehash']


def connect_db():
    '''
    Connect to DB
    '''
    conn = sqlite3.connect(DB_NAME)
    return conn


def init_db():
    '''
    Initialize DB, using schema.sql
    '''

    conn = connect_db()
    cur = conn.cursor()
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as schema:
        cur.executescript(schema.read())
    conn.commit()
    conn.close()


def init_values(body: object):
    '''
    Initialize values of body

    Args:
        body: body to initialize

    Returns:
        body: body initialized with None
    '''
    body['address'] = body['address'] if 'address' in body else None
    body['annote'] = body['annote'] if 'annote' in body else None
    body['author'] = body['author'] if 'author' in body else None
    body['booktitle'] = body['booktitle'] if 'booktitle' in body else None
    body['chapter'] = body['chapter'] if 'chapter' in body else None
    body['doi'] = body['doi'] if 'doi' in body else None
    body['edition'] = body['edition'] if 'edition' in body else None
    body['editor'] = body['editor'] if 'editor' in body else None
    body['howpublished'] = body['howpublished'] if 'howpublished' in body else None
    body['institution'] = body['institution'] if 'institution' in body else None
    body['journal'] = body['journal'] if 'journal' in body else None
    body['issn'] = body['issn'] if 'issn' in body else None
    body['month'] = body['month'] if 'month' in body else None
    body['note'] = body['note'] if 'note' in body else None
    body['number'] = body['number'] if 'number' in body else None
    body['organization'] = body['organization'] if 'organization' in body else None
    body['pages'] = body['pages'] if 'pages' in body else None
    body['publisher'] = body['publisher'] if 'publisher' in body else None
    body['school'] = body['school'] if 'school' in body else None
    body['series'] = body['series'] if 'series' in body else None
    body['title'] = body['title'] if 'title' in body else None
    body['volume'] = body['volume'] if 'volume' in body else None
    body['year'] = body['year'] if 'year' in body else None
    body['url'] = body['url'] if 'url' in body else None
    return body


def get_entry(entry_id: int) -> object:
    '''
    Get an entry from DB

    Args:
        entry_id: id of entry

    Returns:
        entry: entry

    '''
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(
        'SELECT * FROM entries WHERE entry_id=?', (entry_id,)).fetchone()

    if result:
        entry = dict(result)
        for key in key_to_remove:
            entry.pop(key)
        return entry
    else:
        return None


def insert_entry(body: object) -> object:
    '''
    Add an entry to DB

    Args:
        body: body of entry to add

    Returns:
        body: body of entry added
    '''
    body = init_values(body)
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('INSERT INTO entries (address, annote, booktitle, chapter, doi, edition, editor, howpublished, author, institution, journal, issn, month, note, number, organization, pages, publisher, school, series, title, entry_type, url, volume, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (body['address'], body['annote'], body['booktitle'], body['chapter'], body['doi'], body['edition'], body['editor'], body['howpublished'], body['author'], body['institution'], body['journal'], body['issn'], body['month'], body['note'], body['number'], body['organization'], body['pages'], body['publisher'], body['school'], body['series'], body['title'], body['entry_type'], body['url'], body['volume'], body['year']))
    conn.commit()

    # check if added successfully
    result = cur.execute(
        'SELECT * FROM entries WHERE entry_id=?', (cur.lastrowid,)).fetchone()
    conn.close()

    result = dict(result)
    for key in key_to_remove:
        result.pop(key)
    if result == body:
        return body
    else:
        return None


def update_entry(entry_id: int, body: object) -> object:
    '''
    Update an entry in DB

    Args:
        entry_id: id of entry
        body: body of entry to update

    Returns:
        body: body of entry updated

    Note:
        Body includes "address", "annote", "booktitle", "chapter", "doi", "edition", "editor", "howpublished", "author", "institution", "journal", "issn", "month", "note", "number", "organization", "pages", "publisher", "school", "series", "title", "entry_type", "url", "volume", "year"
    '''
    body = init_values(body)
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('UPDATE entries SET address=?, annote=?, booktitle=?, chapter=?, doi=?, edition=?, editor=?, howpublished=?, author=?, institution=?, journal=?, issn=?, month=?, note=?, number=?, organization=?, pages=?, publisher=?, school=?, series=?, title=?, entry_type=?, url=?, volume=?, year=? WHERE entry_id=?',
                (body['address'], body['annote'], body['booktitle'], body['chapter'], body['doi'], body['edition'], body['editor'], body['howpublished'], body['author'], body['institution'], body['journal'], body['issn'], body['month'], body['note'], body['number'], body['organization'], body['pages'], body['publisher'], body['school'], body['series'], body['title'], body['entry_type'], body['url'], body['volume'], body['year'], entry_id))
    conn.commit()

    # check if updated successfully
    result = cur.execute(
        'SELECT * FROM entries WHERE entry_id=?', (entry_id,)).fetchone()
    conn.close()

    result = dict(result)
    for key in key_to_remove:
        result.pop(key)
    if result == body:
        return body
    else:
        return None


def delete_entry(entry_id: int) -> None | str:
    '''
    Delete an entry from DB

    Args:
        entry_id: id of entry

    Returns:
        None if success
    '''

    conn = connect_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM entries WHERE entry_id=?', (entry_id,))
    conn.commit()
    conn.close()

    # check if deleted successfully
    conn = connect_db()
    cur = conn.cursor()
    result = cur.execute(
        'SELECT * FROM entries WHERE entry_id=?', (entry_id,)).fetchone()

    if result:
        return 'Failed to delete entry'
    else:
        return None


def get_all_entries() -> list:
    '''
    Get all entries from DB

    Returns:
        entries: list of entries

    '''
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute('SELECT * FROM entries').fetchall()
    conn.close()

    entries = [dict(entry) for entry in result]
    for entry in entries:
        for key in key_to_remove:
            entry.pop(key)
    return entries


def update_filepath(entry_id: int, filepath: str) -> str:
    '''
    Update filepath of an entry in DB

    Args:
        entry_id: id of entry
        filepath: filepath of entry to update

    Returns:
        filepath: filepath of entry updated
    '''
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('UPDATE entries SET filepath=? WHERE entry_id=?',
                (filepath, entry_id))

    # get updated entry
    cur.execute('SELECT * FROM entries WHERE entry_id=?', (entry_id,))
    conn.commit()
    conn.close()

    # check if updated successfully
    if cur.fetchone()['filepath'] == filepath:
        return filepath
    else:
        return 'Error'


def get_filepath(entry_id: int) -> str:
    '''
    Get filepath of an entry from DB

    Args:
        entry_id: id of entry

    Returns:
        filepath: filepath of entry
    '''
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM entries WHERE entry_id=?', (entry_id,))
    conn.commit()
    conn.close()

    # check if updated successfully
    return cur.fetchone()['filepath']
