from sdk.send_message import send_group_message
from sdk.message import text_message
from typing import List, Tuple
import random
from core.plugin import Plugin
from sdk.temp_data import alloc, fetch, dump, random_key
import time
from sdk.timer import Timer

def hupai(pai: List[int]) -> bool:
    if sum(pai) == 0:
        return True
    if sum(pai) % 3 == 2:
        for i in range(1, 10):
            if pai[i] >= 2:
                new_pai = pai[:]
                new_pai[i] -= 2
                if hupai(new_pai):
                    return True
        return False
    for i in range(1, 8):
        if pai[i] >= 1 and pai[i+1] >= 1 and pai[i+2] >= 1:
            new_pai = pai[:]
            new_pai[i] -= 1
            new_pai[i+1] -= 1
            new_pai[i+2] -= 1
            if hupai(new_pai):
                return True
    for i in range(1, 10):
        if pai[i] >= 3:
            new_pai = pai[:]
            new_pai[i] -= 3
            if hupai(new_pai):
                return True
    return False

def ting(pai: List[int]) -> List[int]:
    ret = []
    for i in range(1, 10):
        if pai[i] != 4:
            new_pai = pai[:]
            new_pai[i] += 1
            if hupai(new_pai):
                ret.append(i)
    return ret

def make_exercise(difficulty: int = 1, num: int = 13) -> Tuple[List[int], List[int]]:
    a = list(range(1, 10)) * 4
    while True:
        random.shuffle(a)
        count = [0] * 10
        for i in range(num):
            count[a[i]] += 1
        tp = ting(count)
        if len(tp) >= difficulty:
            return sorted(a[:num]), tp

def to_message(pai: List[int]) -> str:
    return "".join(map(str, pai))

async def handler(session: str, group_id: int, sender_user_id: int, message: str):
    key = f"tingpai_{group_id}"
    if message in ["清一色", "清一色hard", "清一色superhard", "清一色extrahard"]:
        if fetch(key) != None:
            await send_group_message(session, group_id, text_message("请先猜对当前听牌，或输入“结束游戏”"))
            return
        
        if message == "清一色":
            exercise, answer = make_exercise()
        elif message == "清一色hard":
            exercise, answer = make_exercise(4)
        elif message == "清一色superhard":
            exercise, answer = make_exercise(4, 16)
        elif message == "清一色extrahard":
            exercise, answer = make_exercise(5, 19)

        game_key = random_key()

        alloc(key, {
            "exercise": exercise,
            "answer": answer,
            "key": game_key
        })
        await send_group_message(session, group_id, text_message(f"{to_message(exercise)} 听牌是？"))

        tingpai.register_timer(Timer(10), no_answer, session, group_id, game_key)
        return
    
    data = fetch(key)
    if data == None:
        return

    if message == "结束游戏":
        await send_group_message(session, group_id, text_message(f"游戏结束，答案是：{to_message(data['answer'])}"))
        dump(key)
        return
    
    if message == to_message(data['answer']):
        await send_group_message(session, group_id, text_message(f"答对咯，答案是{to_message(data['answer'])}！"))
        dump(key)
        return
    else:
        await send_group_message(session, group_id, text_message(f"回答错了喵，请继续回答喵~"))
        return

async def no_answer(session: str, group_id: int, key: str):
    data = fetch(f"tingpai_{group_id}")
    if data == None or data["key"] != key:
        return
    await send_group_message(session, group_id, text_message(f"游戏超时结束，答案是：{to_message(data['answer'])}"))
    dump(f"tingpai_{group_id}")

def checker(group_id: int, sender_user_id: int, message: str):
    return message in ["清一色", "结束游戏", "清一色hard", "清一色superhard", "清一色extrahard"] or all([i in "123456789" for i in message])

tingpai = Plugin('tingpai')
tingpai.register_callback('group.text_message', handler, checker)
