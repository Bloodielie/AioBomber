import sys
from asyncio import Task, sleep

from loguru import logger


async def pending_tasks(max_time_wait: int = 20, wait_between_check: int = 1) -> None:
    time = 0
    while True:
        if len(Task.all_tasks()) > 1:
            await sleep(wait_between_check)
            time += wait_between_check
        elif time >= max_time_wait or len(Task.all_tasks()) == 1:
            break


def configuration_logger(error_handler: bool = False, is_debug: bool = False) -> None:
    logger.remove()
    if is_debug:
        level = 'DEBUG'
    else:
        level = 'INFO'
    logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{level}</level> | {message}",
               level=level)
    if error_handler:
        logger.add('error.log', format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
                   level="ERROR")
