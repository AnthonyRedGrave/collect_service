import pytest
from django.urls import reverse
from things.tests.factories import ThingFactory, ThingMessageFactory
from rest_framework.test import APIRequestFactory, force_authenticate
from things.views import ThingViewSet


pytestmark = pytest.mark.django_db

def test_ThingViewSet_get_queryset__success(api_client_with_credentials):
    ThingFactory.create_batch(100)
    url = reverse('thing-list')
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 100


def test_ThingViewSet_post_new_thing__success():
    thing = ThingFactory()
    data = {
        'title': thing.title,
        'content': thing.content,
        'state': thing.state,
        'section': thing.section.id,
        'owner': thing.owner
    }
    url = reverse("thing-list")
    view = ThingViewSet.as_view({"post": "create"})
    factory = APIRequestFactory()
    request = factory.post(url, data = data)
    
    force_authenticate(request, user=thing.owner)
    response = view(request)
    response.render()
    assert response
    assert response.status_code == 201



@pytest.mark.parametrize("method, action, url, params", [("delete", "destroy", "thing-detail", {'pk': 1}),
                                                         ("put", "update", "thing-detail", {'pk': 1})])
def test_ThingViewSet__not_allow_request_method(method, action, url, params):
    thing = ThingFactory()
    data = {
        'title': thing.title,
        'content': thing.content,
        'state': thing.state,
        'section': thing.section,
        'image': thing.image.url,
        'owner': thing.owner
    }
    url = reverse(url, kwargs=params)

    factory = APIRequestFactory()
    
    view = ThingViewSet.as_view({method: action})
    request = factory.get(url)
    force_authenticate(request, user=thing.owner)
    response = view(request, data=data)
    print(response, action)
    assert response.status_code == 405


def test_detail_ThingViewSet__success(api_client_with_credentials):
    thing = ThingFactory()
    url = reverse('thing-detail', kwargs={'pk': thing.id})
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200


# ========================test action====================

def test_action_ThingViewSet_get_list_of_messages__success(api_client_with_credentials):
    thing = ThingFactory()
    ThingMessageFactory.create_batch(5, thing = thing)
    url = reverse('thing-message', kwargs={'pk': thing.id})
    response = api_client_with_credentials.get(url)
    assert len(response.json()) == 5
    assert response.status_code == 200




def test_action_ThingViewSet_post_message__success(api_client_with_credentials):
    thing_message = ThingMessageFactory()
    data = {
        'content': thing_message.content,
    }
    url = reverse('thing-message', kwargs={'pk': thing_message.thing.id})
    response = api_client_with_credentials.post(url, data = data)
    assert response.status_code == 200



def test_action_ThingViewSet_post_message_unauthorized__error(api_client):
    thing_message = ThingMessageFactory()
    data = {
        'content': thing_message.content,
    }
    url = reverse('thing-message', kwargs={'pk': thing_message.thing.id})
    response = api_client.post(url, data = data)
    assert response.status_code == 401


def test_action_ThingViewSet_post_message_to_not_found_thing__error(api_client_with_credentials):
    data = {
        'content': "Сообщение для несуществующей вещи",
    }
    url = reverse('thing-message', kwargs={'pk': 100})
    response = api_client_with_credentials.post(url, data = data)
    assert response.status_code == 404


def test_action_ThingViewSet_post_wrong_message__error(api_client_with_credentials):
    thing_message = ThingMessageFactory()
    data = {
        'content': "",
    }
    url = reverse('thing-message', kwargs={'pk': thing_message.thing.id})
    response = api_client_with_credentials.post(url, data = data)
    assert response.status_code == 400
