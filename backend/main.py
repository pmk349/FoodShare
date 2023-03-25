from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

from starlette.responses import RedirectResponse


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
async def main():
    return RedirectResponse(url="/docs/")


@app.post("/account/", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    # check that email does not exist already
    db_account = crud.get_account_by_email(db, email=account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_account(db=db, account=account)

@app.get("/account/{account_id}", response_model=schemas.Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.get_account_by_id(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@app.get("/accounts/", response_model=List[schemas.Account])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accounts = crud.get_accounts(db, skip=skip, limit=limit)
    return accounts



@app.post("/pantry/", response_model=schemas.Pantry)
def create_pantry(pantry: schemas.PantryCreate, db: Session = Depends(get_db)):
    # check that email does not exist already
    db_pantry = crud.get_pantry_by_address(db, address=pantry.address)
    if db_pantry:
        raise HTTPException(status_code=400, detail="Pantry already exists")
    return crud.create_pantry(db=db, pantry=pantry)

@app.get("/pantry/{pantry_id}", response_model=schemas.Pantry)
def read_pantry(pantry_id: int, db: Session = Depends(get_db)):
    db_pantry = crud.get_pantry_by_id(db, pantry_id=pantry_id)
    if db_pantry is None:
        raise HTTPException(status_code=404, detail="Pantry not found")
    return db_pantry

@app.get("/pantries/", response_model=List[schemas.Pantry])
def read_pantries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pantries = crud.get_pantries(db, skip=skip, limit=limit)
    return pantries

@app.post("/inventoryItem/", response_model=schemas.InventoryItem)
def create_inventory_item(inventoryItem: schemas.InventoryItemCreate, db: Session = Depends(get_db)):
    return crud.create_inventoryItem(db=db, inventoryItem=inventoryItem)

@app.get("/inventoryItem/{id}", response_model=schemas.InventoryItem)
def read_inventoryItem(id: int, db: Session = Depends(get_db)):
    db_inventoryItem= crud.get_inventoryItem_by_id(db, id=id)
    if db_inventoryItem is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return db_inventoryItem

@app.get("/inventoryItems/", response_model=List[schemas.InventoryItem])
def read_inventoryItems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    inventoryItems = crud.get_inventoryItems(db, skip=skip, limit=limit)
    return inventoryItems

@app.post("/transactionRequest/", response_model=schemas.TransactionRequest)
def create_trasactionRequest(transactionRequest: schemas.TransactionRequestCreate, db: Session = Depends(get_db)):
    # check that email does not exist already
    return crud.create_transactionRequest(db=db, transactionRequest=transactionRequest)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "127.0.0.1", port=8000)
