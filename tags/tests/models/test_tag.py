from tags.models import Tag
import pytest
from tags.tests.factories import TagFactory

pytestmark = pytest.mark.django_db


def test_soft_delete__success():
    count_b_add = Tag.objects.count()
    tag = TagFactory()
    tag.delete()
    count_a_delete = Tag.objects.count()
    assert count_b_add + 1 == count_a_delete
    tag.refresh_from_db()
    assert tag.deleted == True


def test_hard_delete__success():
    count_before_add = Tag.objects.count()
    tag = TagFactory()
    tag.delete(True)
    count_after_delete = Tag.objects.count()
    assert count_before_add == count_after_delete