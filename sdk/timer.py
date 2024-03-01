import time

class Timer:
    scheduled_time: float
    def __init__(self, delay: float): # in seconds
        self.scheduled_time = time.time() + delay
    
    def check(self) -> bool:
        return time.time() > self.scheduled_time
