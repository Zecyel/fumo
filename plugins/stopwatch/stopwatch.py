from sdk.send_message import send_group_message
from sdk.message import text_message
from core.plugin import Plugin
import asyncio
import time

async def handler(session: str, group_id: int, sender_user_id: int, message: str):
    # if message == '卡顿':
    #     await send_group_message(session, group_id, text_message("10s计时开始"))
    #     # await asyncio.sleep(10)
    #     time.sleep(10)
    #     await send_group_message(session, group_id, text_message("10s计时结束"))
    # raise ZeroDivisionError
    pass

def checker(group_id: int, sender_user_id: int, message: str):
    # raise ZeroDivisionError
    return True

stopwatch = Plugin('stopwatch')
stopwatch.register_callback('message.group.text_message', handler, checker)
