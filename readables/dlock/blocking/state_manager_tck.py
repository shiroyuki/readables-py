"""
Test Compatibility Kit for Blocking Distributed Lock
"""

from typing import Optional

from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from time import sleep, time

from readables.dlock.blocking.core import DLockFactory
from readables.dlock.blocking.state_manager import DLockStateManager


def check(dlsm: DLockStateManager,
          number_of_concurrent_tasks: int = 5,
          task_duration: float = 1.0,
          timeout_duration: Optional[float] = None,
          verbose: bool = False):
    console_lock = Lock()
    timeout_duration = timeout_duration or ((task_duration * number_of_concurrent_tasks) + 1)
    dlf = DLockFactory(manager=dlsm)

    def _worker(idx: int):
        if verbose:
            with console_lock:
                print(f'W-{idx}: Begin')

        with dlf.lock('test') as l:
            if verbose:
                with console_lock:
                    print(f'W-{idx}: Enter the lock.')

            assert l.locked(), 'The distributed lock is not locked at the beginning.'
            sleep(task_duration)

            if verbose:
                with console_lock:
                    print(f'W-{idx}: Exit the lock.')

        if verbose:
            with console_lock:
                print(f'W-{idx}: End')

    with ThreadPoolExecutor(max_workers=number_of_concurrent_tasks) as pool:
        start_time = time()

        futures = []

        for i in range(number_of_concurrent_tasks):
            futures.append(pool.submit(_worker, idx=i))

        for _ in as_completed(futures, timeout=timeout_duration):
            pass

    runtime = time() - start_time

    if verbose:
        print(f'Complete in {runtime:.3f}s')

    assert runtime <= timeout_duration, \
        f'The ACTUAL total runtime ({runtime:.3f}s) exceeded the expected total runtime ({timeout_duration}).'
