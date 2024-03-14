from sdk.send_message import send_group_message, send_friend_message
from sdk.message import text_message
from core.plugin import Plugin
from sdk.chatgpt import ask, plain_msg
from sdk.history import message_from_id
from sdk.message import convert_message
from sdk.temp_data import fetch, alloc, dump

async def long_dialog_handler(session: str, group_id: int, sender_id: int, message):

    key = f"chatgpt_{group_id}_{sender_id}"

    if message[2] == "结束对话":
        dump(key)
        await send_group_message(session, group_id, text_message("对话结束"))
        return

    data = fetch(key)
    if data == None:
        alloc(key, {
            "history": [{
                "role": "system",
                "content": "You are a helpful assistant."
            }],
        })
        data = fetch(key)
    
    data["history"].append({
        "role": "user",
        "content": message[2]
    })

    resp = ask(data["history"])

    data["history"].append({
        "role": "assistant",
        "content": resp
    })

    await send_group_message(session, group_id, text_message(resp))

chatgpt = Plugin('chatgpt')
chatgpt.register_callback('group.@fumo@fumoP', long_dialog_handler)
