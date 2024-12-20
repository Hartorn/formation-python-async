import asyncio


async def some_function():
    print("INSIDE")
    return 42


async def main():
    print("HERE")
    some_function()
    print("THERE")


asyncio.run(main())
