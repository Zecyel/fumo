from sdk.send_message import send_group_message
from sdk.message import text_message
import random
from core.plugin import Plugin
from plugins.answer.book import answer_book

def answer_handler(session: str, group_id: int, sender_user_id: int, message: str):
    if message == "答案之书":
        send_group_message(session, group_id, text_message(random.choice(answer_book)))

answer = Plugin('answer')
answer.register_callback('message.group.text_message', answer_handler)
