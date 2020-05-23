import pytest

from aio_bomber.models import ServiceModel
from aio_bomber.preparer import InformationPreparer


@pytest.fixture()
def preparer():
    yield InformationPreparer()


@pytest.fixture()
def service_model(outgoing_date):
    yield ServiceModel(**outgoing_date)


@pytest.fixture()
def incoming_date():
    return {
        'name': 'test',
        'url': 'https://test',
        'method': 'POST',
        'header': {},
        'static_data': {},
        'dynamic_data': {
            'formatted_phone': 'phone'
        }}


@pytest.fixture()
def outgoing_date():
    return {
        'name': 'test',
        'url': 'https://test',
        'method': 'POST',
        'header': {},
        'static_data': {},
        'dynamic_data': {
            'phone': 'test'
        }}


@pytest.fixture()
def outgoing_date_2():
    return {
        'url': 'https://test',
        'data': {'phone': 'test'},
        'header': {}}


def test_service_model_and_cache(service_model, incoming_date, preparer, outgoing_date_2):
    assert preparer.get_service_model(incoming_date, phone='test') == service_model
    assert preparer.cache['https://test'][0] == service_model
    assert preparer.cache['https://test'][1] == outgoing_date_2
    assert len(preparer) == 1


def test_generation_args(service_model, outgoing_date_2):
    assert service_model.generator_args() == outgoing_date_2
