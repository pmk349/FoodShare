from typing import List

from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

from starlette.responses import RedirectResponse

from database import get_db

router = APIRouter()

@router.post("/transactionRequest/", response_model=schemas.TransactionRequest, tags=["Transaction Request"])
def create_trasactionRequest(transactionRequest: schemas.TransactionRequestCreate, db: Session = Depends(get_db)):
    # check that email does not exist already
    
    # TODO: review the logic in this
    
    return crud.create_transactionRequest(db=db, transactionRequest=transactionRequest)
    
## Approve/Deny Transaction
## View Transaction History
## (we probably also need something like get_pending_transactions)
