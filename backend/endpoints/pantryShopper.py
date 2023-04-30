from typing import List
from fastapi import Depends, FastAPI, HTTPException, APIRouter, Request, Form, status
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

@router.get("/shopper-pantrybrowser", response_class=HTMLResponse, tags=["Pantry"])
def shopper_pantrybrowser(request: Request, db: Session = Depends(get_db)):
    data = []
    account_id = main.SESSION_DATA["id"]
    db_account = crud.get_account_by_id(db, account_id=account_id)
    for i in crud.get_pantries(db):
        manager = crud.get_account_by_id(db, i.manager_id)
        data.append([i.name, i.address, manager.name])
    
    if main.SESSION_DATA["type"] == "shopper":
        return templates.TemplateResponse('SO-pantrybrowser.html',{'request': request,
                                                                    'data': data,
                                                                    'name': db_account.name})
    else:
        return templates.TemplateResponse('shopper-pantrybrowser.html',{'request': request,
                                                                    'data': data,
                                                                    'name': db_account.name})

@router.get("/join-pantry/{pantry_name}", tags=["Pantry Shopper"])
def join_pantry(pantry_name: str, db: Session = Depends(get_db)):
    pantry_id = (crud.get_pantryID_by_name(db, pantry_name))[0]
    rtn = crud.join_pantry(db=db, shopper_id=main.SESSION_DATA['id'], pantry_id=pantry_id)
    if rtn is None:
        raise HTTPException(status_code=404, detail="Internal Error")
    return RedirectResponse("/shopper-pantrybrowser", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/pantryShopper/{shopper_id}", response_model=List[schemas.Pantry], tags=["Pantry Shopper"])
def get_myPantries(shopper_id: int, db: Session = Depends(get_db)):
    myPantries = crud.get_myPantries_by_shopperID(db=db, shopper_id=shopper_id)

    pantryInfo = []
    for p in myPantries:
        pantryInfo.append(crud.get_pantry_by_id(db=db, pantry_id=p.pantry_id))

    return pantryInfo


## Toggle Notifications (func. req. 6) INCOMPLETE
@router.get("/pantryShopper/{shopper_id}/{pantry_id}/{notification_status}", tags=["Pantry Shopper"])
def toggle_notifications(shopper_id: int, pantry_id: int, notification_status: bool, db: Session = Depends(get_db)):
    rtn = crud.update_notifications(db=db, shopper_id=shopper_id, pantry_id=pantry_id,
                                    notification_status=notification_status)
    if rtn is None:
        raise HTTPException(status_code=404, detail="Internal Error")

