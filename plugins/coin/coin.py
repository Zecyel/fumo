from sdk.send_message import send_group_message
from sdk.message import text_message
from core.plugin import Plugin
from sdk.userdata import add_coin, get_coin


async def handler(session: str, group_id: int, sender_user_id: int, message: str):
    # if message == "给我金币" or message == "爆点金币":
    #     add_coin(sender_user_id, 10)
    #     await send_group_message(session, group_id, text_message(f"成功获得10金币"))
    if message == "查询金币":
        coin = get_coin(sender_user_id)
        await send_group_message(session, group_id, text_message(f"你的金币数量为{coin}"))

def checker(group_id: int, sender_user_id: int, message: str):
    return message in ["给我金币", "查询金币", "爆点金币"]

coin = Plugin('coin')
coin.register_callback('group.text_message', handler, checker)