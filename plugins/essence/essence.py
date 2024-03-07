from sdk.send_message import send_group_message
from sdk.message import text_message
from core.plugin import Plugin
from sdk.manage import set_essence

async def handler(session: str, group_id: int, sender_id: int, message):
    print("Entered")
    await set_essence(session, message[0]["message_id"], group_id)
    await send_group_message(session, group_id, text_message("已设精"))

def checker(group_id: int, sender_id: int, message):
    return message[1] == '设精'

essence = Plugin('essence')
essence.register_callback('group.QP', handler, checker)