from sdk.send_message import send_group_message
from sdk.message import web_image_message, text_message
from core.plugin import Plugin

http_code = [100, 101, 102, 103, 200, 201, 202, 203, 204, 205, 206, 207, 208, 226, 300, 301, 302, 303, 304, 305, 307, 308, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423, 424, 425, 426, 428, 429, 431, 444, 450, 451, 497, 498, 499, 500, 501, 502, 503, 504, 506, 507, 508, 509, 510, 511, 521, 522, 523, 525, 530, 599]

async def handler(session: str, group_id: int, sender_id: int, message):
    code = int(message[1][3:])
    if code in http_code:
        await send_group_message(session, group_id, web_image_message(f"https://http.cat/images/{code}.jpg"))
    else:
        await send_group_message(session, group_id, text_message("请输入正确的状态码"))

def checker(group_id: int, sender_id: int, message):
    return message[1][:3] == "cat"

httpcat = Plugin('httpcat')
httpcat.register_callback('group.@fumoP', handler, checker)
