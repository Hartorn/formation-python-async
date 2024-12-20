import asyncio


async def some_function():
    print("INSIDE")
    return 42


async def main():
    print("HERE")
    res = await some_function()
    print("THERE")
    print(res)


asyncio.run(main())
