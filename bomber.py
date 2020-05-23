from argparse import ArgumentParser
from asyncio import get_event_loop, AbstractEventLoop

from loguru import logger

from aio_bomber import configuration_logger, AioBomber


async def main(loop: AbstractEventLoop) -> None:
    parser = ArgumentParser()
    parser.add_argument('--phone', action="store", required=True, type=str, help="Phone for SMS Bomber")
    parser.add_argument('--cycles', action="store", default=1, type=int, help="Number of cycles")
    parser.add_argument('--debug', action="store", default=False, type=bool, help="Debug mode")
    args = parser.parse_args()
    configuration_logger(is_debug=args.debug)

    logger.info('Start AioBomber')
    bomber = AioBomber(loop=loop)
    await bomber.attack(args.cycles, args.phone)

    logger.info('Exit')
    loop.stop()


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(main(loop))
    loop.run_forever()
else:
    raise Exception()
