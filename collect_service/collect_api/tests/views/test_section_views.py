from django.urls.base import reverse
import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from collect_api.tests.factories import SectionFactory, UserFactory
from pytest_factoryboy import register
from collect_api.views import SectionViewSet

register(SectionFactory)
register(UserFactory)

pytestmark = pytest.mark.django_db

def test_SectionViewSet_get_queryset__success(section_factory, api_client_with_credentials):
    section_factory.create_batch(20)
    url = reverse('section-list')
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 20

@pytest.mark.parametrize("method, action, url, params", [("post", "create", "section-list", None),
                                                         ("delete", "destroy", "section-detail", {'pk': 1}),
                                                         ("put", "update", "section-detail", {'pk': 1})])
def test_SectionViewSet__error(section_factory, method, action, url, params):
    section = section_factory()
    user = UserFactory()
    data = {
        'title': section.title,
    }

    url = reverse(url, kwargs=params)
    factory = APIRequestFactory()
    view = SectionViewSet.as_view({method: action})
    request = factory.get(url)
    force_authenticate(request, user=user)
    response = view(request, data=data)
    assert response.status_code == 405


def test_detail_SectionViewSet__success(db, section_factory, api_client_with_credentials):
    section = section_factory()
    url = reverse('section-detail', kwargs={'pk': section.id})
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200