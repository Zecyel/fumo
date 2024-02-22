import requests, json

IP = "127.0.0.1"
PORT = 8096
prefix = f'http://{IP}:{PORT}'

def post(url, body):
    ret = requests.post(prefix + url, data=json.dumps(body)).json()
    if ret["code"] != 0:
        print("Operation failed.") # future will be log
    return ret


def get(url):
    ret = requests.get(prefix + url).json()
    if ret["code"] != 0:
        print("Operation failed.")
    return ret