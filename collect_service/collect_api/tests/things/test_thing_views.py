import pytest
from django.urls import reverse
from collect_api.tests.factories import ThingFactory

from pytest_factoryboy import register

register(ThingFactory) 


def test_ThingViewSet_get_queryset__success(db, thing_factory, api_client_with_credentials):
    thing_factory.create_batch(100)
    url = reverse('thing-list')
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 100


def test_post_ThingViewSet__error(db, thing_factory, api_client_with_credentials):
    thing = thing_factory()
    data = {
        'title': thing.title,
        'content': thing.content,
        'state': thing.state,
        'section': thing.section,
        'image': thing.image.url,
        'owner': thing.owner
    }
    url = reverse('thing-list')
    response = api_client_with_credentials.post(url, data=data)
    assert response.status_code == 405


def test_delete_ThingViewSet__error(db, thing_factory, api_client_with_credentials):
    thing = thing_factory()
    url = reverse('thing-detail', kwargs={'pk': thing.id})
    response = api_client_with_credentials.delete(url)
    assert response.status_code == 405


def test_update_ThingViewSet__error(db, thing_factory, api_client_with_credentials):
    thing = thing_factory()
    url = reverse('thing-detail', kwargs={'pk': thing.id})
    response = api_client_with_credentials.put(url)
    assert response.status_code == 405


def test_detail_ThingViewSet__success(db, thing_factory, api_client_with_credentials):
    thing = thing_factory()
    url = reverse('thing-detail', kwargs={'pk': thing.id})
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200