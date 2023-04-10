from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud, models, schemas, session

import endpoints

from database import SessionLocal, engine, get_db

from starlette.responses import RedirectResponse

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR,'templates')))
app.mount("/static", StaticFiles(directory =Path(__file__).parent.parent.absolute() / "static"), name="static")


app.include_router(endpoints.account.router)
app.include_router(endpoints.pantry.router)
app.include_router(endpoints.inventoryItem.router)
app.include_router(endpoints.transactionRequest.router)
app.include_router(endpoints.pantryShopper.router)

global SESSION_DATA
SESSION_DATA = dict()

@app.get('/')
def main(request: Request):
    session.init_session()
    return RedirectResponse(url="/signin/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "127.0.0.1", port=8000)
