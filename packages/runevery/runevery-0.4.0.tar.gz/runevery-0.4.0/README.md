Runevery (one word, as in 'bakery') is a simple async scheduling library to rule all your tasks.

> [!NOTE]
> It is highly recommended to use type-checking with runevery. Not only did I spent some time polishing it here, but also types are cool and nice. And I won't be covering some stuff that is obvious from the names.

> [!IMPORTANT]
> This package is fresh and the readme is a stub. It includes most of the information, but at times poorly worded or structured. This doc doesn't have enough examples of advanced usage, which is also not great.

# Installation

Just install [`runevery` package](https://pypi.org/project/runevery/) (pip, poetry, you name it).

# Introduction

Let's say we want to update user information every hour.

```python
import asyncio
from runevery import run

@run.every.hour
async def update_users():
    ...

# this last line and asyncio import are omitted in other examples for clarity
asyncio.run(run.loop())
```

Well... That is what you need.

Okay, maybe every two hours then?

```python
from runevery import run

# @run.every.2hours # oops, that didn't work
@run.every.two_hours # i mean...
async def update_users():
    ...
```

Well, full disclosure, you don't necessarily need to call `run.every.two_hours_and_seven_minutes` (although you actually can), you can actually use `run.every(hours=2, minutes=7)`:

```python
from runevery import run

@run.every(hours=2, minutes=7)
async def update_users():
    ...
```

But that's boring. Let's dive into some other features.

# Advanced

## Task scheduling process explanation

`runevery` is a rather simple library when it comes to checking if a task should run.

You start with a `Scheduler` instance (runevery.run is a pre-defined one).  
Then you populate it's task pool (the best way is through `scheduler.every`, but you can also add tasks to the scheduler.tasks dict) with instances of `SchedulingTask`.

On creation, `SchedulingTask` creates its own run queue with one element (current timestamp). This queue defines when the executions should take place. It doesn't try to add many elements to the queue, one (next run) is often enough.

When you run the scheduler loop, it iterates over all tasks and gives each one a tick (calls `task.tick(self)`, actually). Task then decides if it should run a callback (if the nearest element of the queue is less than the current time and no [aging](#aging) is involved).

Then it uses something similar to `loop.create_task(callback(...))` to run your callback, removes the used queue entry and inserts a new one. That's all!

## Aging

Often, recurring tasks are not just "need to run every 5 minutes", but bound to an external time state. For example, you may need to run a task every 24h, but exactly at 3:45 AM.
Or you need to update your data not more that once in an hour, using a non-persistent script.

In solutions like cron, the first example is trivial. But the second is rather weird for cron to use. `runevery` tries to solve both and more with "aging" information.

You can attach any object that implements aging protocol (later on that), and the task will automatically reschedule if it needs to wait a bit more.

Aging protocol is simple: you need anything with a method `get_remaining_time(interval: float) -> float`. This method accepts the interval from the task (in seconds), and should return the amount of time to wait. If it's positive, the task would reschedule to a later point.

For example:

```python
from runevery import run
import pickle as json # oopsie woopsie
from time import time

# a very good database implementation, do not try at home
class VeryDatabase:
    def __init__(self):
        with open("mydatabase.txt") as file:
            self.data = json.load(file)

    def get_remaining_time(self, interval: float) -> float:
        return interval - (time() - self.data["last_update"])

    def save(self):
        with open("mydatabase.txt") as file:
            json.dump(self.data)


db = VeryDatabase()


@run.every.five_days(use_age=db)
async def update_db():
    # this would run not more than once every 5 days, even if we restart the script over and over (assuming that our changes actually persist in the database)
    db.data["last_update"] = time()
    db.save()
```

This solution is simple. `VeryDatabase.get_remaining_time` here calculates how much time had passed since the last update, and returns a difference between interval and that amount.  
The result is basically the amount of time the scheduler needs to wait until interval has passed.

> [!IMPORTANT]
> Keep in mind that the "last_update" field in this example should not be changed from any other script (unless you want those changes to influence the scheduling).

The rescheduling can be done more precisely and creatively, though:

```python
from runevery import run
from time import time


class RoundTimeEnjoyer:
    def get_remaining_time(self, interval: float) -> float:
        ts = int(time())

        if ts % interval != 0: # it's not round enough
            return 0.5 # wait 0.5 seconds to check again
        return 0 # yay!


@run.every(seconds=100_000_000, use_age=db)
async def hundred_million_seconds():
    print(f"yay! it's {int(time())}!") # "yay, it's 1800000000!" (well, your result might actually vary if you're checking this out after 15.01.2027)

```

Since the check is done before the callback is started, task can be rescheduled infinitely before your aging container eventually decides it's time.
Be aware that this could actually skip a round second, so for some cases, a concrete rescheduling is needed (or checking that the callback was actually called, as in database example)

## Manual scheduling magic

Let's suppose you are smart enough to figure out the timestamp of the next run. You say "hey, I want to be able to manage scheduling from inside the callback!!! This is cool!".

Yeah, okay. Add `task` argument to your callback:

```python
from runevery import run, SchedulingTask
from time import time
from math import ceil

def next_round():
    return ceil(int(time()) // 100_000_000) * 100_000_000


@run.every # this is actually more like @run.once, but both are the same and we are managing the scheduling manually anyway
async def hundred_million_seconds(task: SchedulingTask):
    # task.schedule(timestamp) adds an entry in scheduling queue. Your task will run at this timestamp (or later in case of something blocking)
    task.schedule(next_round())

    if int(time()) % 100_000_000:
        return

    print(f"yay! it's {int(time())}!")
```

This callback will run at scheduler loop start, as well as at timestamps such as 1800000000, 1900000000, and so on. The condition is needed to filter out the first non-round run.

Various methods for scheduling are:

### task.schedule(timestamp: float)

Adds a timestamp to the scheduling queue.

### task.discard_run()

Removes the nearest run from the scheduling queue. If the queue is empty, does nothing. If called from a task, removes the _next_ run (since the current is already removed)

### task.reschedule(timestamp: float)

Removes the next run and inserts a new one. Functionally equal to a `task.discard_run()` followed by a `task.schedule(timestamp)`

### task.pause_until(timestamp: float, save_runs: bool = False)

Pause task runs until `timestamp` time. If the nearest run is after `timestamp`, does nothing.

If `save_runs=False` (default), removes all runs before `timestamp`. Otherwise, moves each run to `run_timestamp + timestamp - current_timestamp`.

### task.pause_for(seconds: float, save_runs: bool = False)

Same as `task.pause_until(current_timestamp + seconds, save_runs)`

## Scheduler access from the callback

Same as with task argument, you can add `scheduler` argument and enjoy the full access to the scheduler that has ticked this task. This can be useful if you want, for example, schedule even more tasks dynamically, or edit other tasks, etc.

## Manual ticks

Normally, you should call `scheduler.loop()` as an async coroutine and live happily ever after. But sometimes a more granular control is nice.  
You can use `await scheduler.tick()` to run one iteration of task ticks (will call `sleep(0)` to give control after each task.tick(), if you don't want that, use `await scheduler.tick_nowait()` for an instant tick)

## Many schedulers

`runevery.run` is an instance of a `Scheduler` class. You may want to use several instances with separate task pools for some reason, just do that:

```python
from runevery import Scheduler

walk = Scheduler()
drive = Scheduler()
swim = Scheduler()

@swim.every.five_weeks
async def ummmm():
    print("I don't know")

```

## Error handling

> [IMPORTANT]
> Error callback has to have the same arguments as original the task callback. This limitation may be removed in future versions.

You can pass an extra callback into `on_error` argument:

```python
from runevery import run

async def error_happens():
    print(":(")

@run.once(on_error=error_happens)
async def thisfails():
    raise ValueError

```
