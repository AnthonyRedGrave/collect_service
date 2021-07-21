import factory
from factory import faker
from ..models import Tag


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
    
    title = faker.Faker('name')