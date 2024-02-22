import sdk.api as api
import time

last_send = time.time()

def send_group_message(session: str, group_id, message_chain): # may cause block
    global last_send
    while time.time() - last_send < 0.5:
        pass
    last_send = time.time()
    api.post('/sendGroupMessage', {
        "sessionKey": session,
        "target": group_id,
        "messageChain": message_chain
    })