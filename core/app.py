from sdk.recv_message import recv_message
from sdk.message import convert_message
import sdk.api as api
from sdk.send_message import send_group_message
from core.plugin import Plugin
from typing import List

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

    def run(self):
        print(self.plugin)
        while True:
            msg = recv_message(self.session)
            print("got msg:", msg)
            msg_type, args = convert_message(msg)
            print("========", msg_type, args)
            for plugin in self.plugin:
                plugin.handle(msg_type, **args)
