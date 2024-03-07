from sdk.send_message import send_group_message
from sdk.message import text_message
from core.plugin import Plugin

hint = '''日麻点数计算：
需输入：位置 番数/符数/连庄
y表示庄家，n表示子家，不写默认子家
连庄数可不写，默认零本场
如果番数多余5番可不写符数
例如：y3/40/2表示3番40符的庄家二本场，fumo会说8300(2800)，自摸每人2900，荣和8300
例如：2/50表示子家2番50符的零本场，fumo会说3200(800,1600)，自摸庄家1600子家800，荣和3200'''

def to_100(a: int) -> int:
    if a % 100 != 0:
        return a // 100 * 100 + 100
    return a

async def handler(session: str, group_id: int, sender_id: int, message):
    message = message[1][2:].strip()
    if message == "help":
        await send_group_message(session, group_id, text_message(hint))
        return
    
    zhuangjia = False
    if message[0] in "ny":
        zhuangjia = message[0] == 'y'
        message = message[1:]
    message = list(map(int, message.split('/')))
    fan = message[0]
    if fan > 78:
        await send_group_message(session, group_id, text_message("开了是吧？😡"))
        # return

    if fan < 5:
        fu = message[1]
    else:
        fu = 1000
    lianzhuang = 0
    if len(message) == 3:
        lianzhuang = message[2]

    if fan <= 4: jibendian = min(fu * 2 ** (2 + fan), 2000)
    elif fan == 5: jibendian = 2000
    elif fan in [6, 7]: jibendian = 3000
    elif fan in [8, 9, 10]: jibendian = 4000
    elif fan in [11, 12]: jibendian = 6000
    elif fan >= 13: jibendian = fan // 13 * 8000

    if zhuangjia:
        ronghu = to_100(6 * jibendian) + 300 * lianzhuang
        zimo = to_100(2 * jibendian) + 100 * lianzhuang
        result = f"{ronghu}({zimo})"
    else:
        ronghu = to_100(4 * jibendian) + 300 * lianzhuang
        zimo_zhuang = to_100(2 * jibendian) + 100 * lianzhuang
        zimo_zi = to_100(jibendian) + 100 * lianzhuang
        result = f"{ronghu}({zimo_zi}, {zimo_zhuang})"
    await send_group_message(session, group_id, text_message(result))

def checker(group_id: int, sender_id: int, message):
    return message[1][:2] == "麻将"

mahjong = Plugin('mahjong')
mahjong.register_callback('group.@fumoP', handler, checker)
