from sdk.send_message import send_group_message
from sdk.message import text_message
from core.plugin import Plugin
import random

async def handler(session: str,group_id: int,sender_id: int,message):
    message = message[1]
    if message.startswith("我"):
        message = message[1:]
    choice = message.split('还是')
    if all([i == choice[0] for i in choice]):
        await send_group_message(session, group_id, text_message('杂鱼～你还想骗我说你想要听的话？'))
        return

    if len(choice) == 2 and set(choice[0].split("是")) == set(choice[1].split("是")):
        await send_group_message(session, group_id, text_message('杂鱼～你还想骗我说你想要听的话？'))
        return

    choice.append('杂鱼～我才不回答你的问题呢')
    await send_group_message(session, group_id, text_message(random.choice(choice)))

def checker(group_id: int,sender_id: int,message):
    return '还是' in message[1]

choosing_helper = Plugin('choosing_helper')
choosing_helper.register_callback('group.@fumoP',handler,checker)

