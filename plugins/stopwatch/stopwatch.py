from sdk.send_message import send_group_message
from sdk.message import text_message
from sdk.timer import Timer
from core.plugin import Plugin
import asyncio
import time

async def handler(session: str, group_id: int, sender_user_id: int, message: str):
    if message == "测试":
        await send_group_message(session, group_id, text_message("测试开始"))
        
        stopwatch.register_timer(Timer(5), timer, session, group_id)

async def timer(session: str, group_id: int):
    await send_group_message(session, group_id, text_message("测试结束"))

stopwatch = Plugin('stopwatch')
stopwatch.register_callback('group.text_message', handler)
