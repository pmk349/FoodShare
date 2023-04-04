from typing import List

from fastapi import Depends, FastAPI, HTTPException, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

from starlette.responses import RedirectResponse

from database import get_db

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR,'templates')))

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse('login.html',{'request': request})

@router.post("/account/", response_model=schemas.Account, tags=["account"])
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    # check that email does not exist already
    db_account = crud.get_account_by_email(db, email=account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_account(db=db, account=account)

@router.get("/account/{account_id}", response_model=schemas.Account, tags=["account"])
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.get_account_by_id(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@router.get("/accounts/", response_model=List[schemas.Account], tags=["account"])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accounts = crud.get_accounts(db, skip=skip, limit=limit)
    return accounts


