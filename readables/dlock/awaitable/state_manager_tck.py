import asyncio
from asyncio import Lock, sleep
from time import time

from readables.dlock.awaitable.core import AwaitableDLockFactory
from readables.dlock.awaitable.state_manager import AwaitableDLockStateManager


async def check_awaitable(dlsm: AwaitableDLockStateManager,
                          number_of_concurrent_tasks: int = 5,
                          task_duration: float = 1.0,
                          verbose: bool = False):
    console_lock = Lock()
    timeout_duration = (task_duration * number_of_concurrent_tasks) + 1
    dlf = AwaitableDLockFactory(manager=dlsm)

    async def _worker(idx: int):
        if verbose:
            with console_lock:
                print(f'W-{idx}: Begin')

        async with dlf.lock('test') as l:
            if verbose:
                with console_lock:
                    print(f'W-{idx}: Enter the lock.')

            assert await l.locked(), 'The distributed lock is not locked at the beginning.'
            await sleep(task_duration)

            if verbose:
                with console_lock:
                    print(f'W-{idx}: Exit the lock.')

        if verbose:
            with console_lock:
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