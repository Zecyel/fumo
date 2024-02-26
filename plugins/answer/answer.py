from sdk.send_message import send_group_message
from sdk.message import text_message
import random
from core.plugin import Plugin
from plugins.answer.book import answer_book

async def handler(session: str, group_id: int, sender_user_id: int, message: str):
    await send_group_message(session, group_id, text_message(random.choice(answer_book)))

def checker(group_id: int, sender_user_id: int, message: str):
    return message == "答案之书"

answer = Plugin('answer')
answer.register_callback('message.group.text_message', handler, checker)
