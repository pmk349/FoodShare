from pydantic import BaseModel

global session_data

def init_session():
    session_data = {
        "id": None,  # account id, type
        "type": None,  # 0 = shopper, 1 = manager
        "logged_in": False
    }

def verify_session(acc_type: str) -> bool:
    ''' verify a loged in user is of
        the correct account type '''
    if session_data['logged_in'] != True:
        return False
    if session_data['type'] != acc_type:
        return False
    return True

def wipe_session():
    init_session()


def login(id: int, type: str):
    session_data["id"] = id
    session_data["type"] = type
    session_data["logged_in"] = True
