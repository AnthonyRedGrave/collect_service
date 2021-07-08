import pytest
from django.urls import reverse
from collect_api.tests.factories import ThingFactory
from rest_framework.test import APIRequestFactory, force_authenticate
from collect_api.views import ThingViewSet
from pytest_factoryboy import register

register(ThingFactory) 

pytestmark = pytest.mark.django_db

def test_ThingViewSet_get_queryset__success(thing_factory, api_client_with_credentials):
    thing_factory.create_batch(100)
    url = reverse('thing-list')
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 100


@pytest.mark.parametrize("method, action, url, params", [("post", "create", "thing-list", None),
                                                         ("delete", "destroy", "thing-detail", {'pk': 1}),
                                                         ("put", "update", "thing-detail", {'pk': 1})])
def test_ThingViewSet__error(thing_factory, method, action, url, params):
    thing = thing_factory()
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


def test_detail_ThingViewSet__success(thing_factory, api_client_with_credentials):
    thing = thing_factory()
    url = reverse('thing-detail', kwargs={'pk': thing.id})
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200