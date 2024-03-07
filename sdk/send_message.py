import sdk.api as api
import time
import asyncio
from sdk.temp_data import dump

last_send = time.time()

async def send_group_message(session: str, group_id, *message_chain): # may cause block
    global last_send
    dump(f'repeat_{group_id}')
    while time.time() - last_send < 1:
        await asyncio.sleep(1)
    last_send = time.time()
    api.post('/sendGroupMessage', {
        "sessionKey": session,
        "target": group_id,
        "messageChain": message_chain
    })