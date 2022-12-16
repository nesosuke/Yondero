from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter
from modules import db
from modules.models import Entry

router = APIRouter(prefix='/api/v1')
# initialize database
db.init_db()


@router.get('/entry')
def all_entry():
    result = db.get_all_entries() if db.get_all_entries() else 'No entries found'

    return result


@router.post('/entry')
def create_entry(entry: Entry):
    data = jsonable_encoder(entry)

    result = db.insert_entry(data)

    return result


@router.get('/entry/{entry_id}')
def get_entry(entry_id: int):
    result = db.get_entry(entry_id) if db.get_entry(
        entry_id) else 'No entry found'

    return result


@router.put('/entry/{entry_id}')
def update_entry(entry_id: int, entry: Entry):
    data = jsonable_encoder(entry)

    result = db.update_entry(entry_id, data)

    return result


@router.delete('/entry/{entry_id}', status_code=204)
def delete_entry(entry_id: int):
    result = db.delete_entry(entry_id)

    if result is None:
        return None
    else:
        return result
