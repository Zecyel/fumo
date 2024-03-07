from sdk.send_message import send_group_message
from sdk.message import text_message
from sdk.timer import Timer
from core.plugin import Plugin
from sdk.temp_data import alloc, fetch, dump
from sdk.user import user_group_nickname

async def handler(session: str, group_id: int, sender_id: int, message):
    message = message[1][2:]
    key = f"score_{group_id}"
    if fetch(key) == None:
        alloc(key, [])

    if message == "板":
        score = sorted(fetch(key), key=lambda x: x['score'], reverse=True)
        msg = "计分板：\n" + "\n".join([f"{user_group_nickname(session, group_id, x['user_id'])}：{x['score']}" for x in score])
        await send_group_message(session, group_id, text_message(msg))
        return

    if message == "结束":
        dump(key)
        await send_group_message(session, group_id, text_message("计分已结束！"))
        return

    delta = int(message)
    data = fetch(key)
    for i in range(len(data)):
        if data[i]['user_id'] == sender_id:
            data[i]['score'] += delta
            break
    else:
        data.append({'user_id': sender_id, 'score': delta})

def checker(group_id: int, sender_id: int, message):
    return message[1][:2] == "计分"

score = Plugin('score')
score.register_callback('group.@fumoP', handler, checker)
