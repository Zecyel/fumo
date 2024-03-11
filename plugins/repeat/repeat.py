from sdk.send_message import send_group_message
from sdk.message import text_message
from sdk.temp_data import alloc, fetch, dump
from core.plugin import Plugin
import asyncio

async def handler(session: str, group_id: int, sender_id: int, message):
    asyncio.sleep(0.5)
    key = f"repeat_{group_id}"
    data = fetch(key)
    if data == None:
        alloc(key, {
            'msg': message[0]
        })
        return
    
    if data['msg'] == message[0]:
        await send_group_message(session, group_id, text_message(f"{message[0]}"))
        dump(key)
    else:
        data['msg'] = message[0]

repeat = Plugin('repeat')
repeat.register_callback('group.P', handler)