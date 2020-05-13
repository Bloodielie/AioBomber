from asyncio import run
from app.aio_bomber import configuration_logger, AioBomber
from loguru import logger
from argparse import ArgumentParser


async def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('--phone', action="store", required=True, type=str, help="Phone for SMS Bomber")
    parser.add_argument('--cycles', action="store", default=1, type=int, help="Number of cycles")
    args = parser.parse_args()
    configuration_logger()
    logger.info('Start AioBomber!')
    bomber = AioBomber()
    await bomber.attack(args.cycles, args.phone)
    await bomber.close_session()
    logger.info('Exit!')

if __name__ == "__main__":
    run(main())
else:
    raise Exception()
