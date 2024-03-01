# FUMO Documentation

## Tutorial

群聊机器人是使用最普遍的一种机器人，而大部分的群聊机器人都是靠消息驱动的（即群友说了一句话，然后fumo回应）。其他情况，例如fumo主动向群聊发送消息（例如每日词云定时在零点发送），私聊机器人等，在此教程中不作讨论。

### 1. 初始化一个插件

首先需要为这个插件起一个名字，插件的名字和python中变量名的要求相同，即不能以数字开头，只能包含字母数字下划线。

例如，如果插件名字为`guess`，则需要创建文件`guess.py`，框架如下：

```python
from core.plugin import Plugin

async def handler(session: str, group_id: int, sender_user_id: int, message: str):
    pass

guess = Plugin('guess')
guess.register_callback('group.text_message', handler)
```

### 2. 理解消息处理函数

注意这一行代码：

```python
guess.register_callback('group.text_message', handler)
```

这行代码表示当收到群的**纯文本消息**时，调用`handler`函数进行处理。

`handler`的四个参数解释：
- `session`: 机器人与QQ服务器的会话标识符（不用管）
- `group_id`: 群号
- `sender_user_id`: 消息发送者QQ号
- `message`: 消息内容

### 3. 向群中发送消息

首先需要导入两个模块：

```python
from sdk.send_message import send_group_message
from sdk.message import text_message
```

通常来说，可以通过`await send_group_message(session, group_id, text_message("hello"))`就可以向群中发送消息。

例如，现在已经部署的`摸摸`插件，其源代码如下：

```python
from sdk.send_message import send_group_message
from sdk.message import text_message
from core.plugin import Plugin

privileged_user = [2530469979]
async def handler(session: str, group_id: int, sender_user_id: int, message: str):
    if message[:2] == "摸摸":
        if sender_user_id in privileged_user:
            await send_group_message(session, group_id, text_message("主人喵~"))
        else:
            await send_group_message(session, group_id, text_message("爪巴"))

pat = Plugin('pat')
pat.register_callback('group.text_message', handler)
```

### 4. 数据持久化

很多时候，qq机器人不局限于“一问一答”，可以通过导入模块`from sdk.temp_data import alloc, fetch, dump`来临时保存数据。

这三个函数都需要的一个参数是`key`，是很重要的一个参数，它用于“区分上下文”。具体来说，`alloc`函数会为这个`key`分配一个内存空间，`fetch`函数会从该内存空间中读取数据，`dump`函数会向该内存空间中写入数据。

函数参数：（注意下文所述的“对象”，不能是`int`, `str`, `bool`或`float`，通常来说可以用`dict`）

```python
def alloc(key: str, value: object): # 创建一个key对应的对象
def fetch(key: str) -> object: # 根据key读取这个对象，如果没找到则返回 None
def dump(key: str): # 删除key对应的对象
```

先来一个简单的demo：

```python
async def handler(session: str, group_id: int, sender_user_id: int, message: str):
    key = "aha"
    if message == "保存":
        alloc(key, {
            "group_id": group_id.
            "sender_user_id": sender_user_id
        })
        await send_group_message(session, group_id, text_message("已保存"))
        return
    
    if message == "读取":
        data = fetch(key)
        if data == None:
            await send_group_message(session, group_id, text_message("未找到相关数据"))
            return
        await send_group_message(session, group_id, text_message(f"找到数据：群号{group_id}，发送者qq号{sender_user_id}"))
        return

    if message == "删除":
        dump(key)
```

这段代码可以在发送消息“保存”时保存发送者和群聊的qq号，发送消息“读取”时读取并发送保存的数据，发送消息“删除”时删除保存的数据。

那么这段代码存在什么问题呢？

答案是，fumo不止加了一个群，如果在A群保存，B群读取，则会读取到A群的数据（很怪就是了）

那么怎么改呢？

答案是，让`key`依赖于不同的群而不同，将`key = "aha"`改成`key = f"aha_{group_id}"`就可以起到隔离的作用。（PS，如果改成`key = f"aha_{sender_user_id}"`，那么可以让用户A保存的数据只能被用户A读取，因为不同用户发送消息时key不相同，不会读取到其他用户的数据）

### 5. 一个实例

```python
from sdk.send_message import send_group_message
from sdk.message import text_message
from plugins.guess_npc.saying import npc_saying
import random
from core.plugin import Plugin
from sdk.temp_data import alloc, fetch, dump

npc_saying = npc_saying = {
    "向导": [
        "我的工作是为你接下来的任务提供建议。建议你遇到任何困难时都来和我谈谈。",
        "他们说，有个人会告诉你如何在这地方上生存……哦等下。那个人就是我。",
        "晚上你应该呆在家里。黑夜在外面转悠非常危险。"
    ],
    "商人": [
        "剑克纸！赶紧买一把。",
        "你想要苹果？你想要胡萝卜？你想要菠萝？我们只有火把。",
        "美好的清晨，你说呢？你需要什么？"
    ],
    "护士": [
        "转过头去咳嗽。",
        "我见过更大的……是的，我确实见过更大的伤口。",
    ]
}

npc_name = [key for (key, value) in npc_saying.items()]

async def handler(session: str, group_id: int, sender_user_id: int, message: str):
    key = f"guess_npc_{group_id}"
    if message == "猜npc":
        if fetch(key) != None:
            await send_group_message(session, group_id, text_message("请先猜对当前npc，或输入“结束游戏”"))
            return
        
        npc = random.choice(npc_name)
        saying = random.choice(npc_saying[npc])
        alloc(key, {
            "npc": npc,
            "saying": saying
        })
        await send_group_message(session, group_id, text_message(saying))
        return
        
    data = fetch(key)

    if message == "结束游戏":
        await send_group_message(session, group_id, text_message(f"游戏结束，答案是：{data['npc']}"))
        dump(key)
        return
    
    if message == data["npc"]:
        await send_group_message(session, group_id, text_message(f"猜对咯，答案是{data['npc']}！"))
        dump(key)
        return
    elif message in npc_name:
        await send_group_message(session, group_id, text_message(f"猜错了，继续猜吧！"))
        return

guess_npc = Plugin('guess_npc')
guess_npc.register_callback('group.text_message', handler)
```