from sdk.send_message import send_group_message
from sdk.message import text_message
from sdk.user import user_group_nickname
import random
from core.plugin import Plugin
from plugins.battle.army import army, death

def battle_handler(session: str, group_id: int, sender_user_id: int, message):
    if len(message) == 3 and message[2]["type"] == "Plain" and message[2]["text"].strip() == "":
        message = message[:2]
    if len(message) != 2:
        return
    if message[0]["type"] != "Plain" or message[1]["type"] != "At":
        return
    if message[0]["text"].strip() == "决斗":
        player1 = user_group_nickname(session, group_id, sender_user_id)
        player2 = user_group_nickname(session, group_id, message[1]["target"])
        if player1 == player2:
            send_group_message(session, group_id, text_message(f"你个杂鱼，才不能和自己决斗呢"))
            return

        if random.random() > 0.5:
            player1, player2 = player2, player1

        army1 = random.choice(army)
        army2 = random.choice(army)

        send_group_message(session, group_id, text_message(f"{player1} 与 {player2} 的决斗开始！"))
        send_group_message(session, group_id, text_message(f"{player1} 使用了 {army1}"))
        send_group_message(session, group_id, text_message(f"{player2} 使用了 {army2}"))

        if random.random() > 0.5:
            player1, player2 = player2, player1
            army1, army2 = army2, army1
        
        hint = random.choice(death)

        send_group_message(session, group_id, text_message(f"{player1} {hint}，凶手是 {player2} 的 {army2}。"))
        

battle = Plugin('battle')
battle.register_callback('message.group.message', battle_handler)
