temp_data = {}

def alloc(key: str, value: object):
    temp_data[key] = value

def fetch(key: str) -> object:
    if not key in temp_data:
        return None
    return temp_data[key]

def dump(key: str):
    del temp_data[key]
