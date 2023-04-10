import main, crud
from sqlalchemy.orm import Session

def init_session() -> None:
    main.SESSION_DATA = {
        "id": None,  # account id, type
        "type": None,  # 0 = shopper, 1 = manager
        "logged_in": False,

        # Manager Only
        "pantries_managed": None, # int
        "students_helped": None, # int
        "total_transactions": None # int
    }

def verify_session(acc_type: str) -> bool:
    ''' verify a loged in user is of
        the correct account type '''
    if main.SESSION_DATA['logged_in'] != True:
        return False
    if main.SESSION_DATA['type'] != acc_type:
        return False
    return True

def wipe_session() -> None:
    init_session()

def login(db: Session, id: int, type: str) -> None:
    main.SESSION_DATA["id"] = id
    main.SESSION_DATA["type"] = type
    main.SESSION_DATA["logged_in"] = True

    if type == "manager":
        main.SESSION_DATA["pantries_managed"] = crud.get_pantries_managed(db=db, id=id)
        main.SESSION_DATA["students_helped"] = crud.get_students_helped(db=db, id=id)
        main.SESSION_DATA["total_transactions"] = crud.get_total_transactions(db=db, id=id)