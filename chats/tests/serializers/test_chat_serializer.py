from things.tests.factories import ThingFactory, UserFactory
import pytest

from chats.serializers import ChatSerializer
from rest_framework.validators import ValidationError

from chats.tests.factories import ChatFactory, MessageFactory

pytestmark = pytest.mark.django_db

def test_chat_serializer_thing__error():
    member_1 = UserFactory()
    member_2 = UserFactory()
    thing = ThingFactory()
    data = {
        "member_1": member_1.id,
        "member_2": member_2.id,
        "thing": thing.id
    }
    serializer = ChatSerializer(data=data)

    with pytest.raises(ValidationError) as e:
        serializer.is_valid(raise_exception = True)
    assert 'thing' in serializer.errors.keys()


def test_chat_serializer_wrong_members_error():
    member_1 = UserFactory()
    member_2 = UserFactory()
    thing = ThingFactory(owner = member_2)
    data = {
        "member_1": member_1.id,
        "member_2": member_2.id,
        "thing": thing.id
    }
    serializer = ChatSerializer(data=data)

    assert serializer.is_valid()
    assert serializer.data == {
                               'member_1': member_1.id,
                               'member_2': member_2.id, 
                               'thing': str(thing), 
                               'member_1_name': member_1.username, 
                               'member_2_name': member_2.username
                              }
    assert serializer.errors == {}


def test_chat_serializer___error():
