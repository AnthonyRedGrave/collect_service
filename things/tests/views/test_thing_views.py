import pytest
from django.urls import reverse
from things.tests.factories import ThingFactory
from things.tests.factories import ThingFactory
from rest_framework.test import APIRequestFactory, force_authenticate
from things.views import ThingViewSet
from freezegun import freeze_time
from django.core.exceptions import ValidationError


@pytest.mark.django_db(True)
class TestThingViewSet:

    def test_get_queryset__success(self, api_client_with_credentials):
        ThingFactory.create_batch(100)
        url = reverse('thing-list')
        response = api_client_with_credentials.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 100

    def test_post_new_thing__success(self):
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

    @pytest.mark.parametrize("method, action, url, params", [("delete", "destroy", "thing-detail",{'pk': 1}), 
                                                             ("put", "update", "thing-detail", {'pk': 1})])
    def test_not_allow_request_methods(self, method, action, url, params):
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

    def test_detail__success(self, api_client_with_credentials):
        thing = ThingFactory(tags=4, comments=5)
        url = reverse('thing-detail', kwargs={'pk': thing.id})
        response = api_client_with_credentials.get(url)
        assert response.status_code == 200


class TestThingViewSetActionComment:

    def test_action_get_list_of_comments__success(self, api_client_with_credentials):
        thing = ThingFactory.create(comments = 5)
        url = reverse('thing-comment', kwargs={'pk': thing.id})
        response = api_client_with_credentials.get(url)
        assert len(response.json()) == 5
        assert response.status_code == 200

    def test_action_post_comment__success(self, api_client_with_credentials):
        thing = ThingFactory.create(comments=1)
        data = {
            'content': "Новый комментарий для вещи",
        }
        url = reverse('thing-comment', kwargs={'pk': thing.id})
        response = api_client_with_credentials.post(url, data = data)
        assert response.status_code == 200
        assert response.json() == {'Comment': 'Created!'}

    def test_action_post_comment_unauthorized__error(self, api_client):
        thing = ThingFactory.create(comments=1)
        data = {
            'content': "Новый комментарий для вещи, но я не авторизовался",
        }
        url = reverse('thing-comment', kwargs={'pk': thing.id})
        response = api_client.post(url, data = data)
        assert response.status_code == 401

    def test_action_post_comment_to_not_found_thing__error(self, api_client_with_credentials):
        data = {
            'content': "Сообщение для несуществующей вещи",
        }
        url = reverse('thing-comment', kwargs={'pk': 100})
        response = api_client_with_credentials.post(url, data = data)
        assert response.status_code == 404

    def test_post_wrong_comment__error(self, api_client_with_credentials):
        thing = ThingFactory.create(comments=1)
        data = {
            'content': "",
        }
        url = reverse('thing-comment', kwargs={'pk': thing.id})
        response = api_client_with_credentials.post(url, data = data)
        assert response.status_code == 400


class TestThingViewSetActionMost:

    def test_get_list_of_10_things_with_tags__success(self, api_client_with_credentials):
        ThingFactory.create_batch(20, tags = "random")
        url = reverse('thing-most')
        response = api_client_with_credentials.get(url)
        assert len(response.json()) == 10
        assert response.status_code == 200
