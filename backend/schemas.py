from typing import List, Union

from pydantic import BaseModel


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


class PantryBase(BaseModel):
    address: str


class PantryCreate(PantryBase):
    name: str


class Pantry(PantryBase):
    id: int
    manager_id: int

    class Config:
        orm_mode = True