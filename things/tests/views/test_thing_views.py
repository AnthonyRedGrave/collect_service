import pytest
from django.urls import reverse
from rest_framework import response
from things.models import Deal, Thing
from things.tests.factories import ThingFactory, DealFactory, UserFactory
from rest_framework.test import APIRequestFactory, force_authenticate
from things.views import ThingViewSet

import json

from django.core.files.uploadedfile import SimpleUploadedFile



@pytest.mark.django_db(True)
class TestThingViewSet:
    def test_get_queryset__success(self, api_client_with_credentials):
        ThingFactory.create_batch(100)
        url = reverse("thing-list")
        response = api_client_with_credentials.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 100

    def test_post_new_thing__success(self):
        thing = ThingFactory()
        image_path = "media/tests/images/test_image.jpeg"
        image = SimpleUploadedFile(name='test_image.jpeg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        data = {
            "title": "Новая вещь",
            "content": "Новый контент",
            "state": "Awesome",
            "section": thing.section.id,
            "owner": thing.owner,
            "image": image
        }
        url = reverse("thing-list")
        view = ThingViewSet.as_view({"post": "create"})
        factory = APIRequestFactory()
        request = factory.post(url, data=data)

        force_authenticate(request, user=thing.owner)
        response = view(request)
        response.render()
        thing = Thing.objects.last()
        assert response
        assert thing.image
        assert response.status_code == 201

    @pytest.mark.parametrize(
        "method, action, url, params",
        [
            ("delete", "destroy", "thing-detail", {"pk": 1}),
            ("put", "update", "thing-detail", {"pk": 1}),
        ],
    )
    def test_not_allow_request_methods(self, method, action, url, params):
        thing = ThingFactory()
        data = {
            "title": thing.title,
            "content": thing.content,
            "state": thing.state,
            "section": thing.section,
            "image": thing.image.url,
            "owner": thing.owner,
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
        url = reverse("thing-detail", kwargs={"pk": thing.id})
        response = api_client_with_credentials.get(url)
        assert response.status_code == 200


class TestThingViewSetActionComment:
    def test_action_get_list_of_comments__success(self, api_client_with_credentials):
        thing = ThingFactory.create(comments=5)
        url = reverse("thing-comment", kwargs={"pk": thing.id})
        response = api_client_with_credentials.get(url)
        assert len(response.json()) == 5
        assert response.status_code == 200

    def test_action_post_comment__success(self, api_client_with_credentials):
        thing = ThingFactory.create(comments=1)
        data = {
            "content": "Новый комментарий для вещи",
        }
        url = reverse("thing-comment", kwargs={"pk": thing.id})
        response = api_client_with_credentials.post(url, data=data)
        assert response.status_code == 200
        assert response.json() == {"Comment": "Created!"}

    def test_action_post_comment_unauthorized__error(self, api_client):
        thing = ThingFactory.create(comments=1)
        data = {
            "content": "Новый комментарий для вещи, но я не авторизовался",
        }
        url = reverse("thing-comment", kwargs={"pk": thing.id})
        response = api_client.post(url, data=data)
        assert response.status_code == 401

    def test_action_post_comment_to_not_found_thing__error(
        self, api_client_with_credentials
    ):
        data = {
            "content": "Сообщение для несуществующей вещи",
        }
        url = reverse("thing-comment", kwargs={"pk": 100})
        response = api_client_with_credentials.post(url, data=data)
        assert response.status_code == 404

    def test_post_wrong_comment__error(self, api_client_with_credentials):
        thing = ThingFactory.create(comments=1)
        data = {
            "content": "",
        }
        url = reverse("thing-comment", kwargs={"pk": thing.id})
        response = api_client_with_credentials.post(url, data=data)
        assert response.status_code == 400


class TestThingViewSetActionMost:
    def test_get_list_of_10_things_with_tags__success(
        self, api_client_with_credentials
    ):
        ThingFactory.create_batch(20, tags="random")
        url = reverse("thing-most")
        response = api_client_with_credentials.get(url)
        assert len(response.json()) == 10
        assert response.status_code == 200


class TestDeal:
    def test_get_deal_status_accepted__success(self, api_client):
        thing = ThingFactory()
        request_user = UserFactory()
        api_client.force_authenticate(user=request_user)
        url = reverse("deal-list")
        data = {
            'thing': thing.id,
            'cost': '100.00'
        }
        response = api_client.post(url, data=data)
        deal = Deal.objects.get(new_owner = request_user, thing=thing, old_owner = thing.owner, cost = 100.00)
        result = response.json()
        assert response.status_code == 201
        assert deal.thing.id == data['thing']
        assert result['cost'] == data['cost']
        assert deal.old_owner == thing.owner
        assert deal.new_owner == request_user
        assert deal.status == "accepted"


    def test_get_deal_status_log_confirmed__success(self, api_client):
        thing = ThingFactory()
        request_user = UserFactory()
        deal = DealFactory(
            thing=thing,
            old_owner=thing.owner,
            new_owner=request_user
        )
        data = {
            "status": "confirmed",
            "cost": '101.00'
        }
        api_client.force_authenticate(user=request_user)
        url = reverse("deal-detail", kwargs={'pk': deal.id})
        response = api_client.patch(url, data=data)
        result = response.json()
        assert response.status_code == 200
        assert result['status'] == data["status"]
        assert result['cost'] == data['cost']


    def test_get_deal_status_log_completed__success(self, api_client):
        thing = ThingFactory()
        request_user = UserFactory()
        deal = DealFactory(
            thing=thing, old_owner=thing.owner, new_owner=request_user
        )
        data = {
            "status": "completed",
            "cost": '110.00'
        }
        api_client.force_authenticate(user=request_user)
        url = reverse("deal-detail", kwargs={"pk": deal.id})
        response = api_client.patch(url, data=data)
        result = response.json()
        assert response.status_code == 200
        assert result['status'] == data["status"]
        assert result['cost'] == data['cost']


    def test_all_actions_buy__success(self, api_client):
        thing = ThingFactory()
        request_user = UserFactory()
        statuses = []

        api_client.force_authenticate(user=request_user)
        data = {
            'thing': thing.id,
            'cost': '100.00'
        }
        url = reverse('deal-list')
        
        response = api_client.post(url, data=data)
        deal = Deal.objects.get(new_owner = request_user, thing=thing, old_owner = thing.owner, cost = 100.00)
        statuses.append(deal.status)
        result = response.json()
        assert response.status_code == 201
        assert deal.thing.id == data['thing']
        assert result['cost'] == data['cost']
        assert deal.old_owner == thing.owner
        assert deal.new_owner == request_user
        assert deal.status == "accepted"

        data = {
            "status": "confirmed",
            "cost": '105.00'
        }
        url = reverse("deal-detail", kwargs={"pk": deal.id})
        response = api_client.patch(url, data=data)
        result = response.json()
        statuses.append(result['status'])
        assert response.status_code == 200
        assert result['status'] == data["status"]
        assert result['cost'] == data['cost']

        data = {
            "status": "completed",
            "cost": '103.00'
        }

        url = reverse("deal-detail", kwargs={"pk": deal.id})
        response = api_client.patch(url, data=data)
        result = response.json()
        statuses.append(result['status'])
        assert response.status_code == 200
        assert result['status'] == data["status"]
        assert result['cost'] == data['cost']
        assert statuses == ['accepted', 'confirmed', 'completed']


class TestRate:
    @pytest.mark.parametrize(
        "value, label", [("like", "1"), ("dislike", "-1")])
    def test_action_rate_get_thing_all_likes_and_dislikes__success(self, api_client_with_credentials, value, label):
        thing = ThingFactory(votes="random")
        url = reverse("thing-rate", kwargs={"pk": thing.id})
        data= {'value': value}
        response = api_client_with_credentials.generic(method="GET", path=url, data=json.dumps(data), content_type='application/json')
        result_votes_count = len(response.json())
        votes_count = thing.vote_set.filter(value=label).count()
        assert response.status_code == 200
        assert result_votes_count == votes_count

    @pytest.mark.parametrize(
        "value", [("like"), ("dislike")])
    def test_action_rate_post_like_to_thing__success(self, api_client_with_credentials, value):
        thing = ThingFactory()
        url = reverse("thing-rate", kwargs={"pk": thing.id})
        data = {'value': value}
        response = api_client_with_credentials.post(url, data=data)
        assert response
        assert response.status_code == 200
    

    @pytest.mark.parametrize(
        "value", [("like"), ("dislike")])
    def test_action_rate_post_like_to_thing__success(self, api_client_with_credentials, value):
        thing = ThingFactory()
        url = reverse("thing-rate", kwargs={"pk": thing.id})
        data = {'value': value}
        response = api_client_with_credentials.post(url, data=data)
        assert response
        assert response.status_code == 200
        

    @pytest.mark.parametrize(
        "value_first, value_second", [("like", "dislike"), ("dislike", "like")])
    def test_action_rate_post_swap_like_and_dislike__success(self, api_client_with_credentials, value_first, value_second):
        thing = ThingFactory()
        url = reverse("thing-rate", kwargs={"pk": thing.id})
        data = {'value': value_first}
        response = api_client_with_credentials.post(url, data=data)
        assert response.json()['value'] == value_first
        assert response.status_code == 200
        data = {'value': value_second}
        response = api_client_with_credentials.post(url, data=data)
        assert response.json()['value'] == value_second
        assert response.status_code == 200

    
    def test_action_rate_post__delete_like__success(self, api_client_with_credentials):
        thing = ThingFactory()
        url = reverse("thing-rate", kwargs={"pk": thing.id})
        data = {'value': "like"}
        response = api_client_with_credentials.post(url, data=data)
        assert response.json()['value'] == 'like'
        assert response.status_code == 200

        response = api_client_with_credentials.post(url, data=data)
        assert response.json()['value'] == None
        assert response.status_code == 200


class TestFilter:
    def test_filter_state__success(self, api_client_with_credentials):
        things = ThingFactory.create_batch(5)
        url = "http://0.0.0.0:8000/api/things/?state=Good"
        response = api_client_with_credentials.get(url)

        thing_before_after_filtering = [thing.state for thing in things]
        thing_states_after_filtering = [thing['state'] for thing in response.json()]

        assert thing_before_after_filtering != thing_states_after_filtering


    def test_filter_state__error(self, api_client_with_credentials):
        ThingFactory.create_batch(5)
        url = "http://0.0.0.0:8000/api/things/?state=WrongState"
        response = api_client_with_credentials.get(url)
        assert response.status_code == 400
        assert response.json()['state'][0] == "Select a valid choice. WrongState is not one of the available choices."

    @pytest.mark.freeze_time("2021-08-31")
    def test_filter_date_published_start__success(self, api_client_with_credentials):
        ThingFactory.create_batch(5)
        url = "http://0.0.0.0:8000/api/things/?date_start=2021-07-31"
        response = api_client_with_credentials.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 5
    

    @pytest.mark.freeze_time("2021-08-31")
    def test_filter_date_published_end__success(self, api_client_with_credentials):
        ThingFactory.create_batch(5)
        url = "http://0.0.0.0:8000/api/things/?date_end=2021-09-30"
        response = api_client_with_credentials.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 5


    def test_filter_date_published_start_with_invalid_date__error(self, api_client_with_credentials):
        ThingFactory.create_batch(5)
        url = "http://0.0.0.0:8000/api/things/?date_start=2021-07-wrong"
        response = api_client_with_credentials.get(url)
        assert response.json()['date_start'][0] == "Enter a valid date."
        assert response.status_code == 400
    

    def test_ordering_title__success(self, api_client_with_credentials):
        things = ThingFactory.create_batch(5)
        url = "http://0.0.0.0:8000/api/things/?order_by=title"
        response = api_client_with_credentials.get(url)

        thing_titles_before_ordering = [thing.title for thing in things]
        ordering_thing_titles = sorted(thing_titles_before_ordering)
        ordering_response = [thing['title'] for thing in response.json()]

        assert thing_titles_before_ordering != ordering_response
        assert ordering_thing_titles == ordering_response

    def test_ordering_title__error(self, api_client_with_credentials):
        ThingFactory.create_batch(5)
        url = "http://0.0.0.0:8000/api/things/?order_by=titl"
        response = api_client_with_credentials.get(url)
        assert response.status_code == 400
        assert response.json()['order_by'][0] == "Select a valid choice. titl is not one of the available choices."


    def test_filter_tags__success(self, api_client_with_credentials):
        ThingFactory.create_batch(5, tags=3)
        url = "http://0.0.0.0:8000/api/things/?tags=1&tags=2&tags=3"
        response = api_client_with_credentials.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 1


class TestMessage:
    def test_get_thing_messages__success(self, api_client_with_credentials):
        thing = ThingFactory(messages = 5)
        url = reverse("thing-message", kwargs={"pk": thing.id})
        response = api_client_with_credentials.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 5

    
    def test_post_thing_message__success(self, api_client_with_credentials):
        thing = ThingFactory()
        url = reverse("thing-message", kwargs={"pk": thing.id})
        data = {
            "content": "Новое сообщения"
        }
        response = api_client_with_credentials.post(url, data=data)
        assert response.status_code == 200
        assert response.json() == {"Message": "Created!"}