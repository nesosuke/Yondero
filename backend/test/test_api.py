import pytest


mock_data_to_find = {'id': 1,
                     'entry_type': 'article',  # required
                     'title': 'title',  # required
                     'author': 'author',
                     'journal': 'journal',
                     'volume': 1,
                     'number': 1,
                     'pages': '1-10',
                     'year': 2022,
                     'month': 1,
                     'note': 'note',
                     'key': 'key',  # citation key
                     'attachments': 'attachments_path',  # attachment file path
                     'created_at': '2021-01-01 00:00:00',  # datetime, ISO 8601
                     'updated_at': '2021-01-01 00:00:00',   # datetime, ISO 8601
                     'deleted_at': 'none',  # datetime, ISO 8601 or 'none'
                     "deleted": False
                     }

mock_data_to_register = {
    'entry_type': 'article',
    'title': 'title'
}

mock_data_to_update = {
    'entry_type': 'article',
    'title': 'title_updated'
}
