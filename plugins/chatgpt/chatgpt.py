import traceback
from sdk.send_message import send_group_message, send_friend_message
from sdk.message import text_message
from core.plugin import Plugin
from sdk.chatgpt import ask, plain_msg
from sdk.history import message_from_id
from sdk.message import convert_message
from sdk.temp_data import fetch, alloc, dump
from sdk.log import logger

import time

group_logger = logger("chatgpt", "Group")
friend_logger = logger("chatgpt", "Friend")

def dialog(key: str, message: str, logger) -> str:
    if message == "结束对话":
        dump(key)
        return "对话结束"

    data = fetch(key)

    if data != None and time.time() - data['time'] > 7200: # 2 hr
        dump(key)
        data = None

    if data == None:
        alloc(key, {
            "history": [{
                "role": "system",
                "content": "You are a helpful assistant."
            }],
            "time": time.time()
        })
        data = fetch(key)

    data["time"] = time.time()

    data["history"].append({
        "role": "user",
        "content": message
    })

    try:
        resp = ask(data["history"])
        data["history"].append({
            "role": "assistant",
            "content": resp
        })
    except:
        resp = "网络错误/关键词异常，请更换prompt后重试"
        logger["error"](message)
        logger["error"](traceback.format_exc())

    return resp


async def group_message_handler(session: str, group_id: int, sender_id: int, message):
    key = f"chatgpt_{group_id}_{sender_id}"
    resp = dialog(key, message[2], group_logger)
    group_logger["info"](f"{group_id}: {sender_id}: {message[2]}\n{resp}")
    await send_group_message(session, group_id, text_message(resp))

async def friend_message_handler(session: str, sender_id: int, message):
    key = f"chatgpt_{sender_id}"
    resp = dialog(key, message[0], friend_logger)
    friend_logger["info"](f"{sender_id}: {message[0]}\n{resp}")
    await send_friend_message(session, sender_id, text_message(resp))

chatgpt = Plugin('chatgpt')
chatgpt.register_callback('group.@fumo@fumoP', group_message_handler)

chatgpt.register_callback('friend.P', friend_message_handler)
