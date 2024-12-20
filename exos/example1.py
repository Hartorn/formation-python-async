#!/usr/bin/env python3
# rand.py

import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO)


async def makerandom(idx: int, threshold: int = 6) -> int:
    logging.getLogger(str(idx)).info("Initiated makerandom(%s)", idx)

    i = random.randint(0, 10)
    while i <= threshold:
        logging.getLogger(str(idx)).info(
            "makerandom(%s) == %s too low; retrying.", idx, i
        )
        await asyncio.sleep(idx + 1)
        i = random.randint(0, 10)
    logging.getLogger(str(idx)).info("---> Finished: makerandom(%s) == {%s}", idx, i)
    return i


async def main():
    res = await asyncio.gather(*(makerandom(i, 10 - i - 1) for i in range(3)))
    return res


if __name__ == "__main__":
    random.seed(444)
    r1, r2, r3 = asyncio.run(main())
    logging.getLogger().info("r1: %s, r2: %s, r3: %s", r1, r2, r3)
