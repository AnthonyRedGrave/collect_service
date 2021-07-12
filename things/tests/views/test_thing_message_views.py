from things.models import Thing
from _pytest.mark import param
from django.http import request
from django.urls.base import resolve
import pytest
from django.urls import reverse, resolve
from things.tests.factories import ThingMessageFactory, UserFactory
from rest_framework.test import APIRequestFactory, force_authenticate
from things.views import ThingMessageViewSet


pytestmark = pytest.mark.django_db

def test_ThingMessageViewSet__user_have_messages(api_client_with_credentials):
    user = UserFactory()
    api_client_with_credentials.force_authenticate(user = user)
    ThingMessageFactory.create_batch(20, user=user)
    url = reverse('thingmessage-list')
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200


def test_ThingMessageViewSet__user_dont_have_messages(api_client_with_credentials):
    user = UserFactory()
    api_client_with_credentials.force_authenticate(user = user)
    ThingMessageFactory.create_batch(20)
    url = reverse('thingmessage-list')
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize("method, action, url, params", [("post", "create", "thingmessage-list", None),
                                                         ("delete", "destroy", "thingmessage-detail", {'pk': 1}),
                                                         ("put", "update", "thingmessage-detail", {'pk': 1})])
def test_ThingMessageViewSet__not_allow_request_method(method, action, url, params):
    thing_message = ThingMessageFactory()
    
    data = {
        'user': thing_message.user.id,
        'content': thing_message.content,
        'thing': thing_message.thing.id
    }
    url = reverse(url, kwargs=params)

    factory = APIRequestFactory()
    
    view = ThingMessageViewSet.as_view({method: action})
    request = factory.get(url)
    force_authenticate(request, user=thing_message.user)
    response = view(request, data=data)
    assert response.status_code == 405


def test_detail_ThingMessageViewSet__success(api_client_with_credentials, create_user):
    user = create_user
    api_client_with_credentials.force_authenticate(user = user)
    thing_message = ThingMessageFactory(user=user)
    url = reverse('thingmessage-detail', kwargs={'pk': thing_message.id})
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
