from typing import List
from fastapi import Depends, FastAPI, HTTPException, APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud, models, schemas, session
import main
import datetime

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
    return templates.TemplateResponse('manager-transactions.html',{'request': request,
                                                                   'data': data,
                                                                   'data2': data2})

@router.get("/shopper-donaterecieve", response_model=schemas.TransactionRequest, tags=["Transaction Request"])
def shopper_donaterecieve(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse('shopper-donaterecieve.html',{'request': request})

@router.post("/create_transactionRequest/", response_model=schemas.TransactionRequest, tags=["Transaction Request"])
def create_transactionRequest(request: Request, db: Session = Depends(get_db), item_type: str = Form(), quantity: int = Form(), expiration_date: str = Form(), summary: str = Form(), anonymous: bool = Form()):
    current_time = datetime.datetime.now()
    time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
    crud.create_inventoryItem(db=db, inventoryItem=schemas.InventoryItemCreate(item_type=item_type, expiration_date=expiration_date, quantity=quantity, summary=summary, anonymous=anonymous))
    crud.create_transactionRequest(db=db, transactionRequest=schemas.TransactionRequestCreate(req_time = time_str, quantity = quantity, summary = summary, anonymous = anonymous))
    return RedirectResponse()

@router.post("/transactionRequest/{pantry_id}", response_model=List[schemas.TransactionRequest], tags=["Transaction Request"])
def get_pending_transactions(pantry_id: int, db: Session = Depends(get_db)):
    return crud.get_pending_transactions(db=db, pantry_id=pantry_id)
@router.post("/transactionHistory/{pantry_id}", response_model=List[schemas.TransactionRequest], tags=["Transaction Request"])
def get_transaction_history(pantry_id: int, db: Session = Depends(get_db)):
    return crud.get_transaction_history(db=db, pantry_id=pantry_id)

@router.post("/transactionRequest/{pantry_id}/{transaction_id}/{status}", tags=["Transaction Request"])
def update_pending_transaction(pantry_id: int, transaction_id: int, status: str, db: Session = Depends(get_db)):
    return crud.update_pending_transaction(db=db, pantry_id=pantry_id, transaction_id=transaction_id, status=status)
