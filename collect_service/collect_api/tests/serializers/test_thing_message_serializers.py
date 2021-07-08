import pytest

from collect_api.tests.factories import ThingMessageFactory, UserFactory, ThingFactory
from pytest_factoryboy import register
from collect_api.serializers import ThingMessageSerializer
from rest_framework.validators import ValidationError

register(ThingMessageFactory)
register(UserFactory)
register(ThingFactory)

pytestmark = pytest.mark.django_db

@pytest.mark.parametrize("content", ("Текст первого сообщения", "Текст второго сообщения"))
def test_thing_message_serializer_content__success(content, user_factory, thing_factory):
    user = user_factory()
    thing = thing_factory()

    data = {
        'content': content,
        'user': user.id,
        'thing': thing.id
    }
    serializer = ThingMessageSerializer(data=data)
    
    assert serializer.is_valid() == True
    assert serializer.errors == {}


@pytest.mark.parametrize("content", (False, "", None))
def test_thing_message_serializer_content__error(content, thing_factory):
    thing = thing_factory()
    data = {
        'content': content,
        'user': thing.owner_id,
        'thing': thing.id
    }
       
    serializer = ThingMessageSerializer(data=data)
    with pytest.raises(ValidationError) as e:
        serializer.is_valid(raise_exception = True)
    assert 'content' in serializer.errors.keys()
    assert 'user' not in serializer.errors.keys()
    assert 'thing' not in serializer.errors.keys()

    