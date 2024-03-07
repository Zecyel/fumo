from sdk.send_message import send_group_message
from sdk.message import text_message
import random
from core.plugin import Plugin
from plugins.answer.book import answer_book
from sdk.temp_data import fetch

async def handler(session: str, group_id: int, sender_id: int, message):
    data = fetch(f'guess_npc_{group_id}')
    if data != None:
        await send_group_message(session, group_id, text_message(data['npc']))
    else:
        await send_group_message(session, group_id, text_message(random.choice(answer_book)))

def checker(group_id: int, sender_id: int, message):
    return message[1] == "答案之书"

answer = Plugin('answer')
answer.register_callback('group.@fumoP', handler, checker)
