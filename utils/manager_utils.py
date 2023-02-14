from utils.default import *
from utils.postgres_utils import *

from sqlalchemy.engine import Engine


def manual_edit_inventory(item_id: int, manager_id: int, engine: Engine,
                          quantity = None,
                          expr_date = None,
                          description = None,
                          image = None) -> bool:
    '''
    Allow a Manager to manually edit the following fields of items in their pantries:

            Attr            Postgres      Python
        1. Quantity     :     int      :   int
        2. Expr Date    :    date      : datetime.date
        3. Description  : varchar(200) :   str
        4. Image        :   bytea      :

    :param item_id:
    :param manager_id: corresponds to id in Account table
    :param engine: corresponds to id in Inventory_Item table
    :return: bool
    '''


    # 1. check that manager_id is of pantry of item
    def _manager_item(item_id, manager_id, engine) -> bool:
        sql=f'''
        select *
        from pantry as p, inventory as i
        where p.id = i.pantry_id
            and p.manager_id = {manager_id}
            and i.item_id = {item_id};
        '''
        return exec_sql(engine, sql)


    if not _manager_item(item_id, manager_id, engine):
        raise Warning('...') #TODO: replace this
        return False

    # check if params exist
    params = {
        "quantity": quantity,
        "expration_date": expr_date,
        "description" : description,
        "image" : image
    }

    sql='''
    update inventory_item
    set 
    '''

    # add updated fields
    for key, val in params.items():
        if val is not None:
            sql+=f'{key} = {val},'


    sql += '''
    where p.id = i.pantry_id
        and p.manager_id = {manager_id}
        and i.item_id = {item_id};'''








    return False
