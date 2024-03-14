import requests, json
from config import URL_PREFIX
from sdk.log import logger

api_logger = logger("runtime", "Api")

def post(url, body):
    ret = requests.post(URL_PREFIX + url, data=json.dumps(body)).json()
    if "code" in ret and ret["code"] != 0:
        api_logger["error"](f"Post API failed.\nRequest: {url}\n{body}\nResponse: {ret}")
    else:
        # api_logger["info"](f"Post: Request: {url}\n{body}\nResponse:{ret}")
        pass
    return ret


def get(url):
    ret = requests.get(URL_PREFIX + url).json()
    if "code" in ret and ret["code"] != 0:
        api_logger["error"](f"Get API failed.\nRequest: {url}\nResponse: {ret}")
    else:
        # api_logger["info"](f"Get: Request: {url}\nResponse:{ret}")
        pass
    return ret