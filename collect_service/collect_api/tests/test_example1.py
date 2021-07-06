import pytest
from django.urls import reverse




# def test_create_thing_message(db, thing_message_factory, api_client):
#     thing_message = thing_message_factory()
#     data = {
#         'user': thing_message.user.id,
#         'content': thing_message.content,
#         'thing': thing_message.thing.id
#     }
#     url = reverse('thingmessage-list')
#     response = api_client.post(url, data=data)
#     assert response.status_code == 201


# def test_get_detail_thing(db, thing_factory, api_client):
#     thing = thing_factory()
#     url = reverse('thing-detail', kwargs={'pk':thing.id})
#     response = api_client.get(url)
#     assert response.status_code == 200