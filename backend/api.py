# main.py
from fastapi import FastAPI

from modules import database

from modules.models import Item, Body


app = FastAPI()

origins = [
    "http://localhost/api",
    "http://localhost:8000/api",
]


@app.get("/")
def read_root():
    '''
    get root
    '''
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def get_item(item_id):
    '''
    get item from id
    '''
    result = database.find_item(item_id)

    return result


@app.post("/items", response_model=Item)
def post_item(item: Item):
    '''
    register item
    '''

    result = database.register_item(item)

    return result


@app.put("/items", response_model=Body)
def put_item(body: Body):
    '''
    update item
    '''
    item_id = body.item_id
    item = body.item.dict()

    return database.update_item(item_id, item)


@app.delete("/items", response_model=Body)
def delete_item(body: Body):
    '''
    delete item
    '''
    item_id = body.item_id

    return database.delete_item(item_id)
