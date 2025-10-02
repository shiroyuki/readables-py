import asyncio
from asyncio import Lock, sleep
from time import time
from typing import Optional

from readables.dlock.awaitable.core import AwaitableDLockFactory
from readables.dlock.awaitable.state_manager import AwaitableDLockStateManager


async def check_awaitable(dlsm: AwaitableDLockStateManager,
                          number_of_concurrent_tasks: int = 5,
                          task_duration: float = 1.0,
                          timeout_duration: Optional[float] = None,
                          verbose: bool = False):
    timeout_duration = timeout_duration or ((task_duration * number_of_concurrent_tasks) + 1)
    dlf = AwaitableDLockFactory(manager=dlsm)

    async def _worker(idx: int):
        if verbose:
            print(f'W-{idx}: Begin')

        async with dlf.lock('test') as l:
            if verbose:
                print(f'W-{idx}: Enter the lock.')

            assert await l.locked(), 'The distributed lock is not locked at the beginning.'
            await sleep(task_duration)

            if verbose:
                print(f'W-{idx}: Exit the lock.')

        if verbose:
            print(f'W-{idx}: End')

    start_time = time()

    cr_list = [
        _worker(i)
        for i in range(number_of_concurrent_tasks)
    ]

    await asyncio.gather(*cr_list)

    runtime = time() - start_time

    if verbose:
        print(f'Complete in {runtime:.3f}s')

    assert runtime <= timeout_duration, \
        f'The ACTUAL total runtime ({runtime:.3f}s) exceeded the expected total runtime ({timeout_duration}).'
