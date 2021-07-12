import factory
from comments.models import Comment
from things.tests.factories import UserFactory, ThingFactory


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment
    
    content = factory.Faker('text')
    user = factory.SubFactory(UserFactory)
    content_object = factory.SubFactory(ThingFactory)
