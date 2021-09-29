from things.tests.factories import UserFactory
import pytest

from chats.tests.factories import ChatFactory

pytestmark = pytest.mark.django_db

def test_chat_model_cannot_create_two_chats_with_same_users():
    member_1 = UserFactory()
    member_2 = UserFactory()
    chat_1 = ChatFactory(member_1 = member_1, member_2 = member_2)
    