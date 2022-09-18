from pydantic import BaseModel


class Item(BaseModel):
    '''
    Item={
        "entry_type": "article",
        "title": "title",
        }
    '''

    entry_type: str
    title: str
    author: str | None = None
    journal: str | None = None
    volume: int | None = None
    number: int | None = None
    pages: str | None = None
    year: int | None = None
    month: int | None = None
    note: str | None = None
    citekey: str | None = None


class Body(BaseModel):
    '''
    Body={item_id: int, item: Item}
    '''

    item_id: int | None = None
    item: Item
