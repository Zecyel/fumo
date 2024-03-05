from random import choice

temp_data = {}

def alloc(key: str, value: object):
    temp_data[key] = value

def fetch(key: str) -> object:
    if not key in temp_data:
        return None
    return temp_data[key]

def dump(key: str):
    if key in temp_data:
        del temp_data[key]

def random_key() -> str:
    return "".join([choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(8)])