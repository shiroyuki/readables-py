# Distributed Lock

> [!NOTICE]
> This code is experimental. More documentation will be provided soon.

```python
from readables.dlock.blocking.core import DLockFactory
from readables.dlock.blocking.state_manager import LocalLockStateManager

dlf = DLockFactory(manager=LocalLockStateManager())

with dlf.lock('sample'):
    # At the point, the lock has been acquired.
    ...
# At this point, the lock has been released.
```