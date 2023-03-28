from typing import List

from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

from starlette.responses import RedirectResponse

from database import get_db

router = APIRouter()

@router.post("/inventoryItem/", response_model=schemas.InventoryItem, tags=["Inventory Item"])
def create_inventory_item(inventoryItem: schemas.InventoryItemCreate, db: Session = Depends(get_db)):
    return crud.create_inventoryItem(db=db, inventoryItem=inventoryItem)

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
