import requests, json
from config import URL_PREFIX

def post(url, body):
    ret = requests.post(URL_PREFIX + url, data=json.dumps(body)).json()
    if "code" in ret and ret["code"] != 0:
        print("Operation failed.") # future will be log
    return ret


def get(url):
    ret = requests.get(URL_PREFIX + url).json()
    if "code" in ret and ret["code"] != 0:
        print("Operation failed.")
    return ret