import pytest
from django.urls.base import reverse
from django.contrib.auth.models import User
from collect_api.tests.factories import UserFactory


@pytest.mark.parametrize("username, email, password", [("user1", "us@inbox.ru", "password1"), ("user2", "us2@inbox.ru", "password2")])
def test_jwt_get_access_token(db, create_user, api_client, username, email, password):
    user = User.objects.create_user(username, email, password)
    data = {
        'username': user.username,
        'password': password
    }
    url = reverse('token_obtain_pair')
    response = api_client.post(url, data, format='json')
    
    assert response.status_code == 200
    assert response.data['access']
