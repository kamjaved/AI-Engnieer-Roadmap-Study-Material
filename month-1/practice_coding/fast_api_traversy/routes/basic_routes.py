from fastapi import APIRouter

router = APIRouter(tags=["Basic Router"])

items = [
    {"id": 1, "name": "Item One"},
    {"id": 2, "name": "Item Two"},
    {"id": 3, "name": "Item Three"},
    {"id": 4, "name": "Item Four"},
    {"id": 5, "name": "Item Five"},
]


@router.get("/health")
def health_checker():
    return {"status": "ok"}


@router.get("/items")
def get_items():
    return items


@router.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    return {"Error": "Item not found"}


@router.get("/items_with_query")
def get_item_with_query(skip: int = 0, limit: int = 2):
    return items[skip : skip + limit]


@router.post("/items")
def create_item(item: dict):
    items.append(item)
    return items
