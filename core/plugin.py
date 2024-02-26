from typing import List, Dict, Union, Tuple, Callable
import collections

import json

Callback = collections.namedtuple("Callback", ["event_type", "fn", "checker"])

class Plugin:
    name: str
    # scope: Dict[str, Union[List[int], str]] # str must be "all"
    callback: List[Callback]

    session: str # will be set by app for safety

    def __init__(self, _name: str):
        self.name = _name
        # with open(f"plugin/{_name}/{_name}.json", 'r') as f:
            # config = json.loads(f.read())
        # self.scope = config.scope

        self.callback = []

    def handle(self, event_type: str, **kwargs):
        task = []
        for i in self.callback:
            if i.event_type == event_type:
                try:
                    if i.checker(**kwargs):
                        task.append(i.fn(self.session, **kwargs))
                except:
                    # save it into log
                    print(f"{self.name} failed to handle {event_type}")
                    pass
        return task

    def register_callback(self, event_type: str, handler: Callable, checker: Callable = lambda *args,  **kwargs: True):
        # handler don't have to be a function, as long as it can be executed.
        self.callback.append(Callback(event_type, handler, checker))
    