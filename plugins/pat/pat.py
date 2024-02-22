from sdk.send_message import send_group_message
from sdk.message import text_message
from core.plugin import Plugin

privileged_user = [2530469979]
def pat_handler(session: str, group_id: int, sender_user_id: int, message: str):
    if message == '摸摸':
        if sender_user_id in privileged_user:
            send_group_message(session, group_id, text_message("主人喵~"))
        else:
            send_group_message(session, group_id, text_message("爪巴"))

pat = Plugin('pat') # will automatically load pat.json
pat.register_callback('message.group.text_message', pat_handler) # common message
