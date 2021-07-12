import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from things.tests.factories import UserFactory

from pytest_factoryboy import register

register(UserFactory)


@pytest.fixture
def create_user(db):
    return UserFactory(password="12345")


@pytest.fixture
def access_token(db, create_user):
    user = create_user(username="user1", password='12345')
    data = {
        'username': user.username,
        'password': '12345'
    }
    url = reverse('token_obtain_pair')
    response = api_client.post(url, data, format='json')
    
    return response.data['access']

@pytest.fixture
def api_client_with_credentials(db, create_user):
    api_client = APIClient()
    api_client.force_authenticate(user=create_user)
    return api_client


@pytest.fixture
def api_client(db):
    api_client = APIClient()
    return api_client

