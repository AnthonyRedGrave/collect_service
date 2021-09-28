from things.tests.factories import ThingFactory, UserFactory
import factory

from ..models import Chat, Message


class ChatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Chat

    member_1 = factory.SubFactory(UserFactory)
    member_2 = factory.SubFactory(UserFactory)
    thing = factory.SubFactory(ThingFactory)


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    user = factory.SubFactory(UserFactory)
    content = factory.Faker("text")
    chat = factory.SubFactory(ChatFactory)