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
    db_account = models.Account(id = id, 
                                name = account.name, 
                                email=account.email, 
                                password=hashed_password, 
                                account_type = account.account_type)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

#########################################################
################ SHOPPER FUNCTIONS ######################
#########################################################

def get_pantries(db: Session, skip: int = 0, limit: int = 100):
    '''
    Return an array of accounts. (README-UserStory-A1A)
    '''
    return db.query(models.Pantry).offset(skip).limit(limit).all()


def get_pantry_by_id(db: Session, pantry_id: int):
    '''
    Return info about a pantry/select a pantry. (README-UserStory-A1B)
    '''
    return db.query(models.Pantry).filter(models.Pantry.id == pantry_id).first()


def get_pantry_by_address(db: Session, address: str):
    '''
    Email is unique in the DDL.
    '''
    return db.query(models.Pantry).filter(models.Pantry.address == address).first()



def join_pantry(db: Session, shopper_id: int, pantry_id: int):
    '''
    No return. Update pantry-shopper. (README-UserStory-A1B)
    '''
    db_pantryShopper = models.Pantry_Shopper(pantry_id = pantry_id,
                                            shopper_id = shopper_id,
                                            notifications = True)
    db.add(db_pantryShopper)
    db.commit()
    db.refresh(db_pantryShopper)
    return db_pantryShopper


def get_myPantries_by_shopperID(db: Session, shopper_id: int):
    return db.query(models.Pantry_Shopper).filter(models.Pantry_Shopper.shopper_id == shopper_id)


# def toggle_notifications(...):
#     '''
#     No return. Update notification in pantry_shopper. (README-UserStory-A2B)
#     '''
#     pass


def create_transactionRequest(db: Session, transactionRequest: schemas.TransactionRequestCreate):
    '''
    (README-UserStory-A3/A4)
    '''
    if (db.query(func.max(models.TransactionRequest.id)).one())[0] != None:
        id = (db.query(func.max(models.TransactionRequest.id)).one())[0] + 1
    else:
        id = 1
    db_transactionRequest = models.TransactionRequest(id = id,
                                                      shopper_id = transactionRequest.name,
                                                      pantry_id = transactionRequest.pantry_id,
                                                      item_id = transactionRequest.item_id,
                                                      req_time = transactionRequest.req_time,
                                                      req_status = transactionRequest.req_status,
                                                      req_action = transactionRequest.req_action,
                                                      quantity = transactionRequest.quantity,
                                                      summary = transactionRequest.summary,
                                                      anonymous = transactionRequest.anonymous)
    db.add(db_transactionRequest)
    db.commit()
    db.refresh(db_transactionRequest)
    return db_transactionRequest

#########################################################
################ MANGER FUNCTIONS #######################
#########################################################


def create_pantry(db: Session, pantry: schemas.PantryCreate):
    '''
    (README-UserStory-B2).
    '''

    if (db.query(func.max(models.Pantry.id)).one())[0] != None:
        id = (db.query(func.max(models.Pantry.id)).one())[0] + 1
    else:
        id = 1
    db_pantry = models.Pantry(id = id,
                              name = pantry.name,
                              manager_id = None,
                              address = pantry.address)
    db.add(db_pantry)
    db.commit()
    db.refresh(db_pantry)
    return db_pantry


#########################################################
################## TRANSACTIONS/MISC ####################
#########################################################

def get_inventoryItem_by_id(db: Session, inventoryItem_id: int):
    return db.query(models.Inventory_Item).filter(models.Inventory_Item.id == inventoryItem_id).first()

def get_inventoryItems(db: Session, skip: int = 0, limit: int = 100):
    '''
    Return an array of accounts. (README-UserStory-A1A)
    '''
    return db.query(models.Inventory_Item).offset(skip).limit(limit).all()

def get_inventory_by_pantryID(db: Session, id: int):
    '''
    Return an array of accounts. (README-UserStory-A1A)
    '''
    return db.query(models.Inventory).filter(models.Inventory.pantry_id == id).all()

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
    db_inventoryItem = models.Inventory_Item(id = id,
                                             item_type = inventoryItem.item_type,
                                             quantity = inventoryItem.quantity,
                                             expr_date = inventoryItem.experation_date,
                                             description = inventoryItem.description)
    db.add(db_inventoryItem)
    db.commit()
    db.refresh(db_inventoryItem)
    return db_inventoryItem




