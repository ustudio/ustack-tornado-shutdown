import asyncio
from collections.abc import Callable
import logging
import signal
from typing import Any, Optional


async def on_sigterm(start_grace: Optional[Callable[[], Any]] = None) -> None:
    event = asyncio.Event()

    asyncio.get_running_loop().add_signal_handler(signal.SIGTERM, event.set)

    await event.wait()

    logging.info("Received signal SIGTERM")

    if start_grace is not None:
        logging.info("Starting grace period")
        start_grace()

        await asyncio.sleep(2)

    logging.info("Done waiting for SIGTERM")
