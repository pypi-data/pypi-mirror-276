from __future__ import annotations

from .parser import parse_interval, sum_units
from .task import Aging, SchedulingTask, TaskCallback
from asyncio import sleep
from typing_extensions import NotRequired, TypedDict, Unpack, overload


class Scheduler:
    def __init__(self) -> None:
        self.tasks: dict[str, SchedulingTask] = {}
        self.name_counters: dict[str, int] = {}

    async def tick(self) -> None:
        """send ticks to every task, giving control on every iteration"""
        for task in self.tasks.values():
            task.tick(self)
            await sleep(0)

    async def loop(self) -> None:
        """run scheduler indefinitely"""
        while True:
            await self.tick()

    async def tick_nowait(self) -> None:
        """send ticks to every task, but do not give control at all"""
        for task in self.tasks.values():
            task.tick(self)

    def add_task(self, task: SchedulingTask) -> None:
        key: str = task.final_name
        callback_name: str = key

        if key not in self.name_counters:
            self.name_counters[key] = 0
        else:
            callback_name = f"{key} #{self.name_counters[key]}"

        self.name_counters[key] += 1

        self.tasks[callback_name] = task

    @property
    def every(self) -> SchedulerPolicy:
        return SchedulerPolicy(self)

    @property
    def once(self) -> SchedulerPolicy:
        return SchedulerPolicy(self)


class SchedulerPolicyKwargs(TypedDict):
    # basic policy fields
    use_age: NotRequired[Aging | None]
    on_error: NotRequired[TaskCallback | None]
    name: NotRequired[str | None]

    # scheduler (why not)
    scheduler: NotRequired[Scheduler]

    # units
    milliseconds: NotRequired[float]
    seconds: NotRequired[float]
    minutes: NotRequired[float]
    hours: NotRequired[float]
    days: NotRequired[float]
    weeks: NotRequired[float]
    ms: NotRequired[float]
    s: NotRequired[float]
    m: NotRequired[float]
    h: NotRequired[float]
    d: NotRequired[float]
    w: NotRequired[float]


class SchedulerPolicy:
    def __init__(
        self,
        scheduler: Scheduler,
        interval: float = 0,
        on_error: TaskCallback | None = None,
        use_age: Aging | None = None,
        name: str | None = None,
    ):
        self.scheduler = scheduler
        self.interval = interval
        self.on_error = on_error
        self.use_age = use_age
        self.name = name

    def derive(self, **kwargs) -> SchedulerPolicy:
        data = {
            "scheduler": self.scheduler,
            "interval": self.interval,
            "use_age": self.use_age,
            "on_error": self.on_error,
            "name": self.name,
        }

        data.update({k: v for k, v in kwargs.items() if k in data})

        return SchedulerPolicy(**data)

    def age_with(self, aging: Aging) -> SchedulerPolicy:
        return self.derive(use_age=aging)

    def set_error_handler(self, on_error: TaskCallback) -> SchedulerPolicy:
        return self.derive(on_error=on_error)

    def set_name(self, name: str) -> SchedulerPolicy:
        return self.derive(name=name)

    def __getattr__(self, attr: str) -> SchedulerPolicy:
        interval = parse_interval(attr)

        return self.derive(interval=interval)

    @overload
    def __call__(
        self, f: None = None, **kwargs: Unpack[SchedulerPolicyKwargs]
    ) -> SchedulerPolicy:
        ...

    @overload
    def __call__(self, f: TaskCallback) -> None:
        ...

    def __call__(
        self,
        f: TaskCallback | None = None,
        **kwargs: Unpack[SchedulerPolicyKwargs],
    ) -> SchedulerPolicy | None:
        if f:
            self.scheduler.add_task(
                SchedulingTask(
                    callback=f,
                    interval=self.interval,
                    on_error=self.on_error,
                    use_age=self.use_age,
                )
            )
            return

        interval = sum_units(
            {k: v for k, v in kwargs.items() if isinstance(v, (int, float))}
        )

        if interval:
            return self.derive(**kwargs, interval=interval)

        return self.derive(**kwargs)


run = Scheduler()
