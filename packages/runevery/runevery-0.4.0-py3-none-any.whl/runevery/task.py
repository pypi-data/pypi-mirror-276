from __future__ import annotations

import inspect
from time import time
from asyncio import Task, AbstractEventLoop, get_event_loop
from time import time
from typing_extensions import Coroutine, Protocol, Callable
from heapq import heapify, heappush, heappop, heapreplace
from random import randint

from .utils import format_duration


TaskCallback = Callable[..., Coroutine[None, None, None]]


class Aging(Protocol):
    def get_remaining_time(self, interval: float) -> float:
        ...


class SchedulingTask:
    def __init__(
        self,
        callback: TaskCallback,
        interval: float,
        on_error: TaskCallback | None = None,
        use_age: Aging | None = None,
        name: str | None = None,
    ):
        self.callback = callback
        self.callback_kwargs = self.inspect_callback(callback)
        self.on_error = on_error

        self.interval = interval
        self.runs: dict[float, Task[None]] = {}
        self.scheduled: list[float] = [self.time]
        self.use_age = use_age
        self.name = name

    @property
    def time(self):
        return time()

    @staticmethod
    def inspect_callback(callback: TaskCallback) -> set[str]:
        signature = inspect.signature(callback)
        return set(signature.parameters)

    def run_callback(
        self,
        callback: TaskCallback,
        scheduler: Scheduler,
        event_loop: AbstractEventLoop | None,
    ):
        if not event_loop:
            event_loop = get_event_loop()

        kwargs = {
            "task": self,
            "scheduler": scheduler,
        }

        task = event_loop.create_task(
            callback(
                **{k: v for k, v in kwargs.items() if k in self.callback_kwargs},
            )
        )

        # save a reference to callback run so GC will not delete the task
        random_id = randint(0, int(10e9))
        self.runs[random_id] = task
        task.add_done_callback(lambda _: self.runs.pop(random_id, None))

    def tick(self, scheduler: Scheduler, event_loop: AbstractEventLoop | None = None):
        cur_time = self.time

        if not self.scheduled:
            return

        if self.scheduled[0] > cur_time:
            return

        aging_obj = self.use_age

        if aging_obj:
            diff = aging_obj.get_remaining_time(self.interval)

            if diff > 0:
                self.reschedule(self.time + diff)
                return

        if self.interval:
            self.schedule(cur_time + self.interval)

        self.discard_run()
        self.run(self.callback, scheduler, event_loop)

    def run(self, callback: TaskCallback, scheduler: Scheduler, event_loop):
        async def callback_wrapper(**kwargs):
            try:
                await callback(**kwargs)
            except:
                if self.on_error:
                    self.run_callback(self.on_error, scheduler, event_loop)

        self.run_callback(callback_wrapper, scheduler, event_loop)

    def schedule(self, ts: float):
        heappush(self.scheduled, ts)

    def discard_run(self):
        if len(self.scheduled):
            heappop(self.scheduled)

    def reschedule(self, ts: float):
        if len(self.scheduled):
            heapreplace(self.scheduled, ts)
        else:
            self.schedule(ts)

    def pause_until(self, timestamp: float, save_runs: bool = False):
        i = 0

        if timestamp <= self.time:
            timestamp = self.time

        diff = timestamp - self.scheduled[0]

        if diff < 0:
            return

        while i < len(self.scheduled):
            if self.scheduled[i] > timestamp:
                i += 1
                continue

            if save_runs:
                self.scheduled[i] += diff
                i += 1
            else:
                self.scheduled.pop(i)

        if not self.scheduled:
            self.scheduled.append(timestamp)

        heapify(self.scheduled)

    def pause_for(self, milliseconds: float, save_runs: bool = False):
        self.pause_until(self.time + milliseconds, save_runs)

    def format_freq(self) -> str:
        if not self.interval:
            return "once"

        return f"every {format_duration(self.interval)}"

    @property
    def default_name(self):
        return self.callback.__name__

    @property
    def final_name(self):
        return self.name or self.default_name

    def __repr__(self):
        return f"Task['run {self.final_name} {self.format_freq()}']"


from .scheduler import Scheduler
