import asyncio
import contextvars

# https://docs.python.org/3/library/contextvars.html#asyncio-support
client_addr_var = contextvars.ContextVar("client_addr")


def render_goodbye():
    # The address of the currently handled client can be accessed
    # without passing it explicitly to this function.

    client_addr = client_addr_var.get()
    return f"Good bye, client @ {client_addr}\r\n".encode()


async def handle_request(reader, writer):
    addr = writer.transport.get_extra_info("socket").getpeername()
    client_addr_var.set(addr)

    # In any code that we call is now possible to get
    # client's address by calling 'client_addr_var.get()'.

    while True:
        line = await reader.readline()
        print(line)
        if not line.strip():
            break

    writer.write(b"HTTP/1.1 200 OK\r\n")  # status line
    writer.write(b"\r\n")  # headers
    writer.write(render_goodbye())  # body
    writer.close()


async def main():
    srv = await asyncio.start_server(handle_request, "127.0.0.1", 8081)

    async with srv:
        await srv.serve_forever()


asyncio.run(main())

# To test it you can use telnet or curl:
#     telnet 127.0.0.1 8081
#     curl 127.0.0.1:8081
