IP = "127.0.0.1"
PORT = 8096
VERIFY_KEY = "1234567890"
QQ = 3793571711
base = f'http://{IP}:{PORT}'

GROUP_ID = 853478479

import requests
import json

session = None

def init() -> bool:
    global session

    verification = requests.post(f'{base}/verify', data=json.dumps({
        "verifyKey": VERIFY_KEY
    })).json()
    
    if verification["code"] != 0:
        print("Error occured when verifying.")
        return False

    session = verification["session"]
    print(verification)

    logins = requests.get(f'{base}/botList').json()
    print(logins)

    binds = requests.post(f'{base}/bind', data=json.dumps({
        "sessionKey": session,
        "qq": QQ
    })).json()
    print(binds)

    if binds["code"] != 0:
        print("Error occured when binding.")
        return False

    return True


if init():

    info = requests.get(f'{base}/friendList?sessionKey={session}').json()
    print(info)

    print("session:", session)

    import time

    ret = requests.post(f'{base}/sendGroupMessage', data=json.dumps({
        "sessionKey": session,
        "target": GROUP_ID,
        "messageChain": [
            { "type": "Plain", "text": f"时间：{ time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.localtime())}" },
            { "type":"Image", "url":"https://i0.hdslb.com/bfs/album/67fc4e6b417d9c68ef98ba71d5e79505bbad97a1.png" }
        ]
    })).json()

    print(ret)

    # ret = requests.post(f'{base}/sendFriendMessage', data=json.dumps({
    #     "sessionKey": session,
    #     "target": 2530469979,
    #     "messageChain": [
    #         { "type": "Plain", "text": "Hello, Terraria" }
    #     ]
    # })).json()

    # print(ret)