from sdk.send_message import send_group_message
from sdk.message import text_message
from sdk.user import user_group_nickname
import random
from core.plugin import Plugin
from plugins.battle.army import army, death, prefix
from sdk.userdata import add_coin, get_coin

async def battle_handler(session: str, group_id: int, sender_user_id: int, message):
    if len(message) == 3 and message[2]["type"] == "Plain" and message[2]["text"].strip() == "":
        message = message[:2]
    if len(message) != 2:
        return
    if message[0]["type"] != "Plain" or message[1]["type"] != "At":
        return
    if message[0]["text"].strip() == "决斗":
        user_id_1 = sender_user_id
        user_id_2 = message[1]["target"]
        if user_id_1 == user_id_2:
            await send_group_message(session, group_id, text_message(f"你个杂鱼，才不能和自己决斗呢"))
            return
        
        if get_coin(user_id_1) < 10:
            await send_group_message(session, group_id, text_message(f"金币不足，无法进行决斗"))
            return

        if get_coin(user_id_2) < 10:
            await send_group_message(session, group_id, text_message(f"被决斗者金币不足，无法进行决斗"))
            return
        
        player1 = user_group_nickname(session, group_id, user_id_1)
        player2 = user_group_nickname(session, group_id, user_id_2)

        army1 = random.choice(prefix) + " " + random.choice(army)
        army2 = random.choice(prefix) + " " + random.choice(army)

        await send_group_message(session, group_id, text_message(f"{player1} 与 {player2} 的决斗开始！"))
        await send_group_message(session, group_id, text_message(f"{player1} 使用了 {army1}"))
        await send_group_message(session, group_id, text_message(f"{player2} 使用了 {army2}"))

        if random.random() > 0.5:
            user_id_1, user_id_2 = user_id_2, user_id_1
            player1, player2 = player2, player1
            army1, army2 = army2, army1
        
        hint = random.choice(death)

        await send_group_message(session, group_id, text_message(f"{player1} {hint}，凶手是 {player2} 的 {army2}。"))
        add_coin(user_id_1, -10)
        add_coin(user_id_2, 10)
        await send_group_message(session, group_id, text_message(f"{player1}向{player2}奉上了10金币"))
        
battle = Plugin('battle')
battle.register_callback('group.message', battle_handler)
