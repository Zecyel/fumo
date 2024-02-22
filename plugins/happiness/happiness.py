from sdk.send_message import send_group_message
from sdk.message import text_message
import random
from core.plugin import Plugin

saying = [
    "我已经习惯了没有家，但我不介意有一个。",
    "我感觉很好。",
    "看来我离家很远了。",
    "我把这个地方留给我自己……我太喜欢它了。",
    "我有一颗自由的灵魂。我不喜欢这么多人挤在我身边。",
    "我讨厌拥挤。我更喜欢开阔的地方！",
    "我很喜欢在森林闲逛。我喜欢这里。",
    "我不太喜欢海洋。这里没什么可做的。",
    "我讨厌腐化之地，这里的恐怖力量瞬间就能把人撕成碎片。",
    "我讨厌猩红之地，这里的恐怖力量瞬间就能把人撕成碎片。",
    "我讨厌地牢，这里的恐怖力量瞬间就能把人撕成碎片。",
    "我很喜欢服装商，我们有很多共同点。",
    "我很喜欢动物学家，我们有很多共同点。",
    "蒸汽朋克人惹怒我了。也许是因为奇怪的衣服？",
    "我讨厌油漆工在附近。这个世界本来就是很美好的！",
    "身边有公主让我感到轻松自在，就像终于摆脱了诅咒一样。"
]

def happiness_handler(session: str, group_id: int, sender_user_id: int, message: str):
    if message == "快乐":
        send_group_message(session, group_id, text_message(random.choice(saying)))

happiness = Plugin('httpcat')
happiness.register_callback('message.group.text_message', happiness_handler)
