import main


def init_session():
    main.SESSION_DATA = {
        "id": None,  # account id, type
        "type": None,  # 0 = shopper, 1 = manager
        "logged_in": False
    }

def verify_session(acc_type: str) -> bool:
    ''' verify a loged in user is of
        the correct account type '''
    if main.SESSION_DATA['logged_in'] != True:
        return False
    if main.SESSION_DATA['type'] != acc_type:
        return False
    return True

def wipe_session():
    init_session()

def login(id: int, type: str):
    main.SESSION_DATA["id"] = id
    main.SESSION_DATA["type"] = type
    main.SESSION_DATA["logged_in"] = True
