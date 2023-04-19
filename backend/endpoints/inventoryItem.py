from typing import List
from fastapi import Depends, FastAPI, HTTPException, APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud, models, schemas, session
import main

from .pantry import your_pantries

from utils import utils
from database import SessionLocal, engine


from starlette.responses import RedirectResponse

from database import get_db

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR,'templates')))

router = APIRouter()

@router.get("/manager-inventories", response_class=HTMLResponse, tags=["Inventory Item"])
def manager_inventories(request: Request):
    return templates.TemplateResponse('manager-inventories.html',{'request': request})

@router.post("/inventoryItem/", response_model=schemas.InventoryItem, tags=["Inventory Item"])
def create_inventory_item(inventoryItem: schemas.InventoryItemCreate, db: Session = Depends(get_db)):
    return crud.create_inventoryItem(db=db, inventoryItem=inventoryItem) #TODO: DEBUG

@router.get("/inventoryItem/{item_id}", response_model=schemas.InventoryItem, tags=["Inventory Item"])
def read_inventoryItem(item_id: int, db: Session = Depends(get_db)):
    db_inventoryItem= crud.get_inventoryItem_by_id(db, inventoryItem_id=item_id)
    if db_inventoryItem is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return db_inventoryItem

@router.get("/inventoryItem_by_Pantry/{pantry_id}", response_model=List[schemas.InventoryItem], tags=["Inventory Item"])
def read_inventoryItem_by_pantryID(pantry_id: int, db: Session = Depends(get_db)):

    inventory = crud.get_inventory_by_pantryID(db, id=pantry_id)
    # if inventory is None:
    #     raise HTTPException(status_code=404, detail="Pantry inventory is empty")

    items = []
    for pair in inventory:
        item_id = pair.item_id
        items.append(crud.get_inventoryItem_by_id(db, inventoryItem_id=item_id))

    return items


@router.get("/inventoryItems/", response_model=List[schemas.InventoryItem], tags=["Inventory Item"])
def read_inventoryItems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    inventoryItems = crud.get_inventoryItems(db, skip=skip, limit=limit)
    return inventoryItems


## Create/Remove InventoryItems manually, for managers only (func. req. 9)
@router.post("/inventoryAdd/{pantry_id}", tags=["Inventory Item"])
def manager_create_inventory_item(inventoryItem: schemas.InventoryItemCreate, pantry_id: int, db: Session = Depends(get_db)):
    rtn = crud.create_inventoryItem(db=db, inventoryItem=inventoryItem) #TODO: TEST
    if rtn is None:
        raise HTTPException(status_code=404, detail="Item could not be created")

    rtn = crud.add_item_to_pantry(db=db, item_id=rtn.id, pantry_id=pantry_id)
    if rtn is None:
        raise HTTPException(status_code=404, detail="Inventory item could not be added")
@router.post("/inventoryRemove/{pantry_id}/{item_id}", tags=["Inventory Item"])
def manager_remove_inventory_item(pantry_id: int, item_id: int, db: Session = Depends(get_db)):
    rtn = crud.remove_item_from_inventory(db=db, pantry_id=pantry_id, item_id=item_id)
    if rtn is None:
        raise HTTPException(status_code=404, detail="Inventory item could not be removed from pantry")
