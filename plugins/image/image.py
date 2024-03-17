from sdk.send_message import send_group_message
from sdk.message import instant_image_message
from core.plugin import Plugin
from PIL import Image

async def handler(session: str, group_id: int, sender_id: int, message):
    a = Image.new("RGB", (50, 50), (255, 255, 0))
    await send_group_message(session, group_id, instant_image_message(a))

def checker(group_id: int, sender_id: int, message):
    return message[0] == "image"

image = Plugin('image')
image.register_callback('group.P', handler, checker)
