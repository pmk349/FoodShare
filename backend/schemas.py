from typing import List, Union

from pydantic import BaseModel
from datetime import date, datetime

#########################################################
##################### Account ###########################
#########################################################

class AccountBase(BaseModel):
    email: str


class AccountCreate(AccountBase):
    name: str
    password: str
    account_type: str


class Account(AccountBase):
    id: int

    class Config:
        orm_mode = True

#########################################################
###################### Pantry ###########################
#########################################################

class PantryBase(BaseModel):
    address: str


class PantryCreate(PantryBase):
    name: str


class Pantry(PantryBase):
    name: str

    class Config:
        orm_mode = True

#########################################################
################## Pantry Shopper #######################
#########################################################

class PantryShopperBase(BaseModel):
    pass

class PantryShopperCreate(PantryShopperBase):
    notifications: bool

class PantryShopper(PantryShopperBase):
    pantry_id: int
    shopper_id: int

    class Config:
        orm_mode = True

#########################################################
################## Inventory Item #######################
#########################################################

class InventoryItemBase(BaseModel):
    item_type: str


class InventoryItemCreate(InventoryItemBase):
    quantity: int
    expiration_date: date
    summary: str

class InventoryItem(InventoryItemBase):
    #id: int
    quantity: int
    expiration_date: date
    summary: str

    class Config:
        orm_mode = True


#########################################################
#################### Inventory ##########################
#########################################################

class InventoryBase(BaseModel):
    pass


class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    pantry_id: int
    item_id: int

    class Config:
        orm_mode = True

#########################################################
############### Transaction Request #####################
#########################################################

class TransactionRequestBase(BaseModel):
    shopper_id: int
    pantry_id: int
    item_id: int

class TransactionRequestCreate(TransactionRequestBase):
    req_time: str
    req_status: str
    req_action: str
    quantity: str
    summary: str
    anonymous: bool

class TransactionRequest(TransactionRequestBase):
    id: int

    class Config:
        orm_mode = True