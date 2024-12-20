import asyncio

from contextvars import ContextVar
from uuid import uuid4

import asyncio


class DbConnection:
    async def commit(self):
        await asyncio.sleep(1)

    async def rollback(self):
        await asyncio.sleep(1)

    async def start(self):
        await asyncio.sleep(1)

    async def close(self):
        await asyncio.sleep(1)


class LazyDbConnection:
    def __init__(self):
        self.id = uuid4()
        self._db_connection = None

    async def __aenter__(self):
        # We defer the connection start at first get_db
        return self

    async def get_db(self):
        if self._db_connection is None:
            # Initialise connection if needed
            self._db_connection = await DbConnection().start()

        return self._db_connection

    async def __aexit__(self, exc_type, exc, tb):
        if self._db_connection is None:
            return
        try:
            if exc is None:
                await self._db_connection.commit()
            await self._db_connection.rollback()
        finally:
            await self._db_connection.close()


# https://docs.python.org/3/library/contextvars.html#asyncio-support
db_singleton: ContextVar[LazyDbConnection] = ContextVar("db", default=None)

async def do_something():

    db = await db_singleton.get().get_db()
    # Do something with db
    return 42

async def do_something_else():

    db = await db_singleton.get().get_db()
    # Do something with db
    return 27

async def handle_request(reader, writer):
    async with LazyDbConnection():
        response = sum(await asyncio.gather(do_something(), do_something_else()))

    writer.write(b'HTTP/1.1 200 OK\r\n')  # status line
    writer.write(b'\r\n')  # headers
    writer.write(response)  # body
    writer.close()

async def main():
    srv = await asyncio.start_server(
        handle_request, '127.0.0.1', 8081)

    async with srv:
        await srv.serve_forever()

asyncio.run(main())

# To test it you can use telnet or curl:
#     telnet 127.0.0.1 8081
#     curl 127.0.0.1:8081
