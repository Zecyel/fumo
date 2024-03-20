from sdk.send_message import send_group_message
from sdk.message import text_message
from core.plugin import Plugin
import random

async def handler(session: str,group_id: int,sender_id: int,message):
    if message[1][0]=='我':
        message[1]=message[1][1:]
    list = message[1].split('还是')
    list.append('杂鱼～我才不回答你的问题呢')
    if list[0]==list[1]:
        await send_group_message(session, group_id, text_message('杂鱼～你还想骗我说你想要听的话？'))
    elif ('是' in list[0]) and (list[0].split('是')[0] == list[1].split('是')[1]):
        await send_group_message(session, group_id, text_message('杂鱼～你还想骗我说你想要听的话？'))
    else:
        await send_group_message(session, group_id, text_message(random.choice(list)))
def checker(group_id: int,sender_id: int,message):
    return '还是' in message[1]

choosing_helper = Plugin('choosing_helper')
choosing_helper.register_callback('group.@fumoP',handler,checker)

