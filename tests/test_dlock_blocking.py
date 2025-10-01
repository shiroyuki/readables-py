from unittest import TestCase

from readables.dlock.blocking.state_manager import LocalLockStateManager
from readables.dlock.blocking.state_manager_tck import check


class TestUnit(TestCase):
    def test_tck(self):
        check(LocalLockStateManager())