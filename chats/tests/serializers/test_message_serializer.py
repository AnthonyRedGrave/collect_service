import pytest

from chats.serializers import MessageSerializer
from chats.tests.factories import ChatFactory

pytestmark = pytest.mark.django_db


def test_message_serializer_chat__success():
    chat = ChatFactory()
    data = {
        'chat': chat.id,
        'content': "Новое сообщение"
    }
    serializer = MessageSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.data == {
                                'chat': str(chat),
                                'content': "Новое сообщение"
                              }
    assert serializer.errors == {}


@pytest.mark.parametrize("content", ("Сообщение", "сооБщЕнИЕ", "   сообщение   ", 123))
def test_message_serializer_content__success(content):
    chat = ChatFactory()
    data = {
        'chat': chat.id,
        'content': content
    }
    serializer = MessageSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.data == {
                                'chat': str(chat),
                                'content': str(content).strip()
                              }
    assert serializer.errors == {}