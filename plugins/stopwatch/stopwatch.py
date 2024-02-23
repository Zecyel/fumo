from sdk.send_message import send_group_message
from sdk.message import text_message
from core.plugin import Plugin
import asyncio
import time

privileged_user = [2530469979, 158291705]
async def stopwatch_handler(session: str, group_id: int, sender_user_id: int, message: str):
    if message == '卡顿':
        await send_group_message(session, group_id, text_message("10s计时开始"))
        # await asyncio.sleep(10)
        time.sleep(10)
        await send_group_message(session, group_id, text_message("10s计时结束"))

stopwatch = Plugin('stopwatch')
stopwatch.register_callback('message.group.text_message', stopwatch_handler)
