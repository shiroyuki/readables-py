from typing import Dict

from readables.annotations import experimental
from readables.dlock.awaitable.state_manager import AwaitableDLockStateManager


@experimental
class AwaitableDLock:
    """
    Awaitable Distributed Lock

    :param DLockStateManager manager: The state manager
    :param str id: The ID of the lock
    """

    def __init__(self,
                 manager: AwaitableDLockStateManager,
                 id: str):
        self.__id = id
        self.__manager = manager

    @property
    def id(self):
        return self.__id

    async def acquire(self):
        await self.__manager.acquire(self.id)

    async def locked(self):
        return await self.__manager.is_actively_locked(self.id)

    async def release(self):
        await self.__manager.release(self.id)

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.release()
        # NOTE: Intentionally not handling error.
        return


@experimental
class AwaitableDLockFactory:
    def __init__(self,
                 manager: AwaitableDLockStateManager):
        self.__manager = manager
        self.__locks: Dict[str, AwaitableDLock] = dict()

    def lock(self, id: str) -> AwaitableDLock:
        return AwaitableDLock(manager=self.__manager,
                              id=id)
