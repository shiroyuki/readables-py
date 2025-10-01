from unittest import TestCase, IsolatedAsyncioTestCase

from readables.dlock.awaitable.state_manager import AwaitableLocalLockStateManager
from readables.dlock.awaitable.state_manager_tck import check_awaitable
from readables.dlock.blocking.state_manager import LocalLockStateManager
from readables.dlock.blocking.state_manager_tck import check


class TestUnit(TestCase):
    def test_tck(self):
        check(LocalLockStateManager())


class AwaitableTestUnit(IsolatedAsyncioTestCase):
    async def test_tck(self):
        await check_awaitable(AwaitableLocalLockStateManager())