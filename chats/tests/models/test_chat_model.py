from things.tests.factories import UserFactory
import pytest

from chats.tests.factories import ChatFactory
from chats.models import Chat

from django.db import IntegrityError, transaction

pytestmark = pytest.mark.django_db

def test_chat_model_cannot_create_two_chats_with_same_users__error():
    user_1 = UserFactory()
    user_2 = UserFactory()
    ChatFactory(member_1 = user_1, member_2 = user_2)

    with pytest.raises(IntegrityError) as e:
        with transaction.atomic():
            ChatFactory(member_1 = user_1, member_2 = user_2)
            ChatFactory(member_2 = user_1, member_1 = user_2)
    assert Chat.objects.all().count() == 1