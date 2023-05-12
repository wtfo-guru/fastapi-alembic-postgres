import asyncio
import math

import pytest


async def my_coroutine() -> float:
    await asyncio.sleep(0.1)
    return math.e


@pytest.mark.asyncio
async def test_my_coroutine() -> None:
    assert 2 < await my_coroutine() < 3
