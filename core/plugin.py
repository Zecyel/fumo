from typing import List, Dict, Union, Tuple
import json

class Plugin:
    name: str
    # scope: Dict[str, Union[List[int], str]] # str must be "all"
    callback: List[Tuple[str, object]]

    session: str # will be set by app for safety

    def __init__(self, _name: str):
        self.name = _name
        # with open(f"plugin/{_name}/{_name}.json", 'r') as f:
            # config = json.loads(f.read())
        # self.scope = config.scope

        self.callback = []

    def handle(self, event_type: str, **kwargs):
        for i in self.callback:
            if i[0] == event_type:
                i[1](self.session, **kwargs)

    def register_callback(self, event_type: str, handler: object):
        # handler don't have to be a function, as long as it can be executed.
        self.callback.append((event_type, handler))
    