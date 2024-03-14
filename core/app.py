from sdk.recv_message import recv_message
from sdk.message import convert_message
import sdk.api as api
from sdk.send_message import send_group_message
from sdk.log import logger
from core.plugin import Plugin
from typing import List
import asyncio
from queue import Queue
from threading import Thread
import time
import traceback
from config import VERIFY_KEY, QQ

app_logger = logger("runtime", "App")

class App:

    plugin: List[Plugin]
    session: str
    task_queue: Queue

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
        self.task_queue = Queue()

    def register_plugin(self, plugin):
        self.plugin.append(plugin)
        plugin.session = self.session # will be modified later.

    def handle_task(self, task):
        try:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(task)
            loop.close()
        except Exception as e:
            app_logger["error"](f"Message task failed. Traceback: \n{traceback.format_exc()}")
    
    async def message_loop(self):
        print("<Message loop>: Thread started.")
        while True:
            try:
                msg = await recv_message(self.session)
                app_logger["info"](f"Get Message: {msg}")
                msg_type, kwargs = convert_message(msg)
                
                if msg_type == "":
                    continue

                for plugin in self.plugin:
                    for task in plugin.handle_message(msg_type, **kwargs):
                        self.task_queue.put(task)
                await asyncio.sleep(0.05)
            except:
                app_logger["error"](f"Message loop failed. Traceback: \n{traceback.format_exc()}")

    async def timer_loop(self):
        print("<Timer loop>: Thread started.")
        while True:
            for plugin in self.plugin:
                for task in plugin.handle_timer():
                    self.task_queue.put(task)
            await asyncio.sleep(0.05)

    def run(self):
        Thread(target=lambda: asyncio.run(self.message_loop()), name="message_loop").start()
        Thread(target=lambda: asyncio.run(self.timer_loop()), name="timer_loop").start()

        while True:
            if not self.task_queue.empty():
                Thread(target=lambda: self.handle_task(self.task_queue.get()), name="handle_message_task").start()
            time.sleep(0.05)
