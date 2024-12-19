from fastapi import FastAPI, HTTPException
from enum import Enum
from pydantic import BaseModel

app = FastAPI()

class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"

class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category

items = {
    0: Item(name="Hammer", price=9.99, count=20, id= 0, category=Category.TOOLS),
    1: Item(name="Screwdriver", price=5.99, count=20, id= 1, category=Category.TOOLS),
    2: Item(name="Apples", price=1.99, count=100, id= 2, category=Category.CONSUMABLES)
}

@app.get("/")
def index()-> dict[str, dict[int, Item]]:
    return {"items": items}

@app.get("/item/{item_id}")
def get_item(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id}, no found.")
    return items[item_id]
