# ustack-tornado-shutdown
Library for gracefully terminating a Tornado server on SIGTERM

## Example Without Grace Period

```python
import asyncio
from ustack_tornado_shutdown.graceful_shutdown import on_sigterm


async def run_forever():
    while True:
        asyncio.sleep(1)


async def main():
    asyncio.create_task(run_forever())

    await on_sigterm()


if __name__ == "__main__":
    asyncio.run(main())
```

## Example With Grace Period

```python
import asyncio
from tornado.web import Application
from ustack_tornado_shutdown.graceful_shutdown import on_sigterm


async def main():
    app = Application([])

    server = app.listen(8000)

    await on_sigterm(server.stop)


if __name__ == "__main__":
    asyncio.run(main())
```
