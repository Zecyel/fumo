from sdk.send_message import send_group_message
from sdk.message import text_message
from core.plugin import Plugin
from config import DIR_PATH
from sdk.temp_data import fetch, alloc, dump
from plugins.playmaze.solver import solve
from sdk.image import download_image

async def handler(session: str, group_id: int, sender_id: int, message):
    key = f"maze_{group_id}"

    if fetch(key) is None:
        alloc(key, {
            "solving": False
        })
    
    data = fetch(key)
    if data["solving"]:
        await send_group_message(session, group_id, text_message("正在玩maze，请稍等..."))
        return
    
    data["solving"] = True
    await send_group_message(session, group_id, text_message("maze"))

def checker(group_id: int, sender_id: int, message: str):
    return message[1] == '玩maze'

async def maze_handler(session: str, group_id: int, sender_id: int, message):
    key = f"maze_{group_id}"

    await send_group_message(session, group_id, text_message(solve(download_image(message[2]["url"]))))

    data = fetch(key)
    data["solving"] = False

async def maze_handler_1(session: str, group_id: int, sender_id: int, message):
    key = f"maze_{group_id}"

    await send_group_message(session, group_id, text_message(solve(download_image(message[1]["url"]))))

    data = fetch(key)
    data["solving"] = False

def maze_checker(group_id: int, sender_id: int, message: str):
    return sender_id == 449427853 and message[1] == "请通过连续发送操作序列解开迷宫！"# and group_id == 1037308494

def maze_checker_1(group_id: int, sender_id: int, message: str):
    return sender_id == 449427853

async def maze_solved_handler(session: str, group_id: int, sender_id: int, message):
    await send_group_message(session, group_id, text_message("😎"))

def maze_solved_checker(group_id: int, sender_id: int, message: str):
    return sender_id == 449427853 and message[1].startswith("恭喜你成功解开了迷宫！")


playmaze = Plugin('playmaze')
playmaze.register_callback('group.@fumoP', handler, checker)
playmaze.register_callback('group.@fumoPI', maze_handler, maze_checker)
playmaze.register_callback('group.@fumoI', maze_handler_1, maze_checker_1)
playmaze.register_callback('group.@fumoPI', maze_solved_handler, maze_solved_checker)
