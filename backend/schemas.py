from typing import List, Union

from pydantic import BaseModel


class AccountBase(BaseModel):
    email: str


class AccountCreate(AccountBase):
    password: str


class Account(AccountBase):
    id: int
    name: str
    account_type: str

    class Config:
        orm_mode = True