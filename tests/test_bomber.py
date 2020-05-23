import asyncio

import pytest

from aio_bomber.bomber import AioBomber

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def bomber():
    bomber = AioBomber()
    yield bomber
    await bomber.sender.close_session()


def test_event_loop_getter(bomber):
    assert isinstance(bomber._get_loop(), asyncio.AbstractEventLoop)
