from typing import List
from fastapi import Depends, FastAPI, HTTPException, APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud, models, schemas, session
import main
from utils import utils
from database import SessionLocal, engine

from starlette.responses import RedirectResponse

from database import get_db

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR,'templates')))


router = APIRouter()


@router.get("/signin", response_class=HTMLResponse)
def signin(request: Request):
    return templates.TemplateResponse('signin.html',{'request': request})

@router.post("/signin", response_class=HTMLResponse)
def signin(request: Request, db: Session = Depends(get_db),  email: str = Form(), password: str = Form()):
    ''' Only working on Managers. '''
    db_account = crud.get_account_by_email(db, email = email)

    if db_account == None:
        raise HTTPException(status_code=400, detail="No account with that email exists")
    else:
        if db_account.password==utils.encrypt_password(password):
            if db_account.account_type=="shopper":
                return templates.TemplateResponse('signin.html',{'request': request})
            else:
                session.login(id=db_account.id, type='manager')
                return templates.TemplateResponse('manager-dashboard.html',{'request': request})
        else:
            return '''<dialog open>
                            <p>Incorrect Password</p>
                            <form action = "/signin" method="get">
                                <button> OK </button>
                            </form>
                        </dialog>
            '''

@router.get("/signup", response_class=HTMLResponse)
def signup(request: Request):
    return templates.TemplateResponse('signup.html', {'request': request})

@router.post("/signup", response_model = schemas.Account)
def signup(request: Request, db: Session = Depends(get_db), name: str = Form(), email: str = Form(), password: str = Form(), account_type: str = Form()):
    db_account = crud.get_account_by_email(db, email=email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    crud.create_account(db=db, account=schemas.AccountCreate(name = name, email = email, password=password, account_type=account_type))
    if account_type == "shopper":
        return True
    else:
        session.login(id=db_account.id, type='manager')
        return templates.TemplateResponse('manager-dashboard.html',{'request': request})


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


