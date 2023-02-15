from utils.default import *
from utils.postgres_utils import *

from sqlalchemy.engine import Engine



def join_pantry(shopper_id: int, pantry_id: int, engine: Engine): # TODO: add typing/output
    '''
    :param shopper_id: the id of the shopper
    :param pantry_id: the pantry to join
    '''

    if dummy_security_measure():
        '''
        Security:
        
        1. shopper_id exists
        2. pantry_id exists
        '''

        sql=f'''
        begin
        insert into pantry_shopper
        values ({shopper_id},{pantry_id})
        commit;
        '''

        # commit sql
        return exec_sql(engine, sql)
    return ...


def make_request()


