from sdk.send_message import send_group_message
from sdk.message import text_message
from core.plugin import Plugin

privileged_user = [2530469979, 158291705]
async def handler(session: str, group_id: int, sender_user_id: int, message: str):
    if sender_user_id in privileged_user:
        await send_group_message(session, group_id, text_message("主人喵~"))
    else:
        await send_group_message(session, group_id, text_message("爪巴"))

def checker(group_id: int, sender_user_id: int, message: str):
    return message[:2] == "摸摸"

pat = Plugin('pat')
pat.register_callback('group.text_message', handler, checker)
