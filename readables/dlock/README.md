# Distributed Lock

> [!NOTE]
> This code is experimental. More documentation will be provided soon. In the meanwhile,
> please check out [the test](../../tests/test_dlock.py) or the examples below.

### Example with the blocking version

```python
from readables.dlock.blocking.core import DLockFactory
from readables.dlock.blocking.state_manager import LocalLockStateManager

dlf = DLockFactory(manager=LocalLockStateManager())

with dlf.lock('sample'):
    # At the point, the lock has been acquired.
    ... # Your code :)
# At this point, the lock has been released.
```

### Example with the awaitable version

```python
from readables.dlock.awaitable.core import AwaitableDLockFactory
from readables.dlock.awaitable.state_manager import AwaitableLocalLockStateManager

dlf = AwaitableDLockFactory(manager=AwaitableLocalLockStateManager())

async def main():
    async with dlf.lock('sample'):
        # At the point, the lock has been acquired.
        ... # Your code :)
    # At this point, the lock has been released.
```