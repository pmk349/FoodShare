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

@router.post("/create_pantry", response_class=HTMLResponse, tags=["Pantry"])
def create_pantry(request: Request, db: Session = Depends(get_db),  name: str = Form(), street: str = Form(), city: str = Form(), state: str = Form(), zip: str = Form()):
    address = street + " " + city + " " + state + " " + zip
    db_pantry = crud.get_pantry_by_address(db, address=address)
    if db_pantry:
        raise HTTPException(status_code=400, detail="Pantry already exists")
    crud.create_pantry(db=db, pantry=schemas.PantryCreate(name = name, address = address))
    return RedirectResponse("/manager-dashboard", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/your_pantries", response_model=List[schemas.Pantry], tags=["Pantry"])
def your_pantries(db: Session = Depends(get_db)):
    id = main.SESSION_DATA['id']
    pantries = crud.get_pantries_by_managerID(db, id)
    return pantries


@router.get("/shopper-pantrybrowser", response_class=HTMLResponse, tags=["Pantry"])
def shopper_pantrybrowser(request: Request, db: Session = Depends(get_db)):
    data = []
    
    for i in crud.get_pantries(db):
        manager = crud.get_account_by_id(db, i.manager_id)
        data.append([i.name, i.address, manager.name])
    return templates.TemplateResponse('shopper-pantrybrowser.html',{'request': request,
                                                                    'data': data})

@router.get("/shopper-mypantries", response_class=HTMLResponse, tags=["Pantry"])
def shopper_mypantries(request: Request, db: Session = Depends(get_db)):
    data = []
    my_pantries = crud.get_myPantries_by_shopperID(db, main.SESSION_DATA["id"])
    for i in my_pantries:
        pantry = crud.get_pantry_by_id(db, i.pantry_id)
        manager_name = (crud.get_account_by_id(db, pantry.manager_id)).name
        data.append([pantry.name, pantry.address, manager_name])

    return templates.TemplateResponse('shopper-mypantries.html',{'request': request,
                                                                 'data': data})


@router.post("/pantry/", response_model=schemas.Pantry, tags=["Pantry"])
def create_pantry(pantry: schemas.PantryCreate, db: Session = Depends(get_db)):
    # check that email does not exist already
    db_pantry = crud.get_pantry_by_address(db, address=pantry.address)
    if db_pantry:
        raise HTTPException(status_code=400, detail="Pantry already exists")
    return crud.create_pantry(db=db, pantry=pantry)

@router.get("/pantry/{pantry_id}", response_model=schemas.Pantry, tags=["Pantry"])
def read_pantry(pantry_id: int, db: Session = Depends(get_db)):
    db_pantry = crud.get_pantry_by_id(db, pantry_id=pantry_id)
    if db_pantry is None:
        raise HTTPException(status_code=404, detail="Pantry not found")
    return db_pantry

@router.get("/pantries/", response_model=List[schemas.Pantry], tags=["Pantry"])
def read_pantries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pantries = crud.get_pantries(db, skip=skip, limit=limit)
    return pantries