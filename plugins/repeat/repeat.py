from sdk.send_message import send_group_message
from sdk.message import text_message
from sdk.temp_data import alloc, fetch, dump
from core.plugin import Plugin
import json
import asyncio

async def handler(session: str, group_id: int, sender_user_id: int, message: str):
    asyncio.sleep(0.5)
    key = f"repeat_{group_id}"
    data = fetch(key)
    if data == None:
        alloc(key, {
            'msg': message
        })
        return
    
    if data['msg'] == message:
        await send_group_message(session, group_id, text_message(f"{message}"))
        dump(key)
    else:
        data['msg'] = message

async def handler2(session: str, group_id: int, sender_user_id: int, message):
    key = f"repeat_{group_id}"
    data = fetch(key)
    if data == None:
        alloc(key, {
            'msg': message,
        })
        return
    if json.dumps(data['msg'], ensure_ascii=False) == json.dumps(message, ensure_ascii=False):
        await send_group_message(session, group_id, message)
        dump(key)
    else:
        data['msg'] = message

repeat = Plugin('repeat')
repeat.register_callback('group.text_message', handler)
repeat.register_callback('group.message', handler2)