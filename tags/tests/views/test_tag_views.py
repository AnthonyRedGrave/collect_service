from django.urls.base import reverse
import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from things.tests.factories import UserFactory
from tags.tests.factories import TagFactory
from tags.views import TagViewSet

pytestmark = pytest.mark.django_db

def test_TagViewSet_get_queryset__success(api_client_with_credentials):
    TagFactory.create_batch(20)
    url = reverse('tag-list')
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 20


@pytest.mark.parametrize("method, action, url, params", [("post", "create", "tag-list", None),
                                                         ("delete", "destroy", "tag-detail", {'pk': 1}),
                                                         ("put", "update", "tag-detail", {'pk': 1})])
def test_TagViewSet__not_allow_request_method(method, action, url, params):
    tag = TagFactory()
    user = UserFactory()
    data = {
        'title': tag.title,
    }

    url = reverse(url, kwargs=params)
    factory = APIRequestFactory()
    view = TagViewSet.as_view({method: action})
    request = factory.get(url)
    force_authenticate(request, user=user)
    response = view(request, data=data)
    assert response.status_code == 405


def test_detail_TagViewSet__success(api_client_with_credentials):
    section = TagFactory()
    url = reverse('tag-detail', kwargs={'pk': section.id})
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200