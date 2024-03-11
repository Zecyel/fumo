from sdk.send_message import send_group_message, send_friend_message
from sdk.message import text_message
from core.plugin import Plugin
import random

privileged_user = [2530469979, 158291705]
async def handler(session: str, group_id: int, sender_id: int, message):
    if random.random() > 0.8:
        await send_group_message(session, group_id, text_message("( *・ω・)✄╰ひ╯"))
        return

    if sender_id in privileged_user:
        await send_group_message(session, group_id, text_message("主人喵~"))
    else:
        await send_group_message(session, group_id, text_message("爪巴"))

def checker(group_id: int, sender_id: int, message):
    return message[1][:2] == "摸摸"

async def handler2(session: str, sender_id: int, message):
    await send_friend_message(session, sender_id, text_message("喵喵喵，fumo想和主人永远永远在一起喵~"))

def checker2(sender_id: int, message):
    return message[0] == "摸摸"

pat = Plugin('pat')
pat.register_callback('group.@fumoP', handler, checker)

pat.register_callback('friend.P', handler2, checker2)