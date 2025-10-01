from typing import Dict

from readables.annotations import experimental
from readables.dlock.blocking.state_manager import DLockStateManager


@experimental
class DLock:
    """
    Blocking Distributed Lock

    :param DLockStateManager manager: The state manager
    :param str id: The ID of the lock
    """

    def __init__(self,
                 manager: DLockStateManager,
                 id: str):
        self.__id = id
        self.__manager = manager

    @property
    def id(self):
        return self.__id

    def acquire(self):
        self.__manager.acquire(self.id)

    def locked(self):
        return self.__manager.is_actively_locked(self.id)

    def release(self):
        self.__manager.release(self.id)

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        # NOTE: Intentionally not handling error.
        return


@experimental
class DLockFactory:
    def __init__(self,
                 manager: DLockStateManager):
        self.__manager = manager
        self.__locks: Dict[str, DLock] = dict()

    def lock(self, id: str) -> DLock:
        return DLock(manager=self.__manager,
                     id=id)
