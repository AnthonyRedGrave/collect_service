from django.urls.base import reverse
import pytest

from collect_api.tests.factories import SectionFactory
from pytest_factoryboy import register

register(SectionFactory)


def test_SectionViewSet_get_queryset__success(db, section_factory, api_client_with_credentials):
    section_factory.create_batch(20)
    url = reverse('section-list')
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 20


def test_post_SectionViewSet__error(db, section_factory, api_client_with_credentials):
    section = section_factory()
    data = {
        'title': section.title,
    }
    url = reverse('section-list')
    response = api_client_with_credentials.post(url, data=data)
    assert response.status_code == 405


def test_delete_SectionViewSet__error(db, section_factory, api_client_with_credentials):
    section = section_factory()
    url = reverse('section-detail', kwargs={'pk': section.id})
    response = api_client_with_credentials.delete(url)
    assert response.status_code == 405


def test_update_SectionViewSet__error(db, section_factory, api_client_with_credentials):
    section = section_factory()
    url = reverse('section-detail', kwargs={'pk': section.id})
    response = api_client_with_credentials.put(url)
    assert response.status_code == 405


def test_detail_SectionViewSet__success(db, section_factory, api_client_with_credentials):
    section = section_factory()
    url = reverse('section-detail', kwargs={'pk': section.id})
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200