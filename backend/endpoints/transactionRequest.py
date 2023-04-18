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

@router.get("/manager-transactions", response_class=HTMLResponse, tags=["Inventory Item"])
def manager_transactions(request: Request):
    return templates.TemplateResponse('manager-transactions.html',{'request': request})

@router.post("/transactionRequest/", response_model=schemas.TransactionRequest, tags=["Transaction Request"])
def create_trasactionRequest(transactionRequest: schemas.TransactionRequestCreate, db: Session = Depends(get_db)):
    # check that email does not exist already

    # TODO: review the logic in this

    return crud.create_transactionRequest(db=db, transactionRequest=transactionRequest)

@router.post("/transactionRequest/{pantry_id}", response_model=List[schemas.TransactionRequest], tags=["Transaction Request"])
def get_pending_transactions(pantry_id: int, db: Session = Depends(get_db)):
    return crud.get_pending_transactions(db=db, pantry_id=pantry_id)
@router.post("/transactionHistory/{pantry_id}", response_model=List[schemas.TransactionRequest], tags=["Transaction Request"])
def get_transaction_history(pantry_id: int, db: Session = Depends(get_db)):
    return crud.get_transaction_history(db=db, pantry_id=pantry_id)

@router.post("/transactionRequest/{pantry_id}/{transaction_id}/{status}", tags=["Transaction Request"])
def update_pending_transaction(pantry_id: int, transaction_id: int, status: str, db: Session = Depends(get_db)):
    return crud.update_pending_transaction(db=db, pantry_id=pantry_id, transaction_id=transaction_id, status=status)
