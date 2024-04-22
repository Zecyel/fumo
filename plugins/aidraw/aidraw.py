import traceback
from sdk.send_message import send_group_message
from sdk.message import text_message, web_image_message
from core.plugin import Plugin
from sdk.aidraw import draw
from sdk.log import logger

logger = logger("runtime", "AIDraw")

async def handler(session: str, group_id: int, sender_id: int, message):
    message = message[1][2:]
    try:
        url = draw(message)
        # print(url)
        await send_group_message(session, group_id, web_image_message(url))
    except:
        await send_group_message(session, group_id, text_message(f"错误"))
        logger["info"](f"{traceback.format_exc()}")
        
    
    
def checker(group_id: int, sender_id: int, message):
    return message[1].startswith("画画")

aidraw = Plugin('aidraw')
aidraw.register_callback('group.@fumoP', handler, checker)
