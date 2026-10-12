"""Sliding-window rate limiter.

In-process memory works for a single instance. For several instances,
swap this for a Redis-backed limiter with the same allow() interface.
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict, deque


class RateLimiter:
    def __init__(self, per_minute: int):
        self.per_minute = per_minute
        self.hits: dict[str, deque] = defaultdict(deque)
        self.lock = threading.Lock()

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        with self.lock:
            q = self.hits[key]
            while q and now - q[0] > 60:
                q.popleft()
            if len(q) >= self.per_minute:
                return False
            q.append(now)
            if len(self.hits) > 50_000:  # keep memory bounded
                for k in [k for k, v in self.hits.items() if not v][:10_000]:
                    del self.hits[k]
            return True
