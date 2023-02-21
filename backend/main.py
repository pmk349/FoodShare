from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

import uvicorn

print("hi")

models.Base.metadata.create_all(bind=engine)

print("hello")
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/account/", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):

    # check that email does not exist already
    db_account = crud.get_account_by_email(db, email=account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_account(db=db, account=account)


@app.get("/account/", response_model=List[schemas.Account])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accounts = crud.get_accounts(db, skip=skip, limit=limit)
    return accounts


@app.get("/accounts/{account_id}", response_model=schemas.Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")