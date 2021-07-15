import pytest
from django.urls import reverse
from things.tests.factories import ThingFactory, UserFactory
from things.tests.factories import ThingFactory
from rest_framework.test import APIRequestFactory, force_authenticate
from things.views import ThingViewSet
from rest_framework.test import APITestCase


@pytest.mark.django_db(True)
class TestThingViewSet(APITestCase):
    
    test_not_allow_request_methods_params = [("delete", "destroy", "thing-detail",{'pk': 1}), 
                                             ("put", "update", "thing-detail", {'pk': 1})]

    def test_ThingViewSet_get_queryset__success(self):
        ThingFactory.create_batch(100)
        user = UserFactory()
        url = reverse('thing-list')
        self.client.force_login(user=user)
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 100

    def test_ThingViewSet_post_new_thing__success(self):
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

    def test_not_allow_request_methods(self):
        for method, action, url, params in self.test_not_allow_request_methods_params:
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

    def test_detail_ThingViewSet__success(self):
        thing = ThingFactory(tags=4, comments=5)
        url = reverse('thing-detail', kwargs={'pk': thing.id})
        self.client.force_login(user=thing.owner)
        response = self.client.get(url)
        assert response.status_code == 200


class TestThingViewSetActionComment(APITestCase):

    def test_action_ThingViewSet_get_list_of_comments__success(self):
        thing = ThingFactory.create(comments = 5)
        url = reverse('thing-comment', kwargs={'pk': thing.id})
        self.client.force_login(user=thing.owner)
        response = self.client.get(url)
        assert len(response.json()) == 5
        assert response.status_code == 200

    def test_action_ThingViewSet_post_comment__success(self):
        thing = ThingFactory.create(comments=1)
        data = {
            'content': "Новый комментарий для вещи",
        }
        url = reverse('thing-comment', kwargs={'pk': thing.id})
        self.client.force_login(user=thing.owner)
        response = self.client.post(url, data = data)
        assert response.status_code == 200
        assert response.json() == {'Comment': 'Created!'}

    def test_action_ThingViewSet_post_comment_unauthorized__error(self):
        thing = ThingFactory.create(comments=1)
        data = {
            'content': "Новый комментарий для вещи, но я не авторизовался",
        }
        url = reverse('thing-comment', kwargs={'pk': thing.id})
        response = self.client.post(url, data = data)
        assert response.status_code == 401

    def test_action_ThingViewSet_post_comment_to_not_found_thing__error(self):
        user = UserFactory()
        data = {
            'content': "Сообщение для несуществующей вещи",
        }
        url = reverse('thing-comment', kwargs={'pk': 100})
        self.client.force_login(user=user)
        response = self.client.post(url, data = data)
        assert response.status_code == 404

    def test_action_ThingViewSet_post_wrong_comment__error(self):
        thing = ThingFactory.create(comments=1)
        data = {
            'content': "",
        }
        url = reverse('thing-comment', kwargs={'pk': thing.id})
        self.client.force_login(user=thing.owner)
        response = self.client.post(url, data = data)
        assert response.status_code == 400


class TestThingViewSetActionMost(APITestCase):

    def test_action_most_ThingViewSet_get_list_of_10_things_with_tags__success(self):
        ThingFactory.create_batch(20, tags = "random")
        user = UserFactory()
        url = reverse('thing-most')
        self.client.force_login(user=user)
        response = self.client.get(url)
        assert len(response.json()) == 10
        assert response.status_code == 200