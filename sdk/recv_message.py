import sdk.api as api
import time
import queue

last_fetch = time.time()

message_pool = queue.Queue()

def recv_message(session: str): # may cause block
    global message_pool
    if not message_pool.empty():
        return message_pool.get()
    while True:
        global last_fetch
        if time.time() - last_fetch < 0.1:
            continue
        last_fetch = time.time()
        recv = api.get(f'/countMessage?sessionKey={session}')
        count = recv["data"]
        if count == 0:
            continue
        recv = api.get(f'/fetchMessage?sessionKey={session}&count={count}')
        for i in recv["data"]:
            message_pool.put(i)
        break
    return message_pool.get()
