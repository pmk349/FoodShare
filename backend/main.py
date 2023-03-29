from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas

import endpoints

from database import SessionLocal, engine, get_db

from starlette.responses import RedirectResponse

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(endpoints.account.router)
app.include_router(endpoints.pantry.router)
app.include_router(endpoints.inventoryItem.router)
app.include_router(endpoints.transactionRequest.router)
app.include_router(endpoints.pantryShopper.router)

@app.get('/')
async def main():
    return RedirectResponse(url="/docs/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "127.0.0.1", port=8000)
