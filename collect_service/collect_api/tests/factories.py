import factory
from ..models import Thing, ThingMessage, Section
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)
    
    first_name = factory.Faker('first_name')
    username = factory.Faker('first_name')
    password = "12345"
    last_name = factory.Faker('last_name')


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Section
    
    title = factory.Faker('name')


class ThingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Thing

    title = factory.Faker('first_name')
    content = factory.Faker('text')
    state = factory.Faker('name')
    owner = factory.SubFactory(UserFactory)
    section = factory.SubFactory(SectionFactory)
    is_sold = False
    image = factory.Faker('image_url')
    owner = factory.SubFactory(UserFactory)


class ThingMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ThingMessage

    user = factory.SubFactory(UserFactory)
    content = factory.Faker('text')
    thing = factory.SubFactory(ThingFactory)