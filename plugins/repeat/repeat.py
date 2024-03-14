from sdk.send_message import send_group_message
from sdk.message import text_message
from sdk.temp_data import alloc, fetch, dump
from core.plugin import Plugin
import asyncio

async def handler(session: str, group_id: int, sender_id: int, message):
    await asyncio.sleep(0.5)
    key = f"repeat_{group_id}"
    data = fetch(key)
    if data == None:
        alloc(key, {
            'msg': message[0],
            'repeated': False
        })
        return
    
    if data['msg'] == message[0]:
        if data['repeated'] == False:
            await send_group_message(session, group_id, text_message(f"{message[0]}"))
            data['repeated'] = True
    else:
        data['msg'] = message[0]
        data['repeated'] = False

repeat = Plugin('repeat')
repeat.register_callback('group.P', handler)