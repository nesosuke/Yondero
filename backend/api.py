# main.py
from fastapi import FastAPI
from pydantic import BaseModel

from modules import database

from modules.models import Item, Body


app = FastAPI()

origins = [
    "http://localhost",
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


@app.post("/items")
def post_item(body: Body):
    '''
    register item
    '''
    item = body.item.dict()

    result = database.register_item(item)

    return result


@app.put("/items")
def put_item(body: Body):
    '''
    update item
    '''
    item_id = body.item_id
    item = body.item.dict()

    return database.update_item(item_id, item)


@app.delete("/items")
def delete_item(body: Body):
    '''
    delete item
    '''
    item_id = body.item_id

    return database.delete_item(item_id)
