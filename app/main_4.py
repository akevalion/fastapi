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

Selection = dict[
    str, str | int | float | Category | None
]
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

@app.post("/add_item")
def add_item(item: Item) -> dict[str, Item]:
    if item.id  in items:
        raise HTTPException(status_code=404, detail=f"Item with id {item.id} already exists.")
    items[item.id]= item
    return {"added": item}
@app.get("/items/")
def query_item_by_parameters(
    name: str | None = None,
    price: float | None = None,
    count: int | None = None,
    category: Category | None = None,
) -> dict[str, Selection | list[Item]]:
    def check_item(item: Item):
        """Check if the item matches the query arguments from the outer scope."""
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count != count,
                category is None or item.category is category,
            )
        )

    selection = [item for item in items.values() if check_item(item)]
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection,
    }
