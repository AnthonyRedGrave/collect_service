import pytest
from django.apps import apps
from things.tests.factories import SectionFactory, ThingFactory, ThingMessageFactory
from comments.tests.factories import CommentFactory
from tags.tests.factories import TagFactory


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "factory",
    (
        ThingFactory,
        ThingMessageFactory,
        SectionFactory,
        TagFactory,
    ),
)
def test_soft_delete__success(factory):
    object = factory()
    object.delete()
    assert object.active == False


def test_comment_soft_delete__success():
    thing = ThingFactory.create(comments=1)
    comment = thing.comments.first()
    comment.delete()
    assert comment.active == False
    assert len(thing.comments) == 1