from sdk.send_message import send_group_message
from sdk.message import web_image_message
from core.plugin import Plugin
import requests, json

def mapper(key: str) -> str:
    dict = {
        "全部": "all",
        "横屏": "pc",
        "竖屏": "mp",
        "银发": "silver",
        "兽耳": "furry",
        # "r18": "r18",
        "p站": "pixiv",
        "收藏": "jitsu"
    }
    if key in dict.keys():
        return dict[key]
    return "all"

async def handler(session: str, group_id: int, sender_id: int, message):
    message = message[1][2:].strip()
    
    ret = requests.get(f"https://moe.jitsu.top/api/?sort={mapper(message)}&type=json&num=1")
    ret = json.loads(ret.content.decode())
    # print(ret)
    await send_group_message(session, group_id, web_image_message(ret["pics"][0]))

def checker(group_id: int, sender_id: int, message):
    return message[1].startswith("涩图")

setu = Plugin('setu')
setu.register_callback('group.@fumoP', handler, checker)
