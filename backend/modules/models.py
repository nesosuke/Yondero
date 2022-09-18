from pydantic import BaseModel

class Item(BaseModel):
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
    item_id: int | None = None
    item: Item
