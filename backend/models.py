from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique = True, index = True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    account_type = Column(String)


class Pantry(Base):
    __tablename__ = 'pantry'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique = True, index = True)
    manager_id = Column(Integer, unique = True, index = True)
    address = Column(String)

class Pantry_Shopper(Base):
    __tablename__ = 'pantry_shopper'

    pantry_id = Column(Integer, primary_key = True, index = True)
    shopper_id = Column(Integer, primary_key = True, index = True)
    notifications = Column(Boolean)

class Inventory_Item(Base):
    __tablename__ = 'inventory_item'

    id = Column(Integer, primary_key = True, index = True)
    item_type = Column(String, unique = True, index = True)
    quantity = Column(Integer)
    expiration_date = Column(String)
    summary = Column(String)
    # image = ...


class Inventory(Base):
    __tablename__ = 'inventory'

    pantry_id = Column(Integer, primary_key = True, index = True)
    item_id = Column(Integer, primary_key = True, index = True)


class TransactionRequest(Base):
    __tablename__ = 'transaction_request'

    id = Column(Integer, primary_key = True, index = True)
    shopper_id = Column(Integer)
    pantry_id = Column(Integer)
    item_id = Column(Integer)
    req_time = Column(String)
    req_status = Column(String) # Pending Approved Denied
    req_action = Column(String) # Receive vs Donate
    quantity = Column(Integer)
    summary = Column(String)
    anonymous = Column(Boolean)
