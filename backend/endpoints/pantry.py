from typing import List

from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

from starlette.responses import RedirectResponse

from database import get_db

router = APIRouter()

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