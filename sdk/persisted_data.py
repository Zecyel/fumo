import json
import os

def _get_filename(key: str) -> str:
    return f'data/{key}.json'

def alloc(key: str, value: object):
    with open(_get_filename(key), 'w') as f:
        f.write(json.dumps(value))

class Delegate:

    def __init__(self, key: str, obj: object):
        print(f"{key} {object}")
        self.key = key
        self.obj = obj

    def get(self, key: str) -> object:
        return self.obj[key]

    def set(self, key: str, value: object):
        print(f"debug: setattr {key} {value}")
        # self.obj[key] = value
        self.obj[key] = value
    
    def __del__(self):
        with open(_get_filename(self.key), 'w') as f:
            f.write(json.dumps(self.obj))

def fetch(key: str) -> object:
    filename = _get_filename(key)
    if not os.path.exists(filename):
        return None
    with open(filename, 'r') as f:
        return Delegate(key, json.loads(f.read()))

def dump(key: str):
    filename = _get_filename(key)
    if os.path.exists(filename):
        os.remove(filename)
