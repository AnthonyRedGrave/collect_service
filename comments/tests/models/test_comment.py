from comments.models import Comment
import pytest
from comments.tests.factories import CommentFactory
from things.tests.factories import ThingFactory

pytestmark = pytest.mark.django_db


def test_soft_delete__success():
    count_b_add = Comment.objects.count()
    thing = ThingFactory.create(comments=1)
    comment = thing.comments.first()
    comment.delete()
    count_a_delete = Comment.objects.count()
    assert count_b_add + 1 == count_a_delete
    comment.refresh_from_db()
    assert comment.deleted == True


def test_hard_delete__success():
    count_before_add = Comment.objects.count()
    thing = ThingFactory.create(comments=1)
    comment = thing.comments.first()
    comment.delete(True)
    count_after_delete = Comment.objects.count()
    assert count_before_add == count_after_delete