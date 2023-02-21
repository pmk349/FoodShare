from sqlalchemy.orm import Session
from utils import utils

import models, schemas


def get_account_by_id(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()


def get_account_by_email(db: Session, email: str):
    '''
    Email is unique in the DDL.
    '''
    return db.query(models.Account).filter(models.Account.email == email).first()


def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    '''
    What does this funciton do?

    Just returns an array of accounts?
    '''
    return db.query(models.Account).offset(skip).limit(limit).all()


def create_account(db: Session, account: schemas.AccountCreate):
    '''
    Do we need to check that account_email is not already
    in the database?

    Email is unique in the DDL.
    '''

    hashed_password = utils.encrypt_password(account.password)
    db_account = models.Account(email=account.email, hashed_password=hashed_password)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


'''
    List of CRUD operations to create
    
1. Shopper/Manager
    a. join a pantry -- read + update
    b. make a request -- ...
2. Only Manager
    a. manually edit pantry inventory -- read + update/delete
    b. respond to request -- read + update
3. 


'''