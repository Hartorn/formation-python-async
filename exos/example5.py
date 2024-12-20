import asyncio


async def some_function():
    print("INSIDE")
    return 42


async def main():
    print("HERE")
    t = asyncio.create_task(some_function())
    # await asyncio.sleep(0)
    print("THERE")
    await t


asyncio.run(main())
