import asyncio
import os
import signal
from unittest import IsolatedAsyncioTestCase, mock

from ustack_tornado_shutdown import graceful_shutdown


class TestGracefulShutdown(IsolatedAsyncioTestCase):
    async def send_sigterm(self, wait_task: asyncio.Task[None]) -> bool:
        done = wait_task.done()

        os.kill(os.getpid(), signal.SIGTERM)

        return done

    @mock.patch("asyncio.sleep")
    async def test_on_sigterm_returns_after_sigterm_is_trapped(
        self,
        mock_sleep: mock.Mock
    ) -> None:
        wait_task = asyncio.create_task(graceful_shutdown.on_sigterm())

        finish_task = asyncio.create_task(self.send_sigterm(wait_task))

        await wait_task

        assert not await finish_task

        mock_sleep.assert_not_called()

    @mock.patch("asyncio.sleep")
    async def test_on_sigterm_calls_function_before_returning_when_specified(
        self,
        mock_sleep: mock.Mock
    ) -> None:
        fn = mock.Mock()

        wait_task = asyncio.create_task(graceful_shutdown.on_sigterm(fn))

        finish_task = asyncio.create_task(self.send_sigterm(wait_task))

        await wait_task

        await finish_task

        fn.assert_called_once_with()

        mock_sleep.assert_awaited_once_with(2)
