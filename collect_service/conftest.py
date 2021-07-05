import pytest

from pytest_factoryboy import register
from collect_api.tests.factories import ThingFactory, UserFactory, SectionFactory, ThingMessageFactory
from rest_framework.test import APIClient


@pytest.fixture
def create_user(db):
    return UserFactory()

@pytest.fixture
def api_client(db, create_user):
    api_client = APIClient()
    api_client.force_authenticate(user = create_user)
    yield api_client
    api_client.force_authenticate(user = None)


register(ThingMessageFactory)
register(ThingFactory) 
register(UserFactory)
register(SectionFactory)