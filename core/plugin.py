from typing import List, Callable
import collections
from sdk.timer import Timer
from sdk.log import logger
import traceback

plugin_logger = logger("runtime", "Plugin")

MessageCallback = collections.namedtuple("MessageCallback", ["event_type", "fn", "checker"])
TimerCallback = collections.namedtuple("TimerCallback", ["timer", "fn", "args", "kwargs"])

class Plugin:
    name: str
    message_callback: List[MessageCallback]
    timer_callback: List[TimerCallback]

    session: str # will be set by app for safety

    def __init__(self, _name: str):
        self.name = _name
        self.message_callback = []
        self.timer_callback = []

    def handle_message(self, event_type: str, **kwargs):
        task = []
        for i in self.message_callback:
            if i.event_type == event_type:
                try:
                    if i.checker(**kwargs):
                        task.append(i.fn(self.session, **kwargs))
                except:
                    plugin_logger["error"](f"{self.name} failed to handle {event_type}. Traceback:\n{traceback.format_exc()}")
        
        return task

    def handle_timer(self):

        task = []

        unhandled_timer = []
        for i in self.timer_callback:
            if i.timer.check():
                task.append(i.fn(*i.args, **i.kwargs))
            else:
                unhandled_timer.append(i)

        self.timer_callback = unhandled_timer # remove handled timer

        return task

    def register_callback(self, event_type: str, handler: Callable, checker: Callable = lambda *args,  **kwargs: True):
        # handler don't have to be a function, as long as it can be executed.
        self.message_callback.append(MessageCallback(event_type, handler, checker))
    
    def register_timer(self, timer: Timer, callback: Callable, *args, **kwargs):
        self.timer_callback.append(TimerCallback(timer, callback, args, kwargs))

def compoundChecker(*checkers: List[Callable]):
    def foo(*args, **kwargs):
        for checker in checkers:
            if not checker(*args, **kwargs):
                return False
        return True
    return foo
