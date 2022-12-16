-- sqlite3 schema.sql --
CREATE DATABASE IF NOT EXISTS items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT,
    annote TEXT,
    booktitle TEXT,
    chapter TEXT,
    doi TEXT,
    edition TEXT,
    editor TEXT,
    howpublished TEXT,
    author TEXT,
    institution TEXT,
    journal TEXT,
    issn TEXT,
    month TEXT,
    note TEXT,
    number TEXT,
    organization TEXT,
    pages TEXT,
    publisher TEXT,
    school TEXT,
    series TEXT,
    title TEXT,
    type TEXT,
    volume TEXT,
    year TEXT,
    url TEXT,
    filepath TEXT,
    filehash TEXT,
    updated_at TEXT,
    created_at TEXT
);
