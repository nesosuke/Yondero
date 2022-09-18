# mock data

# Database is using MongoDB

from pymongo import MongoClient

DB_HOST = 'db'
DB_PORT = 27017
DB_NAME = 'yondero'
DB_COLLECTION = 'items'

client = MongoClient(DB_HOST, DB_PORT)
db = client[DB_NAME]
collection = db[DB_COLLECTION]


def find_item(item_id: int) -> dict:
    '''
    find item from id
    '''
    item = collection.find_one({'id': item_id})
    if item is None:
        return {'error': 'item_id not found'}

    return item


def register_item(item: dict) -> int:
    '''
    register item
    '''
    item_id = collection.insert_one(item).inserted_id
    return {'success': 'item registered', 'id': item_id}


def update_item(item_id: int, item: dict) -> dict:
    '''
    update item
    '''
    if find_item(item_id) is None:
        return {'error': 'item_id not found'}

    collection.update_one({'id': item_id}, {'$set': item})
    return {'success': 'item updated'}


def delete_item(item_id: int) -> dict:
    '''
    delete item
    '''
    collection.delete_one({'id': item_id})

    if find_item(item_id) is None:
        return {'success': 'item deleted'}
    return {'error': 'something went wrong'}
