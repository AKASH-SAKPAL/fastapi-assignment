import models
from fastapi import FastAPI, Path, Query, Depends
from typing import Optional
from pydantic import BaseModel
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from models import Item
app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class ItemRequest(BaseModel):
    name: str
    price: Optional[float] = None
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get('/get-item/{id}')
def get_item(id: int = Path(None, description="The Id of the item you'd like to view", gt=0), db: Session = Depends(get_db)):
    db = SessionLocal()
    stock = db.query(Item).filter(Item.id == id).first()
    if stock is None:
        return {"Error": "Item ID does not exists."}
    return stock

@app.get('/get_by_name')
def get_item(name: str = Query(None, description="Name of item."), db: Session = Depends(get_db)):
    db = SessionLocal()
    stock = db.query(Item).filter(Item.name == name).first()
    if stock is None:
        return {"Error": "Name not exists."}
    return stock


@app.post('/create-item/{id}')
def create_item(id: int, item_request: ItemRequest,  db: Session = Depends(get_db)):
    stock = db.query(Item).filter(Item.id == id).first()
    if stock:
        return {"Error": "Item ID already exists."}
    data = Item()
    data.name = item_request.name
    data.price = item_request.price
    data.brand = item_request.brand
    db.add(data)
    db.commit()
    return {"Success": "Item Added"}


@app.put("/update-item/{id}")
def update_item(id: int, item: UpdateItem, db: Session = Depends(get_db)):
    db = SessionLocal()
    stock = db.query(Item).filter(Item.id == id).first()
    if stock is None:
        return {"Error": "Item ID does not exists."}

    if item.name != None:
        stock.name = item.name
    if item.price != None:
        stock.price = item.price
    if item.brand != None:
        stock.brand = item.brand
    db.add(stock)
    db.commit()
    return {"Success": "Item updated!"}


@app.delete("/delete-item/{id}")
def delete_item(id: int = Query(..., description="The Id of item to delete.", gt=0), db: Session = Depends(get_db)):
    db = SessionLocal()
    stock = db.query(Item).filter(Item.id == id).first()
    if stock is None:
        return {"Error": "Item ID does not exists."}

    stock = db.query(Item).filter(Item.id == id).delete()
    db.commit()
    return {"Success": "Item deleted!"}
