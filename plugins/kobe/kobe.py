from sdk.send_message import send_group_message
from sdk.message import text_message
from core.plugin import Plugin

def kobe_handler(session: str, group_id: int, sender_user_id: int, message: str):
    if message == '我有意见':
        send_group_message(session, group_id, text_message("我没意见"))
    elif message == '我没意见':
        send_group_message(session, group_id, text_message("我有意见"))

kobe = Plugin('kobe')
kobe.register_callback('message.group.text_message', kobe_handler)
