import pytest
from aio_bomber.generators import DynamicDataGenerator
from aio_bomber.constants import LIST_OF_LASTTNAME, LIST_OF_FIRSTNAME


generator = DynamicDataGenerator()


@pytest.fixture()
def generator():
    yield DynamicDataGenerator()


def test_email_generation(generator):
    email = generator._email()
    assert isinstance(email, str)
    assert email[11:] == 'gmail.com'

    assert len(email) == 20
    assert len(generator._email(len_email=15)) == 15
    assert generator._email(mail_url='mail.ru')[13:] == 'mail.ru'


def test_lastname(generator):
    assert generator._lastname() in LIST_OF_LASTTNAME


def test_firstname(generator):
    assert generator._firstname() in LIST_OF_FIRSTNAME
