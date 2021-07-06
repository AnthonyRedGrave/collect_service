import pytest
from rest_framework.test import APIClient

from collect_api.tests.factories import UserFactory

from pytest_factoryboy import register
register(UserFactory)

@pytest.fixture
def create_user(db):
    return UserFactory()

@pytest.fixture
def api_client(db, create_user):
    api_client = APIClient()
    api_client.force_authenticate(user=create_user)
    return api_client


