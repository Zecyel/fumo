import requests, json
from config import IP, PORT

prefix = f'http://{IP}:{PORT}'

def post(url, body):
    ret = requests.post(prefix + url, data=json.dumps(body)).json()
    if "code" in ret and ret["code"] != 0:
        print("Operation failed.") # future will be log
    return ret


def get(url):
    ret = requests.get(prefix + url).json()
    if "code" in ret and ret["code"] != 0:
        print("Operation failed.")
    return ret