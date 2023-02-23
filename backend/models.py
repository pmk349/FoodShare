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

    # items = relationship("Item", back_populates="owner")


class Pantry(Base):
    __tablename__ = 'pantry'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique = True, index = True)
    manager_id = Column(Integer, unique = True, index = True)
    address = Column(String)


'''
Build these later...
'''
'''

class Pantry_Shopper(Base):
    __tablename__ = 'pantry_shopper'

    pantry_id = ...
    shopper_id = ...

class Inventory(Base):
    __tablename__ = 'inventory'

    pantry_id = ...
    item_id = ...

class Inventory_Item(Base):
    __tablename__ = 'inventory_item'

    id = ...
    item_type = ...
    quantity = ...
    expr_date = ...
    description = ...
    image = ...
class Transaction(Base):
    __tablename__ = 'transaction'

    id = ...
    shopper_id = ...
    pantry_id = ...
    item_id = ...
    req_time = ...
    req_status = ...
    req_action = ...
    quantity = ...
    description = ...

'''