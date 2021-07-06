import pytest
from django.urls import reverse
from collect_api.tests.factories import ThingMessageFactory, UserFactory
from rest_framework.test import APIClient
from pytest_factoryboy import register

register(ThingMessageFactory)
register(UserFactory)


# @pytest.mark.parametrize("username, password", [("user1", "password1"), ("user2", "password2")])
# def test_ThingMessageViewSet__user_have_messages(db, thing_message_factory, api_client, username, password):
#     user = UserFactory(username=username, password=password)
#     api_client.force_authenticate(user = user)
#     thing_message_factory.create_batch(20, user=user)
#     url = reverse('thingmessage-list')
#     response = api_client.get(url)
#     assert response.status_code == 200


# @pytest.mark.parametrize("username, password", [("user1", "password1"), ("user2", "password2")])
# def test_ThingMessageViewSet__user_dont_have_messages(db, thing_message_factory, api_client, username, password):
#     user = UserFactory(username=username, password=password)
#     api_client.force_authenticate(user = user)
#     thing_message_factory.create_batch(20)
#     url = reverse('thingmessage-list')
#     response = api_client.get(url)
#     # не важно какой юзер, если у него нету сообщений, код 200 и длина массива записей 0
#     assert response.status_code == 200
#     assert len(response.json()) == 0


# def test_post_ThingMessageViewSet__error(db, thing_message_factory, api_client):
#     thing_message = thing_message_factory()
#     data = {
#         'user': thing_message.user.id,
#         'content': thing_message.content,
#         'thing': thing_message.thing.id
#     }
#     url = reverse('thingmessage-list')
#     response = api_client.post(url, data=data)
#     assert response.status_code == 405


# def test_delete_ThingMessageViewSet__error(db, thing_message_factory, api_client):
#     thing_message = thing_message_factory()
#     url = reverse('thingmessage-detail', kwargs={'pk': thing_message.id})
#     response = api_client.delete(url)
#     assert response.status_code == 405


# def test_update_ThingMessageViewSet__error(db, thing_message_factory, api_client):
#     thing_message = thing_message_factory()
#     url = reverse('thingmessage-detail', kwargs={'pk': thing_message.id})
#     response = api_client.put(url)
#     assert response.status_code == 405

# # оказывается, что и для просмотра одной записи нужно, чтобы у залогинившегося юзера был thing_message
# def test_detail_ThingMessageViewSet__success(db, thing_message_factory, api_client, create_user):
#     user = create_user
#     api_client.force_authenticate(user = user)
#     thing_message = thing_message_factory(user=user)
#     print(thing_message.__dict__)
#     url = reverse('thingmessage-detail', kwargs={'pk': thing_message.id})
#     response = api_client.get(url)
#     print(response)
#     assert response.status_code == 200