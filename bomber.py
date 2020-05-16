from asyncio import get_event_loop, AbstractEventLoop
from aio_bomber import configuration_logger, AioBomber
from loguru import logger
from argparse import ArgumentParser
from aio_bomber.utils import pending_tasks


async def main(loop: AbstractEventLoop) -> None:
    parser = ArgumentParser()
    parser.add_argument('--phone', action="store", required=True, type=str, help="Phone for SMS Bomber")
    parser.add_argument('--cycles', action="store", default=1, type=int, help="Number of cycles")
    args = parser.parse_args()
    configuration_logger()

    logger.info('Start AioBomber')
    bomber = AioBomber(loop=loop)
    await bomber.attack(args.cycles, args.phone)
    await pending_tasks()

    logger.info('Exit')
    await bomber.close_session()
    loop.stop()


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(main(loop))
    loop.run_forever()
else:
    raise Exception()
