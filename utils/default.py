from utils.postgres_utils import *
from random import random
from sqlalchemy.engine import Engine
import hashlib
import datetime

def dummy_security_measure() -> bool:
    '''
    To replace with actual security...
    '''

    cond = True
    return cond


# returns an encrypted password
def encrypt_password(password: str) -> str:
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()

# returns a new, unique id for any given table
def generate_id(table: str, engine: Engine) -> int:
    flag=True
    while flag:
        rand_id=random.randint(0, 9999999)
        sql=f'''
        select id
        from {table}
        where id={rand_id};
        '''
        flag=exec_sql(engine, sql)
    return rand_id
