from sdk.send_message import send_group_message
from sdk.message import text_message
from plugins.guess_npc.saying import npc_saying
import random
from core.plugin import Plugin
from sdk.temp_data import alloc, fetch, dump
from sdk.user import user_group_nickname

npc_name = [key for (key, value) in npc_saying.items()]

async def handler(session: str, group_id: int, sender_user_id: int, message: str):
    key = f"guess_npc_{group_id}"
    if message == "猜npc":
        if fetch(key) != None:
            await send_group_message(session, group_id, text_message("请先猜对当前npc，或输入“结束游戏”"))
            return
        
        npc = random.choice(npc_name)
        saying = random.choice(npc_saying[npc])
        saying.replace("__name__", user_group_nickname(session, group_id, sender_user_id))
        alloc(key, {
            "npc": npc,
            "saying": saying
        })
        await send_group_message(session, group_id, text_message(saying))
        return
    data = fetch(key)

    if message == "结束游戏":
        if data == None:
            return
        await send_group_message(session, group_id, text_message(f"游戏结束，答案是：{data['npc']}"))
        dump(key)
        return
    
    if data == None:
        await send_group_message(session, group_id, text_message("请发送“猜npc”来开始游戏"))
        return
    
    if message == data["npc"]:
        await send_group_message(session, group_id, text_message(f"猜对咯，答案是{data['npc']}！"))
        dump(key)
        return
    else:
        await send_group_message(session, group_id, text_message(f"猜错了，继续猜吧！"))
        return

def checker(group_id: int, sender_user_id: int, message: str):
    return message in ["猜npc", "结束游戏"] or message in npc_name

guess_npc = Plugin('guess_npc')
guess_npc.register_callback('message.group.text_message', handler, checker)