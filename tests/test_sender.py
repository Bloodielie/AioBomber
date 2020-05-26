import pytest

from aio_bomber.sender import Sender

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def sender():
    sender = Sender()
    yield sender
    await sender.close_session()


async def test_get_services(sender):
    # Exception
    await sender.get_services(path='./test')

    services = await sender.get_services(path='./services1.json')
    assert isinstance(services, list)
    assert isinstance(services[0], dict)
    await sender.post('https://github.com/', data={'test': True})
