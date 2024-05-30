from utils.log import get_path
import asyncio


async def async_msg():
    await asyncio.sleep(1)
    print('asyncio hello')


def get_utils_log():
    get_path()
