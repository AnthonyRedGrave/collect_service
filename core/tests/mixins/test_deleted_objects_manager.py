import pytest
from things.tests.factories import SectionFactory, ThingFactory, ThingMessageFactory
from tags.tests.factories import TagFactory
from things.models import Thing, ThingMessage, Section
from tags.models import Tag

pytestmark = pytest.mark.django_db


# @pytest.mark.parametrize(
#     "factory, model",
#     (
#         (ThingFactory, Thing),
#         (ThingMessageFactory, ThingMessage),
#         (SectionFactory, Section),
#         (TagFactory, Tag),
#     ),
# )
# def test_soft_delete__success(factory, model):
#     object = factory()
#     object.delete()
#     object.refresh_from_db()
#     assert object.deleted == True
#     assert model.deleted_objects.count() == 1


# def test_comment_soft_delete__success():
#     thing = ThingFactory.create(comments=1)
#     comment = thing.comments.first()
#     comment.delete()
#     comment.refresh_from_db()
#     assert comment.deleted == True
#     assert thing.comments.count() == 1


# @pytest.mark.parametrize(
#     "factory, model",
#     (
#         (ThingFactory, Thing),
#         (ThingMessageFactory, ThingMessage),
#         (SectionFactory, Section),
#         (TagFactory, Tag),
#     ),
# )
# def test_hard_delete__success(factory, model):
#     count_before_add = model.objects.count()
#     object = factory()
#     object.delete(True)
#     count_after_delete = model.objects.count()
#     assert count_before_add == count_after_delete
