from sdk.send_message import send_group_message
from sdk.message import local_voice_message
from core.plugin import Plugin
from config import DIR_PATH

async def handler(session: str, group_id: int, sender_id: int, message):
    await send_group_message(session, group_id, local_voice_message(DIR_PATH + "/asset/sound/6koybirm.mp3"))
genshin = Plugin('genshin')
genshin.register_callback('group.@fumo', handler)
