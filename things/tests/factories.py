from tags.tests.factories import TagFactory
import factory
from ..models import Thing, ThingMessage, Section, Deal
from django.contrib.auth.models import User
import random
from vote.tests.factories import VoteFactory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    first_name = factory.Faker("first_name")
    username = factory.Faker("first_name")
    password = "12345"
    last_name = factory.Faker("last_name")


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Section

    title = factory.Faker("name")


class ThingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Thing

    title = factory.Faker("first_name")
    content = factory.Faker("text")
    state = "Awesome"
    owner = factory.SubFactory(UserFactory)
    section = factory.SubFactory(SectionFactory)
    is_sold = False
    image = factory.Faker("image_url")

    @factory.post_generation
    def comments(self, create, extracted, **kwargs):
        from comments.tests.factories import CommentFactory

        if not create:
            return
        if extracted:
            for n in range(extracted):
                CommentFactory(content_object=self)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            if extracted == "random":
                extracted = random.randint(2, 10)
            tags = TagFactory.create_batch(extracted)
            for tag in tags:
                self.tags.add(tag)

    @factory.post_generation
    def votes(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            if extracted == "random":
                extracted = random.randint(2, 10)
                for n in range(extracted):
                    VoteFactory(thing=self, user=UserFactory())


class ThingMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ThingMessage

    user = factory.SubFactory(UserFactory)
    content = factory.Faker("text")
    thing = factory.SubFactory(ThingFactory)


class DealFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Deal

    old_owner = factory.SubFactory(UserFactory)
    new_owner = factory.SubFactory(UserFactory)
    thing = factory.SubFactory(ThingFactory)
    status = "accepted"
    cost = 100
