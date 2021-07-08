import pytest
from django.urls import reverse
from collect_api.tests.factories import ThingFactory, ThingMessageFactory
from rest_framework.test import APIRequestFactory, force_authenticate
from collect_api.views import ThingViewSet


pytestmark = pytest.mark.django_db

def test_ThingViewSet_get_queryset__success(api_client_with_credentials):
    ThingFactory.create_batch(100)
    url = reverse('thing-list')
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 100


@pytest.mark.parametrize("method, action, url, params", [("post", "create", "thing-list", None),
                                                         ("delete", "destroy", "thing-detail", {'pk': 1}),
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
    assert response.status_code == 405


def test_detail_ThingViewSet__success(api_client_with_credentials):
    thing = ThingFactory()
    url = reverse('thing-detail', kwargs={'pk': thing.id})
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200


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