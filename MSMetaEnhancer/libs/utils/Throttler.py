import asyncio
import time
from collections import deque
from typing import Deque


class Throttler:
    """
    Class to limit number of parallel requests by a rate (number per period of time).
    """
    def __init__(self, rate_limit=10, period=1, retry_interval=0.01):
        self.rate = rate_limit
        self.rate_limit = rate_limit
        self.period = period
        self.retry_interval = retry_interval

        self._task_logs: Deque[float] = deque()

    def increase_limit(self):
        """
        Increase rate up to allow limit.
        """
        if self.rate < self.rate_limit:
            self.rate += 1

    def decrease_limit(self):
        """
        Decrease rate (must be always positive).
        """
        if self.rate > 0:
            self.rate -= 1

    def flush(self):
        now = time.monotonic()
        while self._task_logs:
            if now - self._task_logs[0] > self.period:
                self._task_logs.popleft()
            else:
                break

    async def acquire(self):
        while True:
            self.flush()
            if len(self._task_logs) < self.rate:
                break
            await asyncio.sleep(self.retry_interval)

        self._task_logs.append(time.monotonic())

    async def __aenter__(self):
        await self.acquire()

    async def __aexit__(self, exc_type, exc, tb):
        pass
