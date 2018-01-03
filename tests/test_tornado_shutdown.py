import signal
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from ustack_tornado_shutdown import tornado_shutdown


class TestTornadoShutdown(unittest.TestCase):
    @mock.patch("signal.signal")
    def test_on_sigterm_registers_sigterm_handler_that_shuts_down_server_and_ioloop(
            self, mock_signal):
        mock_server = mock.Mock()
        mock_ioloop = mock.Mock()

        tornado_shutdown.on_sigterm(mock_server, mock_ioloop)

        mock_signal.assert_called_once_with(signal.SIGTERM, mock.ANY)

        # Simulate the OS calling the signal handler
        mock_signal.call_args[0][1]("ignored", "also-ignored")

        mock_ioloop.add_callback_from_signal.assert_called_once_with(mock.ANY)

        # Simulate the IO loop calling the callback
        mock_ioloop.add_callback_from_signal.call_args[0][0]()

        mock_server.stop.assert_called_once_with()
        mock_ioloop.call_later.assert_called_once_with(2, mock.ANY)

        # Simulate the IO loop calling the delayed callback
        mock_ioloop.call_later.call_args[0][1]()

        mock_ioloop.stop.assert_called_once_with()
