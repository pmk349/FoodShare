import hashlib

'''
This file exists for general utilities

'''



def encrypt_password(password: str) -> str:
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()
