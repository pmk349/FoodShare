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

###NEED TO FINISH THIS###
@router.get("/manager-transactions", response_class=HTMLResponse, tags=["Inventory Item"])
def manager_transactions(request: Request, db: Session = Depends(get_db)):
    data = []
    data2 = []
    pending_transactions = []
    transactions = []
    account_id = main.SESSION_DATA["id"]
    pantries = crud.get_pantryIDs_by_managerID(db, account_id)
    print(pantries)
    for i in pantries:
        pending_transactions += crud.get_pending_transactions(db, i.id)
        transactions += crud.get_approved_denied_transactions(db, i.id)

    for x in pending_transactions:
        pantry_name = (crud.get_pantry_by_id(db, x.pantry_id)).name
        if x.anonymous == True:
            shopper_name = "Anonymous"
        else:
            shopper_name = (crud.get_account_by_id(db, x.shopper_id)).name
        data.append([pantry_name, shopper_name, x.request_time, x.request_action, x.summary, x.quantity])
    for x in transactions:
        pantry_name = (crud.get_pantry_by_id(db, x.pantry_id)).name
        if x.anonymous == True:
            shopper_name = "Anonymous"
        else:
            shopper_name = (crud.get_account_by_id(db, x.shopper_id)).name
        data2.append([pantry_name, shopper_name, x.request_time, x.request_action, x.summary, x.quantity, x.request_status])

    print(data)
    print(data2)
    return templates.TemplateResponse('manager-transactions.html',{'request': request,
                                                                   'data': data,
                                                                   'data2': data2})


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
