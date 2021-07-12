import pytest

from things.tests.factories import ThingFactory
from things.serializers import ThingMessageSerializer
from rest_framework.validators import ValidationError

pytestmark = pytest.mark.django_db

@pytest.mark.parametrize("content", ("Текст первого сообщения", "тЕкСт ПерВОго сОобЩенИя", "   Сообщение   ", 123))
def test_thing_message_serializer_content__success(content):
    thing = ThingFactory()

    data = {
        'content': content,
        'user': thing.owner.id,
        'thing': thing.id
    }
    serializer = ThingMessageSerializer(data=data)
    
    assert serializer.is_valid() == True
    assert serializer.data == {'content': str(content).strip(),
                               'user': thing.owner.id,
                               'thing': thing.id,
                               'thing_title': thing.__str__(),
                               'user_name': thing.owner.username}
    assert serializer.errors == {}


@pytest.mark.parametrize("content", (False, "", None))
def test_thing_message_serializer_content__error(content):
    thing = ThingFactory()
    data = {
        'content': content,
        'user': thing.owner.id,
        'thing': thing.id
    }
       
    serializer = ThingMessageSerializer(data=data)
    with pytest.raises(ValidationError) as e:
        serializer.is_valid(raise_exception = True)
    assert 'content' in serializer.errors.keys()
    assert 'user' not in serializer.errors.keys()
    assert 'thing' not in serializer.errors.keys()
