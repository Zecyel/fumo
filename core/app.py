from sdk.recv_message import recv_message
from sdk.message import convert_message
import sdk.api as api
from sdk.send_message import send_group_message
from core.plugin import Plugin
from typing import List
import asyncio

VERIFY_KEY = "1234567890"
QQ = 3793571711

class App:

    plugin: List[Plugin]
    session: str

    def __init__(self):
        verification = api.post('/verify', {
            "verifyKey": VERIFY_KEY
        })
        self.session = verification["session"]

        api.post('/bind', {
            "sessionKey": self.session,
            "qq": QQ
        })

        self.plugin = []


    def register_plugin(self, plugin):
        self.plugin.append(plugin)
        plugin.session = self.session # will be modifyed later.

    # async def task(self, result):
    #     msg = await recv_message(self.session)
    #     print("got msg:", msg) # log system......
    #     msg_type, args = convert_message(msg)
    #     print("========", msg_type, args)
    #     for plugin in self.plugin:
    #         for task in plugin.handle(msg_type, **args):
    #             print('get task', task)
    #             result.append(task)

    # async def run(self):
    #     task = []
    #     task_when_blocked = []
    #     async def receiver(task):
    #         await self.task(task)

    #     while True:
    #         task = task_when_blocked[:]
    #         task_when_blocked = []
    #         await self.task(task)
    #         print(task)
    #         await asyncio.gather(*task, receiver(task_when_blocked))
    #         await asyncio.sleep(0.05)


    async def run(self):
        while True:
            task = []
            
            msg = await recv_message(self.session)
            print("got msg:", msg) # log system......
            msg_type, args = convert_message(msg)
            print("========", msg_type, args)
            
            for plugin in self.plugin:
                task = [*task, *plugin.handle(msg_type, **args)]
            print(task)
            await asyncio.gather(*task)
            await asyncio.sleep(0.05)
