from typing import List

from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

from starlette.responses import RedirectResponse

from database import get_db

router = APIRouter()

@router.post("/pantryShopper/{shopper_id}/{pantry_id}", tags=["Pantry Shopper"])
def join_pantry(shopper_id: int, pantry_id: int, db: Session = Depends(get_db)):
    rtn = crud.join_pantry(db=db, shopper_id=shopper_id, pantry_id=pantry_id)
    if rtn is None:
        raise HTTPException(status_code=404, detail="Internal Error")

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

