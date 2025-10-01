from abc import ABC, abstractmethod
from threading import Lock
from typing import Dict

from readables.annotations import experimental


@experimental
class DLockStateManager(ABC):
    """
    An interface of the lock state manager
    """
    @abstractmethod
    def acquire(self, lock_id: str):
        raise NotImplemented()

    @abstractmethod
    def is_actively_locked(self, lock_id: str) -> bool:
        raise NotImplemented()

    @abstractmethod
    def release(self, lock_id: str):
        raise NotImplemented()


@experimental
class LocalLockStateManager(DLockStateManager):
    """
    Local Lock State Manager
    """
    def __init__(self):
        self.__access_lock = Lock()
        self.__locks: Dict[str, Lock] = dict()

    def acquire(self, lock_id: str):
        with self.__access_lock:
            if lock_id not in self.__locks:
                self.__locks[lock_id] = Lock()
        # End of accessing to the lock map

        # Acquire the lock.
        self.__locks.get(lock_id).acquire()

    def is_actively_locked(self, lock_id: str) -> bool:
        with self.__access_lock:
            return lock_id in self.__locks or self.__locks.get(lock_id).locked()
        # End of access to the lock map

    def release(self, lock_id: str):
        with self.__access_lock:
            if lock_id not in self.__locks:
                return

            lock = self.__locks.get(lock_id)

            if lock.locked():
                lock.release()
        # End of access to the lock map

