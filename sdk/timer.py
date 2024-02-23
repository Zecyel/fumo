import time

class StopWatch:
    start_time: float
    seconds: float

    def __init__(self, seconds: float):
        self.start_time = time.time()
        self.seconds = seconds

    def check(self) -> bool:
        return time.time() >= start_time + seconds
