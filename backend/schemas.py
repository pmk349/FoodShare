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
    manager_id: int

    class Config:
        orm_mode = True

#########################################################
################## Pantry Shopper #######################
#########################################################

class PantryShopperBase(BaseModel):
    pass

class PantryShopperCreate(PantryShopperBase):
    pass

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
    id: int
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
    req_time: datetime
    req_action: str
    quantity: int
    summary: str
    anonymous: bool

class TransactionRequest(TransactionRequestBase):
    id: int
    req_status: str

    class Config:
        orm_mode = True
