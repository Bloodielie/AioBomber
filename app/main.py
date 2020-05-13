from fastapi import FastAPI
from app.aio_bomber import configuration_logger, AioBomber
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='AioBomber', redoc_url=None)
configuration_logger()
bomber = AioBomber()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)


@app.get("/start")
def read_root(phone: int, cycles: int = 1):
    logger.info(f'{phone}')
    print(phone)
    print(cycles)
    return {"Hello": "World"}


@app.on_event("shutdown")
async def shutdown():
    await bomber.close_session()
