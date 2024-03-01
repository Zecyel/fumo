from sdk.send_message import send_group_message
from sdk.message import text_message
from core.plugin import Plugin
from sdk.userdata import get_coin, add_coin
from sdk.persisted_data import alloc, fetch
import random

async def handler(session: str, group_id: int, sender_user_id: int, message: str):
    key = f"pray_box_{group_id}"
    if fetch(key) == None:
        alloc(key, {
            "coin": 10
        })
    if message == "许愿箱":
        await send_group_message(session, group_id, text_message(f"许愿箱中金币数量为{fetch(key).get('coin')}\n输入“许愿”来许愿，有50%的概率获得许愿箱中的金币，50%的概率消耗等量金币哦"))
        return
    if message == "许愿":
        bet = fetch(key).get('coin')
        if get_coin(sender_user_id) < bet:
            await send_group_message(session, group_id, text_message(f"你的金币数量不足，无法许愿哦~"))
            return
        lucky = random.random() > 0.5
        if lucky:
            add_coin(sender_user_id, bet)
            fetch(key).set('coin', 10)
            await send_group_message(session, group_id, text_message(f"恭喜你获得fumo的奖励！获得{bet}金币！"))
        else:
            add_coin(sender_user_id, -bet)
            fetch(key).set('coin', bet * 2)
            await send_group_message(session, group_id, text_message(f"fumo感受到了你的许愿，慷慨接纳了你的{bet}金币！"))

def checker(group_id: int, sender_user_id: int, message: str):
    return message in ["许愿", "许愿箱"]

pray = Plugin('pray')
pray.register_callback('group.text_message', handler, checker)