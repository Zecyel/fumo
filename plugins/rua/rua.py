from core.plugin import Plugin
from plugins.rua.data_source import generate_gif
from config import DIR_PATH
from sdk.image import download_image
from sdk.send_message import send_group_message
from sdk.message import local_image_message

async def handler(session: str, group_id: int, sender_id: int, message):
    im = generate_gif(f'{DIR_PATH}/asset/rua', download_image(message[1]["url"]))
    await send_group_message(session, group_id, local_image_message(f"{DIR_PATH}/asset/rua/output.gif"))

def checker(group_id: int, sender_id: int, message):
    return message[0] == "rua"

rua = Plugin('rua')
rua.register_callback('group.PI', handler, checker)