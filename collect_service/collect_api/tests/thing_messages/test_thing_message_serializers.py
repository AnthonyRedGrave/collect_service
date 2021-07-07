import pytest

from collect_api.tests.factories import ThingMessageFactory, UserFactory, ThingFactory
from pytest_factoryboy import register
from collect_api.serializers import ThingMessageSerializer

register(ThingMessageFactory)
register(UserFactory)
register(ThingFactory)


@pytest.mark.parametrize("content, user", [("Текст первого сообщения", {'username': 'user1', 'password': 'password1'}),
                                           ("Текст второго сообщения", {'username': 'user2', 'password': 'password2'})])
def test_thing_message_serializer__success(db,content, user, user_factory, thing_factory):
    user = user_factory(username = user['username'], password = user['password'])
    thing = thing_factory()

    data = {
        'content': content,
        'user': user.id,
        'thing': thing.id
    }
    serializer = ThingMessageSerializer(data=data)
    
    assert serializer.is_valid() == True
    assert serializer.errors == {}


@pytest.mark.parametrize("content, user, thing", [("Текст первого сообщения", "user1", "thing1"),
                                                  ("Текст второго сообщения", "user2", "thing2")])
def test_thing_message_serializer__error(content, user, thing):
    data = {
        'content': content,
        'user': user,
        'thing': thing
    }
       
    serializer = ThingMessageSerializer(data=data)
    assert serializer.is_valid() == False


    