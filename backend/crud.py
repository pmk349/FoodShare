from sqlalchemy.orm import Session
from sqlalchemy import func
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
    id = (db.query(func.max(models.Account.id)).one())[0] + 1
    hashed_password = utils.encrypt_password(account.password)
    db_account = models.Account(id = id, name = account.name, email=account.email, password=hashed_password, account_type = account.account_type)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def get_pantry_by_id(db: Session, pantry_id: int):
    return db.query(models.Pantry).filter(models.Pantry.id == pantry_id).first()

def get_pantry_by_address(db: Session, address: str):
    '''
    Email is unique in the DDL.
    '''
    return db.query(models.Pantry).filter(models.Pantry.address == address).first()

def get_pantries(db: Session, skip: int = 0, limit: int = 100):
    '''
    What does this funciton do?

    Just returns an array of accounts?
    '''
    return db.query(models.Pantry).offset(skip).limit(limit).all()

def create_pantry(db: Session, pantry: schemas.PantryCreate):
    '''
    Do we need to check that account_email is not already
    in the database?

    Email is unique in the DDL.
    '''
    id = (db.query(func.max(models.Pantry.id)).one())[0] + 1
    db_pantry = models.Pantry(id = id, name = pantry.name, manager_id = None, address = pantry.address)
    db.add(db_pantry)
    db.commit()
    db.refresh(db_pantry)
    return db_pantry


def get_inventoryItem_by_id(db: Session, inventoryItem_id: int):
    return db.query(models.Inventory_Item).filter(models.Inventory_Item.id == inventoryItem_id).first()

def create_inventoryItem(db: Session, inventoryItem: schemas.InventoryItem):
    '''
    Do we need to check that account_email is not already
    in the database?

    Email is unique in the DDL.
    '''
    if (db.query(func.max(models.Inventory_Item.id)).one())[0] != None:
        id = (db.query(func.max(models.Inventory_Item.id)).one())[0] + 1
    else:
        id = 1
    db_inventoryItem = models.Inventory_Item(id = id, item_type = inventoryItem.item_type, quantity = inventoryItem.quantity, expr_date = inventoryItem.expr_date, description = inventoryItem.description)
    db.add(db_inventoryItem)
    db.commit()
    db.refresh(db_inventoryItem)
    return db_inventoryItem



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