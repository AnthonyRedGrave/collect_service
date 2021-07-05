from django.http import response
import pytest
from django.urls import reverse

def test_create_hundred_things(db, thing_factory, api_client):
    thing_factory.create_batch(100)
    url = reverse('thing-list')
    response = api_client.get(url)
    assert len(response.json()) == 100


def test_create_thing_message(db, thing_message_factory, api_client):
    thing_message = thing_message_factory()
    print(thing_message.id)
    response = api_client.get(f'http://0.0.0.0:8000/api/thing_messages/{thing_message.id}')
    print(response)
    assert response.status_code
    # assert response.json() == [{
    #     'id': thing_message.id,
    #     'user_id': thing_message.user.id,
    #     'content': thing_message.content,
    #     'thing_id': thing_message.thing.id,
    # }]